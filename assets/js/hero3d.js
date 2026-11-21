/* ==========================================================================
   WZ HERO — Three.js particle shell + shader glow
   Pointer parallax, scroll drift, visibility pause, reduced-motion and
   context-loss fallbacks. If WebGL is unavailable the canvas is removed and
   the CSS wash behind the portrait carries the hero.
   ========================================================================== */
import * as THREE from 'three';

const mount = document.getElementById('heroCanvas');
const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

function hasWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (_) {
    return false;
  }
}

if (mount && hasWebGL()) {
  try {
    init(mount);
  } catch (err) {
    mount.classList.add('webgl-off');
    console.warn('[hero3d] WebGL init failed, using CSS fallback.', err);
  }
} else if (mount) {
  mount.classList.add('webgl-off');
}

function init(host) {
  const small = window.matchMedia('(max-width: 760px)').matches;
  const renderer = new THREE.WebGLRenderer({
    alpha: true,
    antialias: window.devicePixelRatio < 2,
    powerPreference: 'high-performance',
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, small ? 1.5 : 2));
  renderer.setClearColor(0x000000, 0);
  host.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(48, 1, 0.1, 100);
  camera.position.set(0, 0, 6.4);

  /* --- shader glow ------------------------------------------------------- */
  const glowUniforms = {
    uTime: { value: 0 },
    uPointer: { value: new THREE.Vector2(0, 0) },
    uAspect: { value: 1 },
  };
  const glow = new THREE.Mesh(
    new THREE.PlaneGeometry(2, 2),
    new THREE.ShaderMaterial({
      uniforms: glowUniforms,
      transparent: true,
      depthWrite: false,
      depthTest: false,
      blending: THREE.AdditiveBlending,
      vertexShader: /* glsl */ `
        varying vec2 vUv;
        void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }
      `,
      fragmentShader: /* glsl */ `
        precision highp float;
        varying vec2 vUv;
        uniform float uTime;
        uniform vec2 uPointer;
        uniform float uAspect;

        float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }
        float noise(vec2 p){
          vec2 i = floor(p), f = fract(p);
          vec2 u = f * f * (3.0 - 2.0 * f);
          return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),
                     mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
        }

        void main(){
          vec2 p = (vUv - 0.5) * vec2(uAspect, 1.0);
          p += uPointer * 0.06;
          float t = uTime * 0.045;
          float n = noise(p * 2.4 + vec2(t, -t * 0.7));
          n += 0.5 * noise(p * 5.1 - vec2(t * 0.8, t));
          float core = smoothstep(0.58, 0.0, length(p * vec2(0.92, 0.78)));
          vec3 red = vec3(0.894, 0.0, 0.219);
          vec3 warm = vec3(1.0, 0.42, 0.35);
          vec3 col = mix(red, warm, n * 0.55);
          float alpha = core * (0.16 + n * 0.28) + (n - 0.55) * 0.05 * core;
          gl_FragColor = vec4(col, clamp(alpha, 0.0, 0.7));
        }
      `,
    })
  );
  glow.frustumCulled = false;
  scene.add(glow);

  /* --- particle shell ----------------------------------------------------- */
  const count = small ? 620 : 1250;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const sizes = new Float32Array(count);
  const cream = new THREE.Color('#FAF3E9');
  const red = new THREE.Color('#FF2E56');

  for (let i = 0; i < count; i++) {
    // spherical shell with a little radial jitter
    const u = Math.random();
    const v = Math.random();
    const theta = u * Math.PI * 2;
    const phi = Math.acos(2 * v - 1);
    const r = 2.5 + Math.pow(Math.random(), 1.8) * 2.4;
    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta) * 0.72;
    positions[i * 3 + 2] = r * Math.cos(phi) * 0.6 - 0.8;

    const c = Math.random() < 0.22 ? red : cream;
    const dim = 0.55 + Math.random() * 0.45;
    colors[i * 3] = c.r * dim;
    colors[i * 3 + 1] = c.g * dim;
    colors[i * 3 + 2] = c.b * dim;
    sizes[i] = Math.random() < 0.08 ? 0.055 : 0.016 + Math.random() * 0.02;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setAttribute('aSize', new THREE.BufferAttribute(sizes, 1));

  const points = new THREE.Points(
    geo,
    new THREE.PointsMaterial({
      vertexColors: true,
      size: 0.032,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.85,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })
  );
  points.rotation.z = 0.2;
  scene.add(points);

  /* --- state -------------------------------------------------------------- */
  const pointer = { x: 0, y: 0 };
  const eased = { x: 0, y: 0 };
  let scrollT = 0;
  let raf = 0;
  let visible = true;
  let running = false;
  let t0 = performance.now();

  function resize() {
    const r = host.getBoundingClientRect();
    const w = Math.max(1, r.width);
    const h = Math.max(1, r.height);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    glowUniforms.uAspect.value = w / h;
  }

  const ro = new ResizeObserver(resize);
  ro.observe(host);
  resize();

  function onPointer(e) {
    pointer.x = (e.clientX / window.innerWidth) * 2 - 1;
    pointer.y = (e.clientY / window.innerHeight) * 2 - 1;
  }
  window.addEventListener('pointermove', onPointer, { passive: true });

  function onScroll() {
    const r = host.getBoundingClientRect();
    scrollT = THREE.MathUtils.clamp(-r.top / Math.max(1, r.height), 0, 1);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  function render(now) {
    const t = (now - t0) / 1000;
    eased.x += (pointer.x - eased.x) * 0.045;
    eased.y += (pointer.y - eased.y) * 0.045;

    camera.position.x = eased.x * 0.55;
    camera.position.y = -eased.y * 0.4;
    camera.position.z = 6.4 + scrollT * 1.9;
    camera.lookAt(0, 0, 0);

    points.rotation.y = t * 0.045 + eased.x * 0.16;
    points.rotation.x = -eased.y * 0.12 + scrollT * 0.18;
    points.position.y = scrollT * 0.6;

    glowUniforms.uTime.value = t;
    glowUniforms.uPointer.value.set(eased.x, -eased.y);

    renderer.render(scene, camera);
  }

  function loop(now) {
    if (!running) return;
    render(now);
    raf = requestAnimationFrame(loop);
  }

  function start() {
    if (running || !visible) return;
    running = true;
    raf = requestAnimationFrame(loop);
  }
  function stop() {
    running = false;
    cancelAnimationFrame(raf);
  }

  const io = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    visible ? start() : stop();
  }, { threshold: 0.05 });
  io.observe(host);

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop();
    else if (visible && !motionQuery.matches) start();
  });

  function applyMotion() {
    if (motionQuery.matches) {
      stop();
      render(performance.now()); // one static frame
    } else {
      start();
    }
  }
  motionQuery.addEventListener?.('change', applyMotion);
  applyMotion();

  renderer.domElement.addEventListener('webglcontextlost', e => {
    e.preventDefault();
    stop();
    host.classList.add('webgl-off');
  });
  renderer.domElement.addEventListener('webglcontextrestored', () => {
    host.classList.remove('webgl-off');
    start();
  });

  window.addEventListener('pagehide', () => {
    stop();
    ro.disconnect();
    io.disconnect();
    window.removeEventListener('pointermove', onPointer);
    window.removeEventListener('scroll', onScroll);
  });
}
