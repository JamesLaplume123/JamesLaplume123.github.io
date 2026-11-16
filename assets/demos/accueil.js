/* Accueil : le héros vivant, la bande des solutions et la carte.
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
    cartes.forEach(function (c) {
      c.addEventListener("pointerenter", function (e) { if (e.pointerType !== "touch") ouvre(c); });
      c.addEventListener("focusin", function () { ouvre(c); });
    });
    ouvre(cartes[0]);
  });

  /* ================================================================ Carte : l'onde de la base seulement à l'écran */
  var carte = document.querySelector("[data-ac-carte]");
  if (carte && "IntersectionObserver" in window) {
    new IntersectionObserver(function (e) { carte.classList.toggle("is-vue", e[0].isIntersecting); }, { threshold: .1 }).observe(carte);
  }
})();
