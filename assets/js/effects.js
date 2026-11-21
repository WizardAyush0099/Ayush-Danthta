/* ==========================================================================
   WZ EFFECTS — a reusable collection of 112 interface effects
   Vanilla DOM + GSAP (optional). Every entry exposes apply({el, gsap, ...}).
   The portfolio uses a curated subset; effects.html demonstrates the rest.
   ========================================================================== */

export const reduced = () =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
export const lerp = (a, b, t) => a + (b - a) * t;

export function splitChars(el, tag = 'span') {
  const text = el.textContent || '';
  el.textContent = '';
  const chars = [];
  for (const ch of text) {
    const s = document.createElement(tag);
    s.textContent = ch === ' ' ? '\u00A0' : ch;
    s.style.display = 'inline-block';
    s.style.willChange = 'transform, opacity';
    el.appendChild(s);
    chars.push(s);
  }
  return chars;
}

export function splitWords(el) {
  const words = (el.textContent || '').trim().split(/\s+/);
  el.textContent = '';
  return words.map(w => {
    const outer = document.createElement('span');
    outer.style.display = 'inline-block';
    outer.style.overflow = 'hidden';
    outer.style.verticalAlign = 'top';
    const inner = document.createElement('span');
    inner.style.display = 'inline-block';
    inner.textContent = w;
    outer.appendChild(inner);
    el.appendChild(outer);
    el.appendChild(document.createTextNode(' '));
    return inner;
  });
}

const GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/\\<>=+*#@';

export function scramble(el, finalText, { duration = 700, fps = 22 } = {}) {
  const original = finalText ?? el.textContent;
  if (reduced()) { el.textContent = original; return Promise.resolve(); }
  return new Promise(resolve => {
    const start = performance.now();
    const id = setInterval(() => {
      const t = (performance.now() - start) / duration;
      let out = '';
      for (let i = 0; i < original.length; i++) {
        const ch = original[i];
        out += ch === ' ' || t * original.length > i
          ? ch
          : GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
      }
      el.textContent = out;
      if (t >= 1) {
        clearInterval(id);
        el.textContent = original;
        resolve();
      }
    }, 1000 / fps);
  });
}

export function magnetize(el, strength = 0.25, max = 18) {
  if (reduced()) return () => {};
  const move = e => {
    const r = el.getBoundingClientRect();
    const dx = clamp((e.clientX - (r.left + r.width / 2)) * strength, -max, max);
    const dy = clamp((e.clientY - (r.top + r.height / 2)) * strength, -max, max);
    el.style.transform = `translate3d(${dx}px, ${dy}px, 0)`;
  };
  const leave = () => { el.style.transform = ''; };
  el.addEventListener('pointermove', move);
  el.addEventListener('pointerleave', leave);
  return () => {
    el.removeEventListener('pointermove', move);
    el.removeEventListener('pointerleave', leave);
  };
}

export function tilt(el, max = 10) {
  if (reduced() || !matchMedia('(hover:hover) and (pointer:fine)').matches) return () => {};
  const move = e => {
    const r = el.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    const y = (e.clientY - r.top) / r.height;
    el.style.transform = `perspective(900px) rotateX(${((0.5 - y) * max).toFixed(2)}deg) rotateY(${((x - 0.5) * max).toFixed(2)}deg)`;
    el.style.setProperty('--mx', `${(x * 100).toFixed(1)}%`);
    el.style.setProperty('--my', `${(y * 100).toFixed(1)}%`);
  };
  const leave = () => { el.style.transform = ''; };
  el.addEventListener('pointermove', move);
  el.addEventListener('pointerleave', leave);
  return () => {
    el.removeEventListener('pointermove', move);
    el.removeEventListener('pointerleave', leave);
  };
}

const rnd = (a, b) => a + Math.random() * (b - a);
const EASE = 'power3.out';

/* ==========================================================================
   REVEAL — 12
   ========================================================================== */
const reveal = [
  { id: 'fade-up', name: 'Fade up', cat: 'Reveal', apply: ({ el, gsap, st }) =>
    gsap.from(el, { y: 44, autoAlpha: 0, duration: 1, ease: EASE, scrollTrigger: st({ trigger: el, start: 'top 88%' }) }) },
  { id: 'fade-in', name: 'Soft fade', cat: 'Reveal', apply: ({ el, gsap, st }) =>
    gsap.from(el, { autoAlpha: 0, duration: 1.2, ease: 'power2.out', scrollTrigger: st({ trigger: el, start: 'top 90%' }) }) },
  { id: 'blur-in', name: 'Blur in', cat: 'Reveal', apply: ({ el, gsap, st }) =>
    gsap.from(el, { filter: 'blur(14px)', autoAlpha: 0, duration: 1.1, ease: 'power2.out', scrollTrigger: st({ trigger: el, start: 'top 88%' }) }) },
  { id: 'scale-in', name: 'Scale in', cat: 'Reveal', apply: ({ el, gsap, st }) =>
    gsap.from(el, { scale: 0.9, autoAlpha: 0, duration: 1, ease: 'expo.out', scrollTrigger: st({ trigger: el, start: 'top 88%' }) }) },
  { id: 'rotate-in', name: 'Rotate in', cat: 'Reveal', apply: ({ el, gsap, st }) =>
    gsap.from(el, { rotate: -4, y: 30, autoAlpha: 0, duration: 1, ease: EASE, scrollTrigger: st({ trigger: el, start: 'top 88%' }) }) },
  { id: 'clip-up', name: 'Clip up', cat: 'Reveal', apply: ({ el, gsap, st }) =>
    gsap.fromTo(el, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: 1.1, ease: 'expo.out', scrollTrigger: st({ trigger: el, start: 'top 86%' }) }) },
  { id: 'clip-left', name: 'Clip from left', cat: 'Reveal', apply: ({ el, gsap, st }) =>
    gsap.fromTo(el, { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0 0 0)', duration: 1.1, ease: 'expo.out', scrollTrigger: st({ trigger: el, start: 'top 86%' }) }) },
  { id: 'mask-wipe', name: 'Mask wipe', cat: 'Reveal', apply: ({ el, gsap, st }) => {
    el.style.clipPath = 'polygon(0 0, 0 0, 0 100%, 0 100%)';
    gsap.to(el, { clipPath: 'polygon(0 0, 100% 0, 100% 100%, 0 100%)', duration: 1.2, ease: 'expo.inOut', scrollTrigger: st({ trigger: el, start: 'top 86%' }) });
  } },
  { id: 'line-mask', name: 'Line mask', cat: 'Reveal', apply: ({ el, gsap, st }) => {
    const lines = splitWords(el);
    gsap.set(lines, { yPercent: 110 });
    gsap.to(lines, { yPercent: 0, duration: 1, stagger: 0.045, ease: 'expo.out', scrollTrigger: st({ trigger: el, start: 'top 88%' }) });
  } },
  { id: 'stagger-chars', name: 'Stagger chars', cat: 'Reveal', apply: ({ el, gsap, st }) => {
    const chars = splitChars(el);
    gsap.from(chars, { yPercent: 120, autoAlpha: 0, duration: 0.6, stagger: 0.022, ease: 'back.out(1.6)', scrollTrigger: st({ trigger: el, start: 'top 88%' }) });
  } },
  { id: 'stagger-words', name: 'Stagger words', cat: 'Reveal', apply: ({ el, gsap, st }) => {
    const words = splitWords(el);
    gsap.from(words, { yPercent: 120, autoAlpha: 0, duration: 0.8, stagger: 0.06, ease: EASE, scrollTrigger: st({ trigger: el, start: 'top 88%' }) });
  } },
  { id: 'curtain-reveal', name: 'Curtain split', cat: 'Reveal', apply: ({ el, gsap, st }) => {
    const inner = document.createElement('div');
    inner.innerHTML = el.innerHTML;
    el.innerHTML = '';
    el.style.position = 'relative';
    inner.style.position = 'relative';
    inner.style.zIndex = '1';
    const cover = document.createElement('i');
    cover.style.cssText = 'position:absolute;inset:0;background:var(--red,#E40038);transform-origin:top;z-index:2;display:block';
    el.append(inner, cover);
    gsap.set(inner, { yPercent: 12 });
    gsap.to(cover, { scaleY: 0, duration: 1, ease: 'expo.inOut', scrollTrigger: st({ trigger: el, start: 'top 86%' }) });
    gsap.to(inner, { yPercent: 0, duration: 1.1, ease: 'expo.out', scrollTrigger: st({ trigger: el, start: 'top 86%' }) });
  } },
];

/* ==========================================================================
   HOVER — 16
   ========================================================================== */
const hover = [
  { id: 'hover-lift', name: 'Lift', cat: 'Hover', apply: ({ el }) => {
    el.style.transition = 'transform .5s cubic-bezier(.2,.8,.2,1), box-shadow .5s';
    el.addEventListener('pointerenter', () => { el.style.transform = 'translateY(-8px)'; el.style.boxShadow = '0 24px 50px rgba(0,0,0,.28)'; });
    el.addEventListener('pointerleave', () => { el.style.transform = ''; el.style.boxShadow = ''; });
  } },
  { id: 'hover-image-zoom', name: 'Image zoom', cat: 'Hover', apply: ({ el }) => {
    el.style.overflow = 'hidden';
    const img = el.querySelector('img') || el;
    img.style.transition = 'transform .9s cubic-bezier(.2,.8,.2,1)';
    el.addEventListener('pointerenter', () => { img.style.transform = 'scale(1.08)'; });
    el.addEventListener('pointerleave', () => { img.style.transform = ''; });
  } },
  { id: 'hover-tilt', name: '3D tilt', cat: 'Hover', apply: ({ el }) => tilt(el, 9) },
  { id: 'hover-magnetic', name: 'Magnetic pull', cat: 'Hover', apply: ({ el }) => magnetize(el, 0.22, 16) },
  { id: 'hover-spotlight', name: 'Spotlight', cat: 'Hover', apply: ({ el }) => {
    el.style.position = 'relative';
    el.style.background = 'radial-gradient(220px 220px at var(--mx,50%) var(--my,50%), rgba(255,45,85,.35), transparent 70%)';
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      el.style.setProperty('--mx', `${e.clientX - r.left}px`);
      el.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  } },
  { id: 'hover-shine', name: 'Shine sweep', cat: 'Hover', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.overflow = 'hidden';
    const shine = document.createElement('i');
    shine.style.cssText = 'position:absolute;inset:0;pointer-events:none;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.4) 50%,transparent 65%);transform:translateX(-130%);transition:transform .9s cubic-bezier(.2,.8,.2,1)';
    el.appendChild(shine);
    el.addEventListener('pointerenter', () => { shine.style.transform = 'translateX(130%)'; });
    el.addEventListener('pointerleave', () => { shine.style.transform = 'translateX(-130%)'; });
  } },
  { id: 'hover-underline', name: 'Underline draw', cat: 'Hover', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.textDecoration = 'none';
    const line = document.createElement('i');
    line.style.cssText = 'position:absolute;left:0;right:0;bottom:-3px;height:1px;background:currentColor;transform:scaleX(0);transform-origin:right;transition:transform .45s cubic-bezier(.2,.8,.2,1)';
    el.appendChild(line);
    el.addEventListener('pointerenter', () => { line.style.transform = 'scaleX(1)'; line.style.transformOrigin = 'left'; });
    el.addEventListener('pointerleave', () => { line.style.transform = 'scaleX(0)'; line.style.transformOrigin = 'right'; });
  } },
  { id: 'hover-border-run', name: 'Border run', cat: 'Hover', apply: ({ el }) => {
    el.style.border = '1px solid rgba(250,243,233,.2)';
    el.style.transition = 'border-color .4s, box-shadow .4s';
    el.addEventListener('pointerenter', () => { el.style.borderColor = '#FF2E56'; el.style.boxShadow = '0 0 0 1px #FF2E56 inset'; });
    el.addEventListener('pointerleave', () => { el.style.borderColor = 'rgba(250,243,233,.2)'; el.style.boxShadow = ''; });
  } },
  { id: 'hover-invert', name: 'Invert', cat: 'Hover', apply: ({ el }) => {
    el.style.transition = 'background .35s, color .35s';
    el.addEventListener('pointerenter', () => { el.style.background = 'var(--cream,#FAF3E9)'; el.style.color = '#0B0705'; });
    el.addEventListener('pointerleave', () => { el.style.background = ''; el.style.color = ''; });
  } },
  { id: 'hover-color', name: 'Grayscale to colour', cat: 'Hover', apply: ({ el }) => {
    const t = el.querySelector('img') || el;
    t.style.filter = 'grayscale(1)';
    t.style.transition = 'filter .6s';
    el.addEventListener('pointerenter', () => { t.style.filter = 'grayscale(0)'; });
    el.addEventListener('pointerleave', () => { t.style.filter = 'grayscale(1)'; });
  } },
  { id: 'hover-arrow', name: 'Arrow slide', cat: 'Hover', apply: ({ el }) => {
    const a = document.createElement('span');
    a.textContent = '↗';
    a.style.cssText = 'display:inline-block;margin-left:8px;transition:transform .4s cubic-bezier(.2,.8,.2,1)';
    el.appendChild(a);
    el.addEventListener('pointerenter', () => { a.style.transform = 'translate(6px,-6px)'; });
    el.addEventListener('pointerleave', () => { a.style.transform = ''; });
  } },
  { id: 'hover-scramble', name: 'Letter scramble', cat: 'Hover', apply: ({ el }) => {
    const text = el.textContent;
    let busy = false;
    el.addEventListener('pointerenter', () => {
      if (busy) return;
      busy = true;
      scramble(el, text, { duration: 500 }).then(() => { busy = false; });
    });
  } },
  { id: 'hover-glitch', name: 'Glitch', cat: 'Hover', apply: ({ el, gsap }) => {
    el.addEventListener('pointerenter', () => {
      gsap.fromTo(el, { x: -4, skewX: 6 }, { x: 0, skewX: 0, duration: 0.35, ease: 'steps(4)' });
    });
  } },
  { id: 'hover-skew', name: 'Skew press', cat: 'Hover', apply: ({ el }) => {
    el.style.transition = 'transform .3s cubic-bezier(.2,.8,.2,1)';
    el.addEventListener('pointerenter', () => { el.style.transform = 'skewX(-4deg) translateX(4px)'; });
    el.addEventListener('pointerleave', () => { el.style.transform = ''; });
  } },
  { id: 'hover-label', name: 'Floating label', cat: 'Hover', apply: ({ el }) => {
    el.style.position = 'relative';
    const tag = document.createElement('span');
    tag.textContent = 'View';
    tag.style.cssText = 'position:absolute;top:-14px;right:-10px;background:var(--red,#E40038);color:#FAF3E9;font-size:8px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;padding:5px 8px;opacity:0;transform:translateY(6px);transition:.3s;pointer-events:none';
    el.appendChild(tag);
    el.addEventListener('pointerenter', () => { tag.style.opacity = '1'; tag.style.transform = 'none'; });
    el.addEventListener('pointerleave', () => { tag.style.opacity = '0'; tag.style.transform = 'translateY(6px)'; });
  } },
  { id: 'hover-blur-zoom', name: 'Zoom blur', cat: 'Hover', apply: ({ el }) => {
    el.style.transition = 'filter .4s, transform .4s';
    el.addEventListener('pointerenter', () => { el.style.filter = 'blur(1px)'; el.style.transform = 'scale(1.02)'; });
    el.addEventListener('pointerleave', () => { el.style.filter = ''; el.style.transform = ''; });
  } },
];

/* ==========================================================================
   SCROLL — 14
   ========================================================================== */
const scroll = [
  { id: 'parallax-y', name: 'Parallax Y', cat: 'Scroll', apply: ({ el, gsap, st }) =>
    gsap.to(el, { yPercent: -18, ease: 'none', scrollTrigger: st({ trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }) }) },
  { id: 'parallax-x', name: 'Parallax X', cat: 'Scroll', apply: ({ el, gsap, st }) =>
    gsap.to(el, { xPercent: 12, ease: 'none', scrollTrigger: st({ trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }) }) },
  { id: 'depth-layers', name: 'Depth layers', cat: 'Scroll', apply: ({ el, gsap, st }) => {
    const kids = [...el.children];
    kids.forEach((k, i) => gsap.to(k, { yPercent: -8 * (i + 1), ease: 'none', scrollTrigger: st({ trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }) }));
  } },
  { id: 'pin-section', name: 'Pinned section', cat: 'Scroll', demo: false, apply: ({ el, gsap, st }) =>
    gsap.to(el, { ease: 'none', scrollTrigger: st({ trigger: el, start: 'top top', end: '+=100%', pin: true, scrub: true }) }) },
  { id: 'horizontal-pan', name: 'Horizontal pan', cat: 'Scroll', demo: false, apply: ({ el, gsap, st }) => {
    const track = el.querySelector('[data-pan]') || el.firstElementChild || el;
    const dist = () => Math.max(0, track.scrollWidth - el.clientWidth);
    gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: st({ trigger: el, start: 'top top', end: () => '+=' + dist(), pin: true, scrub: 1, invalidateOnRefresh: true }) });
  } },
  { id: 'scroll-progress', name: 'Scroll progress', cat: 'Scroll', apply: ({ el, gsap }) => {
    const bar = document.createElement('i');
    bar.style.cssText = 'position:absolute;left:0;bottom:0;height:2px;background:var(--red,#E40038);width:100%;transform-origin:left;transform:scaleX(0)';
    el.style.position = 'relative';
    el.appendChild(bar);
    gsap.to(bar, { scaleX: 1, ease: 'none', scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 20%', scrub: true } });
  } },
  { id: 'counter-scroll', name: 'Counter', cat: 'Scroll', apply: ({ el, gsap, st }) => {
    const target = Number(el.dataset.count || el.textContent.replace(/\D/g, '') || 100);
    const obj = { v: 0 };
    el.textContent = '0';
    gsap.to(obj, { v: target, duration: 1.6, ease: 'power2.out', scrollTrigger: st({ trigger: el, start: 'top 90%' }), onUpdate: () => { el.textContent = Math.round(obj.v); } });
  } },
  { id: 'text-scrub', name: 'Text colour scrub', cat: 'Scroll', apply: ({ el, gsap, st }) => {
    el.style.color = 'rgba(250,243,233,.16)';
    gsap.to(el, { color: 'rgba(250,243,233,1)', ease: 'none', scrollTrigger: st({ trigger: el, start: 'top 80%', end: 'bottom 40%', scrub: true }) });
  } },
  { id: 'image-scale-scrub', name: 'Image scale scrub', cat: 'Scroll', apply: ({ el, gsap, st }) => {
    const img = el.querySelector('img') || el;
    gsap.fromTo(img, { scale: 1.18 }, { scale: 1, ease: 'none', scrollTrigger: st({ trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }) });
  } },
  { id: 'rotate-scrub', name: 'Rotate on scroll', cat: 'Scroll', apply: ({ el, gsap, st }) =>
    gsap.to(el, { rotate: 24, ease: 'none', scrollTrigger: st({ trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }) }) },
  { id: 'opacity-scrub', name: 'Opacity scrub', cat: 'Scroll', apply: ({ el, gsap, st }) =>
    gsap.fromTo(el, { autoAlpha: 0.15 }, { autoAlpha: 1, ease: 'none', scrollTrigger: st({ trigger: el, start: 'top 90%', end: 'top 40%', scrub: true }) }) },
  { id: 'pin-stack', name: 'Pin stack', cat: 'Scroll', demo: false, apply: ({ el, gsap, st }) => {
    const cards = [...el.children];
    cards.forEach((c, i) => gsap.to(c, { y: -i * 14, scale: 1 - i * 0.03, scrollTrigger: st({ trigger: el, start: 'top top', end: '+=80%', pin: true, scrub: true }) }));
  } },
  { id: 'snap-sections', name: 'Snap sections', cat: 'Scroll', demo: false, apply: ({ el, ScrollTrigger }) => {
    const sections = [...el.children];
    ScrollTrigger.create({ trigger: el, start: 'top top', end: 'bottom bottom', snap: { snapTo: 1 / Math.max(1, sections.length - 1), duration: 0.4 } });
  } },
  { id: 'velocity-skew', name: 'Velocity skew', cat: 'Scroll', apply: ({ el, ScrollTrigger }) => {
    let proxy = { skew: 0 }, setter = gsap.quickSetter(el, 'skewY', 'deg');
    ScrollTrigger.create({
      trigger: el, start: 'top bottom', end: 'bottom top',
      onUpdate: self => {
        const v = clamp(self.getVelocity() / -420, -8, 8);
        gsap.to(proxy, { skew: v, duration: 0.25, ease: 'power3', overwrite: true, onUpdate: () => setter(proxy.skew) });
      }
    });
  } },
];

/* ==========================================================================
   TEXT — 12
   ========================================================================== */
const text = [
  { id: 'typewriter', name: 'Typewriter', cat: 'Text', apply: ({ el }) => {
    const original = el.textContent;
    el.textContent = '';
    let i = 0;
    const id = setInterval(() => { el.textContent = original.slice(0, ++i); if (i >= original.length) clearInterval(id); }, 55);
  } },
  { id: 'decode', name: 'Decode', cat: 'Text', apply: ({ el }) => {
    const text = el.textContent;
    el.textContent = '';
    [...text].forEach((ch, i) => {
      const s = document.createElement('span');
      s.textContent = ch === ' ' ? '\u00A0' : ch;
      s.style.display = 'inline-block';
      s.style.opacity = '0';
      el.appendChild(s);
      setTimeout(() => { s.textContent = ch; s.style.opacity = '1'; s.style.transition = 'opacity .2s'; }, 20 * i);
    });
  } },
  { id: 'scramble-on-view', name: 'Scramble on view', cat: 'Text', apply: ({ el, st }) => {
    const t = el.textContent;
    el.textContent = ' ';
    st({ trigger: el, start: 'top 90%', once: true, onEnter: () => scramble(el, t, { duration: 900 }) });
  } },
  { id: 'text-wave', name: 'Wave', cat: 'Text', apply: ({ el, gsap }) => {
    const chars = splitChars(el);
    gsap.to(chars, { y: -10, duration: 0.4, ease: 'sine.inOut', stagger: { each: 0.03, yoyo: true, repeat: -1 } });
  } },
  { id: 'gradient-fill', name: 'Gradient fill', cat: 'Text', apply: ({ el }) => {
    el.style.backgroundImage = 'linear-gradient(90deg,#FAF3E9,#FF2E56,#FAF3E9)';
    el.style.backgroundSize = '200% 100%';
    el.style.webkitBackgroundClip = 'text';
    el.style.backgroundClip = 'text';
    el.style.color = 'transparent';
    el.style.animation = 'wz-gradient 4s linear infinite';
    if (!document.getElementById('wz-gradient-kf')) {
      const s = document.createElement('style');
      s.id = 'wz-gradient-kf';
      s.textContent = '@keyframes wz-gradient{to{background-position:-200% 0}}';
      document.head.appendChild(s);
    }
  } },
  { id: 'outline-fill', name: 'Outline fill', cat: 'Text', apply: ({ el }) => {
    el.style.color = 'transparent';
    el.style.webkitTextStroke = '1px #FAF3E9';
    el.style.transition = 'color .5s, -webkit-text-stroke-color .5s';
    el.addEventListener('pointerenter', () => { el.style.color = '#FAF3E9'; el.style.webkitTextStrokeColor = 'transparent'; });
    el.addEventListener('pointerleave', () => { el.style.color = 'transparent'; el.style.webkitTextStrokeColor = '#FAF3E9'; });
  } },
  { id: 'variable-weight', name: 'Weight shift', cat: 'Text', apply: ({ el }) => {
    el.style.fontVariationSettings = '"wght" 300';
    el.style.transition = 'font-variation-settings .5s';
    el.addEventListener('pointerenter', () => { el.style.fontVariationSettings = '"wght" 900'; });
    el.addEventListener('pointerleave', () => { el.style.fontVariationSettings = '"wght" 300'; });
  } },
  { id: 'split-lines', name: 'Split lines', cat: 'Text', apply: ({ el, gsap, st }) => {
    const lines = splitWords(el);
    gsap.from(lines, { yPercent: 110, duration: 0.9, stagger: 0.08, ease: 'expo.out', scrollTrigger: st({ trigger: el, start: 'top 88%' }) });
  } },
  { id: 'word-rotate', name: 'Word rotate', cat: 'Text', apply: ({ gsap, host }) => {
    const el = host;
    const words = ['design', 'build', 'motion', 'ship'];
    let i = 0;
    const span = document.createElement('span');
    span.textContent = words[0];
    el.textContent = '';
    el.appendChild(span);
    setInterval(() => {
      i = (i + 1) % words.length;
      gsap.to(span, { yPercent: -100, autoAlpha: 0, duration: 0.35, onComplete: () => {
        span.textContent = words[i];
        gsap.fromTo(span, { yPercent: 100, autoAlpha: 0 }, { yPercent: 0, autoAlpha: 1, duration: 0.35 });
      } });
    }, 2200);
  } },
  { id: 'marquee-type', name: 'Type marquee', cat: 'Text', apply: ({ el }) => {
    const content = el.innerHTML;
    el.innerHTML = `<span>${content}</span><span aria-hidden="true">${content}</span>`;
    el.style.display = 'flex'; el.style.width = 'max-content'; el.style.gap = '3rem';
    el.style.animation = 'wz-marquee 18s linear infinite';
    if (!document.getElementById('wz-marquee-kf')) {
      const s = document.createElement('style');
      s.id = 'wz-marquee-kf';
      s.textContent = '@keyframes wz-marquee{to{transform:translateX(-50%)}}';
      document.head.appendChild(s);
    }
  } },
  { id: 'text-mask-reveal', name: 'Masked lines', cat: 'Text', apply: ({ el }) => {
    const text = el.textContent;
    el.textContent = '';
    const wrap = document.createElement('span');
    wrap.style.cssText = 'display:block;overflow:hidden';
    const inner = document.createElement('span');
    inner.textContent = text;
    inner.style.cssText = 'display:block;transform:translateY(110%);transition:transform .9s cubic-bezier(.16,1,.3,1)';
    wrap.appendChild(inner);
    el.appendChild(wrap);
    requestAnimationFrame(() => requestAnimationFrame(() => { inner.style.transform = 'none'; }));
  } },
  { id: 'cursor-type', name: 'Cursor caret', cat: 'Text', apply: ({ el }) => {
    const caret = document.createElement('i');
    caret.style.cssText = 'display:inline-block;width:1px;height:1em;background:currentColor;vertical-align:-.12em;margin-left:2px;animation:wz-blink 1s steps(2) infinite';
    el.appendChild(caret);
    if (!document.getElementById('wz-blink-kf')) {
      const s = document.createElement('style');
      s.id = 'wz-blink-kf';
      s.textContent = '@keyframes wz-blink{50%{opacity:0}}';
      document.head.appendChild(s);
    }
  } },
];

/* ==========================================================================
   CURSOR — 8
   ========================================================================== */
const cursorFx = [
  { id: 'cursor-dot', name: 'Local dot', cat: 'Cursor', apply: ({ el }) => {
    el.style.position = 'relative';
    el.style.cursor = 'none';
    const dot = document.createElement('i');
    dot.style.cssText = 'position:absolute;width:6px;height:6px;border-radius:50%;background:var(--cream,#FAF3E9);pointer-events:none;transform:translate(-50%,-50%);mix-blend-mode:difference;z-index:9';
    el.appendChild(dot);
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      dot.style.left = e.clientX - r.left + 'px';
      dot.style.top = e.clientY - r.top + 'px';
    });
  } },
  { id: 'cursor-ring-lag', name: 'Ring lag', cat: 'Cursor', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.cursor = 'none';
    const ring = document.createElement('i');
    ring.style.cssText = 'position:absolute;width:38px;height:38px;border:1px solid rgba(250,243,233,.5);border-radius:50%;pointer-events:none;transform:translate(-50%,-50%);transition:width .3s,height .3s;z-index:9';
    el.appendChild(ring);
    let x = 0, y = 0, tx = 0, ty = 0;
    el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(); tx = e.clientX - r.left; ty = e.clientY - r.top; });
    (function loop() { x = lerp(x, tx, 0.14); y = lerp(y, ty, 0.14); ring.style.left = x + 'px'; ring.style.top = y + 'px'; requestAnimationFrame(loop); })();
  } },
  { id: 'cursor-blend', name: 'Difference blend', cat: 'Cursor', apply: ({ el }) => {
    el.style.position = 'relative';
    const c = document.createElement('i');
    c.style.cssText = 'position:absolute;inset:0;pointer-events:none;background:radial-gradient(80px 80px at var(--cx,50%) var(--cy,50%),#FAF3E9 0 18%,transparent 70%);mix-blend-mode:difference;opacity:.55';
    el.appendChild(c);
    el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(); c.style.setProperty('--cx', `${e.clientX - r.left}px`); c.style.setProperty('--cy', `${e.clientY - r.top}px`); });
  } },
  { id: 'cursor-trail', name: 'Trail', cat: 'Cursor', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.overflow = 'hidden';
    const dots = Array.from({ length: 8 }, () => {
      const d = document.createElement('i');
      d.style.cssText = 'position:absolute;width:4px;height:4px;border-radius:50%;background:var(--red,#E40038);pointer-events:none;opacity:.5;transform:translate(-50%,-50%)';
      el.appendChild(d); return d;
    });
    let x = 0, y = 0;
    el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(); x = e.clientX - r.left; y = e.clientY - r.top; });
    (function loop() {
      let px = x, py = y;
      dots.forEach((d, i) => {
        px = lerp(px, x, 0.35 - i * 0.03);
        py = lerp(py, y, 0.35 - i * 0.03);
        d.style.left = px + 'px'; d.style.top = py + 'px';
      });
      requestAnimationFrame(loop);
    })();
  } },
  { id: 'cursor-label', name: 'Cursor label', cat: 'Cursor', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.cursor = 'none';
    const wrap = document.createElement('i');
    wrap.style.cssText = 'position:absolute;width:64px;height:64px;border-radius:50%;background:var(--red,#E40038);color:#FAF3E9;display:grid;place-items:center;font-size:8px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;font-style:normal;pointer-events:none;transform:translate(-50%,-50%) scale(0);transition:transform .25s;z-index:9';
    wrap.textContent = 'Drag';
    el.appendChild(wrap);
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      wrap.style.left = e.clientX - r.left + 'px';
      wrap.style.top = e.clientY - r.top + 'px';
      wrap.style.transform = 'translate(-50%,-50%) scale(1)';
    });
    el.addEventListener('pointerleave', () => { wrap.style.transform = 'translate(-50%,-50%) scale(0)'; });
  } },
  { id: 'cursor-hide-native', name: 'Hidden native cursor', cat: 'Cursor', apply: ({ el }) => {
    el.style.cursor = 'none';
    el.style.backgroundImage = 'radial-gradient(circle at var(--cx,50%) var(--cy,50%),rgba(255,46,86,.35),transparent 18%)';
    el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(); el.style.setProperty('--cx', `${e.clientX - r.left}px`); el.style.setProperty('--cy', `${e.clientY - r.top}px`); });
  } },
  { id: 'cursor-scale-link', name: 'Scale on target', cat: 'Cursor', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.cursor = 'none';
    const d = document.createElement('i');
    d.style.cssText = 'position:absolute;width:10px;height:10px;border-radius:50%;background:var(--cream,#FAF3E9);pointer-events:none;transform:translate(-50%,-50%);transition:width .25s,height .25s;z-index:9';
    el.appendChild(d);
    el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(); d.style.left = e.clientX - r.left + 'px'; d.style.top = e.clientY - r.top + 'px'; });
    el.addEventListener('pointerenter', () => { d.style.width = '44px'; d.style.height = '44px'; d.style.mixBlendMode = 'difference'; });
    el.addEventListener('pointerleave', () => { d.style.width = '10px'; d.style.height = '10px'; d.style.mixBlendMode = ''; });
  } },
  { id: 'cursor-snap', name: 'Magnetic snap', cat: 'Cursor', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.cursor = 'none';
    const d = document.createElement('i');
    d.style.cssText = 'position:absolute;width:12px;height:12px;border-radius:50%;border:1px solid var(--red,#E40038);pointer-events:none;transform:translate(-50%,-50%);transition:left .18s,top .18s;z-index:9';
    el.appendChild(d);
    el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(); d.style.left = e.clientX - r.left + 'px'; d.style.top = e.clientY - r.top + 'px'; });
  } },
];

/* ==========================================================================
   DEPTH & 3D — 12   (canvas / CSS; the hero runs the full WebGL scene)
   ========================================================================== */
function canvasFx(el, draw) {
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block';
  el.style.position = 'relative';
  el.style.overflow = 'hidden';
  el.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  let w = 0, h = 0, raf = 0, visible = true;
  const size = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const r = el.getBoundingClientRect();
    w = Math.max(1, r.width); h = Math.max(1, r.height);
    canvas.width = w * dpr; canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  size();
  const ro = new ResizeObserver(size);
  ro.observe(el);
  const io = new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) { cancelAnimationFrame(raf); frame(performance.now()); } }, { threshold: 0 });
  io.observe(el);
  function frame(t) {
    if (!visible) return;
    ctx.clearRect(0, 0, w, h);
    draw(ctx, w, h, t, el);
    raf = requestAnimationFrame(frame);
  }
  raf = requestAnimationFrame(frame);
  return () => { cancelAnimationFrame(raf); ro.disconnect(); io.disconnect(); canvas.remove(); };
}

const depth = [
  { id: 'layers-3d', name: 'Layered card 3D', cat: 'Depth', apply: ({ el }) => {
    el.style.transformStyle = 'preserve-3d';
    [...el.children].forEach((k, i) => { k.style.transform = `translateZ(${i * 22}px)`; });
    tilt(el, 14);
  } },
  { id: 'orbit', name: 'Orbit', cat: 'Depth', apply: ({ el }) => {
    el.style.perspective = '800px';
    const stage = document.createElement('i');
    stage.style.cssText = 'position:absolute;inset:0;display:grid;place-items:center;transform-style:preserve-3d;animation:wz-orbit 12s linear infinite';
    stage.innerHTML = '<b style="position:absolute;width:18px;height:18px;border-radius:50%;background:#FF2E56;transform:translateZ(70px)"></b><b style="position:absolute;width:10px;height:10px;border-radius:50%;background:#FAF3E9;transform:rotateY(120deg) translateZ(70px)"></b><b style="position:absolute;width:14px;height:14px;border:1px solid #FAF3E9;transform:rotateY(240deg) translateZ(70px)"></b>';
    el.style.position = 'relative';
    el.appendChild(stage);
    if (!document.getElementById('wz-orbit-kf')) {
      const s = document.createElement('style'); s.id = 'wz-orbit-kf';
      s.textContent = '@keyframes wz-orbit{to{transform:rotateY(360deg) rotateX(12deg)}}';
      document.head.appendChild(s);
    }
  } },
  { id: 'holo-foil', name: 'Holographic foil', cat: 'Depth', apply: ({ el }) => {
    el.style.backgroundImage = 'conic-gradient(from var(--ang,0deg), #FF2E56, #FAF3E9, #6f7bff, #FF2E56)';
    el.style.backgroundBlendMode = 'color';
    el.style.animation = 'wz-holo 6s linear infinite';
    if (!document.getElementById('wz-holo-kf')) {
      const s = document.createElement('style'); s.id = 'wz-holo-kf';
      s.textContent = '@property --ang{syntax:"<angle>";initial-value:0deg;inherits:false}@keyframes wz-holo{to{--ang:360deg}}';
      document.head.appendChild(s);
    }
  } },
  { id: 'floating-layers', name: 'Floating layers', cat: 'Depth', apply: ({ el, gsap }) => {
    [...el.children].forEach((k, i) => gsap.to(k, { y: i % 2 ? 12 : -12, duration: 2 + i * 0.4, yoyo: true, repeat: -1, ease: 'sine.inOut', delay: i * 0.2 }));
  } },
  { id: 'depth-pointer', name: 'Pointer depth', cat: 'Depth', apply: ({ el }) => {
    const kids = [...el.children];
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      kids.forEach((k, i) => { k.style.transform = `translate3d(${-x * (i + 1) * 9}px,${-y * (i + 1) * 9}px,0)`; });
    });
    el.addEventListener('pointerleave', () => kids.forEach(k => { k.style.transform = ''; }));
  } },
  { id: 'perspective-grid', name: 'Perspective grid', cat: 'Depth', apply: ({ el }) => canvasFx(el, (ctx, w, h, t) => {
    ctx.strokeStyle = 'rgba(250,243,233,.18)'; ctx.lineWidth = 1;
    const hz = h * 0.55, off = (t / 40) % 40;
    for (let i = 0; i < 14; i++) {
      const z = i + off / 40;
      const y = hz + (h - hz) / z;
      if (y > h) continue;
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }
    for (let i = -10; i <= 10; i++) {
      ctx.beginPath(); ctx.moveTo(w / 2 + i * 10, hz); ctx.lineTo(w / 2 + i * w / 8, h); ctx.stroke();
    }
  }) },
  { id: 'starfield', name: 'Starfield', cat: 'Depth', apply: ({ el }) => canvasFx(el, (ctx, w, h) => {
    const n = Math.min(120, Math.floor(w * h / 2600));
    for (let i = 0; i < n; i++) {
      const x = (i * 97.13) % w, y = (i * 53.71) % h;
      const a = 0.15 + ((i * 37) % 70) / 100;
      ctx.fillStyle = `rgba(250,243,233,${a})`;
      ctx.fillRect(x, y, 1.4, 1.4);
    }
  }) },
  { id: 'particle-field', name: 'Particle field', cat: 'Depth', apply: ({ el }) => {
    const pts = [];
    canvasFx(el, (ctx, w, h, t) => {
      if (!pts.length) for (let i = 0; i < 70; i++) pts.push({ x: Math.random() * w, y: Math.random() * h, vx: rnd(-0.25, 0.25), vy: rnd(-0.25, 0.25) });
      ctx.fillStyle = 'rgba(255,46,86,.75)';
      pts.forEach((p, i) => {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;
        ctx.beginPath(); ctx.arc(p.x, p.y, 1.6, 0, Math.PI * 2); ctx.fill();
        for (let j = i + 1; j < pts.length; j++) {
          const q = pts[j], d = Math.hypot(p.x - q.x, p.y - q.y);
          if (d < 60) { ctx.strokeStyle = `rgba(250,243,233,${0.18 * (1 - d / 60)})`; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke(); }
        }
      });
    });
  } },
  { id: 'wireframe-torus', name: 'Wireframe torus', cat: 'Depth', apply: ({ el }) => canvasFx(el, (ctx, w, h, t) => {
    const cx = w / 2, cy = h / 2, R = Math.min(w, h) * 0.26, r = R * 0.36, a = t / 1400;
    ctx.strokeStyle = 'rgba(250,243,233,.35)'; ctx.lineWidth = 1;
    for (let i = 0; i < 20; i++) {
      ctx.beginPath();
      for (let j = 0; j <= 34; j++) {
        const u = (i / 20) * Math.PI * 2, v = (j / 34) * Math.PI * 2;
        const x = (R + r * Math.cos(v)) * Math.cos(u), y = (R + r * Math.cos(v)) * Math.sin(u) * 0.55, z = r * Math.sin(v);
        const s = 1 + z / (R * 3);
        const px = cx + (x * Math.cos(a) - y * Math.sin(a)) * s;
        const py = cy + (x * Math.sin(a) + y * Math.cos(a)) * s;
        j ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
      }
      ctx.stroke();
    }
  }) },
  { id: 'vertex-wave', name: 'Vertex wave', cat: 'Depth', apply: ({ el }) => canvasFx(el, (ctx, w, h, t) => {
    ctx.strokeStyle = 'rgba(255,46,86,.55)'; ctx.lineWidth = 1;
    const step = 14;
    for (let x = 0; x <= w; x += step) {
      const y = h / 2 + Math.sin(x / 38 + t / 500) * 16 + Math.cos(x / 71 - t / 700) * 9;
      x === 0 ? ctx.beginPath() && ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.stroke();
  }) },
  { id: 'shader-glow', name: 'Shader-style glow', cat: 'Depth', apply: ({ el }) => canvasFx(el, (ctx, w, h, t) => {
    const g = ctx.createRadialGradient(w * 0.5 + Math.sin(t / 900) * w * 0.12, h * 0.5 + Math.cos(t / 1100) * h * 0.1, 4, w / 2, h / 2, Math.max(w, h) * 0.5);
    g.addColorStop(0, 'rgba(255,46,86,.85)');
    g.addColorStop(0.4, 'rgba(255,46,86,.14)');
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  }) },
  { id: 'noise-displace', name: 'Noise displace', cat: 'Depth', apply: ({ el }) => {
    const img = el.querySelector('img') || el;
    el.style.position = 'relative';
    img.style.transition = 'filter .4s';
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      img.style.filter = `blur(${Math.abs(x) * 2}px) contrast(1.05)`;
      img.style.transform = `scale(1.04) translateX(${x * 8}px)`;
    });
    el.addEventListener('pointerleave', () => { img.style.filter = ''; img.style.transform = ''; });
  } },
];

/* ==========================================================================
   ATMOSPHERE — 10
   ========================================================================== */
const atmosphere = [
  { id: 'grain', name: 'Film grain', cat: 'Atmosphere', apply: ({ el }) => {
    el.style.position = 'relative';
    const g = document.createElement('i');
    g.style.cssText = 'position:absolute;inset:0;pointer-events:none;opacity:.4;mix-blend-mode:overlay;background-image:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'140\' height=\'140\'%3E%3Cfilter id=\'n\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'3\'/%3E%3C/filter%3E%3Crect width=\'140\' height=\'140\' filter=\'url(%23n)\' opacity=\'0.55\'/%3E%3C/svg%3E")';
    el.appendChild(g);
  } },
  { id: 'scanlines', name: 'Scanlines', cat: 'Atmosphere', apply: ({ el }) => {
    el.style.position = 'relative';
    const g = document.createElement('i');
    g.style.cssText = 'position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(0,0,0,.32) 0 1px,transparent 1px 3px);opacity:.6';
    el.appendChild(g);
  } },
  { id: 'vignette', name: 'Vignette', cat: 'Atmosphere', apply: ({ el }) => {
    el.style.position = 'relative';
    const g = document.createElement('i');
    g.style.cssText = 'position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,.75) 100%)';
    el.appendChild(g);
  } },
  { id: 'aurora', name: 'Aurora', cat: 'Atmosphere', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.overflow = 'hidden';
    const g = document.createElement('i');
    g.style.cssText = 'position:absolute;inset:-40%;background:radial-gradient(40% 50% at 30% 40%,rgba(255,46,86,.55),transparent 70%),radial-gradient(40% 50% at 70% 60%,rgba(96,110,255,.45),transparent 70%);filter:blur(30px);animation:wz-aurora 14s ease-in-out infinite alternate';
    el.appendChild(g);
    if (!document.getElementById('wz-aurora-kf')) {
      const s = document.createElement('style'); s.id = 'wz-aurora-kf';
      s.textContent = '@keyframes wz-aurora{to{transform:translate3d(8%,-6%,0) rotate(8deg) scale(1.15)}}';
      document.head.appendChild(s);
    }
  } },
  { id: 'mesh-gradient', name: 'Mesh gradient', cat: 'Atmosphere', apply: ({ el }) => {
    el.style.background = 'conic-gradient(from 180deg at 50% 50%, #0B0705, #2a0a12, #0B0705, #12100e, #0B0705)';
    el.style.backgroundSize = '180% 180%';
    el.style.animation = 'wz-mesh 16s ease-in-out infinite alternate';
    if (!document.getElementById('wz-mesh-kf')) {
      const s = document.createElement('style'); s.id = 'wz-mesh-kf';
      s.textContent = '@keyframes wz-mesh{to{background-position:100% 100%;filter:hue-rotate(25deg)}}';
      document.head.appendChild(s);
    }
  } },
  { id: 'halftone', name: 'Halftone', cat: 'Atmosphere', apply: ({ el }) => {
    el.style.backgroundImage = 'radial-gradient(rgba(250,243,233,.5) 1px, transparent 1.4px)';
    el.style.backgroundSize = '7px 7px';
    el.style.opacity = '.9';
  } },
  { id: 'dither', name: 'Dither grid', cat: 'Atmosphere', apply: ({ el }) => {
    const g = document.createElement('i');
    el.style.position = 'relative';
    g.style.cssText = 'position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(45deg,rgba(250,243,233,.28) 25%,transparent 25%,transparent 75%,rgba(250,243,233,.28) 75%),linear-gradient(45deg,rgba(250,243,233,.28) 25%,transparent 25%,transparent 75%,rgba(250,243,233,.28) 75%);background-size:4px 4px;background-position:0 0,2px 2px;opacity:.35';
    el.appendChild(g);
  } },
  { id: 'duotone', name: 'Duotone', cat: 'Atmosphere', apply: ({ el }) => {
    el.style.filter = 'grayscale(1) sepia(1) hue-rotate(310deg) saturate(4) contrast(1.05)';
  } },
  { id: 'bloom', name: 'Bloom', cat: 'Atmosphere', apply: ({ el }) => {
    el.style.boxShadow = '0 0 40px rgba(255,46,86,.35), inset 0 0 60px rgba(255,46,86,.18)';
    el.style.border = '1px solid rgba(255,46,86,.4)';
  } },
  { id: 'noise-border', name: 'Rough border', cat: 'Atmosphere', apply: ({ el }) => {
    el.style.border = '1px solid transparent';
    el.style.backgroundImage = 'linear-gradient(#120d0a,#120d0a),url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'60\' height=\'60\'%3E%3Cfilter id=\'n\'%3E%3CfeTurbulence baseFrequency=\'0.22\' numOctaves=\'2\'/%3E%3C/filter%3E%3Crect width=\'60\' height=\'60\' filter=\'url(%23n)\'/%3E%3C/svg%3E")';
    el.style.backgroundOrigin = 'border-box';
    el.style.backgroundClip = 'padding-box, border-box';
    el.style.boxShadow = '0 0 0 1px rgba(250,243,233,.18)';
  } },
];

/* ==========================================================================
   MICRO — 12
   ========================================================================== */
const micro = [
  { id: 'ripple', name: 'Click ripple', cat: 'Micro', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.overflow = 'hidden';
    el.addEventListener('pointerdown', e => {
      const r = el.getBoundingClientRect();
      const s = document.createElement('i');
      const size = Math.max(r.width, r.height) * 2;
      s.style.cssText = `position:absolute;left:${e.clientX - r.left - size / 2}px;top:${e.clientY - r.top - size / 2}px;width:${size}px;height:${size}px;border-radius:50%;background:rgba(250,243,233,.35);transform:scale(0);transition:transform .6s ease-out,opacity .6s;pointer-events:none`;
      el.appendChild(s);
      requestAnimationFrame(() => { s.style.transform = 'scale(1)'; s.style.opacity = '0'; });
      setTimeout(() => s.remove(), 650);
    });
  } },
  { id: 'press-scale', name: 'Press scale', cat: 'Micro', apply: ({ el }) => {
    el.style.transition = 'transform .15s';
    el.addEventListener('pointerdown', () => { el.style.transform = 'scale(.96)'; });
    el.addEventListener('pointerup', () => { el.style.transform = ''; });
    el.addEventListener('pointerleave', () => { el.style.transform = ''; });
  } },
  { id: 'copy-feedback', name: 'Copy to clipboard', cat: 'Micro', apply: ({ el }) => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(el.dataset.copy || el.textContent.trim()); } catch (_) {}
      const old = el.textContent;
      el.textContent = 'Copied';
      setTimeout(() => { el.textContent = old; }, 1200);
    });
  } },
  { id: 'toggle', name: 'Toggle switch', cat: 'Micro', apply: ({ el }) => {
    el.innerHTML = '';
    el.style.cssText += ';display:inline-flex;align-items:center;gap:10px;cursor:pointer;user-select:none';
    const track = document.createElement('i');
    track.style.cssText = 'width:42px;height:22px;border-radius:20px;background:rgba(250,243,233,.2);position:relative;transition:background .3s';
    const knob = document.createElement('b');
    knob.style.cssText = 'position:absolute;top:3px;left:3px;width:16px;height:16px;border-radius:50%;background:#FAF3E9;transition:transform .3s';
    track.appendChild(knob);
    const label = document.createElement('span');
    label.textContent = 'Off';
    el.append(track, label);
    let on = false;
    el.addEventListener('click', () => {
      on = !on;
      track.style.background = on ? '#E40038' : 'rgba(250,243,233,.2)';
      knob.style.transform = on ? 'translateX(20px)' : '';
      label.textContent = on ? 'On' : 'Off';
      el.setAttribute('aria-pressed', String(on));
    });
    el.setAttribute('role', 'button');
    el.setAttribute('tabindex', '0');
  } },
  { id: 'tooltip', name: 'Tooltip', cat: 'Micro', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.cursor = 'help';
    const tip = document.createElement('span');
    tip.textContent = el.dataset.tip || 'Helpful context';
    tip.style.cssText = 'position:absolute;left:50%;bottom:calc(100% + 10px);transform:translate(-50%,6px);background:#FAF3E9;color:#0B0705;font-size:11px;padding:7px 10px;white-space:nowrap;opacity:0;transition:.25s;pointer-events:none;z-index:5';
    el.appendChild(tip);
    el.addEventListener('pointerenter', () => { tip.style.opacity = '1'; tip.style.transform = 'translate(-50%,0)'; });
    el.addEventListener('pointerleave', () => { tip.style.opacity = '0'; tip.style.transform = 'translate(-50%,6px)'; });
  } },
  { id: 'shine-button', name: 'Sheen button', cat: 'Micro', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.overflow = 'hidden';
    el.style.animation = 'wz-sheen 3.6s ease-in-out infinite';
    if (!document.getElementById('wz-sheen-kf')) {
      const s = document.createElement('style'); s.id = 'wz-sheen-kf';
      s.textContent = '@keyframes wz-sheen{0%,60%{box-shadow:0 0 0 0 rgba(255,46,86,0)}70%{box-shadow:0 0 0 6px rgba(255,46,86,.15)}100%{box-shadow:0 0 0 0 rgba(255,46,86,0)}}';
      document.head.appendChild(s);
    }
  } },
  { id: 'checkbox-draw', name: 'Drawn checkbox', cat: 'Micro', apply: ({ el }) => {
    el.innerHTML = '<svg viewBox="0 0 32 32" width="32" height="32" aria-hidden="true"><rect x="2" y="2" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 17l6 6L25 10" fill="none" stroke="#FF2E56" stroke-width="3" stroke-dasharray="40" stroke-dashoffset="40"/></svg>';
    el.style.cursor = 'pointer';
    const path = el.querySelector('path');
    el.addEventListener('click', () => {
      const on = path.style.strokeDashoffset === '0';
      path.style.transition = 'stroke-dashoffset .5s ease';
      path.style.strokeDashoffset = on ? '40' : '0';
    });
  } },
  { id: 'slider-fill', name: 'Range slider', cat: 'Micro', apply: ({ el }) => {
    el.innerHTML = '<input type="range" min="0" max="100" value="42" aria-label="Value" style="width:100%;accent-color:#E40038">';
    el.style.width = '100%';
  } },
  { id: 'drag-hint', name: 'Drag hint', cat: 'Micro', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.cursor = 'grab';
    const h = document.createElement('span');
    h.textContent = '← drag →';
    h.style.cssText = 'position:absolute;bottom:10px;left:50%;transform:translateX(-50%);font-size:9px;letter-spacing:.2em;text-transform:uppercase;opacity:.55;transition:opacity .3s;white-space:nowrap';
    el.appendChild(h);
    el.addEventListener('pointerenter', () => { h.style.opacity = '0'; });
    el.addEventListener('pointerleave', () => { h.style.opacity = '.55'; });
  } },
  { id: 'toast', name: 'Toast', cat: 'Micro', apply: ({ el }) => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => {
      const t = document.createElement('div');
      t.textContent = 'Saved to the brief';
      t.style.cssText = 'position:fixed;left:50%;bottom:32px;transform:translate(-50%,20px);background:#FAF3E9;color:#0B0705;font:600 12px/1 Archivo,sans-serif;letter-spacing:.08em;text-transform:uppercase;padding:14px 20px;z-index:999;opacity:0;transition:.35s';
      document.body.appendChild(t);
      requestAnimationFrame(() => { t.style.opacity = '1'; t.style.transform = 'translate(-50%,0)'; });
      setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translate(-50%,20px)'; setTimeout(() => t.remove(), 400); }, 1900);
    });
  } },
  { id: 'shimmer', name: 'Skeleton shimmer', cat: 'Micro', apply: ({ el }) => {
    el.innerHTML = '';
    el.style.background = 'rgba(250,243,233,.08)';
    el.style.position = 'relative'; el.style.overflow = 'hidden';
    const s = document.createElement('i');
    s.style.cssText = 'position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(250,243,233,.22),transparent);transform:translateX(-100%);animation:wz-shimmer 1.6s infinite';
    el.appendChild(s);
    if (!document.getElementById('wz-shimmer-kf')) {
      const st = document.createElement('style'); st.id = 'wz-shimmer-kf';
      st.textContent = '@keyframes wz-shimmer{to{transform:translateX(100%)}}';
      document.head.appendChild(st);
    }
  } },
  { id: 'focus-ring', name: 'Focus ring', cat: 'Micro', apply: ({ el }) => {
    el.tabIndex = 0;
    el.style.outline = 'none';
    el.addEventListener('focus', () => { el.style.boxShadow = '0 0 0 2px #0B0705, 0 0 0 4px #FF2E56'; });
    el.addEventListener('blur', () => { el.style.boxShadow = ''; });
  } },
];

/* ==========================================================================
   TRANSITIONS — 8   (play on click)
   ========================================================================== */
function overlay(color = '#E40038') {
  const o = document.createElement('i');
  o.style.cssText = `position:fixed;inset:0;background:${color};z-index:9998;pointer-events:none;transform:scaleY(0);transform-origin:bottom`;
  document.body.appendChild(o);
  return o;
}
const transitions = [
  { id: 'curtain', name: 'Curtain', cat: 'Transition', demo: false, apply: ({ el }) => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => {
      const o = overlay();
      o.animate([{ transform: 'scaleY(0)', transformOrigin: 'bottom' }, { transform: 'scaleY(1)', transformOrigin: 'bottom' }, { transform: 'scaleY(0)', transformOrigin: 'top' }], { duration: 1100, easing: 'cubic-bezier(.76,0,.24,1)' }).onfinish = () => o.remove();
    });
  } },
  { id: 'circle-wipe', name: 'Circle wipe', cat: 'Transition', demo: false, apply: ({ el }) => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => {
      const o = overlay('#FAF3E9');
      o.style.transform = 'none';
      o.style.clipPath = 'circle(0% at 50% 50%)';
      o.animate([{ clipPath: 'circle(0% at 50% 50%)' }, { clipPath: 'circle(150% at 50% 50%)' }, { clipPath: 'circle(0% at 50% 50%)' }], { duration: 1200, easing: 'ease-in-out' }).onfinish = () => o.remove();
    });
  } },
  { id: 'fade-through', name: 'Fade through', cat: 'Transition', demo: false, apply: ({ el }) => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => {
      const o = overlay('#0B0705');
      o.style.transform = 'none'; o.style.opacity = '0';
      o.animate([{ opacity: 0 }, { opacity: 1 }, { opacity: 0 }], { duration: 900 }).onfinish = () => o.remove();
    });
  } },
  { id: 'pixelate', name: 'Pixelate', cat: 'Transition', demo: false, apply: ({ el }) => {
    el.style.cursor = 'pointer';
    el.style.transition = 'filter .5s';
    el.addEventListener('click', () => {
      el.style.filter = 'blur(10px) contrast(1.4)';
      setTimeout(() => { el.style.filter = ''; }, 420);
    });
  } },
  { id: 'liquid-sweep', name: 'Liquid sweep', cat: 'Transition', demo: false, apply: ({ el }) => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => {
      const o = overlay('#FF2E56');
      o.style.transform = 'none';
      o.animate([
        { clipPath: 'inset(100% 0 0 0)' },
        { clipPath: 'inset(0% 0 0 0)' },
        { clipPath: 'inset(0 0 100% 0)' }
      ], { duration: 1100, easing: 'cubic-bezier(.76,0,.24,1)' }).onfinish = () => o.remove();
    });
  } },
  { id: 'split-flap', name: 'Split flap', cat: 'Transition', demo: false, apply: ({ el }) => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => {
      const top = overlay('#120d0a'), bot = overlay('#120d0a');
      top.style.transformOrigin = 'top'; bot.style.transformOrigin = 'bottom';
      top.style.top = '0'; top.style.height = '50%'; top.style.bottom = 'auto';
      bot.style.top = '50%'; bot.style.height = '50%'; bot.style.bottom = 'auto';
      top.style.transform = 'scaleY(1)'; bot.style.transform = 'scaleY(1)';
      top.animate([{ transform: 'scaleY(1)' }, { transform: 'scaleY(0)' }], { duration: 500, fill: 'forwards' });
      bot.animate([{ transform: 'scaleY(1)' }, { transform: 'scaleY(0)' }], { duration: 500, delay: 380, fill: 'forwards' }).onfinish = () => { top.remove(); bot.remove(); };
    });
  } },
  { id: 'veil', name: 'Veil', cat: 'Transition', demo: false, apply: ({ el }) => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => {
      const o = overlay('rgba(11,7,5,.92)');
      o.style.transform = 'none'; o.style.opacity = '0'; o.style.backdropFilter = 'blur(8px)';
      o.animate([{ opacity: 0 }, { opacity: 1 }, { opacity: 0 }], { duration: 1000, easing: 'ease-in-out' }).onfinish = () => o.remove();
    });
  } },
  { id: 'scroll-mask', name: 'Scroll mask', cat: 'Transition', demo: false, apply: ({ el, gsap, st }) => {
    gsap.fromTo(el, { clipPath: 'inset(12% 0 12% 0)' }, { clipPath: 'inset(0% 0 0% 0)', ease: 'none', scrollTrigger: st({ trigger: el, start: 'top bottom', end: 'top center', scrub: true }) });
  } },
];

/* ==========================================================================
   CARDS & GALLERY — 8
   ========================================================================== */
const cards = [
  { id: 'card-spotlight', name: 'Card spotlight', cat: 'Cards', apply: ({ el }) => {
    el.style.position = 'relative'; el.style.overflow = 'hidden';
    const s = document.createElement('i');
    s.style.cssText = 'position:absolute;inset:0;pointer-events:none;background:radial-gradient(180px 180px at var(--mx,50%) var(--my,50%),rgba(255,46,86,.28),transparent 70%);opacity:0;transition:opacity .3s';
    el.appendChild(s);
    el.addEventListener('pointermove', e => { const r = el.getBoundingClientRect(); el.style.setProperty('--mx', `${e.clientX - r.left}px`); el.style.setProperty('--my', `${e.clientY - r.top}px`); s.style.opacity = '1'; });
    el.addEventListener('pointerleave', () => { s.style.opacity = '0'; });
    tilt(el, 7);
  } },
  { id: 'card-stack', name: 'Stacked deck', cat: 'Cards', apply: ({ el }) => {
    const kids = [...el.children];
    el.style.position = 'relative'; el.style.height = '160px';
    kids.forEach((k, i) => {
      k.style.cssText += `;position:absolute;inset:0;transition:transform .5s cubic-bezier(.2,.8,.2,1);transform:translateY(${i * 10}px) rotate(${(i - 1) * 2}deg)`;
    });
    el.addEventListener('pointerenter', () => kids.forEach((k, i) => { k.style.transform = `translateY(${i * 18}px) rotate(${(i - 1) * 5}deg)`; }));
    el.addEventListener('pointerleave', () => kids.forEach((k, i) => { k.style.transform = `translateY(${i * 10}px) rotate(${(i - 1) * 2}deg)`; }));
  } },
  { id: 'card-flip', name: 'Flip card', cat: 'Cards', apply: ({ el }) => {
    el.style.perspective = '900px';
    const inner = document.createElement('div');
    inner.innerHTML = el.innerHTML;
    inner.style.cssText = 'position:relative;height:100%;transition:transform .7s cubic-bezier(.2,.8,.2,1);transform-style:preserve-3d';
    el.innerHTML = '';
    el.appendChild(inner);
    const front = document.createElement('div');
    front.style.cssText = 'position:absolute;inset:0;display:grid;place-items:center;backface-visibility:hidden';
    front.textContent = el.dataset.front || 'Front';
    const back = document.createElement('div');
    back.style.cssText = 'position:absolute;inset:0;display:grid;place-items:center;backface-visibility:hidden;transform:rotateY(180deg);background:#E40038;color:#FAF3E9';
    back.textContent = el.dataset.back || 'Back';
    inner.append(front, back);
    el.addEventListener('pointerenter', () => { inner.style.transform = 'rotateY(180deg)'; });
    el.addEventListener('pointerleave', () => { inner.style.transform = ''; });
  } },
  { id: 'card-image-reveal', name: 'Image reveal card', cat: 'Cards', apply: ({ el, gsap, st }) => {
    const img = el.querySelector('img');
    const cover = document.createElement('i');
    cover.style.cssText = 'position:absolute;inset:0;background:#FAF3E9;transform-origin:top;z-index:2';
    el.style.position = 'relative'; el.style.overflow = 'hidden';
    el.appendChild(cover);
    gsap.to(cover, { scaleY: 0, duration: 1, ease: 'expo.inOut', scrollTrigger: st({ trigger: el, start: 'top 85%' }) });
    if (img) gsap.from(img, { scale: 1.15, duration: 1.3, ease: 'expo.out', scrollTrigger: st({ trigger: el, start: 'top 85%' }) });
  } },
  { id: 'drag-carousel', name: 'Drag carousel', cat: 'Cards', apply: ({ el }) => {
    el.style.display = 'flex'; el.style.gap = '14px'; el.style.overflowX = 'auto'; el.style.cursor = 'grab';
    el.style.scrollbarWidth = 'none'; el.style.scrollSnapType = 'x mandatory';
    [...el.children].forEach(k => { k.style.flex = '0 0 65%'; k.style.scrollSnapAlign = 'start'; });
    let down = false, sx = 0, sl = 0;
    el.addEventListener('pointerdown', e => { down = true; sx = e.clientX; sl = el.scrollLeft; el.setPointerCapture(e.pointerId); });
    el.addEventListener('pointermove', e => { if (down) el.scrollLeft = sl - (e.clientX - sx); });
    el.addEventListener('pointerup', () => { down = false; });
  } },
  { id: 'infinite-marquee', name: 'Infinite marquee', cat: 'Cards', apply: ({ el }) => {
    const inner = el.innerHTML;
    el.innerHTML = `<div style="display:flex;gap:24px;width:max-content;animation:wz-marquee 16s linear infinite">${inner}${inner}</div>`;
    el.style.overflow = 'hidden';
    if (!document.getElementById('wz-marquee-kf')) {
      const s = document.createElement('style'); s.id = 'wz-marquee-kf';
      s.textContent = '@keyframes wz-marquee{to{transform:translateX(-50%)}}';
      document.head.appendChild(s);
    }
  } },
  { id: 'filter-grid', name: 'Filter grid', cat: 'Cards', apply: ({ el }) => {
    const kids = [...el.children];
    const cats = [...new Set(kids.map(k => k.dataset.cat).filter(Boolean))];
    const bar = document.createElement('div');
    bar.style.cssText = 'display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap';
    ['all', ...cats].forEach((c, i) => {
      const b = document.createElement('button');
      b.textContent = c;
      b.style.cssText = 'font:600 9px/1 Archivo,sans-serif;letter-spacing:.14em;text-transform:uppercase;padding:7px 10px;border:1px solid rgba(250,243,233,.25);background:none;color:inherit;cursor:pointer';
      if (!i) { b.style.background = '#FAF3E9'; b.style.color = '#0B0705'; }
      b.addEventListener('click', () => {
        [...bar.children].forEach(x => { x.style.background = 'none'; x.style.color = ''; });
        b.style.background = '#FAF3E9'; b.style.color = '#0B0705';
        kids.forEach(k => { k.style.display = c === 'all' || k.dataset.cat === c ? '' : 'none'; });
      });
      bar.appendChild(b);
    });
    el.parentNode.insertBefore(bar, el);
    el.style.display = 'grid'; el.style.gridTemplateColumns = 'repeat(3,1fr)'; el.style.gap = '10px';
  } },
  { id: 'sticky-stack', name: 'Sticky stack', cat: 'Cards', apply: ({ el }) => {
    [...el.children].forEach((k, i) => {
      k.style.position = 'sticky'; k.style.top = `${80 + i * 18}px`;
      k.style.marginBottom = '10px';
    });
  } },
];

/* ==========================================================================
   REGISTRY
   ========================================================================== */
export const effects = [...reveal, ...hover, ...scroll, ...text, ...cursorFx, ...depth, ...atmosphere, ...micro, ...transitions, ...cards];

export const categories = ['Reveal', 'Hover', 'Scroll', 'Text', 'Cursor', 'Depth', 'Atmosphere', 'Micro', 'Transition', 'Cards'];

export const countByCategory = () =>
  categories.reduce((acc, c) => ({ ...acc, [c]: effects.filter(e => e.cat === c).length }), {});

export const getEffect = id => effects.find(e => e.id === id);

export function mountEffect(id, el, ctx = {}) {
  const fx = getEffect(id);
  if (!fx || !el) return null;
  if (fx.demo === false && !ctx.force) return null;
  if (reduced()) return null;
  return fx.apply({
    el,
    host: ctx.host || el,
    gsap: ctx.gsap || window.gsap,
    ScrollTrigger: ctx.ScrollTrigger || window.ScrollTrigger,
    st: ctx.st || ((o = {}) => ({ ...o, markers: false })),
    THREE: ctx.THREE || null,
  }) || null;
}

export default effects;
