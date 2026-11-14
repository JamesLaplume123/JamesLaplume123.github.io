/* Laboratoire des cartes « Matière » (page privée /labo-cartes/).
   Chaque carte est une dalle rendue par un shader WebGL2 écrit à la main : verre qui réfracte la
   vraie scène du mode, biseau qui accroche la lumière, cristal à facettes avec dispersion, verre fumé.
   Le texte reste en HTML par-dessus (chiffres nets). Sans WebGL2 : repli CSS avec les vraies images.
   Mouvement seulement sous html.fx; hors écran, rien ne tourne. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var root = document.querySelector("[data-mt-root]");
  if (!root) return;
  function $(s, r) { return (r || root).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || root).querySelectorAll(s)); }
  function c01(v) { return Math.max(0, Math.min(1, v)); }
  function fr(v, d) { return v.toFixed(d).replace(".", ",").replace("-", "−"); }

  var dirty = true;
  function poke() { dirty = true; }

  /* ---------- Thermostat : glisser sur le cadran, boutons − / +, clavier ---------- */
  var dial = $("[data-mt-dial]");
  var TH = { min: +dial.dataset.min, max: +dial.dataset.max, set: +dial.dataset.set, now: +dial.dataset.now, shown: +dial.dataset.set };
  var SWEEP = 270, A0 = -135;
  var elSet = $("[data-mt-set]"), elState = $("[data-mt-state]"), elArc = $("[data-mt-arc]");
  function paintThermo() {
    var f = c01((TH.set - TH.min) / (TH.max - TH.min));
    elSet.textContent = fr(TH.set, 1);
    dial.setAttribute("aria-valuenow", TH.set);
    dial.setAttribute("aria-valuetext", fr(TH.set, 1) + " degrés");
    var heat = TH.set > TH.now + 0.2;
    elState.textContent = heat ? "Chauffage en cours" : (TH.set < TH.now - 0.2 ? "Au repos, consigne atteinte" : "Température maintenue");
    dial.classList.toggle("is-heat", heat);
    if (elArc) elArc.setAttribute("stroke-dasharray", (f * 100).toFixed(2) + " 100");
    poke();
  }
  function setTemp(v) {
    v = Math.round(Math.max(TH.min, Math.min(TH.max, v)) * 2) / 2;
    if (v === TH.set) return;
    TH.set = v; paintThermo();
  }
  function fromPointer(e) {
    var r = dial.getBoundingClientRect();
    var x = e.clientX - (r.left + r.width / 2), y = e.clientY - (r.top + r.height / 2);
    var a = Math.atan2(x, -y) * 180 / Math.PI;
    if (a < A0 && a < -157.5) a = 135; else if (a < A0) a = A0;
    if (a > 135) a = a > 157.5 ? (x < 0 ? A0 : 135) : 135;
    setTemp(TH.min + (a - A0) / SWEEP * (TH.max - TH.min));
  }
  var dragging = false;
  dial.addEventListener("pointerdown", function (e) {
    var r = dial.getBoundingClientRect();
    var d = Math.hypot(e.clientX - (r.left + r.width / 2), e.clientY - (r.top + r.height / 2)) / (r.width / 2);
    if (d < 0.6 || d > 1.08) return;              /* seul l'anneau se saisit; le centre reste lisible */
    dragging = true; dial.setPointerCapture(e.pointerId); dial.classList.add("is-drag"); fromPointer(e); e.preventDefault();
  });
  dial.addEventListener("pointermove", function (e) { if (dragging) fromPointer(e); });
  ["pointerup", "pointercancel"].forEach(function (n) {
    dial.addEventListener(n, function () { dragging = false; dial.classList.remove("is-drag"); });
  });
  dial.addEventListener("keydown", function (e) {
    var k = e.key, s = 0;
    if (k === "ArrowUp" || k === "ArrowRight") s = 0.5; else if (k === "ArrowDown" || k === "ArrowLeft") s = -0.5;
    else if (k === "Home") { setTemp(TH.min); e.preventDefault(); return; } else if (k === "End") { setTemp(TH.max); e.preventDefault(); return; }
    if (s) { setTemp(TH.set + s); e.preventDefault(); }
  });
  $$("[data-mt-step]").forEach(function (b) {
    b.addEventListener("click", function () { setTemp(TH.set + (+b.dataset.mtStep)); });
  });
  paintThermo();

  /* ---------- Porte du garage ---------- */
  var door = $("[data-mt-door]");
  if (door) door.addEventListener("click", function () {
    var open = door.getAttribute("aria-pressed") !== "true";
    door.setAttribute("aria-pressed", open ? "true" : "false");
    $("[data-mt-door-l]").textContent = open ? "Fermer la porte 1" : "Ouvrir la porte 1";
    $("[data-mt-door-v]").textContent = open ? "Ouverte" : "Fermée";
  });

  /* ================================================================ WebGL2 */
  var VERT = "#version 300 es\nin vec2 a;void main(){gl_Position=vec4(a,0.,1.);}";
  var FRAG = [
    "#version 300 es",
    "precision highp float;",
    "uniform vec2 uRes,uCard,uOrigin,uView,uCover,uLight;",
    "uniform float uDpr,uPad,uTime,uRefl,uRadius;",
    "uniform vec3 uMat;uniform int uKind;",
    "uniform sampler2D uS0,uS1,uS2,uPhoto;",
    "uniform vec3 uDial;uniform vec2 uArc;",
    "uniform vec4 uSeg[3];uniform float uFlow[3];uniform vec3 uNode[4];",
    "uniform vec4 uTube[2];uniform float uLevel[2];uniform float uReserve;",
    "uniform vec4 uPhotoR,uPhotoUV;uniform float uPhotoOn;",
    "out vec4 o;",
    "float h1(float n){return fract(sin(n*127.1)*43758.5453);}",
    "float h2(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}",
    "float ns(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);",
    " return mix(mix(h2(i),h2(i+vec2(1,0)),f.x),mix(h2(i+vec2(0,1)),h2(i+vec2(1,1)),f.x),f.y);}",
    "float sdRR(vec2 p,vec2 b,float r){vec2 q=abs(p)-b+r;return min(max(q.x,q.y),0.)+length(max(q,0.))-r;}",
    "vec3 spectrum(float x){return clamp(.55+.55*cos(6.2832*(x+vec3(0.,.33,.67))),0.,1.);}",
    /* la vraie scène du mode, floue selon lod (mipmaps) */
    "vec3 scene(vec2 vp,float lod){vec2 uv=(vp-.5*uView)*uCover+.5;vec3 c=vec3(0.);",
    " if(uMat.x>.002)c+=uMat.x*textureLod(uS0,uv,lod).rgb;",
    " if(uMat.y>.002)c+=uMat.y*textureLod(uS1,uv,lod).rgb;",
    " if(uMat.z>.002)c+=uMat.z*textureLod(uS2,uv,lod).rgb;return c;}",
    "vec3 L3(){return normalize(vec3(uLight,.62));}",
    "float spec(vec3 n,float sh){vec3 H=normalize(L3()+vec3(0.,0.,1.));return pow(max(dot(n,H),0.),sh);}",
    /* verre : réfraction de la scène, dispersion chromatique en Platinum */
    "vec3 glass(vec2 p,vec3 n,float lod,float k){vec2 vp=uOrigin+p,off=n.xy*k;",
    " if(uMat.y>.02){float d=.1*uMat.y;return vec3(scene(vp+off*(1.-d),lod).r,scene(vp+off,lod).g,scene(vp+off*(1.+d),lod).b);}",
    " return scene(vp+off,lod);}",
    "vec3 tint(){return uMat.x*vec3(1.,.87,.66)+uMat.y*vec3(.88,.94,1.)+uMat.z*vec3(.66,.67,.69);}",
    "vec3 glowc(){return uMat.x*vec3(1.,.74,.36)+uMat.y*vec3(.9,.95,1.)+uMat.z*vec3(.82,.83,.85);}",
    "vec3 deepc(){return uMat.x*vec3(.78,.36,.05)+uMat.y*vec3(.42,.56,.86)+uMat.z*vec3(.34,.35,.37);}",
    /* tube de verre (profil u de 0 au centre à 1 au bord), rempli ou non de lumière liquide */
    "vec3 tube(vec2 p,vec2 dir,float u,float fill,float along,vec3 liq,vec3 liqDeep,vec3 under){",
    " vec3 n=vec3(dir*u,sqrt(max(1.-u*u,0.)));",
    " vec3 g=glass(p,n,1.2,26.)*tint()*.9+under*.35;",
    " g+=tint()*pow(u,3.)*.22;",
    " float st=.92+.08*sin(along*31.-uTime*1.1+sin(along*13.+uTime*.4)*2.);",
    " vec3 l=mix(liqDeep,liq,pow(n.z,2.2))*st;",
    " l+=uMat.y*spectrum(u*.55+along*1.7+dir.x*.2)*(1.-n.z)*.4;",
    " l+=vec3(1.,.98,.94)*pow(n.z,14.)*.4;",
    " vec3 c=mix(g,l,fill);",
    " c+=vec3(1.,.97,.92)*spec(n,36.)*(.55+.6*fill);",
    " c+=tint()*smoothstep(.8,1.,u)*.16;",
    " return c;}",
    /* ---------- la dalle et tout ce qu'elle porte ---------- */
    "vec4 card(vec2 p){",
    " vec2 hc=.5*uCard;vec2 q=p-hc;",
    " float d=sdRR(q,hc,uRadius);",
    " vec2 g=normalize(vec2(sdRR(q+vec2(1.,0.),hc,uRadius)-sdRR(q-vec2(1.,0.),hc,uRadius),sdRR(q+vec2(0.,1.),hc,uRadius)-sdRR(q-vec2(0.,1.),hc,uRadius))+1e-5);",
    " vec3 L=L3();vec3 gc=glowc(),tn=tint();",
    " if(d>0.){",   /* hors dalle : ombre de contact, lueur du mode */
    "  float sh=.42*exp(-d/16.);float lit=pow(max(dot(g,-L.xy)*.5+.5,0.),3.);",
    "  vec3 gl=gc*exp(-d/9.)*.16*lit*(uMat.x+uMat.y*.9+uMat.z*.3);",
    "  return vec4(gl,sh);}",
    " float bw=uMat.x*13.+uMat.y*24.+uMat.z*8.;",
    " float t=clamp(-d/bw,0.,1.);float s=1.-t;",
    /* biseau : rond en Signature/Base, taillé à facettes en Platinum */
    " float per=abs(g.x)>abs(g.y)?p.y:p.x;float side=g.x*2.+g.y*5.;",
    " float band=min(floor(t*3.),2.);float ft=fract(min(t,.999)*3.);",   /* taille à degrés : trois gradins plats, longues facettes */
    " float sid=floor(side+.5);float sk=per/(74.+38.*band)+h1(band*3.+sid)*7.+(ft-.5)*.22;",
    " float cell=floor(sk)+sid*17.+band*53.;float fx=fract(sk);",
    " float fe=min(min(fx,1.-fx)*(74.+38.*band),min(ft,1.-ft)*bw/3.);float br=h1(cell);",
    " vec2 nr=g*s*s*1.25;",
    " vec2 nf=g*(.95-.33*band)+vec2(-g.y,g.x)*(br-.5)*.5;",
    " vec2 nxy=mix(nr,nf*step(.001,s),uMat.y);",
    " float wav=uMat.x*.07+uMat.z*.02;",
    " nxy+=wav*vec2(sin(p.y*.021+uTime*.21+sin(p.x*.013)*2.),cos(p.x*.017-uTime*.17+sin(p.y*.011)*2.))*t;",
    " vec3 n=normalize(vec3(nxy,1.));",
    " float lod=uMat.x*3.1+uMat.y*2.5+uMat.z*4.3;",
    " vec3 body=glass(p,n,mix(1.2,lod,t),mix(46.,150.-uMat.y*70.,t))*tn;",
    " body=mix(body,vec3(dot(body,vec3(.3,.55,.15)))*tn,uMat.x*.45);",
    " float grain=(h2(floor(p*uDpr))-.5);",
    " body+=uMat.z*grain*.018;",
    " float dark=(uMat.x*.87+uMat.y*.8+uMat.z*.83)*smoothstep(0.,1.,t*1.15);",
    " vec3 col=mix(body*(1.+.9*s)*(1.-uMat.x*.35),vec3(.012,.011,.011)+body*.06,dark);",
    /* reflet d'environnement sur le biseau */
    " float fres=pow(1.-n.z,1.6);",
    " col+=scene(uOrigin+p-n.xy*260.,1.6)*tn*fres*(uMat.x*1.2+uMat.y*2.2+uMat.z*.8);",
    " float lit=max(dot(g,-L.xy),0.);",
    " col+=vec3(1.,.96,.9)*spec(n,uMat.x*28.+uMat.y*70.+uMat.z*14.)*s*(uMat.x*1.5+uMat.y*2.2+uMat.z*.5);",
    /* arêtes : filet vif dehors, filet fin dedans (la taille du verre) */
    " float e1=smoothstep(2.4,.5,-d);float e2=smoothstep(1.3,0.,abs(-d-bw));",
    " col+=mix(gc,vec3(1.),.35)*e1*(.22+1.25*pow(lit,2.))*(uMat.x+uMat.y*1.15+uMat.z*.5);",
    " col+=gc*e2*(.1+.5*pow(max(dot(g,L.xy),0.),2.))*(uMat.x+uMat.y+uMat.z*.4);",
    " float fm=uMat.y*step(.001,s);",
    " col*=1.-fm*.5*step(br,.34);",
    " col+=fm*(vec3(.9,.95,1.)*exp(-fe*1.5)*.42+spectrum(ft*.5+br*.6+dot(nxy,L.xy)*.6)*exp(-fe*.6)*.13);",
    /* intérieur : voile de lumière en haut, rubans de verre (Signature, Base) ou éclats (Platinum) */
    " float inner=smoothstep(.9,1.,t);",
    " col+=tn*inner*.05*smoothstep(uCard.y*.55,0.,p.y);",
    " float xw=p.x/uCard.x;",
    " float y1=uCard.y*(.9-.2*xw*xw)+sin(xw*3.1+uTime*.13)*16.;",
    " float y2=uCard.y*(.99-.42*xw)+sin(xw*2.3-uTime*.11+1.3)*20.;",
    " float lo=min(y1,y2),hi=max(y1,y2);",
    " float fillr=smoothstep(lo-1.,lo+1.,p.y)*smoothstep(hi+1.,hi-1.,p.y);",
    " float er=exp(-abs(p.y-y1)*1.7)+exp(-abs(p.y-y2)*1.7);",
    " float hot=pow(.5+.5*sin(xw*5.2+uLight.x*2.2+uTime*.19),6.);",
    " float rb=uMat.x+uMat.z*.45;",
    " col+=inner*rb*(gc*fillr*(.02+.04*hot)+mix(gc,vec3(1.),.4)*er*(.05+.5*hot));",
    " float dg=q.x*.74+q.y*.67;",   /* Platinum : la table du cristal renvoie deux plans de lumière en biais */
    " float pl=exp(-pow((dg-uLight.x*120.+90.)/54.,2.))+.6*exp(-pow((dg-uLight.x*120.-170.)/20.,2.));",
    " col+=uMat.y*inner*vec3(.8,.88,1.)*pl*.045;",
    /* ---------- cadran : anneau de verre, arc de lumière liquide, perle ---------- */
    " if(uKind==1){",
    "  vec2 v=p-uDial.xy;float r=length(v);float R=uDial.z;float w=R*.092;const float A=2.35619;",
    "  float a=atan(v.x,-v.y);float aa=clamp(a,-A,A);float af=(aa+A)/(2.*A);",
    "  vec2 cp=R*vec2(sin(aa),-cos(aa));float dr=length(v-cp);",
    "  float Ri=R-w-R*.16;",
    "  if(r<Ri){float u=r/Ri;vec3 nd=normalize(vec3(v/Ri*.55,1.));",   /* lentille centrale : assombrit, garde le chiffre net */
    "   col=mix(col,vec3(.006)+glass(p,nd,4.,30.)*tn*.07,.9);",
    "   col+=tn*.07*pow(max(dot(nd,normalize(L+vec3(0.,0.,1.))),0.),6.)*smoothstep(1.,.2,u);",
    "   col+=gc*smoothstep(3.,0.,Ri-r)*.2;}",
    "  float fillA=smoothstep(uArc.x+.003,uArc.x-.003,af);",
    "  float gd=max(dr-w,0.);",
    "  col+=gc*exp(-gd/(R*.07))*fillA*.24*(uMat.x+uMat.y*.8+uMat.z*.4);",
    /* graduations gravées, allumées jusqu'à la consigne */
    "  float ti=((a+A)/(2.*A))*54.;float tf=abs(fract(ti+.5)-.5)*(2.*A/54.)*r;",
    "  float maj=step(abs(mod(floor(ti+.5),9.)),.5);",
    "  float tin=R-w-R*mix(.105,.135,maj),tout=R-w-R*.05;",
    "  float tk=smoothstep(mix(.75,1.1,maj),.1,tf)*step(tin,r)*step(r,tout)*step(-A-.02,a)*step(a,A+.02);",
    "  float ton=step(ti/54.,uArc.x+.004);",
    "  col=mix(col,mix(vec3(.5,.5,.52)*.5,gc*1.25,ton),tk*mix(.55,.95,ton));",
    /* repère de la température intérieure */
    "  float an=-A+2.*A*uArc.y;float dn=abs(a-an)*r;",
    "  col=mix(col,vec3(1.),smoothstep(1.3,.3,dn)*step(R+w+R*.035,r)*step(r,R+w+R*.1));",
    "  float u=dr/w;",
    "  if(u<1.){vec2 dir=(v-cp)/max(dr,1e-4);",
    "   vec3 tc=tube(p,dir,u,fillA,af,gc,deepc(),col);",
    "   col=mix(col,tc,smoothstep(1.,.9,u));}",
    "  float ak=-A+2.*A*uArc.x;vec2 kp=R*vec2(sin(ak),-cos(ak));float dk=length(v-kp);float rk=w*1.6;",
    "  col+=gc*exp(-max(dk-rk,0.)/(R*.05))*.22;",
    "  if(dk<rk){float uk=dk/rk;vec2 kd=(v-kp)/max(dk,1e-4);vec3 nk=vec3(kd*uk,sqrt(max(1.-uk*uk,0.)));",
    "   vec3 kc=glass(p,nk,.6,-34.)*tn*.8+mix(deepc()*.5,gc,pow(nk.z,3.))*.5;",
    "   kc+=uMat.y*spectrum(uk*.7+kd.x*.3+kd.y*.2)*(1.-nk.z)*.4;",
    "   kc+=vec3(1.)*spec(nk,70.)*2.2+mix(gc,vec3(1.),.5)*pow(uk,7.)*.7;",
    "   col=mix(col,kc,smoothstep(1.,.93,uk));}",
    " }",
    /* ---------- flux : tubes de verre où circule la lumière, perles aux nœuds ---------- */
    " if(uKind==2){",
    "  for(int i=0;i<3;i++){vec2 A0=uSeg[i].xy,B0=uSeg[i].zw;vec2 pa=p-A0,ba=B0-A0;float len=length(ba);",
    "   float hh=clamp(dot(pa,ba)/dot(ba,ba),0.,1.);vec2 dv=pa-ba*hh;float dd=length(dv);float w=3.5+6.5*uFlow[i];",
    "   float pulse=.42+.58*pow(.5+.5*sin(hh*len*.085-uTime*2.6-float(i)*1.7),3.);",
    "   col+=gc*exp(-max(dd-w,0.)/9.)*.2*pulse*(uMat.x+uMat.y*.8+uMat.z*.45);",
    "   if(dd<w){float u=dd/w;vec3 tc=tube(p,dv/max(dd,1e-4),u,pulse,hh*len/160.,gc,deepc(),col);col=mix(col,tc,smoothstep(1.,.85,u));}}",
    "  for(int i=0;i<4;i++){vec2 nv=p-uNode[i].xy;float rr=uNode[i].z;float dd=length(nv);",
    "   col+=gc*exp(-max(dd-rr,0.)/7.)*.1;",
    "   if(dd<rr){float u=dd/rr;vec3 nn=normalize(vec3(nv/rr*pow(u,3.)*1.6,1.));",
    "    vec3 nc=mix(vec3(.01)+glass(p,nn,3.5,60.)*tn*.16,glass(p,nn,1.5,90.)*tn*1.1,smoothstep(.7,1.,u));",
    "    nc+=vec3(1.,.96,.9)*spec(nn,24.)*1.2*smoothstep(.6,1.,u)+mix(gc,vec3(1.),.3)*smoothstep(.93,1.,u)*(.3+.9*max(dot(nv/max(dd,1e-4),-L.xy),0.));",
    "    nc+=uMat.y*spectrum(u*1.5+nv.x*.02)*smoothstep(.72,1.,u)*.16;",
    "    col=mix(col,nc,smoothstep(1.,.96,u));}}",
    " }",
    /* ---------- batteries : cylindres de verre, énergie verte liquide ---------- */
    " if(uKind==3){",
    "  vec3 gr=vec3(.204,.827,.6),grD=vec3(.02,.36,.24);",
    "  for(int i=0;i<2;i++){vec4 T=uTube[i];vec2 hb=.5*T.zw;vec2 tq=p-(T.xy+hb);float rad=hb.y;",
    "   float sd=sdRR(tq,hb,rad);float lx=T.x+T.z*uLevel[i];",
    "   float inl=smoothstep(lx+1.,lx-1.,p.x);",
    "   col+=gr*exp(-max(sd,0.)/11.)*.17*smoothstep(lx+20.,lx-10.,p.x);",
    "   if(sd<0.){float u=clamp(1.+sd/rad,0.,1.);",
    "    vec2 tg=normalize(vec2(sdRR(tq+vec2(1.,0.),hb,rad)-sdRR(tq-vec2(1.,0.),hb,rad),sdRR(tq+vec2(0.,1.),hb,rad)-sdRR(tq-vec2(0.,1.),hb,rad))+1e-5);",
    "    float core=smoothstep(.86,.7,u);",   /* liquide au cœur, paroi de verre du mode autour */
    "    float men=exp(-abs(p.x-lx)*.45);",
    "    vec3 liq=gr*(1.+.5*men);vec3 tc=tube(p,tg,u,inl*core,(p.x-T.x)/150.,liq,grD,col);",
    "    tc=mix(tc,tc*.55+vec3(.01),(1.-inl)*core*.5);",
    "    float rx=T.x+T.z*uReserve;tc=mix(tc,vec3(.98,.75,.14),smoothstep(1.2,.3,abs(p.x-rx))*core*.9);",
    "    col=mix(col,tc,smoothstep(0.,-1.2,sd));}}",
    " }",
    /* ---------- véhicule : la photo réelle sous une vitre biseautée (jamais teintée) ---------- */
    " if(uKind==4&&uPhotoOn>.5){",
    "  vec2 hb=.5*uPhotoR.zw;vec2 pq=p-(uPhotoR.xy+hb);float sd=sdRR(pq,hb,12.);",
    "  if(sd<0.){vec2 uv=(p-uPhotoR.xy)/uPhotoR.zw*uPhotoUV.xy+uPhotoUV.zw;",
    "   vec3 ph=texture(uPhoto,uv).rgb;",
    "   float bev=smoothstep(7.,0.,-sd);",
    "   vec2 pg=normalize(vec2(sdRR(pq+vec2(1.,0.),hb,12.)-sdRR(pq-vec2(1.,0.),hb,12.),sdRR(pq+vec2(0.,1.),hb,12.)-sdRR(pq-vec2(0.,1.),hb,12.))+1e-5);",
    "   float gl=exp(-pow((pq.x*.8+pq.y*.6-uLight.x*90.+60.)/70.,2.))*.05;",
    "   ph+=vec3(1.)*gl+mix(gc,vec3(1.),.4)*bev*(.1+.8*pow(max(dot(pg,-L.xy),0.),2.))+uMat.y*spectrum(pq.x*.01+pq.y*.013)*bev*.12;",
    "   col=mix(col,ph,smoothstep(0.,-1.2,sd));}",
    " }",
    /* éclats : étoiles de cristal (Platinum), lueurs chaudes (Signature) */
    " float sp=0.;",
    " for(int i=0;i<5;i++){float fi=float(i);vec2 c=vec2(h1(fi+1.)>.5?uCard.x-uRadius*.4:uRadius*.4,0.);",
    "  c=i<2?vec2(mix(uRadius,uCard.x-uRadius,h1(fi+3.)),i==0?1.5:uCard.y-1.5):vec2(c.x>uCard.x*.5?uCard.x-1.5:1.5,mix(uRadius,uCard.y-uRadius,h1(fi+5.)));",
    "  if(i==4)c=vec2(uCard.x-uRadius*.32,uRadius*.32);",
    "  vec2 dv=abs(p-c);float tw=pow(max(sin(fi*2.4+uLight.x*2.6+uLight.y*1.7+uTime*.35),0.),5.);",
    "  sp+=tw*(exp(-dv.x*1.1-dv.y*.085)+exp(-dv.y*1.1-dv.x*.085)+1.6*exp(-dot(dv,dv)*.09));}",
    " col+=sp*(uMat.y*vec3(.92,.96,1.)*.95+uMat.x*vec3(1.,.82,.5)*.38);",
    " return vec4(col,1.);}",
    "void main(){",
    " vec2 p=vec2(gl_FragCoord.x,uRes.y-gl_FragCoord.y)/uDpr-uPad;",
    " float H=uCard.y;",
    " if(p.y<=H+uPad*.5){o=card(p);return;}",
    /* reflet sur le sol poli : image miroir étirée, qui s'éteint */
    " float dy=p.y-H-uPad*.5;",
    " float wob=(ns(vec2(p.x*.045,dy*.012))-.5);",
    " vec2 pm=vec2(p.x+wob*dy*.09,H-dy*(1.+wob*.25));",
    " vec4 c=card(pm);",
    " float f=exp(-dy/(uRefl*.34))*(uMat.x*.5+uMat.y*.5+uMat.z*.26);",
    " f*=.72+.5*ns(vec2(p.x*.11,3.));",
    " o=vec4(c.rgb*f*step(.5,c.a),c.a*f*.75*step(.5,c.a));",
    "}"
  ].join("\n");

  var MODES = ["signature", "platinum", "base"];
  var SCENES = ["/media/modes/scene-signature.webp", "/media/modes/scene-platinum.webp", "/media/modes/base.webp"];
  var cards = $$("[data-mt]").map(function (el) {
    return { el: el, kind: { thermo: 1, flux: 2, batt: 3, auto: 4 }[el.dataset.mt], cv: $("canvas", el), vis: true };
  });
  var PAD = 28, small = matchMedia("(max-width: 720px)");
  var cap = small.matches ? 1.25 : 1.5, dpr = Math.min(window.devicePixelRatio || 1, cap);   /* finesse du rendu, abaissée si l'appareil peine */

  function compile(gl, type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s) || "shader");
    return s;
  }
  function setup(c) {
    var gl = c.cv.getContext("webgl2", { alpha: true, premultipliedAlpha: true, antialias: false, powerPreference: "high-performance" });
    if (!gl) return false;
    var pr = gl.createProgram();
    gl.attachShader(pr, compile(gl, gl.VERTEX_SHADER, VERT));
    gl.attachShader(pr, compile(gl, gl.FRAGMENT_SHADER, FRAG));
    gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr) || "link");
    gl.useProgram(pr);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(pr, "a"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    c.gl = gl; c.u = {};
    ["uRes", "uCard", "uOrigin", "uView", "uCover", "uLight", "uDpr", "uPad", "uTime", "uRefl", "uRadius", "uMat", "uKind", "uS0", "uS1", "uS2",
      "uPhoto", "uDial", "uArc", "uSeg", "uFlow", "uNode", "uTube", "uLevel", "uReserve", "uPhotoR", "uPhotoUV", "uPhotoOn"].forEach(function (n) {
      c.u[n] = gl.getUniformLocation(pr, n);
    });
    c.tex = [];
    for (var i = 0; i < 4; i++) {
      var t = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([4, 4, 4, 255]));
      c.tex.push(t);
    }
    gl.uniform1i(c.u.uS0, 0); gl.uniform1i(c.u.uS1, 1); gl.uniform1i(c.u.uS2, 2); gl.uniform1i(c.u.uPhoto, 3);
    gl.uniform1i(c.u.uKind, c.kind); gl.uniform1f(c.u.uPhotoOn, 0);
    c.cv.addEventListener("webglcontextlost", function (e) { e.preventDefault(); c.lost = true; root.classList.remove("mt-gl-on"); });
    return true;
  }
  var ok = false;
  try { ok = cards.every(setup); } catch (e) { ok = false; }
  if (!ok) return;                                  /* repli CSS : les vraies images, cadre de cristal */

  /* Textures : la scène de chaque mode (réduite : elle n'est vue qu'à travers le verre) et la photo du véhicule */
  function upload(c, unit, img, maxW) {
    var gl = c.gl, w = Math.min(maxW, img.naturalWidth), h = Math.round(w * img.naturalHeight / img.naturalWidth);
    var cv = document.createElement("canvas"); cv.width = w; cv.height = h;
    cv.getContext("2d").drawImage(img, 0, 0, w, h);
    gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, c.tex[unit]);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cv);
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  }
  var sceneAspect = 16 / 9, loaded = [false, false, false];
  function loadScene(i) {
    if (loaded[i]) return; loaded[i] = true;
    var im = new Image();
    im.onload = function () {
      sceneAspect = im.naturalWidth / im.naturalHeight;
      cards.forEach(function (c) { upload(c, i, im, 960); });
      poke();
    };
    im.src = SCENES[i];
  }
  var photoEl = $("[data-mt-photo] img"), photoAspect = 4 / 3;
  function loadPhoto() {
    var c = cards.filter(function (k) { return k.kind === 4; })[0];
    if (!c || !photoEl) return;
    var im = new Image();
    im.onload = function () {
      photoAspect = im.naturalWidth / im.naturalHeight;
      upload(c, 3, im, 1024); c.gl.uniform1f(c.u.uPhotoOn, 1);
      c.photo = true; layout(); poke();
    };
    im.src = photoEl.currentSrc || photoEl.src;
  }

  /* Géométrie : le shader suit la mise en page HTML (rectangles mesurés) */
  function rel(el, base) { var r = el.getBoundingClientRect(); return { x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height }; }
  function layout() {
    dpr = Math.min(window.devicePixelRatio || 1, cap);
    cards.forEach(function (c) {
      var gl = c.gl, b = c.el.getBoundingClientRect();
      var cs = getComputedStyle(c.el), refl = parseFloat(cs.getPropertyValue("--mt-refl")) || 0;
      PAD = parseFloat(cs.getPropertyValue("--mt-pad")) || 28;
      c.w = b.width; c.h = b.height; c.refl = refl;
      var W = Math.round((b.width + 2 * PAD) * dpr), Hh = Math.round((b.height + 1.5 * PAD + refl) * dpr);
      if (c.cv.width !== W || c.cv.height !== Hh) { c.cv.width = W; c.cv.height = Hh; }
      gl.viewport(0, 0, W, Hh);
      gl.uniform2f(c.u.uRes, W, Hh); gl.uniform2f(c.u.uCard, b.width, b.height);
      gl.uniform1f(c.u.uDpr, dpr); gl.uniform1f(c.u.uPad, PAD); gl.uniform1f(c.u.uRefl, Math.max(refl, 1));
      gl.uniform1f(c.u.uRadius, parseFloat(getComputedStyle(c.el).borderTopLeftRadius) || 22);
      if (c.kind === 1) { var d = rel(dial, b); gl.uniform3f(c.u.uDial, d.x + d.w / 2, d.y + d.h / 2, d.w / 2 * 0.86); }
      if (c.kind === 2) {
        var ns = $$("[data-mt-node]", c.el).map(function (n) { var r = rel(n, b); return [r.x + r.w / 2, r.y + r.h / 2, r.w / 2]; });
        var nodes = [], segs = [], fl = [];
        ns.forEach(function (n) { nodes.push(n[0], n[1], n[2]); });
        [1, 2, 3].forEach(function (k) {
          var a = ns[0], t = ns[k], dx = t[0] - a[0], dy = t[1] - a[1], l = Math.hypot(dx, dy) || 1;
          segs.push(a[0] + dx / l * (a[2] - 2), a[1] + dy / l * (a[2] - 2), t[0] - dx / l * (t[2] - 2), t[1] - dy / l * (t[2] - 2));
          fl.push(+$$("[data-mt-node]", c.el)[k].dataset.flow);
        });
        gl.uniform3fv(c.u.uNode, nodes); gl.uniform4fv(c.u.uSeg, segs); gl.uniform1fv(c.u.uFlow, fl);
      }
      if (c.kind === 3) {
        var tb = [], lv = [];
        $$("[data-mt-tube]", c.el).forEach(function (t) { var r = rel(t, b); tb.push(r.x, r.y, r.w, r.h); lv.push(+t.dataset.level); });
        gl.uniform4fv(c.u.uTube, tb); gl.uniform1fv(c.u.uLevel, lv); gl.uniform1f(c.u.uReserve, +c.el.dataset.reserve);
      }
      if (c.kind === 4 && c.photo) {
        var p = rel($("[data-mt-photo]", c.el), b), ra = p.w / p.h, sx = 1, sy = 1;
        if (ra > photoAspect) sy = photoAspect / ra; else sx = ra / photoAspect;
        gl.uniform4f(c.u.uPhotoR, p.x, p.y, p.w, p.h);
        gl.uniform4f(c.u.uPhotoUV, sx, sy, (1 - sx) / 2, (1 - sy) * 0.62);
      }
    });
    poke();
  }

  /* Matière : fondu d'un mode à l'autre (or liquide → cristal → verre fumé) */
  var mat = [0, 0, 0], target = 0;
  function readMode() {
    target = Math.max(0, MODES.indexOf(doc.getAttribute("data-mode") || "signature"));
    loadScene(target); poke();
  }
  readMode(); mat[target] = 1;
  new MutationObserver(readMode).observe(doc, { attributes: true, attributeFilter: ["data-mode"] });

  /* Lumière : suit le pointeur, sinon dérive lentement toute seule */
  var mouse = { x: 0, y: 0, on: 0 }, light = { x: -0.45, y: -0.6 };
  addEventListener("pointermove", function (e) {
    mouse.x = e.clientX / innerWidth * 2 - 1; mouse.y = e.clientY / innerHeight * 2 - 1; mouse.on = 1; poke();
  }, { passive: true });
  addEventListener("scroll", poke, { passive: true });
  addEventListener("resize", layout);
  if (window.ResizeObserver) { var ro = new ResizeObserver(layout); cards.forEach(function (c) { ro.observe(c.el); }); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
  if (window.IntersectionObserver) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { cards.forEach(function (c) { if (c.el === e.target) c.vis = e.isIntersecting; }); });
      poke();
    }, { rootMargin: "80px" });
    cards.forEach(function (c) { io.observe(c.el); });
  }

  var reduce = matchMedia("(prefers-reduced-motion: reduce)");
  var last = performance.now(), clock = 0, probe = { n: 0, t: 0, last: last };
  function frame(now) {
    requestAnimationFrame(frame);
    if (document.hidden) { last = now; return; }
    var dt = Math.min(0.05, (now - last) / 1000); last = now;
    var live = doc.classList.contains("fx") && !reduce.matches;
    var moving = false, i;
    for (i = 0; i < 3; i++) {
      var goal = i === target ? 1 : 0, dlt = goal - mat[i];
      if (Math.abs(dlt) > 0.002) { mat[i] += dlt * (live ? Math.min(1, dt * 4.2) : 1); moving = true; } else mat[i] = goal;
    }
    var sdl = TH.set - TH.shown;
    if (Math.abs(sdl) > 0.004) { TH.shown += sdl * (live ? Math.min(1, dt * 14) : 1); moving = true; } else TH.shown = TH.set;
    if (!live && !dirty && !moving) return;
    if (live) {
      clock += dt;
      if (probe.n < 60) { probe.n++; probe.t += now - probe.last; if (probe.n === 60 && probe.t / 60 > 24 && cap > 1) { cap = 1; probe.n = 0; probe.t = 0; layout(); } }
    }
    probe.last = now;
    var lx = -0.45 + 0.28 * Math.sin(clock * 0.23), ly = -0.6 + 0.16 * Math.cos(clock * 0.17);
    if (mouse.on) { lx = lx * 0.35 + mouse.x * 0.75; ly = ly * 0.35 + mouse.y * 0.7 - 0.25; }
    var kk = live ? Math.min(1, dt * 5) : 1;
    light.x += (lx - light.x) * kk; light.y += (ly - light.y) * kk;
    dirty = false;
    var sum = mat[0] + mat[1] + mat[2] || 1;
    var vw = innerWidth, vh = innerHeight, sc = Math.max(vw / sceneAspect, vh);   /* hauteur de l'image en « cover » */
    cards.forEach(function (c) {
      if (!c.vis || c.lost) return;
      var gl = c.gl, b = c.el.getBoundingClientRect();
      gl.uniform2f(c.u.uOrigin, b.left, b.top); gl.uniform2f(c.u.uView, vw, vh);
      gl.uniform2f(c.u.uCover, 1 / (sc * sceneAspect), 1 / sc);
      gl.uniform3f(c.u.uMat, mat[0] / sum, mat[1] / sum, mat[2] / sum);
      gl.uniform1f(c.u.uTime, clock);
      var cx = (b.left + b.width / 2) / vw * 2 - 1;
      gl.uniform2f(c.u.uLight, light.x - cx * 0.25, light.y);
      if (c.kind === 1) gl.uniform2f(c.u.uArc, c01((TH.shown - TH.min) / (TH.max - TH.min)), c01((TH.now - TH.min) / (TH.max - TH.min)));
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    });
  }
  layout(); loadPhoto();
  root.classList.add("mt-gl-on");
  [0, 1, 2].forEach(function (i) { if (i !== target) setTimeout(function () { loadScene(i); }, 900 + i * 300); });
  requestAnimationFrame(frame);
})();
