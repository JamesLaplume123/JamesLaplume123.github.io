/* Laboratoire des cartes « Vivant » (page privée /labo-cartes/).
   1. La photo vivante : un petit shader WebGL éclaire la vraie photo zone par zone (rien n'est recoloré :
      la photo montre tout allumé, éteindre une lampe assombrit sa zone), baisse les stores, ouvre la porte
      du garage, anime la chaleur du foyer et donne du relief au garage de collection.
   2. Les objets 3D (three.js, chargé seulement ici) : maquette de la résidence et batteries domestiques.
   3. Les commandes : panneau qui se déplie depuis le point touché, tiroir de pièce, cadran rond, ruban
      de la journée, propositions de JARVIS. Tous les états sont liés entre eux.
   Sans WebGL : photos fixes, mêmes commandes. Mouvement seulement sous html.fx, en pause hors écran. */
(function () {
  "use strict";
  var root = document.querySelector("[data-vv]");
  if (!root) return;
  var doc = document.documentElement;
  var D = JSON.parse(root.querySelector("[data-vv-data]").textContent);
  function $(s, c) { return (c || root).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || root).querySelectorAll(s)); }
  var rm = matchMedia("(prefers-reduced-motion: reduce)");
  function fx() { return doc.classList.contains("fx") && !rm.matches; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function fr(v, d) { return v.toFixed(d == null ? 1 : d).replace(".", ","); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var NB = " ";
  var IC = {
    x: '<path d="M6 6l12 12M18 6 6 18"/>', spark: '<path d="M12 3l1.7 5.3L19 10l-5.3 1.7L12 17l-1.7-5.3L5 10l5.3-1.7z"/>',
    clock: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>'
  };
  function ic(k) { return '<svg class="vv-i" viewBox="0 0 24 24" aria-hidden="true">' + IC[k] + "</svg>"; }

  /* ================================================================ État */
  var S = { scene: "salon", night: 0, blind: 0, door: 0, vent: 0, beam: 0, set: D.th.set, inside: D.th.inside, reserve: D.en.reserve, level: "tout", room: null, L: {}, lit: {} };
  var SPOT = {};   // "scène:id" -> définition
  Object.keys(D.scenes).forEach(function (k) {
    D.scenes[k].spots.forEach(function (s) {
      s.key = k + ":" + s.id; s.scene = k; SPOT[s.key] = s;
      if (s.kind === "light" || s.kind === "fire") S.L[s.key] = { on: s.on ? 1 : 0, level: 1, tone: 1 };
    });
  });
  D.rooms.forEach(function (r) { S.lit[r.id] = r.lit; });
  var cur = { night: 0, blind: 0, door: 0, beam: 0, heat: 0, inL: 0, mx: 0, my: 0 };   // valeurs affichées, qui rejoignent l'état
  Object.keys(S.L).forEach(function (k) { cur[k] = S.L[k].on; });
  function lightTarget(k) { var l = S.L[k]; return l.on ? l.level : 0; }
  var TONES = [["Bougie", "#ffb46b", [1, .52, .16]], ["Chaud", "#ffd9a8", [0, 0, 0]], ["Neutre", "#f4f1ea", [.42, .55, .8]]];

  var listeners = [];
  function changed() { listeners.forEach(function (f) { f(); }); kick(); }

  /* ================================================================ Boucle d'animation */
  var raf = 0, last = 0, clockT = 0, vis = { scene: true, house: false, batt: false };
  var tick3d = [];
  function kick() { if (!raf) raf = requestAnimationFrame(frame); }
  function approach(key, target, rate, dt) {
    var c = cur[key];
    if (!fx()) { cur[key] = target; return c !== target; }
    var n = c + (target - c) * (1 - Math.exp(-rate * dt));
    if (Math.abs(target - n) < .002) n = target;
    cur[key] = n; return n !== c;
  }
  function frame(t) {
    raf = 0;
    var dt = Math.min(.05, (t - last) / 1000 || .016); last = t;
    var busy = false;
    Object.keys(S.L).forEach(function (k) { busy = approach(k, lightTarget(k), 5, dt) || busy; });
    busy = approach("night", S.night, 2.2, dt) || busy;
    busy = approach("blind", S.blind, 2.4, dt) || busy;
    busy = approach("door", S.door, 1.3, dt) || busy;
    busy = approach("beam", S.beam, 6, dt) || busy;
    busy = approach("heat", heatAmount(), 1.5, dt) || busy;
    busy = approach("inL", cur.door > .02 ? 1 : 0, 3, dt) || busy;
    busy = approach("mx", mouse.x, 6, dt) || busy;
    busy = approach("my", mouse.y, 6, dt) || busy;
    var alive = fx() && vis.scene && S.scene === "salon" && (cur["salon:foyer"] > .02 || cur.heat > .02);
    if (alive) clockT += dt;
    if (vis.scene && (busy || alive || sceneDirty)) { drawScene(); sceneDirty = false; }
    var more = false;
    tick3d.forEach(function (f) { more = f(dt, busy) || more; });
    if (busy || alive || more) kick();
  }
  function heatAmount() { return clamp((S.set - S.inside) / 2.5, 0, 1); }

  /* ================================================================ 1. La photo vivante */
  var view = $("[data-vv-view]"), canvas = $("[data-vv-gl]"), gl = null, prog = null, U = {}, tex = {}, sceneDirty = true;
  var mouse = { x: 0, y: 0 };
  var VS = "attribute vec2 a;varying vec2 v;void main(){v=vec2(a.x*.5+.5,.5-a.y*.5);gl_Position=vec4(a,0.,1.);}";
  var FS = [
    "precision mediump float;varying vec2 v;",
    "uniform sampler2D uTex,uAux;uniform vec4 uCover;uniform vec4 uZ[14];uniform float uI[14];uniform vec3 uC[14];",
    "uniform float uAmb,uSkyI,uBlind,uFireI,uHeat,uTime,uOpen,uInL,uBeamI,uKind,uNight,uAsp;",
    "uniform vec4 uSky[2];uniform vec4 uFire;uniform float uWin[5];uniform float uDoor[6];uniform vec4 uCrop;uniform vec2 uMouse;uniform vec3 uBeams[2];",
    "float g(vec2 p,vec4 z){vec2 d=(p-z.xy)/z.zw;return exp(-dot(d,d));}",
    "void main(){",
    " vec2 p=v*uCover.xy+uCover.zw;",
    " if(uKind>1.5){float dp=texture2D(uAux,p).r;p+=(dp-.42)*uMouse*vec2(.026,.012);}",
    " if(uKind<.5){",   /* voile de chaleur au-dessus des flammes */
    "  float hx=smoothstep(uFire.x-.02,uFire.x+.03,p.x)*smoothstep(uFire.z+.02,uFire.z-.03,p.x);",
    "  float hy=smoothstep(uFire.y-.2,uFire.y-.04,p.y)*smoothstep(uFire.y+.06,uFire.y-.01,p.y);",
    "  p.x+=sin(p.y*120.-uTime*4.)*.0011*hx*hy*uFireI;",
    " }",
    " vec3 col=texture2D(uTex,p).rgb;float inDoor=0.;",
    " if(uKind>.5&&uKind<1.5){",   /* porte de garage : le panneau remonte, l'intérieur apparaît */
    "  float u=(p.x-uDoor[0])/(uDoor[2]-uDoor[0]);",
    "  float top=mix(uDoor[1],uDoor[3],u),bot=mix(uDoor[5],uDoor[4],u);float w=(p.y-top)/(bot-top);",
    "  if(u>0.&&u<1.&&w>0.&&w<1.){",
    "   float e=1.-uOpen*.94;",
    "   if(w>e){vec3 q=texture2D(uAux,vec2(mix(uCrop.x,uCrop.z,u),mix(uCrop.y,uCrop.w,w))).rgb;",
    "    float sh=smoothstep(e,e+.16,w);float side=smoothstep(0.,.05,u)*smoothstep(1.,.95,u);",
    "    col=q*(.06+.94*uInL)*(.3+.7*sh)*(.55+.45*side);inDoor=1.;}",
    "   else{col=texture2D(uTex,vec2(p.x,mix(top,bot,w+(1.-e)))).rgb*(1.-.3*uOpen);col*=1.-.55*smoothstep(e-.035,e,w)*step(.002,uOpen);}",
    "  }",
    "  float sp=smoothstep(-.12,.1,u)*smoothstep(1.12,.9,u)*smoothstep(bot-.005,bot+.02,p.y)*smoothstep(bot+.36,bot,p.y);",
    "  col+=vec3(1.,.8,.55)*.22*sp*uOpen*uInL*(.4+col.g*2.);",
    " }",
    " float s=0.;vec3 tint=vec3(0.);",
    " for(int i=0;i<14;i++){float k=uI[i]*g(p,uZ[i]);s+=k;tint+=uC[i]*k;}",
    " s+=uSkyI*(g(p,uSky[0])+g(p,uSky[1]));",
    " float L=uAmb+(1.-uAmb)*clamp(s*1.35,0.,1.);",
    " if(uKind<.5){",
    "  float fb=smoothstep(uFire.x-.012,uFire.x+.012,p.x)*smoothstep(uFire.z+.012,uFire.z-.012,p.x)*smoothstep(uFire.y-.012,uFire.y+.012,p.y)*smoothstep(uFire.w+.012,uFire.w-.012,p.y);",
    "  L*=mix(1.,mix(.035,1.,uFireI),fb);",
    " }",
    " if(inDoor<.5)col*=L;",
    " float lum=dot(col,vec3(.3,.6,.1));col+=tint*lum*.5;",
    " if(uKind<.5){",   /* baie vitrée : nuit et stores */
    "  float wu=(p.x-uWin[0])/(uWin[2]-uWin[0]);float wt=mix(uWin[1],uWin[3],wu);float wv=(p.y-wt)/(uWin[4]-wt);",
    "  float inW=step(0.,wu)*step(0.,wv)*step(wv,1.);",
    "  col*=mix(1.,.13,uNight*inW);",
    "  float bl=inW*step(wv,uBlind*.985);",
    "  float weave=.92+.08*sin(p.y*700.)*sin(p.x*520.);",
    "  vec3 fab=vec3(.12,.108,.095)*weave*(.4+.8*L)*(.82+.3*wv)+col*.2;",
    "  fab*=1.-.5*smoothstep(uBlind*.985-.03,uBlind*.985,wv);",
    "  col=mix(col,fab,bl);",
    "  col+=vec3(1.,.42,.14)*uHeat*.16*smoothstep(.38,1.,p.y)*(.75+.25*sin(p.x*7.+p.y*11.-uTime*.9));",   /* la chaleur monte du plancher */
    " }",
    " if(uKind>1.5){",   /* phares */
    "  for(int i=0;i<2;i++){vec2 d=(p-uBeams[i].xy)*vec2(uAsp,1.);float r=uBeams[i].z;float dd=dot(d,d);",
    "   float gw=exp(-dd/(r*r*.05))*1.5+exp(-dd/(r*r))*.5+exp(-dd/(r*r*14.))*.12;",
    "   float fl=exp(-d.x*d.x/(r*r*3.))*exp(-((d.y-r*2.6)/(r*1.5))*((d.y-r*2.6)/(r*1.5)))*.22;",
    "   col+=vec3(.9,.95,1.)*(gw+fl)*uBeamI;}",
    " }",
    " gl_FragColor=vec4(col,1.);",
    "}"
  ].join("\n");

  function initGL() {
    try { gl = canvas.getContext("webgl", { antialias: false, alpha: false, powerPreference: "low-power" }); } catch (e) { gl = null; }
    if (!gl) return false;
    function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return gl.getShaderParameter(s, gl.COMPILE_STATUS) ? s : null; }
    var a = sh(gl.VERTEX_SHADER, VS), b = sh(gl.FRAGMENT_SHADER, FS);
    if (!a || !b) { gl = null; return false; }
    prog = gl.createProgram(); gl.attachShader(prog, a); gl.attachShader(prog, b); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { gl = null; return false; }
    gl.useProgram(prog);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, "a"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    ["uTex", "uAux", "uCover", "uZ", "uI", "uC", "uAmb", "uSkyI", "uBlind", "uFireI", "uHeat", "uTime", "uOpen", "uInL", "uBeamI", "uKind", "uNight", "uAsp",
      "uSky", "uFire", "uWin", "uDoor", "uCrop", "uMouse", "uBeams"].forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
    gl.uniform1i(U.uTex, 0); gl.uniform1i(U.uAux, 1);
    canvas.addEventListener("webglcontextlost", function (e) { e.preventDefault(); root.classList.remove("is-gl"); });
    return true;
  }
  function loadTex(url, cb) {
    if (tex[url]) { if (tex[url].ok) cb(); else tex[url].wait.push(cb); return; }
    var rec = tex[url] = { ok: false, wait: [cb], t: null, w: 1, h: 1 }, im = new Image();
    im.onload = function () {
      var t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, im);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      rec.t = t; rec.w = im.naturalWidth; rec.h = im.naturalHeight; rec.ok = true;
      rec.wait.forEach(function (f) { f(); }); rec.wait = [];
    };
    im.src = url;
  }
  /* Cadrage « cover » partagé par le shader, la photo de repli et les points de commande */
  function cover(sc) {
    var r = view.getBoundingClientRect(), ca = r.width / Math.max(1, r.height), ia = sc.ratio[0] / sc.ratio[1];
    var f = sc.focus.split(" "), fxp = parseFloat(f[0]) / 100, fyp = parseFloat(f[1]) / 100;
    if (ia > ca) { var sx = ca / ia; return [sx, 1, (1 - sx) * fxp, 0]; }
    var sy = ia / ca; return [1, sy, 0, (1 - sy) * fyp];
  }
  function placeSpots() {
    var sc = D.scenes[S.scene], c = cover(sc);
    sc.spots.forEach(function (s) {
      var el = s.el, x = (s.x / 100 - c[2]) / c[0], y = (s.y / 100 - c[3]) / c[1];
      el.style.setProperty("--px", (x * 100).toFixed(2) + "%"); el.style.setProperty("--py", (y * 100).toFixed(2) + "%");
      el.classList.toggle("is-out", x < .03 || x > .97 || y < .04 || y > .96);
      el.classList.toggle("is-left", x > .7);
    });
  }
  function resizeScene() {
    placeSpots();
    if (!gl) return;
    var r = view.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var w = Math.round(r.width * dpr), h = Math.round(r.height * dpr);
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; gl.viewport(0, 0, w, h); }
    sceneDirty = true; kick();
  }
  var shown = null;   // scène dont les textures sont prêtes
  function drawScene() {
    if (!gl || !shown) return;
    var sc = D.scenes[shown], kind = shown === "salon" ? 0 : shown === "entree" ? 1 : 2;
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex[sc.img].t);
    var aux = sc.inside || sc.depth;
    if (aux) { gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, tex[aux].t); }
    gl.uniform4fv(U.uCover, cover(sc));
    var Z = new Float32Array(56), I = new Float32Array(14), C = new Float32Array(42), n = 0;
    sc.spots.forEach(function (s) {
      if (!s.zones) return;
      var tone = TONES[S.L[s.key].tone][2];
      s.zones.forEach(function (z) {
        if (n > 13) return;
        Z.set(z, n * 4); I[n] = cur[s.key];
        C[n * 3] = tone[0] * .12; C[n * 3 + 1] = tone[1] * .12; C[n * 3 + 2] = tone[2] * .12; n++;
      });
    });
    gl.uniform4fv(U.uZ, Z); gl.uniform1fv(U.uI, I); gl.uniform3fv(U.uC, C);
    gl.uniform1f(U.uKind, kind); gl.uniform1f(U.uAmb, sc.amb * (1 - .3 * cur.night)); gl.uniform1f(U.uNight, cur.night);
    gl.uniform1f(U.uAsp, sc.ratio[0] / sc.ratio[1]);
    var sky = new Float32Array(8); if (sc.sky) { sky.set(sc.sky[0], 0); sky.set(sc.sky[1], 4); }
    gl.uniform4fv(U.uSky, sky); gl.uniform1f(U.uSkyI, sc.sky ? (1 - .86 * cur.night) * (1 - .8 * cur.blind) : 0);
    gl.uniform1fv(U.uWin, new Float32Array(sc.window || [2, 0, 3, 0, 1])); gl.uniform1f(U.uBlind, cur.blind);
    gl.uniform4fv(U.uFire, new Float32Array(sc.fire || [2, 2, 3, 3])); gl.uniform1f(U.uFireI, kind === 0 ? cur["salon:foyer"] : 0);
    gl.uniform1f(U.uHeat, cur.heat); gl.uniform1f(U.uTime, clockT);
    gl.uniform1fv(U.uDoor, new Float32Array(sc.door || [2, 0, 3, 0, 1, 1])); gl.uniform4fv(U.uCrop, new Float32Array(sc.crop || [0, 0, 1, 1]));
    gl.uniform1f(U.uOpen, cur.door); gl.uniform1f(U.uInL, cur.inL);
    gl.uniform2f(U.uMouse, cur.mx, cur.my);
    var bm = new Float32Array(6); if (sc.beams) { bm.set(sc.beams[0], 0); bm.set(sc.beams[1], 3); }
    gl.uniform3fv(U.uBeams, bm); gl.uniform1f(U.uBeamI, cur.beam);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }

  function showScene(key, quiet) {
    S.scene = key;
    var sc = D.scenes[key];
    $$("[data-vv-tab]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-vv-tab") === key ? "true" : "false"); });
    $$("[data-vv-spots]").forEach(function (b) { b.hidden = b.getAttribute("data-vv-spots") !== key; });
    $$("[data-vv-ph]").forEach(function (b) { b.hidden = b.getAttribute("data-vv-ph") !== key; });
    $(".vv-sky").hidden = key !== "salon";
    closePop(); placeSpots(); refreshLabels();
    if (gl) {
      var need = [sc.img]; if (sc.inside) need.push(sc.inside); if (sc.depth) need.push(sc.depth);
      var left = need.length;
      need.forEach(function (u) { loadTex(u, function () { if (--left === 0 && S.scene === key) { shown = key; root.classList.add("is-gl"); sceneDirty = true; kick(); } }); });
    }
    if (!quiet) changed();
  }

  /* ================================================================ Libellés et états liés */
  function watts() {
    var w = 0;
    Object.keys(S.L).forEach(function (k) { var s = SPOT[k]; w += (s.w || 0) * (lightTarget(k) - (s.on ? 1 : 0)); });
    return w;
  }
  function houseKw() { return D.en.house + watts() / 1000 + (S.vent ? .18 : 0) + clamp(S.set - D.th.set, -3, 4) * .35 + (S.L["salon:foyer"].on ? 0 : .25); }
  var J = $("[data-vv-jr]");
  function journal(txt) {
    var li = document.createElement("li"); li.className = "is-new"; li.innerHTML = "<time>16" + NB + "h" + NB + "40</time>" + esc(txt);
    J.insertBefore(li, J.firstChild); while (J.children.length > 5) J.removeChild(J.lastChild);
  }
  var toastEl = $("[data-vv-toast]"), toastT = 0;
  function toast(t) { toastEl.textContent = t; toastEl.classList.add("is-on"); clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove("is-on"); }, 4200); }

  function refreshLabels() {
    var sc = D.scenes[S.scene], on = 0, tot = 0;
    sc.spots.forEach(function (s) {
      var p = null;
      if (s.kind === "light" || s.kind === "fire") { p = S.L[s.key].on; if (s.kind === "light") { tot++; on += p; } }
      else if (s.kind === "blind") p = S.blind > .5 ? 1 : 0;
      else if (s.kind === "door") p = S.door;
      else if (s.kind === "beam") p = S.beam;
      if (p != null) s.el.setAttribute("aria-pressed", p ? "true" : "false");
    });
    $("[data-vv-where]").textContent = sc.label;
    var extra = S.scene === "salon" ? (S.L["salon:foyer"].on ? ", foyer allumé" : ", foyer éteint") : S.scene === "entree" ? (S.door ? ", porte 1 ouverte" : ", porte 1 fermée") : ", 2 véhicules";
    $("[data-vv-count]").textContent = on + (on > 1 ? " lumières allumées" : " lumière allumée") + " sur " + tot + extra;
    /* thermostat : le foyer aide, la consigne chauffe */
    var fire = S.L["salon:foyer"].on;
    S.inside = D.th.inside + (fire ? 0 : -.4) + (S.blind > .5 ? .1 : 0);
    $("[data-vv-inside]").textContent = fr(S.inside);
    var st = S.set > S.inside + .2 ? (fire ? "Le foyer aide, chauffe douce" : "Chauffe") : S.set < S.inside - .2 ? "Au repos" : "Température atteinte";
    $("[data-vv-th-state]").textContent = st;
    $("[data-vv-th]").classList.toggle("is-heat", S.set > S.inside + .2);
    $("[data-vv-room-t='salon']").textContent = fr(S.inside, 0);
    $("[data-vv-room-t='garage']").textContent = S.vent ? "10" : "12";
    /* énergie */
    var kw = houseKw(), batt = Math.max(0, kw - D.en.solar);
    $("[data-vv-house-kw]").textContent = fr(kw); $("[data-vv-batt-kw]").textContent = fr(batt);
    var hours = (D.en.cap * (D.en.soc - S.reserve) / 100) / Math.max(.4, kw * .45);
    $("[data-vv-auto]").textContent = "≈" + NB + Math.round(hours) + NB + "h d’autonomie, charges essentielles";
    $("[data-vv-res-v]").textContent = S.reserve + NB + "%";
    /* pièces éclairées dans la maquette */
    var sal = 0, n = 0; D.scenes.salon.spots.forEach(function (s) { if (s.zones) { sal += lightTarget(s.key); n++; } });
    S.lit.salon = sal / n;
    S.lit.garage = Math.max(S.door ? .9 : 0, .0);
  }
  listeners.push(refreshLabels);

  function setLight(key, on, level, silent) {
    var l = S.L[key], s = SPOT[key], was = l.on;
    if (on != null) l.on = on ? 1 : 0;
    if (level != null) l.level = clamp(level, .08, 1);
    if (!silent && was !== l.on) {
      journal(s.label + (l.on ? (s.kind === "fire" ? " allumé" : " : allumé") : (s.kind === "fire" ? " éteint" : " : éteint")));
      if (s.kind === "fire") toast(l.on ? "Foyer allumé. La thermopompe ralentit : le salon gagne 0,4 °C." : "Foyer éteint. La thermopompe reprend le relais.");
    }
    changed();
  }
  function setDoor(open) {
    S.door = open ? 1 : 0; S.vent = open ? 1 : 0;
    journal(open ? "Porte de garage 1 ouverte" : "Porte de garage 1 fermée");
    var old = $("[data-vv-sg='porte']"); if (old) old.remove();
    if (open) {   /* une proposition naît de l'état : la porte reste ouverte */
      var li = document.createElement("li"); li.className = "vv-sg"; li.setAttribute("data-vv-sg", "porte"); li.setAttribute("data-done", "Fermeture automatique de la porte 1 dans 10 minutes, s’il n’y a aucun mouvement.");
      li.innerHTML = '<p>La porte 1 est ouverte et il fait 2 °C dehors. Je la referme seule dans 10 minutes s’il n’y a aucun mouvement ?</p><div class="vv-sg-a"><button type="button" class="vv-go" data-vv-yes>Oui, referme-la</button><button type="button" class="vv-no" data-vv-no>Pas maintenant</button></div>';
      var ul = $("[data-vv-sgs]"); ul.insertBefore(li, ul.firstChild);
    }
    toast(open ? "Porte 1 ouverte. Ventilation du garage en marche, éclairage intérieur allumé." : "Porte 1 fermée et verrouillée. Ventilation arrêtée.");
    changed();
  }
  var AMB = {
    soiree: ["Soirée", { foyer: 1, pierre: 1, biblio: .6, corniche: .6, manger: 0, table: 1, terrasse: 0 }, 0],
    souper: ["Souper", { foyer: 1, pierre: .5, biblio: 0, corniche: .4, manger: 1, table: 1, terrasse: 0 }, 0],
    cinema: ["Cinéma", { foyer: 1, pierre: .2, biblio: 0, corniche: 0, manger: 0, table: .5, terrasse: 0 }, 1],
    eteindre: ["Tout éteint", { pierre: 0, biblio: 0, corniche: 0, manger: 0, table: 0, terrasse: 0 }, null],
    nuit: ["Nuit", { foyer: 0, pierre: 0, biblio: 0, corniche: .5, manger: 0, table: 0, terrasse: 0 }, 1]
  };
  function ambiance(id) {
    var a = AMB[id]; if (!a) return;
    Object.keys(a[1]).forEach(function (k) { var v = a[1][k], l = S.L["salon:" + k]; l.on = v > 0 ? 1 : 0; if (v > 0) l.level = v; });
    if (a[2] != null) S.blind = a[2];
    if (id === "nuit") setSky(1, true);
    journal("Ambiance « " + a[0] + " » au salon"); toast("Ambiance « " + a[0] + " » en place au salon.");
    if (S.scene !== "salon") showScene("salon", true);
    changed();
  }
  function setSky(n, quiet) {
    S.night = n;
    $$("[data-vv-sky]").forEach(function (b) { b.setAttribute("aria-pressed", (b.getAttribute("data-vv-sky") === "nuit") === !!n ? "true" : "false"); });
    if (!quiet) changed();
  }

  /* ================================================================ Panneau qui se déplie */
  var pop = $("[data-vv-pop]"), popKey = null;
  function closePop() { if (pop.hidden) return; pop.hidden = true; pop.innerHTML = ""; if (popKey && SPOT[popKey]) SPOT[popKey].el.classList.remove("is-open"); popKey = null; }
  function confirmRow(question, yes, cb) {
    return '<div class="vv-act" data-vv-confirm><p>' + esc(question) + '</p><button type="button" class="vv-go" data-vv-ok>' + esc(yes) + '</button><button type="button" class="vv-no" data-vv-cancel>Annuler</button></div>';
  }
  function arcHtml(val, lo, hi, unit) {
    return '<div class="vv-arc" data-vv-arc-s role="slider" tabindex="0" aria-label="Réglage" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + val + '">' +
      '<svg viewBox="0 20 256 76"><path class="tr" d="M12 84A150 150 0 0 1 244 84"/><path class="va" d="M12 84A150 150 0 0 1 244 84" pathLength="100" stroke-dasharray="' + val + ' 100"/><circle r="7"/></svg>' +
      "<output><span>" + val + "</span><small>" + unit + "</small></output><em>" + lo + "</em><em>" + hi + "</em></div>";
  }
  function arcSet(el, v) {
    v = Math.round(clamp(v, 0, 100));
    var th = (-50.65 + 101.3 * v / 100) * Math.PI / 180;
    el.querySelector(".va").setAttribute("stroke-dasharray", v + " 100");
    var c = el.querySelector("circle"); c.setAttribute("cx", (128 + 150 * Math.sin(th)).toFixed(1)); c.setAttribute("cy", (179.1 - 150 * Math.cos(th)).toFixed(1));
    el.querySelector("output span").textContent = v; el.setAttribute("aria-valuenow", v);
    return v;
  }
  function bindArc(el, onChange) {
    function at(e) { var r = el.getBoundingClientRect(); onChange(arcSet(el, ((e.clientX - r.left) / r.width * 256 - 12) / 232 * 100)); }
    el.addEventListener("pointerdown", function (e) { el.setPointerCapture(e.pointerId); at(e); el._d = 1; });
    el.addEventListener("pointermove", function (e) { if (el._d) at(e); });
    el.addEventListener("pointerup", function () { el._d = 0; }); el.addEventListener("pointercancel", function () { el._d = 0; });
    el.addEventListener("keydown", function (e) {
      var d = e.key === "ArrowRight" || e.key === "ArrowUp" ? 5 : e.key === "ArrowLeft" || e.key === "ArrowDown" ? -5 : 0;
      if (d) { e.preventDefault(); onChange(arcSet(el, +el.getAttribute("aria-valuenow") + d)); }
    });
    arcSet(el, +el.getAttribute("aria-valuenow"));
  }
  function openPop(key) {
    var s = SPOT[key];
    if (popKey === key) { closePop(); return; }
    closePop(); popKey = key; s.el.classList.add("is-open");
    var h = "", l = S.L[key];
    function head(sub, sw) {
      return '<div class="vv-pop-h"><h3>' + esc(s.label) + "<small data-vv-pop-sub>" + esc(sub) + "</small></h3>" +
        (sw != null ? '<button type="button" class="vv-sw" role="switch" data-vv-sw aria-checked="' + (sw ? "true" : "false") + '" aria-label="' + esc(s.label) + '"></button>' : "") +
        '<button type="button" class="vv-x" data-vv-close aria-label="Fermer">' + ic("x") + "</button></div>";
    }
    function sub() { return s.kind === "fire" ? (l.on ? "Allumé depuis " + (s.since || "16 h 40") : "Éteint") : l.on ? Math.round(s.w * l.level) + NB + "W, allumée depuis " + (s.since || "16 h 40") : "Éteinte"; }
    if (s.kind === "light") {
      h = head(sub(), l.on) + arcHtml(Math.round(l.level * 100), "Tamisé", "Plein", "%") +
        '<div class="vv-row"><span>Teinte du blanc</span>' + TONES.map(function (t, i) { return '<button type="button" class="vv-chip" data-vv-tone="' + i + '" aria-pressed="' + (l.tone === i ? "true" : "false") + '"><i style="--c:' + t[1] + '"></i>' + t[0] + "</button>"; }).join("") + "</div>" +
        (s.scene === "salon" ? '<div class="vv-row"><span>Ambiances du salon</span>' + ["soiree", "souper", "cinema", "eteindre"].map(function (a) { return '<button type="button" class="vv-chip" data-vv-amb="' + a + '">' + AMB[a][0] + "</button>"; }).join("") + "</div>" : "");
    } else if (s.kind === "fire") {
      h = head(sub(), l.on) + arcHtml(Math.round(l.level * 100), "Braise", "Vive", "%") +
        '<dl class="vv-kv"><div><dt>Chaleur fournie</dt><dd data-vv-fire-kw>' + (l.on ? fr(4.2 * l.level) + NB + "kW" : "0" + NB + "kW") + "</dd></div><div><dt>Arrêt automatique</dt><dd>23 h</dd></div><div><dt>Vitre</dt><dd>" + (l.on ? "Chaude, ne pas toucher" : "Tiède") + "</dd></div></dl>";
    } else if (s.kind === "blind") {
      h = head(S.blind > .5 ? "Baissés" : "Ouverts", null) + arcHtml(Math.round(S.blind * 100), "Ouverts", "Baissés", "%") +
        '<dl class="vv-kv"><div><dt>Coucher du soleil</dt><dd>16 h 24</dd></div><div><dt>Chaleur gardée, stores baissés</dt><dd>≈ 0,3 °C par heure</dd></div></dl>';
    } else if (s.kind === "door") {
      h = head(S.door ? "Ouverte" : "Fermée et verrouillée", null) +
        '<dl class="vv-kv"><div><dt>Caméra de l’allée</dt><dd>Personne en vue</dd></div><div><dt>Ventilation</dt><dd data-vv-vent>' + (S.vent ? "En marche, 10 min" : "Arrêtée") + "</dd></div><div><dt>Garage</dt><dd>" + (S.vent ? "10" : "12") + NB + "°C</dd></div><div><dt>Dernière ouverture</dt><dd>" + (S.door ? "À l’instant" : "9 h 38") + "</dd></div></dl>" +
        '<div class="vv-act"><button type="button" class="vv-go" data-vv-door>' + (S.door ? "Fermer la porte 1" : "Ouvrir la porte 1") + "</button></div>";
    } else if (s.kind === "beam") {
      h = head(S.beam ? "Allumés" : "Éteints", S.beam) + '<dl class="vv-kv"><div><dt>Batterie du coupé</dt><dd>12,8 V</dd></div><div><dt>Extinction automatique</dt><dd>30 secondes</dd></div></dl>';
    } else {
      h = head("Garage de collection", null) + '<dl class="vv-kv">' + s.rows.map(function (r) { return "<div><dt>" + esc(r[0]) + "</dt><dd>" + esc(r[1]) + "</dd></div>"; }).join("") + "</dl>";
    }
    h += '<p class="vv-tip">' + ic("spark") + "<span>" + esc(s.tip) + "</span></p>";
    pop.innerHTML = h;
    /* placement : le panneau naît du point touché, coin pointu vers lui */
    var vr = view.getBoundingClientRect(), er = s.el.getBoundingClientRect(), W = 292;
    var cx = er.left + er.width / 2 - vr.left, cy = er.top + er.height / 2 - vr.top;
    pop.hidden = false;
    var H = pop.offsetHeight, right = cx + 22 + W < vr.width - 8, below = cy + 14 + H < vr.height + 60;
    var left = right ? cx + 22 : cx - 22 - W, top = below ? cy + 10 : cy - 10 - H;
    left = clamp(left, 8, vr.width - W - 8); top = Math.max(8, top);
    pop.className = "vv-pop c-" + (below ? "t" : "b") + (right ? "l" : "r");
    pop.style.setProperty("--left", left + "px"); pop.style.setProperty("--top", top + "px");
    pop.style.setProperty("--ox", (cx - left) + "px"); pop.style.setProperty("--oy", (cy - top) + "px");
    pop.hidden = true; void pop.offsetWidth; pop.hidden = false;
    var arc = pop.querySelector("[data-vv-arc-s]");
    if (arc) bindArc(arc, function (v) {
      if (s.kind === "blind") { S.blind = v / 100; pop.querySelector("[data-vv-pop-sub]").textContent = v > 50 ? "Baissés" : "Ouverts"; changed(); }
      else { setLight(key, v > 4 ? 1 : 0, v / 100, false); syncPop(); }
    });
    function syncPop() {
      var sw = pop.querySelector("[data-vv-sw]"); if (sw && l) sw.setAttribute("aria-checked", l.on ? "true" : "false");
      if (l) pop.querySelector("[data-vv-pop-sub]").textContent = sub();
      var fk = pop.querySelector("[data-vv-fire-kw]"); if (fk) fk.textContent = (l.on ? fr(4.2 * l.level) : "0") + NB + "kW";
    }
    pop._sync = syncPop;
    var first = pop.querySelector("[data-vv-sw],[data-vv-door],[data-vv-close]"); if (first) first.focus({ preventScroll: true });
  }
  pop.addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    var s = SPOT[popKey], l = S.L[popKey];
    if (b.hasAttribute("data-vv-close")) { var el = s.el; closePop(); el.focus({ preventScroll: true }); }
    else if (b.hasAttribute("data-vv-sw")) {
      if (s.kind === "beam") { S.beam = S.beam ? 0 : 1; b.setAttribute("aria-checked", S.beam ? "true" : "false"); pop.querySelector("[data-vv-pop-sub]").textContent = S.beam ? "Allumés" : "Éteints"; journal(S.beam ? "Phares du coupé allumés à distance" : "Phares du coupé éteints"); changed(); }
      else { setLight(popKey, !l.on); pop._sync(); }
    }
    else if (b.hasAttribute("data-vv-tone")) { l.tone = +b.getAttribute("data-vv-tone"); $$("[data-vv-tone]", pop).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); if (!l.on) setLight(popKey, 1); else changed(); pop._sync(); sceneDirty = true; }
    else if (b.hasAttribute("data-vv-amb")) { ambiance(b.getAttribute("data-vv-amb")); pop._sync(); var a = pop.querySelector("[data-vv-arc-s]"); if (a) arcSet(a, l.level * 100); }
    else if (b.hasAttribute("data-vv-door")) {
      var act = b.parentNode;
      act.outerHTML = confirmRow(S.door ? "Fermer la porte 1 ? Rien ne bloque le passage." : "Ouvrir la porte 1 ? La caméra de l’allée ne voit personne.", S.door ? "Oui, fermer" : "Oui, ouvrir");
    }
    else if (b.hasAttribute("data-vv-ok")) { var k = popKey; setDoor(!S.door); closePop(); if (k) SPOT[k].el.focus({ preventScroll: true }); }
    else if (b.hasAttribute("data-vv-cancel")) { var k2 = popKey; closePop(); openPop(k2); }
  });
  $$("[data-vv-spot]").forEach(function (b) {
    var s = SPOT[b.getAttribute("data-vv-spot")]; s.el = b;
    b.addEventListener("click", function (e) { e.stopPropagation(); openPop(s.key); });
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { if (!pop.hidden) { var k = popKey; closePop(); SPOT[k].el.focus(); } else closeDrawer(); } });
  view.addEventListener("click", function () { closePop(); });
  view.addEventListener("pointermove", function (e) {
    if (e.pointerType === "touch" || !fx() || S.scene !== "collection") return;
    var r = view.getBoundingClientRect(); mouse.x = ((e.clientX - r.left) / r.width - .5) * 2; mouse.y = ((e.clientY - r.top) / r.height - .5) * 2; kick();
  });
  view.addEventListener("pointerleave", function () { mouse.x = 0; mouse.y = 0; kick(); });
  $$("[data-vv-tab]").forEach(function (b) { b.addEventListener("click", function () { showScene(b.getAttribute("data-vv-tab")); }); });
  $$("[data-vv-sky]").forEach(function (b) { b.addEventListener("click", function () { setSky(b.getAttribute("data-vv-sky") === "nuit" ? 1 : 0); }); });

  /* ================================================================ Cadran rond du thermostat */
  var th = $("[data-vv-th]"), dial = $("[data-vv-dial]"), tmin = +th.getAttribute("data-min"), tmax = +th.getAttribute("data-max");
  function drawDial() {
    function pt(v) { var a = (135 + 270 * (v - tmin) / (tmax - tmin)) * Math.PI / 180; return [100 + 88 * Math.cos(a), 100 + 88 * Math.sin(a)]; }
    var f = (S.set - tmin) / (tmax - tmin), k = pt(S.set), n = pt(S.inside);
    $("[data-vv-arc]").setAttribute("stroke-dasharray", (f * 75).toFixed(2) + " 100");
    var kn = $("[data-vv-knob]"); kn.setAttribute("cx", k[0].toFixed(2)); kn.setAttribute("cy", k[1].toFixed(2));
    var nd = $("[data-vv-nowdot]"); nd.setAttribute("cx", n[0].toFixed(2)); nd.setAttribute("cy", n[1].toFixed(2));
    $("[data-vv-set]").textContent = fr(S.set); dial.setAttribute("aria-valuenow", S.set); dial.setAttribute("aria-valuetext", fr(S.set) + " degrés");
  }
  function setTemp(v) { v = clamp(Math.round(v * 2) / 2, tmin, tmax); if (v === S.set) return; S.set = v; changed(); }
  listeners.push(drawDial);
  function dialAt(e) {
    var r = dial.getBoundingClientRect(), a = Math.atan2(e.clientY - r.top - r.height / 2, e.clientX - r.left - r.width / 2) * 180 / Math.PI;
    var rel = (a - 135 + 720) % 360; if (rel > 270) rel = rel > 315 ? 0 : 270;
    setTemp(tmin + rel / 270 * (tmax - tmin));
  }
  dial.addEventListener("pointerdown", function (e) {
    var r = dial.getBoundingClientRect(), d = Math.hypot(e.clientX - r.left - r.width / 2, e.clientY - r.top - r.height / 2);
    if (d < r.width * .33) return;   // le centre se lit, il ne se glisse pas
    dial.setPointerCapture(e.pointerId); dial._d = 1; dialAt(e);
  });
  dial.addEventListener("pointermove", function (e) { if (dial._d) dialAt(e); });
  function dialEnd() { if (dial._d) { dial._d = 0; journal("Consigne du rez-de-chaussée à " + fr(S.set) + NB + "°C"); } }
  dial.addEventListener("pointerup", dialEnd); dial.addEventListener("pointercancel", dialEnd);
  dial.addEventListener("keydown", function (e) {
    var d = e.key === "ArrowUp" || e.key === "ArrowRight" ? .5 : e.key === "ArrowDown" || e.key === "ArrowLeft" ? -.5 : 0;
    if (d) { e.preventDefault(); setTemp(S.set + d); }
  });
  $$("[data-vv-step]").forEach(function (b) { b.addEventListener("click", function () { setTemp(S.set + +b.getAttribute("data-vv-step")); }); });
  $$("[data-vv-res]").forEach(function (b) { b.addEventListener("click", function () { S.reserve = clamp(S.reserve + +b.getAttribute("data-vv-res"), 10, 50); changed(); }); });

  /* ================================================================ Ruban, propositions */
  var rbd = $("[data-vv-rb-d]");
  $$("[data-vv-ev]").forEach(function (b) {
    b.addEventListener("click", function () {
      $$("[data-vv-ev]").forEach(function (x) { x.classList.toggle("is-on", x === b); });
      var act = b.getAttribute("data-act");
      rbd.innerHTML = "<b>" + esc(b.textContent) + ".</b> " + esc(b.getAttribute("data-d")) + (act ? ' <button type="button" class="vv-chip" data-vv-run="' + act + '">Lancer maintenant</button>' : "");
    });
  });
  rbd.addEventListener("click", function (e) { var b = e.target.closest("[data-vv-run]"); if (b) ambiance(b.getAttribute("data-vv-run")); });
  $("[data-vv-sgs]").addEventListener("click", function (e) {
    var b = e.target.closest("button"), li = b && b.closest("[data-vv-sg]"); if (!li) return;
    var yes = b.hasAttribute("data-vv-yes");
    li.classList.add("is-done"); li.querySelector("p").textContent = yes ? li.getAttribute("data-done") : "D’accord, je n’y touche pas.";
    li.querySelector(".vv-sg-a").remove();
    if (yes) journal(li.getAttribute("data-done"));
  });

  /* ================================================================ Tiroir de pièce */
  var drawer = $("[data-vv-drawer]"), ROOM = {}; D.rooms.forEach(function (r) { ROOM[r.id] = r; });
  var LEVEL = { rdc: "Rez-de-chaussée", etage: "Étage" };
  function closeDrawer() { if (drawer.hidden) return; drawer.hidden = true; S.room = null; markRoom(); changed(); }
  function markRoom() { $$("[data-vv-room]").forEach(function (b) { b.classList.toggle("is-on", b.getAttribute("data-vv-room") === S.room); }); }
  function roomLights(r) {
    var keys = [];
    if (r.id === "salon") keys = D.scenes.salon.spots; else if (r.id === "garage") keys = D.scenes.entree.spots.concat(D.scenes.collection.spots);
    return keys.filter(function (s) { return s.kind === "light" || s.kind === "fire"; });
  }
  function renderDrawer() {
    var r = ROOM[S.room]; if (!r) return;
    var t = r.id === "salon" ? S.inside : r.id === "garage" ? (S.vent ? 10 : 12) : r.t;
    var ls = roomLights(r), li = ls.map(function (s) {
      var l = S.L[s.key];
      return "<li>" + esc(s.label) + "<span>" + (l.on ? (s.kind === "fire" ? "Allumé" : Math.round(l.level * 100) + NB + "%") : "Éteint") + '</span><button type="button" class="vv-sw" role="switch" data-vv-dsw="' + s.key + '" aria-checked="' + (l.on ? "true" : "false") + '" aria-label="' + esc(s.label) + '"></button></li>';
    }).join("");
    if (!ls.length) li = "<li>Éclairage de la pièce<span>" + (S.lit[r.id] ? "Allumé" : "Éteint") + '</span><button type="button" class="vv-sw" role="switch" data-vv-dlit aria-checked="' + (S.lit[r.id] ? "true" : "false") + '" aria-label="Éclairage de la pièce"></button></li>';
    var ex = (r.extra || []).map(function (x) { return "<div><dt>" + esc(x[0]) + "</dt><dd>" + esc(x[0] === "Plancher radiant" && S.vent ? "15 °C, en relance" : x[1]) + "</dd></div>"; }).join("");
    drawer.innerHTML =
      '<div class="vv-dr-h"><div><h2>' + esc(r.label) + "</h2><p>" + LEVEL[r.level] + (r.scene ? ", affiché dans la scène" : "") + '</p></div><button type="button" class="vv-x" data-vv-dclose aria-label="Fermer le tiroir">' + ic("x") + "</button></div>" +
      '<p class="vv-dr-t"><b>' + fr(t, t % 1 ? 1 : 0) + "<small>°C</small></b><span>Humidité " + r.hum + NB + "%" + (r.id === "garage" && S.vent ? ", ventilation en marche" : "") + "</span></p>" +
      (ex ? '<dl class="vv-kv">' + ex + "</dl>" : "") +
      "<h3>Éclairage</h3><ul class=\"vv-li\">" + li + "</ul>" +
      '<p class="vv-next">' + ic("clock") + "<span>" + esc(r.next) + "</span></p>" +
      '<div class="vv-act" data-vv-acts>' + r.acts.map(function (a) { return '<button type="button" class="vv-chip" data-vv-do="' + a[0] + '">' + esc(a[0] === "porte" && S.door ? "Fermer la porte 1" : a[1]) + "</button>"; }).join("") + "</div>" +
      "<h3>Aujourd’hui</h3><ol class=\"vv-jr\">" + r.hist.map(function (x) { var m = x.match(/^(\S+(?: h(?: \d+)?)?)\s(.*)$/); return "<li><time>" + esc(m ? m[1] : "") + "</time>" + esc(m ? m[2] : x) + "</li>"; }).join("") + "</ol>";
  }
  function openRoom(id, ev) {
    var r = ROOM[id]; if (!r) return;
    S.room = id; markRoom();
    if (ev && ev.clientX != null) {
      var dw = Math.min(400, innerWidth - 24), dx = innerWidth - 12 - dw;
      drawer.style.setProperty("--ox", clamp((ev.clientX - dx) / dw * 100, 0, 100) + "%"); drawer.style.setProperty("--oy", clamp(ev.clientY / innerHeight * 100, 0, 100) + "%");
    }
    renderDrawer(); drawer.hidden = true; void drawer.offsetWidth; drawer.hidden = false;
    if (r.scene && S.scene !== r.scene && !(r.id === "garage" && S.scene === "collection")) showScene(r.scene, true);
    if (r.level !== S.level && S.level !== "tout") setLevel(r.level);
    changed();
    var c = drawer.querySelector("[data-vv-dclose]"); if (c) c.focus({ preventScroll: true });
  }
  var DONE = {
    cellier: ["Verrouiller le cellier ?", "Oui, verrouiller", "Cellier verrouillé."],
    ventiler: ["Ventiler le garage 10 minutes ?", "Oui, ventiler", "Ventilation du garage en marche pour 10 minutes."],
    fenetre: ["Placer un rappel à 21 h pour la fenêtre ?", "Oui, à 21 h", "Rappel placé à 21 h : fermer la fenêtre de la suite."],
    prechauffer: ["Préchauffer la suite à 20 °C pour 22 h ?", "Oui, préchauffer", "La suite sera à 20 °C à 22 h."],
    cinema: ["Préparer la salle : projecteur, son et lumières tamisées ?", "Oui, préparer", "Cinéma maison prêt dans 2 minutes."]
  };
  drawer.addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    if (b.hasAttribute("data-vv-dclose")) { closeDrawer(); return; }
    if (b.hasAttribute("data-vv-dsw")) { var k = b.getAttribute("data-vv-dsw"); setLight(k, !S.L[k].on); renderDrawer(); return; }
    if (b.hasAttribute("data-vv-dlit")) { S.lit[S.room] = S.lit[S.room] ? 0 : 1; journal(ROOM[S.room].label + " : éclairage " + (S.lit[S.room] ? "allumé" : "éteint")); renderDrawer(); changed(); return; }
    var acts = b.closest("[data-vv-acts]"), id = b.getAttribute("data-vv-do");
    if (id) {
      if (id === "soiree" || id === "eteindre") { ambiance(id); renderDrawer(); return; }
      var q = id === "porte" ? [S.door ? "Fermer la porte 1 ?" : "Ouvrir la porte 1 ? La caméra de l’allée ne voit personne.", S.door ? "Oui, fermer" : "Oui, ouvrir"] : DONE[id];
      acts.innerHTML = "<p>" + esc(q[0]) + '</p><button type="button" class="vv-go" data-vv-dok="' + id + '">' + esc(q[1]) + '</button><button type="button" class="vv-no" data-vv-dno>Annuler</button>';
      return;
    }
    if (b.hasAttribute("data-vv-dno")) { renderDrawer(); return; }
    if (b.hasAttribute("data-vv-dok")) {
      id = b.getAttribute("data-vv-dok");
      if (id === "porte") { if (S.scene !== "entree") showScene("entree", true); setDoor(!S.door); }
      else { if (id === "ventiler") S.vent = 1; journal(DONE[id][2]); toast(DONE[id][2]); changed(); }
      renderDrawer();
    }
  });
  $$("[data-vv-room]").forEach(function (b) { b.addEventListener("click", function (e) { openRoom(b.getAttribute("data-vv-room"), e); }); });
  function setLevel(lv) {
    S.level = lv;
    $$("[data-vv-level]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-vv-level") === lv ? "true" : "false"); });
    $$("[data-vv-room]").forEach(function (b) { b.classList.toggle("is-dim", lv !== "tout" && ROOM[b.getAttribute("data-vv-room")].level !== lv); });
    changed();
  }
  $$("[data-vv-level]").forEach(function (b) { b.addEventListener("click", function () { setLevel(b.getAttribute("data-vv-level")); }); });

  /* ================================================================ 2. Objets 3D */
  function css(n) { return getComputedStyle(root).getPropertyValue(n).trim(); }
  function init3D(T) {
    var mode = function () { return doc.getAttribute("data-mode") || "signature"; };
    var mobile = innerWidth < 900;
    var envCache = {}, stages = [];
    function makeStage(cv, fov) {
      var r = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true, powerPreference: "high-performance" });
      r.setPixelRatio(Math.min(window.devicePixelRatio || 1, mobile ? 1.5 : 2));
      r.toneMapping = T.ACESFilmicToneMapping; r.toneMappingExposure = 1.2; r.outputColorSpace = T.SRGBColorSpace;
      r.shadowMap.enabled = !mobile; r.shadowMap.type = T.PCFShadowMap;
      var st = { r: r, cv: cv, scene: new T.Scene(), cam: new T.PerspectiveCamera(fov, 1, .1, 400), dirty: true, pm: new T.PMREMGenerator(r) };
      stages.push(st);
      st.size = function () {
        var b = cv.parentNode.getBoundingClientRect(); if (!b.width) return;
        r.setSize(b.width, b.height, false); st.cam.aspect = b.width / b.height; st.cam.updateProjectionMatrix(); st.dirty = true;
      };
      st.env = function () {
        var m = mode(), url = D.modes[m];
        new T.TextureLoader().load(url, function (tx) {
          tx.mapping = T.EquirectangularReflectionMapping; tx.colorSpace = T.SRGBColorSpace;
          var rt = st.pm.fromEquirectangular(tx); st.scene.environment = rt.texture; tx.dispose(); st.dirty = true; kick();
        });
      };
      return st;
    }
    function phys(o) { return new T.MeshPhysicalMaterial(o); }
    function box(g, w, h, d, m, x, y, z, sh) {
      var me = new T.Mesh(new T.BoxGeometry(w, h, d), m); me.position.set(x, y + h / 2, z);
      if (sh !== false) { me.castShadow = true; me.receiveShadow = true; }
      g.add(me); return me;
    }
    function glowTex() {
      var c = document.createElement("canvas"); c.width = c.height = 128; var x = c.getContext("2d");
      var g = x.createRadialGradient(64, 64, 0, 64, 64, 64); g.addColorStop(0, "rgba(255,255,255,.55)"); g.addColorStop(.35, "rgba(255,255,255,.16)"); g.addColorStop(1, "rgba(255,255,255,0)");
      x.fillStyle = g; x.fillRect(0, 0, 128, 128); return new T.CanvasTexture(c);
    }
    var GT = glowTex();
    function grainTex(rep) {   /* grain fin pour la pierre et le sol : relief seulement, aucune couleur */
      var c = document.createElement("canvas"); c.width = c.height = 256; var x = c.getContext("2d"), d = x.createImageData(256, 256), seed = 7;
      for (var i = 0; i < d.data.length; i += 4) { seed = (seed * 16807) % 2147483647; var v = 90 + (seed % 120); d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
      x.putImageData(d, 0, 0); x.globalAlpha = .5; x.drawImage(c, 0, 0, 128, 128, 0, 0, 256, 256);
      var t = new T.CanvasTexture(c); t.wrapS = t.wrapT = T.RepeatWrapping; t.repeat.set(rep, rep); return t;
    }
    var PAL = {
      signature: { accent: 0xa98759, warm: 0xffc98c, key: 0xfff1de, rim: 0x8fa6d8, water: 0x1d5560 },
      platinum: { accent: 0xc9d3e2, warm: 0xfff0dc, key: 0xf2f6ff, rim: 0x9fc0ff, water: 0x2a6f86 },
      base: { accent: 0x8c8c8e, warm: 0xf3e6d2, key: 0xffffff, rim: 0xaab2c0, water: 0x24505a }
    };

    /* ---------------- Maquette de la résidence ---------------- */
    var H = makeStage($("[data-vv-h3d]"), 26), hs = H.scene;
    var mAccent = phys({ color: 0xb8925f, metalness: 1, roughness: .34, envMapIntensity: 1.3 });
    var mClad = phys({ color: 0xb8925f, metalness: .85, roughness: .58, envMapIntensity: .8 });
    var mWall = phys({ color: 0x302d2a, roughness: .86, metalness: 0, bumpMap: grainTex(3), bumpScale: .6 });
    var mStone = phys({ color: 0x4a4540, roughness: .95, metalness: 0, bumpMap: grainTex(2), bumpScale: 1.6 });
    var mRoof = phys({ color: 0x131313, roughness: .5, metalness: .2, clearcoat: .4, clearcoatRoughness: .45, envMapIntensity: .45 });
    var mPlinth = phys({ color: 0x040404, roughness: .12, metalness: .3, clearcoat: 1, clearcoatRoughness: .08, envMapIntensity: 1.4 });
    var mLawn = phys({ color: 0x0b0b0b, roughness: .55, metalness: .1, clearcoat: .5, clearcoatRoughness: .45, envMapIntensity: .5, bumpMap: grainTex(14), bumpScale: .25 });
    var mPave = phys({ color: 0x232221, roughness: .42, metalness: .15, envMapIntensity: .6 });
    var mDeck = phys({ color: 0x38342f, roughness: .6, bumpMap: grainTex(6), bumpScale: .4 });
    var mGlass = phys({ color: 0x0b0d10, roughness: .04, metalness: .1, transparent: true, opacity: .32, clearcoat: 1, envMapIntensity: 1.8, depthWrite: false });
    var mPanel = phys({ color: 0x060a12, roughness: .15, metalness: .5, clearcoat: 1, envMapIntensity: 1.6 });
    var mDoor = phys({ color: 0x1a1a1b, roughness: .5, metalness: .6 });
    var mFloor = phys({ color: 0x1b1a19, roughness: .6 });
    var mFurn = phys({ color: 0x0f0f0f, roughness: .7 });
    var mWater = phys({ color: 0x051417, roughness: .04, metalness: .3, clearcoat: 1, emissive: 0x1d5560, emissiveIntensity: .42, envMapIntensity: 1.4 });
    var mStrip = new T.MeshBasicMaterial({ toneMapped: false, color: 0xffc98c });
    var world = new T.Group(); hs.add(world);
    var gBase = new T.Group(), gRdc = new T.Group(), gUp = new T.Group(), gRoof = new T.Group(), gGarRoof = new T.Group();
    world.add(gBase, gRdc, gUp, gRoof, gGarRoof); world.position.set(.6, 0, -1.4);
    /* socle et terrain */
    box(gBase, 31.6, 1.1, 22.6, mPlinth, -.6, -1.25, 1.4);
    box(gBase, 31.72, .05, 22.72, mAccent, -.6, -.28, 1.4, false);
    box(gBase, 30.6, .16, 21.6, mLawn, -.6, -.15, 1.4);
    box(gBase, 9.4, .06, 8.2, mPave, 9.3, 0, 7.6);          // allée du garage
    box(gBase, 13.6, .22, 4.6, mDeck, -3.2, 0, 5.4);         // terrasse
    box(gBase, 13.6, .05, .08, mStrip, -3.2, .0, 7.74, false); // filet lumineux sous la terrasse
    box(gBase, 8.2, .1, 3.4, mStone, -9.6, 0, 9.9);          // margelle
    box(gBase, 7.4, .08, 2.6, mWater, -9.6, .06, 9.9, false);  // piscine
    box(gBase, 7.2, .03, .05, mStrip, -9.6, .13, 8.66, false);
    box(gBase, 2.3, .34, 2.3, mStone, -3.7, 0, 9.9); box(gBase, 1.8, .06, 1.8, mWater, -3.7, .32, 9.9, false);   // spa
    box(gBase, 3.2, .5, .5, mStone, 2.6, 0, 8.1); box(gBase, .5, .5, 3.4, mStone, 14.4, 0, 9.6);   // muret, jardinière
    [[4.8, 4.2], [4.8, 6.4], [4.8, 8.6], [4.8, 10.8], [13.8, 4.2], [13.8, 6.4], [13.8, 8.6], [13.8, 10.8]].forEach(function (p) {
      box(gBase, .1, .42, .1, mAccent, p[0], 0, p[1]); box(gBase, .14, .05, .14, mStrip, p[0], .42, p[1], false);
    });

    /* pièces : volume cliquable, sol lumineux, halo */
    var rooms = {}, pickables = [];
    function room(id, g, x0, x1, z0, z1, y, h) {
      var w = x1 - x0, d = z1 - z0, cx = (x0 + x1) / 2, cz = (z0 + z1) / 2;
      var gm = new T.MeshBasicMaterial({ toneMapped: false, color: 0xffc98c });
      var fl = box(g, w - .5, .06, d - .5, gm, cx, y + .12, cz, false);
      var bk = box(g, w - .5, h - .5, .05, gm, cx, y + .2, z0 + .32, false);
      var pm = new T.MeshBasicMaterial({ toneMapped: false, color: 0xffffff, transparent: true, opacity: 0, depthWrite: false });
      var pk = box(g, w, h, d, pm, cx, y, cz, false); pk.userData.room = id; pk.renderOrder = 5; pickables.push(pk);
      var sp = new T.Sprite(new T.SpriteMaterial({ map: GT, color: 0xffc98c, blending: T.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0 }));
      sp.position.set(cx, y + h * .5, z1 + .4); sp.scale.set(w * 1.5, h * 2.6, 1); g.add(sp);
      rooms[id] = { gm: gm, pm: pm, sp: sp, lv: 0, hot: 0, x: cx, y: y + h / 2, z: cz };
    }
    /* rez-de-chaussée : x de -10 à 4, z de -6 à 3 */
    box(gRdc, 14.2, .2, 9.2, mFloor, -3, 0, -1.5);
    box(gRdc, 14, 3.3, .3, mWall, -3, .2, -5.85);                    // mur arrière
    box(gRdc, .3, 3.3, 9, mWall, -9.85, .2, -1.5);                   // pignon gauche
    box(gRdc, .22, 3.3, 8.4, mWall, -2, .2, -1.6);                   // cloison salon / cuisine
    box(gRdc, 1.7, 8.6, 1.5, mStone, -9.1, .2, 2.4);                 // cheminée de pierre
    box(gRdc, 1.2, .5, .9, new T.MeshBasicMaterial({ toneMapped: false, color: 0xff9a4a }), -8.9, .9, 2.0, false).userData.fire = 1;
    for (var i = 0; i <= 6; i++) box(gRdc, .09, 3.3, .09, mAccent, -8.2 + i * 2.03, .2, 3, false);   // meneaux
    box(gRdc, 12.2, 3.1, .06, mGlass, -2.1, .3, 2.96, false);         // baie vitrée
    box(gRdc, 3.4, .75, 1.3, mFurn, -6.4, .2, .4); box(gRdc, 1.3, .75, 2.6, mFurn, -4.4, .2, -.6); box(gRdc, 1.6, .4, 1, mFurn, -6.4, .2, -1.4);   // canapé, table
    box(gRdc, 3.2, .95, 1.1, mFurn, 1, .2, -.6); box(gRdc, 5.2, 2.4, .6, mFurn, 1, .2, -5.3);   // îlot, cuisine
    room("salon", gRdc, -10, -2, -6, 3, .2, 3.3); room("cuisine", gRdc, -2, 4, -6, 3, .2, 3.3);
    /* garage : x de 4 à 13.6, z de -5 à 3.6 */
    box(gRdc, 9.6, .2, 8.6, mFloor, 8.8, 0, -.7);
    box(gRdc, 9.6, 3.5, .3, mWall, 8.8, .2, -4.85); box(gRdc, .3, 3.5, 8.6, mWall, 13.45, .2, -.7); box(gRdc, .3, 3.5, 8.6, mWall, 4.15, .2, -.7);
    box(gRdc, 9.6, .7, .3, mWall, 8.8, 3.0, 3.45); box(gRdc, .7, 2.8, .3, mWall, 4.35, .2, 3.45); box(gRdc, .6, 2.8, .3, mWall, 8.8, .2, 3.45); box(gRdc, .7, 2.8, .3, mWall, 13.25, .2, 3.45);
    function gdoor(x) {
      var g = new T.Group(); g.position.set(x, 3.0, 3.42);
      for (var k = 0; k < 5; k++) { var p = new T.Mesh(new T.BoxGeometry(3.7, .52, .08), mDoor); p.position.set(0, -.28 - k * .56, 0); p.castShadow = true; g.add(p); }
      gRdc.add(g); return g;
    }
    var door1 = gdoor(6.6); gdoor(11.0);
    room("garage", gRdc, 4, 13.6, -5, 3.6, .2, 3.5);
    /* plafond du rez-de-chaussée, étage (bardage métallique), toits */
    box(gUp, 14.9, .3, 10.2, mRoof, -3, 3.5, -1.2);
    box(gUp, 14.96, .06, 10.26, mAccent, -3, 3.62, -1.2, false);
    box(gUp, 11, 3, .3, mClad, -.5, 3.8, -5.35); box(gUp, .3, 3, 9.6, mClad, -5.85, 3.8, -.7); box(gUp, .3, 3, 9.6, mClad, 4.85, .0 + 3.8, -.7);
    box(gUp, 11, .2, 9.6, mFloor, -.5, 3.8, -.7);
    box(gUp, .2, 3, 9, mWall, .2, 3.8, -.7);                           // cloison suite / cinéma
    box(gUp, 5.2, 3, .3, mClad, 2.4, 3.8, 3.95);                       // façade pleine du cinéma
    box(gUp, 1.6, 1.1, .34, mGlass, 2.4, 4.9, 3.96, false);
    for (i = 0; i < 26; i++) { if (i > 8 && i < 17) continue; box(gUp, .06, 2.9, .1, mAccent, -.05 + i * .2, 3.85, 4.14, false); }
    for (i = 0; i <= 3; i++) box(gUp, .08, 3, .08, mAccent, -5.7 + i * 1.9, 3.8, 4.05, false);
    box(gUp, 5.9, 2.8, .06, mGlass, -2.85, 3.9, 4.0, false);
    box(gUp, 2.4, .6, 2.2, mFurn, -3.4, 4.0, -2.6); box(gUp, 2.4, 1.1, .25, mFurn, -3.4, 4.0, -3.8);   // lit
    for (i = 0; i < 3; i++) box(gUp, 3.2, .5 + i * .18, .8, mFurn, 2.6, 4.0, -1.2 - i * 1.3);         // gradins du cinéma
    box(gUp, 3.6, 1.9, .06, new T.MeshBasicMaterial({ toneMapped: false, color: 0x1a2230 }), 2.6, 4.5, 3.7, false);       // écran
    room("suite", gUp, -6, .2, -5.5, 4.1, 3.9, 3); room("cinema", gUp, .2, 5, -5.5, 4.1, 3.9, 3);
    box(gRoof, 12.6, .28, 11.4, mRoof, -.5, 6.8, -.4);
    box(gRoof, 12.66, .06, 11.46, mAccent, -.5, 6.9, -.4, false);
    for (i = 0; i < 12; i++) { var pv = box(gRoof, 1.7, .05, 1.05, mPanel, -4.9 + (i % 6) * 1.78, 7.2, -3.4 + Math.floor(i / 6) * 1.5, false); pv.rotation.x = -.14; }
    box(gGarRoof, 10.4, .26, 9.6, mRoof, 8.9, 3.7, -.5);
    box(gGarRoof, 10.46, .06, 9.66, mAccent, 8.9, 3.78, -.5, false);

    var hemi = new T.HemisphereLight(0x9fb2d0, 0x14100c, .7); hs.add(hemi);
    var key = new T.DirectionalLight(0xfff1de, 2.3); key.position.set(-22, 30, 20); key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 5; key.shadow.bias = -.0006; key.shadow.normalBias = .04;
    var sc_ = key.shadow.camera; sc_.left = -24; sc_.right = 24; sc_.top = 24; sc_.bottom = -24; sc_.near = 5; sc_.far = 90;
    hs.add(key);
    var rim = new T.DirectionalLight(0x8fa6d8, .7); rim.position.set(20, 12, -22); hs.add(rim);
    var pl = new T.PointLight(0xffc98c, 0, 30, 1.6); pl.position.set(-4, 2.4, 6.5); hs.add(pl);
    var spillM = new T.MeshBasicMaterial({ toneMapped: false, map: GT, color: 0xffc98c, blending: T.AdditiveBlending, transparent: true, depthWrite: false, opacity: 0 });
    var spill = new T.Mesh(new T.PlaneGeometry(18, 9), spillM); spill.rotation.x = -Math.PI / 2; spill.position.set(-3, .26, 5.6); gBase.add(spill);

    var cam = { az: -.62, el: .46, dist: 86, tEl: .46, tDist: 86, ty: 1.6, auto: true };
    var lift = { up: 0, roof: 0, gar: 0 }, doorK = 0;
    function placeCam() {
      var c = H.cam, ce = Math.cos(cam.el);
      c.position.set(Math.sin(cam.az) * ce * cam.dist, cam.ty + Math.sin(cam.el) * cam.dist, Math.cos(cam.az) * ce * cam.dist);
      c.lookAt(0, cam.ty, 0);
    }
    function ease(o, k, t, dt, rate) { var c = o[k]; if (!fx()) { o[k] = t; return c !== t; } var n = c + (t - c) * (1 - Math.exp(-(rate || 4) * dt)); if (Math.abs(t - n) < .003) n = t; o[k] = n; return n !== c; }
    var warm = new T.Color(), tmpc = new T.Color();
    tick3d.push(function (dt) {
      if (!vis.house) return false;
      var b = false, lv = S.level;
      b = ease(lift, "up", lv === "rdc" ? 9.5 : 0, dt) || b;
      b = ease(lift, "roof", lv === "etage" ? 6 : lv === "rdc" ? 9.5 : 0, dt) || b;
      b = ease(lift, "gar", lv === "rdc" ? 5 : 0, dt) || b;
      b = ease(cam, "el", cam.tEl, dt, 3) || b; b = ease(cam, "dist", cam.tDist, dt, 3) || b;
      gUp.position.y = lift.up; gRoof.position.y = lift.roof; gGarRoof.position.y = lift.gar;
      if (Math.abs(doorK - cur.door) > .001) { doorK = cur.door; b = true; }
      door1.children.forEach(function (p, k) { var y0 = -.28 - k * .56; p.position.y = y0 * (1 - doorK * .93); p.scale.y = 1 - doorK * .9; });
      var lit = { salon: S.lit.salon, cuisine: S.lit.cuisine, garage: Math.max(cur.inL, (cur["collection:rubans"] || 0) * .35), suite: S.lit.suite, cinema: S.lit.cinema * .6 };
      Object.keys(rooms).forEach(function (id) {
        var r = rooms[id];
        b = ease(r, "lv", clamp(lit[id], 0, 1), dt, 5) || b;
        b = ease(r, "hot", S.room === id ? 1 : hover === id ? .55 : 0, dt, 8) || b;
        tmpc.copy(warm).multiplyScalar(.03 + r.lv * .97); r.gm.color.copy(tmpc);
        r.sp.material.opacity = r.lv * .62; r.pm.opacity = r.hot * .16;
      });
      pl.intensity = rooms.salon.lv * 90; spillM.opacity = rooms.salon.lv * .5;
      gRdc.children.forEach(function (m) { if (m.userData.fire) m.material.color.setRGB(1, .55, .22).multiplyScalar(.04 + cur["salon:foyer"] * 1.2); });
      if (cam.auto && fx()) { cam.az += dt * .07; b = true; }
      if (b || H.dirty) { placeCam(); H.r.render(hs, H.cam); H.dirty = false; }
      return b;
    });
    /* glisser pour tourner, toucher pour ouvrir une pièce */
    var hover = null, ray = new T.Raycaster(), v2 = new T.Vector2(), tag = $("[data-vv-h3d-tag]");
    function pick(e) {
      var r = H.cv.getBoundingClientRect(); v2.set((e.clientX - r.left) / r.width * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
      ray.setFromCamera(v2, H.cam);
      var list = pickables.filter(function (p) { var lv = ROOM[p.userData.room].level; return S.level === "tout" || lv === S.level || (S.level === "rdc" && lv === "rdc"); });
      var hit = ray.intersectObjects(list, false)[0]; return hit ? hit.object.userData.room : null;
    }
    function orbit(st, c, limits) {
      var d = null;
      st.cv.addEventListener("pointerdown", function (e) { d = { x: e.clientX, y: e.clientY, m: 0 }; st.cv.setPointerCapture(e.pointerId); c.auto = false; });
      st.cv.addEventListener("pointermove", function (e) {
        if (d) {
          var dx = e.clientX - d.x, dy = e.clientY - d.y; d.x = e.clientX; d.y = e.clientY; d.m += Math.abs(dx) + Math.abs(dy);
          c.az -= dx * .008; if (limits.az) c.az = clamp(c.az, -limits.az, limits.az);
          c.el = c.tEl = clamp(c.el + dy * .005, limits.el[0], limits.el[1]); st.dirty = true; kick();
        } else if (limits.hover) limits.hover(e);
      });
      function up(e) { if (d && d.m < 6 && limits.click) limits.click(e); d = null; }
      st.cv.addEventListener("pointerup", up); st.cv.addEventListener("pointercancel", function () { d = null; });
      st.cv.addEventListener("pointerleave", function () { if (limits.leave) limits.leave(); });
    }
    orbit(H, cam, {
      el: [.16, 1.15],
      hover: function (e) {
        if (e.pointerType === "touch") return;
        var id = pick(e);
        if (id !== hover) { hover = id; H.cv.style.cursor = id ? "pointer" : ""; $$("[data-vv-room]").forEach(function (b) { b.classList.toggle("is-hot", b.getAttribute("data-vv-room") === id); }); kick(); }
        tag.hidden = !id;
        if (id) { var r = H.cv.getBoundingClientRect(); tag.textContent = ROOM[id].label; tag.style.left = (e.clientX - r.left) + "px"; tag.style.top = (e.clientY - r.top) + "px"; }
      },
      leave: function () { hover = null; tag.hidden = true; $$("[data-vv-room]").forEach(function (b) { b.classList.remove("is-hot"); }); kick(); },
      click: function (e) { var id = pick(e); if (id) openRoom(id, e); }
    });
    listeners.push(function () {
      cam.tEl = S.level === "tout" ? Math.min(cam.el, .6) : Math.max(cam.el, .78); cam.tDist = S.level === "rdc" ? 98 : S.level === "etage" ? 92 : 86;
      if (S.level === "tout" && cam.el > .6) cam.tEl = .46;
    });

    /* ---------------- Batteries domestiques ---------------- */
    var B = makeStage($("[data-vv-b3d]"), 28), bs = B.scene;
    function rrect(w, h, r) {
      var s = new T.Shape(), x = -w / 2, y = -h / 2;
      s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
      s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s;
    }
    function slab(w, h, d, r, m, bevel) {
      var g = new T.ExtrudeGeometry(rrect(w, h, r), { depth: d, bevelEnabled: true, bevelThickness: bevel || .012, bevelSize: bevel || .012, bevelSegments: 4, curveSegments: 20 });
      var me = new T.Mesh(g, m); me.castShadow = true; me.receiveShadow = true; return me;
    }
    var mBody = phys({ color: 0x2a2a2b, roughness: .36, metalness: .8, clearcoat: .5, clearcoatRoughness: .25, envMapIntensity: 1.3 });
    var mBack = phys({ color: 0x0a0a0a, roughness: .7, metalness: .2 });
    var mCell = phys({ color: 0x1c1c1d, roughness: .45, metalness: .85 });
    var mBGlass = phys({ color: 0x050607, roughness: .03, metalness: 0, transparent: true, opacity: .34, clearcoat: 1, envMapIntensity: 2, depthWrite: false });
    var mBAcc = phys({ color: 0xb8925f, metalness: 1, roughness: .3, envMapIntensity: 1.4 });
    var bw = new T.Group(); bs.add(bw);
    var ringM = new T.MeshBasicMaterial({ toneMapped: false, color: 0xb8925f });
    var bars = [], NC = 12;
    function cabinet(x) {
      var g = new T.Group(); g.position.set(x, -.02, 0);
      var body = slab(.84, 2.1, .18, .1, mBody, .02); body.position.z = -.12; g.add(body);
      var rec = slab(.56, 1.74, .01, .05, mBack, .004); rec.position.set(0, -.06, .062); g.add(rec);
      var fr_ = new T.Mesh(new T.ExtrudeGeometry((function () { var s = rrect(.6, 1.78, .07); s.holes.push(rrect(.576, 1.756, .058)); return s; })(), { depth: .012, bevelEnabled: false, curveSegments: 20 }), mBAcc);
      fr_.position.set(0, -.06, .112); g.add(fr_);
      var list = [];
      for (var k = 0; k < NC; k++) {
        var y = -.84 + k * .1418;
        var c = new T.Mesh(new T.BoxGeometry(.48, .11, .05), mCell); c.position.set(0, y, .075); g.add(c);
        var bm = new T.MeshBasicMaterial({ toneMapped: false, color: 0x223322 });
        var b = new T.Mesh(new T.BoxGeometry(.38, .026, .012), bm); b.position.set(0, y, .104); g.add(b);
        var sp = new T.Sprite(new T.SpriteMaterial({ map: GT, color: 0xa6c3a2, blending: T.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0 }));
        sp.position.set(0, y, .16); sp.scale.set(.8, .2, 1); g.add(sp);
        list.push({ m: bm, sp: sp });
      }
      var gl_ = slab(.576, 1.756, .012, .055, mBGlass, .004); gl_.position.set(0, -.06, .125); gl_.castShadow = false; g.add(gl_);
      var dot = new T.Mesh(new T.CylinderGeometry(.014, .014, .01, 20), ringM); dot.rotation.x = Math.PI / 2; dot.position.set(0, .93, .085); g.add(dot);
      bw.add(g); bars.push(list); return g;
    }
    cabinet(-.56).rotation.y = .14; cabinet(.56).rotation.y = -.14;
    var FY = -1.1, refl = bw.clone(true); refl.scale.y = -1; refl.position.y = 2 * FY; bs.add(refl);
    refl.traverse(function (o) { o.castShadow = false; });
    var veil = new T.Mesh(new T.PlaneGeometry(9, 6), new T.MeshBasicMaterial({ toneMapped: false, color: 0x000000, transparent: true, opacity: .8, depthWrite: false })); veil.rotation.x = -Math.PI / 2; veil.position.y = FY; veil.renderOrder = 2; bs.add(veil);
    var fl2 = new T.Mesh(new T.PlaneGeometry(8, 5), new T.ShadowMaterial({ opacity: .5 })); fl2.rotation.x = -Math.PI / 2; fl2.position.y = FY + .002; fl2.renderOrder = 3; fl2.receiveShadow = true; bs.add(fl2);
    var fglow = new T.Sprite(new T.SpriteMaterial({ map: GT, color: 0xa6c3a2, blending: T.AdditiveBlending, depthWrite: false, transparent: true, opacity: .2 }));
    fglow.position.set(0, FY + .06, .5); fglow.scale.set(4, .5, 1); fglow.renderOrder = 4; bs.add(fglow);
    bs.add(new T.HemisphereLight(0xb9c6dc, 0x141414, 1.3));
    var bk = new T.DirectionalLight(0xfff1de, 4.2); bk.position.set(-3, 4, 6); bk.castShadow = true; bk.shadow.mapSize.set(1024, 1024); bk.shadow.radius = 6; bk.shadow.bias = -.0008;
    var bc = bk.shadow.camera; bc.left = -3; bc.right = 3; bc.top = 3; bc.bottom = -3; bc.near = 1; bc.far = 16; bs.add(bk);
    var br = new T.DirectionalLight(0x8fa6d8, 1.2); br.position.set(4, 1, -2); bs.add(br);
    var bcam = { az: -.42, el: .08, tEl: .08, auto: false }, soc = [0, 0], okC = new T.Color(), pulse = 0;
    tick3d.push(function (dt) {
      if (!vis.batt) return false;
      var b = false;
      D.en.packs.forEach(function (p, i) { b = ease(soc, i, p.soc / 100, dt, 1.1) || b; });
      var breathe = fx(); if (breathe) pulse += dt;
      bars.forEach(function (list, i) {
        var f = soc[i] * NC;
        list.forEach(function (c, k) {
          var lv = clamp(f - k, 0, 1); if (breathe && lv > 0 && lv < 1) lv *= .7 + .3 * Math.sin(pulse * 2.2);
          tmpc.copy(okC).multiplyScalar(.05 + lv * .95); c.m.color.copy(tmpc); c.sp.material.opacity = lv * .3;
        });
      });
      if (b || B.dirty || breathe) {
        var c = B.cam, d = 7.4, ce = Math.cos(bcam.el);
        c.position.set(Math.sin(bcam.az) * ce * d, .05 + Math.sin(bcam.el) * d, Math.cos(bcam.az) * ce * d); c.lookAt(0, -.12, 0);
        if (!breathe || b || B.dirty || (pulseSkip = !pulseSkip)) B.r.render(bs, B.cam);
        B.dirty = false;
      }
      return b || breathe;
    });
    var pulseSkip = false;
    orbit(B, bcam, { az: 1.05, el: [-.12, .5] });

    /* ---------------- Mode : accent, lumière et environnement ---------------- */
    function applyMode() {
      var p = PAL[mode()] || PAL.signature;
      [mAccent, mClad, mBAcc].forEach(function (m) { m.color.setHex(p.accent); });
      mClad.roughness = mode() === "platinum" ? .32 : .5;
      ringM.color.setHex(p.accent); warm.setHex(p.warm); mStrip.color.setHex(p.warm); pl.color.setHex(p.warm); spillM.color.setHex(p.warm);
      key.color.setHex(p.key); bk.color.setHex(p.key); rim.color.setHex(p.rim); br.color.setHex(p.rim);
      mWater.emissive.setHex(p.water);
      okC.set(css("--ok") || "#a6c3a2"); okC.offsetHSL(0, .1, -.04); fglow.material.color.copy(okC); bars.forEach(function (l) { l.forEach(function (c) { c.sp.material.color.copy(okC); }); });
      Object.keys(rooms).forEach(function (id) { rooms[id].sp.material.color.setHex(p.warm); });
      stages.forEach(function (s) { s.env(); s.dirty = true; });
      kick();
    }
    new MutationObserver(applyMode).observe(doc, { attributes: true, attributeFilter: ["data-mode"] });
    applyMode();
    stages.forEach(function (s) { s.size(); });
    addEventListener("resize", function () { stages.forEach(function (s) { s.size(); }); kick(); });
    root.classList.add("is-3d");
    kick();
  }

  /* ================================================================ Démarrage */
  function watch(el, name) {
    if (!("IntersectionObserver" in window)) { vis[name] = true; return; }
    new IntersectionObserver(function (es) {
      vis[name] = es[0].isIntersecting;
      if (name === "scene") root.classList.toggle("is-paused", !vis.scene);
      if (vis[name]) { sceneDirty = true; kick(); }
    }, { rootMargin: "80px" }).observe(el);
  }
  watch(view, "scene"); watch($("[data-vv-h3d]"), "house"); watch($("[data-vv-b3d]"), "batt");
  var glOk = initGL();
  showScene("salon", true);
  drawDial(); refreshLabels();
  addEventListener("resize", resizeScene); resizeScene();
  new MutationObserver(function () { sceneDirty = true; kick(); }).observe(doc, { attributes: true, attributeFilter: ["class"] });
  if (!glOk) root.classList.add("no-gl");
  var probe = document.createElement("canvas"), can3d = false;
  try { can3d = !!(probe.getContext("webgl2")); } catch (e) { can3d = false; }
  if (!can3d) { root.classList.add("no-3d"); return; }
  import("/assets/vendor/three.module.min.js").then(function (T) {
    try { init3D(T); } catch (e) { root.classList.add("no-3d"); }
  }, function () { root.classList.add("no-3d"); });
})();
