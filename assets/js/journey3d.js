/* ==========================================================================
   WZ — FIELD NOTES

   A scroll-driven Three.js world: Himachal plates are stacked at real depths
   and a camera dollies through them along a spline while the chapters
   cross-fade. Based on the camera-through-layers architecture of the ThreeUI
   Kage page (sections keyed to a camera path), rebuilt here on the studio's own
   photography and palette.

   Plates are graded in the fragment shader (desaturated, shadows pushed to the
   page ink, highlights to cream) so six photographs of different light read as
   one continuous place.

   Fallbacks: no WebGL, reduced motion, or the site's motion toggle all switch
   the section to a static composition — the chapters stay fully readable.
   ========================================================================== */
import * as THREE from 'three';

const section = document.getElementById('journey');
const host = document.getElementById('journeyCanvas');

/* ----------------------------------------------------------------- palette */
const FOG = new THREE.Color('#0B0705');
const SHADOW = new THREE.Color('#0B0705');
const HIGH = new THREE.Color('#FAF3E9');
const FOV = 42;

/* Each layer is placed by depth (world units), then framed in view units:
   cx / cy are fractions of the half-view at that depth, h is a fraction of the
   full view height. Width follows the texture's own aspect, so nothing is
   stretched. `drift` is how far the plate slides across the frame over the
   whole journey — near plates travel further, which is what sells the depth.
   `mobile` overrides apply under 760px where the frame is tall. */
const LAYERS = [
  {
    id: 'ridge', src: 'assets/img/hp/ridge.webp', z: -158,
    cx: 0, cy: -0.02, h: 1.6, opacity: 0.55, fog: 0.62, feather: 0.34,
    sat: 0.30, exposure: 0.9, tint: '#2A3A50', tintAmount: 0.45, drift: 0.03,
    mobile: { h: 2.3 },
  },
  {
    id: 'temple', src: 'assets/img/hp/temple.webp', z: -110,
    cx: 0.0, cy: -0.28, h: 0.56, opacity: 1.0, fog: 0.08, feather: 0.26,
    sat: 0.78, exposure: 1.75, shadow: 0.18, tint: '#E2CDB0', tintAmount: 0.05, drift: 0.09,
    mobile: { h: 0.86, cy: -0.34 },
  },
  {
    id: 'forest', src: 'assets/img/hp/forest.webp', z: -78,
    cx: 0.88, cy: 0.02, h: 1.30, opacity: 0.9, fog: 0.04, feather: 0.32,
    sat: 0.38, exposure: 0.86, tint: '#1B2A20', tintAmount: 0.16, drift: 0.22,
    mobile: { h: 1.7, cx: 0.72 },
  },
  {
    id: 'fir', src: 'assets/img/hp/fir.webp', z: -60, pass: true,
    cx: -0.98, cy: -0.06, h: 1.15, opacity: 0.82, fog: 0.0, feather: 0.36,
    sat: 0.34, exposure: 0.78, tint: '#16211A', tintAmount: 0.2, drift: 0.5,
    mobile: { h: 1.5, cx: -0.94 },
  },
  {
    id: 'canopy', src: 'assets/img/hp/canopy.webp', z: -46, pass: true,
    cx: 0.64, cy: 0.28, h: 1.40, opacity: 0.6, fog: 0.0, feather: 0.4,
    sat: 0.30, exposure: 0.7, tint: '#152018', tintAmount: 0.22, drift: 0.72,
    mobile: { h: 1.6, cx: 0.66 },
  },
  {
    id: 'portrait', src: 'assets/img/portrait-cutout.webp', z: -74,
    cx: 0.40, cy: -0.12, h: 0.58, opacity: 1.0, fog: 0.0, feather: 0.02,
    sat: 0.88, exposure: 1.0, tint: '#FFFFFF', tintAmount: 0.0, drift: 0.24,
    portrait: true, mobile: { h: 0.26, cx: 0.10, cy: 0.16 },
  },
];

/* Chapters: centre of each in section progress, and the half-width of its fade. */
const CHAPTERS = [
  { c: 0.10, w: 0.13 },
  { c: 0.36, w: 0.13 },
  { c: 0.62, w: 0.13 },
  { c: 0.87, w: 0.15 },
];

/* Camera path — a shallow S so the dolly never reads as a straight zoom. */
const CAM = [
  new THREE.Vector3(0.0, 0.70, 16.0),
  new THREE.Vector3(0.95, 0.24, 9.0),
  new THREE.Vector3(-1.20, 0.00, 0.5),
  new THREE.Vector3(0.60, -0.22, -12.0),
  new THREE.Vector3(0.0, -0.08, -30.0),
];
const LOOK = [
  new THREE.Vector3(0.0, -0.30, -60),
  new THREE.Vector3(0.30, -0.26, -66),
  new THREE.Vector3(-0.55, -0.22, -62),
  new THREE.Vector3(0.35, -0.12, -58),
  new THREE.Vector3(0.10, -0.06, -54),
];

const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)');
const smallScreen = window.matchMedia('(max-width: 760px)');

const CAM_CURVE = new THREE.CatmullRomCurve3(CAM, false, 'catmullrom', 0.4);
const LOOK_CURVE = new THREE.CatmullRomCurve3(LOOK, false, 'catmullrom', 0.4);

const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const smoothstep = (e0, e1, x) => {
  const t = clamp((x - e0) / (e1 - e0), 0, 1);
  return t * t * (3 - 2 * t);
};

/* ------------------------------------------------------------------ shaders */
const VERT = /* glsl */ `
  varying vec2 vUv;
  void main(){
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const FRAG = /* glsl */ `
  precision highp float;
  varying vec2 vUv;
  uniform sampler2D uMap;
  uniform vec2 uRes;
  uniform float uOpacity;
  uniform float uFog;
  uniform float uFeather;
  uniform float uGrain;
  uniform float uTime;
  uniform float uSat;
  uniform float uExposure;
  uniform float uContrast;
  uniform float uShadowAmt;
  uniform vec3 uFogColor;
  uniform vec3 uTint;
  uniform float uTintAmount;
  uniform vec3 uShadow;
  uniform vec3 uHigh;

  float rand(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }

  void main(){
    vec4 tex = texture2D(uMap, vUv);

    // --- grade: one palette across six photographs -------------------------
    vec3 col = tex.rgb * uExposure;
    float l = dot(col, vec3(0.2126, 0.7152, 0.0722));
    col = mix(vec3(l), col, uSat);
    col = pow(clamp(col, 0.0, 1.0), vec3(uContrast));
    col = mix(col, uShadow, smoothstep(0.30, 0.0, l) * uShadowAmt);
    col = mix(col, uHigh, smoothstep(0.58, 1.0, l) * 0.18);
    col = mix(col, uTint, uTintAmount);

    // soft edges — plates dissolve into the fog instead of ending in a rectangle
    float fx = smoothstep(0.0, uFeather, vUv.x) * smoothstep(0.0, uFeather, 1.0 - vUv.x);
    float fy = smoothstep(0.0, uFeather * 1.5, vUv.y) * smoothstep(0.0, uFeather * 1.5, 1.0 - vUv.y);
    float a = tex.a * fx * fy;

    // aerial perspective — far plates sit back into the ink
    col = mix(col, uFogColor, uFog);
    a *= uOpacity;

    // a little filmic tooth so the photography sits with the page grain
    col += (rand(vUv * uRes + uTime * 0.7) - 0.5) * uGrain;

    if (a < 0.002) discard;
    gl_FragColor = vec4(col, a);
  }
`;

const SUN_FRAG = /*glsl*/ `
  precision highp float;
  varying vec2 vUv;
  uniform float uTime;
  uniform float uAspect;

  float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float noise(vec2 p){
    vec2 i = floor(p), f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),
               mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
  }

  void main(){
    vec2 p = (vUv - 0.5) * vec2(uAspect, 1.0);
    float d = length(p);
    // a low sun seen through haze: a small core inside a wide, soft bloom
    float core = smoothstep(0.052, 0.018, d);
    float bloom = smoothstep(0.62, 0.0, d);
    bloom *= bloom;
    float n = noise(vUv * 7.0 + uTime * 0.012) * 0.65 + noise(vUv * 17.0 - uTime * 0.018) * 0.35;
    vec3 hot = vec3(0.95, 0.42, 0.24);
    vec3 warm = vec3(0.62, 0.10, 0.12);
    vec3 col = mix(warm, hot, core * 0.85 + n * 0.25);
    float a = core * 0.42 + bloom * 0.30 * (0.7 + n * 0.5);
    gl_FragColor = vec4(col, clamp(a, 0.0, 0.62));
  }
`;

function hasWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (_) {
    return false;
  }
}

/* Shared chapter/rail state — also used when the canvas is unavailable. */
const chapterEls = section ? Array.from(section.querySelectorAll('[data-chapter]')) : [];
const chapterKeys = chapterEls.map(el => Number(el.dataset.chapter));
const tickEls = section ? Array.from(section.querySelectorAll('[data-tick]')) : [];
const distanceEl = section ? section.querySelector('[data-distance]') : null;
const hudEl = section ? section.querySelector('[data-hud]') : null;

function paintChapters(p) {
  if (!chapterEls.length) return;
  let active = 0;
  let best = 9;
  for (let i = 0; i < CHAPTERS.length; i++) {
    const cfg = CHAPTERS[i];
    const d = Math.abs(p - cfg.c);
    if (d < best) { best = d; active = i; }
    const el = chapterEls[chapterKeys.indexOf(i)];
    if (!el) continue;
    const o = 1 - smoothstep(0, cfg.w, d);
    const shift = clamp((p - cfg.c) / (cfg.w || 1), -1, 1);
    el.style.opacity = o.toFixed(3);
    el.style.transform = `translate3d(0, ${(shift * -28).toFixed(2)}px, 0)`;
    el.style.visibility = o < 0.01 ? 'hidden' : 'visible';
  }
  tickEls.forEach((t, i) => t.classList.toggle('is-on', i === active));
  if (distanceEl) distanceEl.textContent = String(Math.round(p * 480)).padStart(3, '0');
}

function paintStaticChapters() {
  chapterEls.forEach(el => {
    el.style.opacity = '1';
    el.style.transform = 'none';
    el.style.visibility = 'visible';
  });
  tickEls.forEach((t, i) => t.classList.toggle('is-on', i === 0));
}

function setStatic(on) {
  if (!section) return;
  section.classList.toggle('is-static', on);
  if (on) paintStaticChapters();
}

if (section) {
  const off = prefersReduced.matches || document.documentElement.dataset.motion === 'off';
  if (off) setStatic(true);

  if (!host || !hasWebGL()) {
    setStatic(true);
    if (host) host.classList.add('webgl-off');
  } else {
    try {
      init(host);
    } catch (err) {
      console.warn('[journey] WebGL init failed, using the static composition.', err);
      setStatic(true);
      host.classList.add('webgl-off');
    }
  }
}

/* --------------------------------------------------------------------- init */
function init(host) {
  const renderer = new THREE.WebGLRenderer({
    alpha: true,
    antialias: false,
    powerPreference: 'high-performance',
  });
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, smallScreen.matches ? 1.5 : 1.75));
  host.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(FOG, 0.0042);

  const camera = new THREE.PerspectiveCamera(FOV, 1, 1, 400);

  /* --- sun behind the ridge ---------------------------------------------- */
  const sunGroup = new THREE.Group();
  const sunUniforms = { uTime: { value: 0 }, uAspect: { value: 1 } };
  const sun = new THREE.Mesh(
    new THREE.PlaneGeometry(1, 1),
    new THREE.ShaderMaterial({
      uniforms: sunUniforms,
      vertexShader: VERT,
      fragmentShader: SUN_FRAG,
      transparent: true,
      depthWrite: false,
      depthTest: false,
      blending: THREE.AdditiveBlending,
    })
  );
  sun.frustumCulled = false;
  sun.renderOrder = -10;
  sunGroup.add(sun);
  scene.add(sunGroup);

  /* --- plates ------------------------------------------------------------- */
  const loader = new THREE.TextureLoader();
  const loaded = [];
  const group = new THREE.Group();
  scene.add(group);

  LAYERS.forEach((cfg, i) => {
    const uniforms = {
      uMap: { value: null },
      uRes: { value: new THREE.Vector2(1, 1) },
      uOpacity: { value: 0 },
      uFog: { value: cfg.fog || 0 },
      uFeather: { value: cfg.feather ?? 0.2 },
      uGrain: { value: 0.05 },
      uTime: { value: 0 },
      uSat: { value: cfg.sat ?? 0.6 },
      uExposure: { value: cfg.exposure ?? 1 },
      uContrast: { value: 1.04 },
      uShadowAmt: { value: cfg.shadow ?? 0.46 },
      uFogColor: { value: FOG.clone() },
      uTint: { value: new THREE.Color(cfg.tint || '#ffffff') },
      uTintAmount: { value: cfg.tintAmount || 0 },
      uShadow: { value: SHADOW.clone() },
      uHigh: { value: HIGH.clone() },
    };

    const mesh = new THREE.Mesh(
      new THREE.PlaneGeometry(1, 1),
      new THREE.ShaderMaterial({
        uniforms,
        vertexShader: VERT,
        fragmentShader: FRAG,
        transparent: true,
        depthWrite: false,
        depthTest: false,
      })
    );
    mesh.renderOrder = i;
    mesh.frustumCulled = false;
    mesh.userData = { cfg, uniforms, aspect: 1, baseOpacity: cfg.opacity ?? 1, baseX: 0, baseY: 0 };
    group.add(mesh);

    loader.load(
      cfg.src,
      tex => {
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.minFilter = THREE.LinearFilter;
        tex.magFilter = THREE.LinearFilter;
        tex.generateMipmaps = false;
        uniforms.uMap.value = tex;
        uniforms.uRes.value.set(tex.image.width, tex.image.height);
        mesh.userData.aspect = tex.image.width / tex.image.height;
        mesh.visible = true;
        layoutMesh(mesh);
        loaded.push(mesh);
      },
      undefined,
      () => {
        console.warn('[journey] missing plate:', cfg.src);
        mesh.visible = false;
      }
    );
    mesh.visible = false;
  });

  /* --- dust --------------------------------------------------------------- */
  const dustCount = smallScreen.matches ? 260 : 520;
  const dustGeo = new THREE.BufferGeometry();
  const dustPos = new Float32Array(dustCount * 3);
  for (let i = 0; i < dustCount; i++) {
    dustPos[i * 3] = (Math.random() - 0.5) * 70;
    dustPos[i * 3 + 1] = (Math.random() - 0.5) * 34;
    dustPos[i * 3 + 2] = -10 - Math.random() * 90;
  }
  dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
  const dust = new THREE.Points(
    dustGeo,
    new THREE.PointsMaterial({
      color: 0xfaf3e9,
      size: 0.10,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.4,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })
  );
  dust.frustumCulled = false;
  scene.add(dust);

  /* --- framing ------------------------------------------------------------ */
  const view = { h: 1, w: 1, aspect: 1 };

  function layerFrame(cfg) {
    const mobile = smallScreen.matches;
    return {
      h: mobile && cfg.mobile?.h ? cfg.mobile.h : cfg.h,
      cx: mobile && cfg.mobile?.cx !== undefined ? cfg.mobile.cx : cfg.cx,
      cy: mobile && cfg.mobile?.cy !== undefined ? cfg.mobile.cy : cfg.cy,
    };
  }

  function layoutMesh(mesh) {
    const { cfg } = mesh.userData;
    const { h, cx, cy } = layerFrame(cfg);

    const z = cfg.z;
    const dh = 2 * Math.abs(z) * Math.tan((FOV * Math.PI) / 360);
    const dw = dh * view.aspect;

    const height = dh * h;
    const width = height * (mesh.userData.aspect || 1);
    mesh.scale.set(width, height, 1);
    mesh.userData.baseX = (cx || 0) * dw * 0.5;
    mesh.userData.baseY = (cy || 0) * dh * 0.5;
    mesh.userData.viewW = dw;
    mesh.userData.viewH = dh;
    mesh.position.set(mesh.userData.baseX, mesh.userData.baseY, z);
  }

  function resize() {
    const r = host.getBoundingClientRect();
    const w = Math.max(1, r.width);
    const h = Math.max(1, r.height);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    view.aspect = camera.aspect;
    view.h = 2 * Math.tan((FOV * Math.PI) / 360);
    view.w = view.h * camera.aspect;

    loaded.forEach(layoutMesh);

    // the sun is framed in the far field, high over the temple
    const sunDist = 190;
    const sunH = 2 * sunDist * Math.tan((FOV * Math.PI) / 360);
    const size = sunH * 0.92;
    sun.scale.set(size, size, 1);
    sunGroup.position.set(-0.10 * sunH * camera.aspect * 0.5, 0.34 * sunH * 0.5, -sunDist);
    sunUniforms.uAspect.value = camera.aspect;

    if (!running) render(performance.now());
  }

  const ro = new ResizeObserver(resize);
  ro.observe(host);

  /* --- state -------------------------------------------------------------- */
  let progress = 0;      // raw scroll progress through the section
  let eased = 0;         // damped, what the camera actually uses
  let pointerX = 0;
  let pointerY = 0;
  let px = 0;
  let py = 0;
  let running = false;
  let visible = false;
  let raf = 0;
  let t0 = performance.now();
  let staticMode = false;

  const tmpPos = new THREE.Vector3();
  const tmpLook = new THREE.Vector3();

  function readScroll() {
    const r = section.getBoundingClientRect();
    const span = Math.max(1, r.height - window.innerHeight);
    progress = clamp(-r.top / span, 0, 1);
  }

  function applyCamera(p) {
    CAM_CURVE.getPointAt(clamp(p, 0.0001, 0.9999), tmpPos);
    LOOK_CURVE.getPointAt(clamp(p, 0.0001, 0.9999), tmpLook);
    camera.position.copy(tmpPos);
    camera.position.x += px * 0.55;
    camera.position.y += py * 0.34;
    camera.lookAt(tmpLook);
  }

  function render(now) {
    const t = (now - t0) / 1000;
    if (!staticMode) eased += (progress - eased) * 0.085;
    applyCamera(eased);

    /* Plates slide at their own speed and breathe with the dolly, so the depth
       reads continuously instead of freezing into one framed photograph. */
    loaded.forEach(mesh => {
      const { cfg, uniforms, baseOpacity, baseX, baseY, viewW } = mesh.userData;
      const u = uniforms;
      u.uTime.value = t;

      const drift = cfg.drift || 0;
      mesh.position.x = baseX + drift * (eased - 0.5) * viewW * 0.5 + px * 0.012 * Math.abs(cfg.z);
      mesh.position.y = baseY + Math.sin(eased * Math.PI * 0.9 + cfg.z * 0.01) * 0.0018 * Math.abs(cfg.z);

      if (cfg.portrait) {
        u.uOpacity.value = smoothstep(0.62, 0.82, eased);
        mesh.rotation.y = px * 0.07;
      } else {
        // foreground plates dissolve as the camera passes them
        const pass = cfg.pass ? 1 - smoothstep(0.50, 0.84, eased) : 1;
        u.uOpacity.value = baseOpacity * clamp(0.30 + eased * 1.35, 0, 1) * pass;
      }
    });

    dust.rotation.y = eased * 0.16 + t * 0.008;
    dust.position.z = eased * 4.5;
    sunUniforms.uTime.value = t;

    renderer.render(scene, camera);
  }

  function loop(now) {
    if (!running) return;
    px += (pointerX - px) * 0.045;
    py += (pointerY - py) * 0.045;
    render(now);
    raf = requestAnimationFrame(loop);
  }

  function start() {
    if (running || staticMode || !visible) return;
    running = true;
    raf = requestAnimationFrame(loop);
  }
  function stop() {
    running = false;
    cancelAnimationFrame(raf);
  }

  function onPointer(e) {
    pointerX = (e.clientX / window.innerWidth) * 2 - 1;
    pointerY = (e.clientY / window.innerHeight) * 2 - 1;
  }
  window.addEventListener('pointermove', onPointer, { passive: true });

  window.addEventListener('scroll', readScroll, { passive: true });
  window.addEventListener('resize', readScroll);

  const io = new IntersectionObserver(
    ([entry]) => {
      visible = entry.isIntersecting;
      if (visible && !staticMode) start();
      else stop();
      if (visible) { readScroll(); paintChapters(staticMode ? 1 : progress); }
    },
    { threshold: 0.02 }
  );
  io.observe(section);

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop();
    else if (visible) start();
  });

  /* text + rail react even when the world is static */
  let ticking = false;
  window.addEventListener(
    'scroll',
    () => {
      if (staticMode || ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        readScroll();
        paintChapters(progress);
        ticking = false;
      });
    },
    { passive: true }
  );

  function applyMode() {
    const off = prefersReduced.matches || document.documentElement.dataset.motion === 'off';
    staticMode = off;
    setStatic(off);
    if (off) {
      stop();
      readScroll();
      eased = 0.58;
      resize();
      render(performance.now());
    } else {
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, smallScreen.matches ? 1.5 : 1.75));
      resize();
      readScroll();
      start();
    }
    if (hudEl) hudEl.textContent = off ? 'Static composition' : 'Scroll to travel';
  }

  prefersReduced.addEventListener?.('change', applyMode);
  smallScreen.addEventListener?.('change', () => {
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, smallScreen.matches ? 1.5 : 1.75));
    resize();
  });

  // the site's motion toggle flips data-motion on <html>
  new MutationObserver(applyMode).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-motion'],
  });

  renderer.domElement.addEventListener('webglcontextlost', e => {
    e.preventDefault();
    stop();
    host.classList.add('webgl-off');
    setStatic(true);
  });
  renderer.domElement.addEventListener('webglcontextrestored', () => {
    host.classList.remove('webgl-off');
    applyMode();
  });

  window.addEventListener('pagehide', () => {
    stop();
    ro.disconnect();
    io.disconnect();
    window.removeEventListener('pointermove', onPointer);
    window.removeEventListener('scroll', readScroll);
    window.removeEventListener('resize', readScroll);
  });

  resize();
  readScroll();
  paintChapters(progress);
  applyMode();

  // exposed for verification in the browser console
  window.__journey = {
    get progress() { return progress; },
    get eased() { return eased; },
    get static() { return staticMode; },
    get plates() { return loaded.length; },
  };
}
