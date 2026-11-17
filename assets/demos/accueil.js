/* Accueil : le héros vivant et la bande des solutions.
   Héros : un petit shader WebGL (même principe que /labo-cartes/) part de la vraie photo, où tout est
   allumé. Éteindre une lumière assombrit seulement ses zones; la porte du garage remonte et laisse voir
   l'intérieur. Rien n'est recoloré. Quand personne ne touche, la maison vit seule, lentement.
   Sans WebGL : la photo reste fixe et les points sont masqués. Mouvement réduit : pas de démonstration
   automatique, états immédiats. Tout se met en pause hors écran. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var rm = matchMedia("(prefers-reduced-motion: reduce)");
  function fx() { return doc.classList.contains("fx") && !rm.matches; }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* ================================================================ Le film du héros
     Six lieux : la maison (scène 0, interactive) puis cinq photos qui se posent dessus, chacune avec ce
     que JARVIS y voit. Le trait de l'onglet actif sert de minuterie; à la fin, on passe au lieu suivant.
     Toucher la maison ou choisir un onglet met le film en pause un moment. Mouvement réduit : pas de
     défilement automatique, les onglets restent utilisables. Les photos se chargent après la page. */
  (function () {
    var h = document.querySelector("[data-ac-hero]"); if (!h) return;
    var scenes = $$("[data-ac-sc]", h), tabs = $$("[data-ac-tab]", h), n = 0, pauseT = 0, changeT = 0;
    if (!tabs.length) return;
    h.setAttribute("data-scene", "0");
    function prete(i) { if (i === 0) return true; var im = scenes[i - 1].querySelector("img"); return !!(im && im.complete && im.naturalWidth); }
    function va(i) {
      if (i === n) return;
      h.classList.toggle("vers-maison", i === 0);
      n = i; h.setAttribute("data-scene", String(i));
      scenes.forEach(function (s, k) { s.classList.toggle("is-on", k === i - 1); });
      tabs.forEach(function (t, k) { t.setAttribute("aria-pressed", k === i ? "true" : "false"); });
      h.classList.remove("is-change"); void h.offsetWidth; h.classList.add("is-change");
      clearTimeout(changeT); changeT = setTimeout(function () { h.classList.remove("is-change"); }, 1600);
    }
    function relance() {   /* repart la minuterie de l'onglet actif */
      var i = tabs[n].querySelector("i"); i.style.animation = "none"; void i.offsetWidth; i.style.animation = "";
    }
    function pause(ms) {
      h.classList.add("is-pause"); clearTimeout(pauseT);
      pauseT = setTimeout(function () { h.classList.remove("is-pause"); }, ms);
    }
    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () { va(k); relance(); pause(k === 0 ? 0 : 2500); });
      t.querySelector("i").addEventListener("animationend", function () {
        if (k !== n) return;
        var s = (n + 1) % tabs.length;
        if (!prete(s)) { relance(); return; }
        va(s);
      });
    });
    $$(".ac-spot", h).forEach(function (b) { b.addEventListener("click", function () { relance(); pause(14000); }); });
    document.addEventListener("visibilitychange", function () { h.classList.toggle("is-pause", document.hidden); });
    /* Les repères : posés sur l'objet, selon le cadrage réel de la photo (object-fit: cover). */
    function pose(sc) {
      var im = sc.querySelector("img"), lis = $$(".ac-hud li", sc);
      if (innerWidth <= 720 || !im.naturalWidth) { lis.forEach(function (li) { li.style.removeProperty("--px"); li.style.removeProperty("--py"); li.classList.remove("is-out", "is-left"); }); return; }
      var cw = sc.clientWidth, ch = sc.clientHeight, r = im.naturalWidth / im.naturalHeight;
      var bw = Math.max(cw, ch * r), bh = bw / r, pos = (sc.getAttribute("data-pos") || "50% 50%").split(" ");
      var ox = (cw - bw) * parseFloat(pos[0]) / 100, oy = (ch - bh) * parseFloat(pos[1]) / 100;
      lis.forEach(function (li) {
        var x = ox + bw * parseFloat(li.getAttribute("data-x")), y = oy + bh * parseFloat(li.getAttribute("data-y"));
        li.style.setProperty("--px", x.toFixed(1) + "px"); li.style.setProperty("--py", y.toFixed(1) + "px");
        li.classList.toggle("is-left", x > cw * 0.6);
        li.classList.toggle("is-out", x < 60 || x > cw - 60 || y < 110 || y > ch - 300);
      });
    }
    function poseTout() { scenes.forEach(pose); }
    addEventListener("resize", poseTout);
    /* Le pointeur déplace doucement la photo : un peu de profondeur. */
    var couche = h.querySelector(".ac-scenes"), tx = 0, ty = 0, cx = 0, cy = 0, rafP = 0;
    function glisse() {
      cx += (tx - cx) * 0.06; cy += (ty - cy) * 0.06;
      couche.style.transform = "translate3d(" + cx.toFixed(2) + "px," + cy.toFixed(2) + "px,0)";
      rafP = Math.abs(tx - cx) + Math.abs(ty - cy) > 0.05 ? requestAnimationFrame(glisse) : 0;
    }
    if (couche && matchMedia("(hover: hover) and (pointer: fine)").matches) {
      h.addEventListener("pointermove", function (e) {
        if (!fx()) return;
        var b = h.getBoundingClientRect();
        tx = ((e.clientX - b.left) / b.width - 0.5) * -22; ty = ((e.clientY - b.top) / b.height - 0.5) * -14;
        if (!rafP) rafP = requestAnimationFrame(glisse);
      });
      h.addEventListener("pointerleave", function () { tx = ty = 0; if (!rafP) rafP = requestAnimationFrame(glisse); });
    }
    function charge() {
      var k = 0;
      (function suivant() {
        if (k >= scenes.length) return;
        var sc = scenes[k++], im = sc.querySelector("img"), src = im.getAttribute("data-src");
        if (!src || im.getAttribute("src")) { suivant(); return; }
        im.onload = function () { pose(sc); suivant(); }; im.onerror = suivant; im.src = src;
      })();
      if (fx()) h.classList.add("is-film");
    }
    if (document.readyState === "complete") charge(); else addEventListener("load", charge);
  })();

  /* ================================================================ Héros vivant */
  var hero = document.querySelector("[data-ac-hero]");
  if (hero) (function () {
    var D = JSON.parse(hero.querySelector("[data-ac-data]").textContent);
    var view = hero.querySelector("[data-ac-view]"), canvas = hero.querySelector("[data-ac-gl]"), photo = hero.querySelector(".ac-ph");
    var S = {}, cur = {}, SPOT = {}, door = null;
    D.spots.forEach(function (s) {
      SPOT[s.id] = s;
      s.el = hero.querySelector('[data-ac-spot="' + s.id + '"]');
      s.etat = s.el.querySelector("[data-ac-etat]");
      if (s.door) { door = s; S[s.id] = 0; } else S[s.id] = 1;
      cur[s.id] = S[s.id];
    });
    cur.inL = 0;

    var gl = null, U = {}, tex = [], pret = false, raf = 0, last = 0, visible = true;
    var VS = "attribute vec2 a;varying vec2 v;void main(){v=vec2(a.x*.5+.5,.5-a.y*.5);gl_Position=vec4(a,0.,1.);}";
    var FS = [
      "precision mediump float;varying vec2 v;",
      "uniform sampler2D uTex,uAux;uniform vec4 uCover;uniform vec4 uZ[10];uniform float uI[10];",
      "uniform float uDoor[6];uniform vec4 uCrop;uniform float uOpen,uInL;",
      "float g(vec2 p,vec4 z){vec2 d=(p-z.xy)/z.zw;return exp(-dot(d,d));}",
      "void main(){",
      " vec2 p=v*uCover.xy+uCover.zw;vec3 col=texture2D(uTex,p).rgb;float inDoor=0.;",
      " float u=(p.x-uDoor[0])/(uDoor[2]-uDoor[0]);",
      " float top=mix(uDoor[1],uDoor[3],u),bot=mix(uDoor[5],uDoor[4],u);float w=(p.y-top)/(bot-top);",
      " if(u>0.&&u<1.&&w>0.&&w<1.){",   /* le panneau remonte, l'intérieur apparaît */
      "  float e=1.-uOpen*.92;",
      "  if(w>e){vec3 q=texture2D(uAux,vec2(mix(uCrop.x,uCrop.z,u),mix(uCrop.y,uCrop.w,w))).rgb;",
      "   float sh=smoothstep(e,e+.2,w);float side=smoothstep(0.,.06,u)*smoothstep(1.,.94,u);",
      "   col=q*(.05+.8*uInL)*(.25+.75*sh)*(.5+.5*side);inDoor=1.;}",
      "  else{col=texture2D(uTex,vec2(p.x,mix(top,bot,w+(1.-e)))).rgb*(1.-.35*uOpen);col*=1.-.6*smoothstep(e-.04,e,w)*step(.002,uOpen);}",
      " }",
      " float sp=smoothstep(-.1,.12,u)*smoothstep(1.1,.88,u)*smoothstep(bot-.004,bot+.02,p.y)*smoothstep(bot+.2,bot,p.y);",
      " col+=vec3(1.,.8,.56)*.16*sp*uOpen*uInL*(.35+col.g*2.);",   /* la lumière du garage sur l'entrée */
      " float k=0.;for(int i=0;i<10;i++){k+=uI[i]*g(p,uZ[i]);}",
      " k=clamp(k*1.7,0.,1.);",
      " float lum=dot(col,vec3(.3,.6,.1));float warm=smoothstep(0.,.13,col.r-col.b);",
      " float keep=mix(.5,.06,smoothstep(.16,.7,lum));",
      " if(inDoor<.5)col=mix(col,col*keep+vec3(.006,.009,.016)*smoothstep(.3,.8,lum),k*warm);",
      " gl_FragColor=vec4(col,1.);",
      "}"
    ].join("\n");

    function initGL() {
      try { gl = canvas.getContext("webgl", { antialias: false, alpha: false, powerPreference: "low-power" }); } catch (e) { gl = null; }
      if (!gl) return false;
      function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return gl.getShaderParameter(s, gl.COMPILE_STATUS) ? s : null; }
      var a = sh(gl.VERTEX_SHADER, VS), b = sh(gl.FRAGMENT_SHADER, FS);
      if (!a || !b) { gl = null; return false; }
      var prog = gl.createProgram(); gl.attachShader(prog, a); gl.attachShader(prog, b); gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { gl = null; return false; }
      gl.useProgram(prog);
      var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
      var loc = gl.getAttribLocation(prog, "a"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
      ["uTex", "uAux", "uCover", "uZ", "uI", "uDoor", "uCrop", "uOpen", "uInL"].forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
      gl.uniform1i(U.uTex, 0); gl.uniform1i(U.uAux, 1);
      gl.uniform1fv(U.uDoor, new Float32Array(D.door)); gl.uniform4fv(U.uCrop, new Float32Array(D.crop));
      canvas.addEventListener("webglcontextlost", function (e) { e.preventDefault(); pret = false; hero.classList.remove("is-gl"); });
      return true;
    }
    function texture(url, unit, cb) {
      var im = new Image();
      im.onload = function () {
        if (!gl) return;
        var t = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, t);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, im);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        tex[unit] = t; cb();
      };
      im.src = url;
    }
    /* Cadrage « cover » partagé par le shader, la photo de repli et les points */
    function cover() {
      var r = view.getBoundingClientRect(), ca = r.width / Math.max(1, r.height), ia = D.ratio[0] / D.ratio[1];
      var f = getComputedStyle(photo).objectPosition.split(" "), fxp = parseFloat(f[0]) / 100, fyp = parseFloat(f[1]) / 100;
      if (ia > ca) { var sx = ca / ia; return [sx, 1, (1 - sx) * fxp, 0]; }
      var sy = ia / ca; return [1, sy, 0, (1 - sy) * fyp];
    }
    function place() {
      var c = cover();
      D.spots.forEach(function (s) {
        var x = (s.x / 100 - c[2]) / c[0], y = (s.y / 100 - c[3]) / c[1];
        s.el.style.setProperty("--px", (x * 100).toFixed(2) + "%"); s.el.style.setProperty("--py", (y * 100).toFixed(2) + "%");
        s.el.classList.toggle("is-out", x < .05 || x > .95 || y < .08 || y > .95);
        s.el.classList.toggle("is-left", x > .62);
      });
    }
    function taille() {
      place();
      if (!gl) return;
      var r = view.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, r.width < 760 ? 2 : 1.5);
      var w = Math.round(r.width * dpr), h = Math.round(r.height * dpr);
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; gl.viewport(0, 0, w, h); }
      kick(true);
    }
    function dessine() {
      if (!gl || !pret) return;
      gl.uniform4fv(U.uCover, cover());
      var Z = new Float32Array(40), I = new Float32Array(10), n = 0;
      D.spots.forEach(function (s) {
        (s.zones || []).forEach(function (z) { if (n < 10) { Z.set(z, n * 4); I[n] = 1 - cur[s.id]; n++; } });
      });
      gl.uniform4fv(U.uZ, Z); gl.uniform1fv(U.uI, I);
      gl.uniform1f(U.uOpen, door ? cur[door.id] : 0); gl.uniform1f(U.uInL, cur.inL);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    function vers(k, cible, vitesse, dt) {
      var c = cur[k];
      if (c === cible) return false;
      if (!fx()) { cur[k] = cible; return true; }
      var n = c + (cible - c) * (1 - Math.exp(-vitesse * dt));
      if (Math.abs(cible - n) < .003) n = cible;
      cur[k] = n; return true;
    }
    var sale = false;
    function kick(force) { if (force) sale = true; if (!raf) raf = requestAnimationFrame(image); }
    function image(t) {
      raf = 0;
      var dt = Math.min(.05, (t - last) / 1000 || .016); last = t;
      var bouge = false;
      D.spots.forEach(function (s) { bouge = vers(s.id, S[s.id], s.door ? 1.15 : 2.6, dt) || bouge; });
      bouge = vers("inL", door && cur[door.id] > .03 ? 1 : 0, 2.4, dt) || bouge;
      if (bouge || sale) { dessine(); sale = false; }
      if (bouge && visible) kick();
    }

    /* États et libellés */
    var ditT = {};
    function regle(id, val, dire) {
      var s = SPOT[id];
      S[id] = val ? 1 : 0;
      s.el.setAttribute("aria-pressed", val ? "true" : "false");
      s.etat.textContent = val ? s.on : s.off;
      if (dire) {
        s.el.classList.add("is-dit");
        clearTimeout(ditT[id]);
        ditT[id] = setTimeout(function () { s.el.classList.remove("is-dit"); }, 2600);
      }
      kick();
    }

    /* La maison vit seule tant que personne ne touche */
    var PAS = [
      ["garage", 1, 4200], ["etage", 0, 3000], ["garage", 0, 3600], ["salon", 0, 2600], ["entree", 0, 3800],
      ["entree", 1, 900], ["salon", 1, 900], ["etage", 1, 5200]
    ];
    var pas = 0, minuterie = 0, reprise = 0;
    function suite(delai) {
      clearTimeout(minuterie);
      minuterie = setTimeout(function () {
        if (!fx() || !visible || document.hidden || Date.now() < reprise) { suite(1500); return; }
        var p = PAS[pas % PAS.length]; pas++;
        regle(p[0], p[1], true);
        suite(p[2]);
      }, delai);
    }
    D.spots.forEach(function (s) {
      s.el.addEventListener("click", function () {
        reprise = Date.now() + 14000;
        regle(s.id, !S[s.id], true);
      });
    });

    if (!initGL()) return;
    var reste = 2;
    function charge() {
      if (--reste) return;
      pret = true; taille();
      requestAnimationFrame(function () { hero.classList.add("is-gl"); });
      suite(2600);
    }
    texture(D.img, 0, charge); texture(D.inside, 1, charge);
    addEventListener("resize", taille);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (e) {
        visible = e[0].isIntersecting; hero.classList.toggle("is-hors", !visible);
        if (visible) kick(true);
      }, { threshold: .05 }).observe(hero);
    }
  })();

  /* ================================================================ Bande des solutions : la carte survolée s'ouvre */
  $$("[data-ac-sols]").forEach(function (bande) {
    var cartes = $$(".ac-sol", bande);
    function ouvre(c) { cartes.forEach(function (x) { x.classList.toggle("is-on", x === c); }); }
    var repos = 0, vue = false;
    cartes.forEach(function (c) {
      c.addEventListener("pointerenter", function (e) { if (e.pointerType !== "touch") { repos = Date.now() + 12000; ouvre(c); } });
      c.addEventListener("focusin", function () { repos = Date.now() + 12000; ouvre(c); });
    });
    ouvre(cartes[0]);
    /* Tant que personne n'y touche, la bande présente ses solutions une à une. */
    if ("IntersectionObserver" in window) new IntersectionObserver(function (e) { vue = e[0].isIntersecting; }, { threshold: 0.4 }).observe(bande);
    setInterval(function () {
      if (!fx() || !vue || document.hidden || innerWidth <= 900 || Date.now() < repos) return;
      var vis = cartes.filter(function (c) { return c.offsetParent !== null; });
      var i = vis.indexOf(vis.filter(function (c) { return c.classList.contains("is-on"); })[0]);
      ouvre(vis[(i + 1) % vis.length]);
    }, 4200);
  });

  /* ================================================================ Aperçu du logiciel : l'écran complet tient dans la fenêtre
     Au-dessus de 720 px, l'appareil est rendu à 1040 px de large puis réduit (zoom) pour que sa hauteur
     tienne sous la barre : s = min(1, (hauteur de fenêtre − 120) / hauteur naturelle, largeur disponible / 1040). */
  var dev = document.querySelector(".ac-dev"), ecran = document.querySelector(".ac-ecran");
  function ajuste() {
    if (!dev || !ecran) return;
    dev.style.zoom = ""; dev.style.width = ""; ecran.style.maxWidth = "";
    if (window.innerWidth <= 720) return;
    var scene = ecran.parentElement, dispo = scene.clientWidth;
    dev.style.width = "1040px";
    var h = dev.offsetHeight;
    if (!h) return;
    var s = Math.min(1, (window.innerHeight - 150) / h, dispo / 1040);
    dev.style.zoom = s;
    ecran.style.maxWidth = (1040 * s) + "px";
  }
  ajuste();

  /* L'écran se redresse en arrivant, puis une visite seule le parcourt : un cadre doré se pose sur une
     zone, le reste s'assombrit, une légende la nomme. Rien n'est cliquable ici : tout mène à /logiciel/. */
  (function () {
    if (!ecran || !dev) return;
    var tour = ecran.querySelector("[data-ac-tour]"), box = tour && tour.querySelector(".ac-tour-b"), lab = tour && tour.querySelector(".ac-tour-l");
    var PAS = []; try { PAS = JSON.parse(ecran.querySelector("[data-ac-tour-data]").textContent); } catch (e) {}
    var CIBLE = {
      xc: function () { var x = dev.querySelector(".ap-xc"); return x && x.parentElement; },
      tl: function () { var x = dev.querySelector(".ap-tl"); return x && (x.closest(".ap-card") || x); },
      ask: function () { var x = dev.querySelector(".ap-ask"); return x && (x.closest(".ap-card") || x); },
      map: function () { var x = dev.querySelector(".ap-map"); return x && (x.closest(".ap-card") || x); },
      search: function () { return dev.querySelector(".ap-search"); }
    };
    var n = -1, vu = false, minut = 0;
    function cadre() {   /* la couche de la visite épouse l'appareil (coins compris) */
      var d = dev.querySelector(".ap-device") || dev, a = ecran.getBoundingClientRect(), b = d.getBoundingClientRect();
      var z = parseFloat(dev.style.zoom) || 1;
      tour.style.left = (b.left - a.left) + "px"; tour.style.top = (b.top - a.top) + "px";
      tour.style.width = b.width + "px"; tour.style.height = b.height + "px";
      tour.style.borderRadius = (parseFloat(getComputedStyle(d).borderTopLeftRadius) * z || 20) + "px";
      return b;
    }
    function va(i) {
      var p = PAS[i], el = p && CIBLE[p[0]] && CIBLE[p[0]]();
      if (!el) return false;
      var b = cadre(), r = el.getBoundingClientRect(), m = 6;
      if (!r.width || r.bottom > b.bottom + 4) return false;
      var x = r.left - b.left - m, y = r.top - b.top - m, w = r.width + m * 2, hh = r.height + m * 2;
      box.style.left = x + "px"; box.style.top = y + "px"; box.style.width = w + "px"; box.style.height = hh + "px";
      lab.classList.add("is-change");
      setTimeout(function () {
        lab.querySelector("b").textContent = p[1]; lab.querySelector("span").textContent = p[2];
        var lw = lab.offsetWidth, lh = lab.offsetHeight, ly = y + hh + 10;
        if (ly + lh > b.height - 90) ly = y - lh - 10;
        if (ly < 8) ly = y + 10;
        lab.style.left = Math.max(8, Math.min(x, b.width - lw - 8)) + "px"; lab.style.top = ly + "px";
        lab.classList.remove("is-change");
      }, 320);
      return true;
    }
    function suite() {
      clearTimeout(minut);
      if (!fx() || !vu || document.hidden || innerWidth <= 720) { ecran.classList.remove("is-tour"); minut = setTimeout(suite, 1500); return; }
      for (var k = 0; k < PAS.length; k++) { n = (n + 1) % PAS.length; if (va(n)) break; }
      ecran.classList.add("is-tour");
      minut = setTimeout(suite, 3400);
    }
    if (!("IntersectionObserver" in window)) return;
    ecran.classList.add("a-anim");
    new IntersectionObserver(function (e) {
      if (e[0].isIntersecting) ecran.classList.add("is-vu");
    }, { threshold: 0.18 }).observe(ecran);
    if (tour && PAS.length) {
      new IntersectionObserver(function (e) {
        var avant = vu; vu = e[0].isIntersecting;
        if (vu && !avant) { clearTimeout(minut); minut = setTimeout(suite, 1500); }
      }, { threshold: 0.45 }).observe(ecran);
      addEventListener("resize", function () { if (ecran.classList.contains("is-tour") && n >= 0) va(n); });
    }
  })();
  window.addEventListener("resize", ajuste);
  window.addEventListener("load", ajuste);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(ajuste);
})();
