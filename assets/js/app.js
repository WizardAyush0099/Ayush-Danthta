/* ==========================================================================
   WZ — interaction layer
   Loader, hero choreography, scroll reveals, pinned work gallery, filters,
   custom cursor, magnetic/tilt hovers, contact form and preference handling.
   Every feature degrades: no GSAP → visible content, no WebGL → CSS hero,
   reduced motion → static composition.
   ========================================================================== */
import { tilt, magnetize, reduced, clamp } from './effects.js';

const doc = document.documentElement;
const body = document.body;
const gsap = window.gsap;
const ScrollTrigger = window.ScrollTrigger;

const motionOff = doc.dataset.motion === 'off' || reduced();
const canAnimate = !!gsap && !motionOff;

if (gsap && ScrollTrigger) gsap.registerPlugin(ScrollTrigger);
body.classList.add('is-loading');

/* ==========================================================================
   LOADER
   ========================================================================== */
const loader = document.getElementById('loader');
const loaderNum = document.getElementById('loaderNum');
const loaderBar = document.getElementById('loaderBar');
const started = performance.now();
let loaderDone = false;
let progress = 0;
let progressRaf = 0;

function paintLoader() {
  if (!loaderNum) return;
  loaderNum.textContent = String(Math.round(progress));
  if (loaderBar) loaderBar.style.width = progress + '%';
}

function creep() {
  if (loaderDone) return;
  progress = Math.min(92, progress + (92 - progress) * 0.055);
  paintLoader();
  progressRaf = requestAnimationFrame(creep);
}
creep();

function hideLoader() {
  if (loaderDone) return;
  loaderDone = true;
  cancelAnimationFrame(progressRaf);
  progress = 100;
  paintLoader();
  body.classList.remove('is-loading');
  if (!loader) return heroIntro();

  if (!canAnimate) {
    loader.classList.add('is-done');
    loader.style.display = 'none';
    return heroIntro();
  }
  gsap.timeline({ onComplete: () => { loader.style.display = 'none'; } })
    .to(loaderNum, { textContent: 100, duration: 0.4, snap: { textContent: 1 }, ease: 'none' }, 0)
    .to(loaderBar, { width: '100%', duration: 0.45, ease: 'power2.inOut' }, 0)
    .to(loader, { duration: 0.1, delay: 0.15 })
    .add(() => loader.classList.add('is-done'))
    .add(heroIntro, '-=0.05')
    .to(loader, { autoAlpha: 0, duration: 0.5, delay: 0.35 });
}

function finishLoading() {
  const elapsed = performance.now() - started;
  const wait = Math.max(0, 900 - elapsed);
  setTimeout(hideLoader, wait);
}

const fontsReady = document.fonts ? document.fonts.ready : Promise.resolve();
Promise.race([
  Promise.all([fontsReady, new Promise(r => window.addEventListener('load', r, { once: true }))]),
  new Promise(r => setTimeout(r, 3200)),
]).then(finishLoading, finishLoading);

setTimeout(hideLoader, 6000); // last-resort failsafe

/* ==========================================================================
   HERO
   ========================================================================== */
const portrait = document.getElementById('portrait');
const portraitImg = document.getElementById('portraitImg');

/* switch to the real cut-out only once it actually loads */
if (portraitImg) {
  const usePhoto = () => doc.classList.add('has-photo');
  if (portraitImg.complete && portraitImg.naturalWidth > 0) usePhoto();
  else {
    portraitImg.addEventListener('load', usePhoto, { once: true });
    portraitImg.addEventListener('error', () => {
      doc.classList.remove('has-photo');
      portraitImg.remove();
      document.querySelectorAll('.about-media img').forEach(img => img.remove());
    }, { once: true });
  }
}

const hero = document.querySelector('.hero');

function heroIntro() {
  if (!canAnimate) return;
  const hasPhoto = doc.classList.contains('has-photo');
  if (portrait && hasPhoto) gsap.set(portrait, { xPercent: -50 });

  const tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
  tl.from('.nav', { yPercent: -110, duration: 1, ease: 'power3.out' }, 0)
    .from('[data-hero-line]', { yPercent: 118, duration: 1.2, stagger: 0.08 }, 0.05)
    .from(portrait, { autoAlpha: 0, y: hasPhoto ? 46 : 18, scale: hasPhoto ? 0.955 : 1, duration: 1.1 }, 0.15)
    .from('.hero-frame', { autoAlpha: 0, duration: 1.1 }, 0.35)
    .from('.hero-rail, .hero-meta > *', { autoAlpha: 0, y: 14, duration: 0.8, stagger: 0.05 }, 0.55)
    .from('.scroll-cue .bar', { scaleX: 0, transformOrigin: 'left', duration: 0.9 }, 0.75);

  if (ScrollTrigger) {
    gsap.to('.hero-type', {
      yPercent: 14, autoAlpha: 0.18, ease: 'none',
      scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true },
    });
    if (portrait && hasPhoto) {
      gsap.to(portrait, {
        yPercent: -7, scale: 1.02, ease: 'none',
        scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true },
      });
    }
    ScrollTrigger.refresh();
  }

  /* pointer parallax on the portrait — only when a real cut-out is present */
  if (portrait && hasPhoto && matchMedia('(hover:hover) and (pointer:fine)').matches) {
    const toX = gsap.quickTo(portrait, 'x', { duration: 0.9, ease: 'power3' });
    const toY = gsap.quickTo(portrait, 'y', { duration: 0.9, ease: 'power3' });
    const toR = gsap.quickTo(portrait, 'rotate', { duration: 1.1, ease: 'power3' });

    hero.addEventListener('pointermove', e => {
      const r = hero.getBoundingClientRect();
      const nx = (e.clientX - r.left) / r.width - 0.5;
      const ny = (e.clientY - r.top) / r.height - 0.5;
      toX(nx * 26);
      toY(ny * 18);
      toR(nx * 1.6);
    }, { passive: true });

    hero.addEventListener('pointerleave', () => {
      toX(0); toY(0); toR(0);
    });
  }
}

/* ==========================================================================
   NAV / MENU
   ========================================================================== */
const nav = document.getElementById('nav');
const menu = document.getElementById('menu');
const menuOpen = document.getElementById('menuOpen');
const menuClose = document.getElementById('menuClose');

let lastY = window.scrollY;
let navLocked = false;

window.addEventListener('scroll', () => {
  const y = window.scrollY;
  if (!nav || menu?.classList.contains('open')) return;
  if (y > lastY && y > 200) nav.classList.add('is-hidden');
  else nav.classList.remove('is-hidden');
  lastY = y;
}, { passive: true });

function setMenu(open) {
  if (!menu) return;
  menu.classList.toggle('open', open);
  menu.setAttribute('aria-hidden', String(!open));
  menuOpen?.setAttribute('aria-expanded', String(open));
  body.style.overflow = open ? 'hidden' : '';
  navLocked = open;
  if (open) menuClose?.focus({ preventScroll: true });
  else menuOpen?.focus({ preventScroll: true });
}

/* keep the navigation legible while the red contact field is behind it */
const contactSection = document.getElementById('contact');
if (contactSection && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => nav?.classList.toggle('is-dark', entry.isIntersecting));
  }, { rootMargin: '-10% 0px -60% 0px' });
  io.observe(contactSection);
}

menuOpen?.addEventListener('click', () => setMenu(true));
menuClose?.addEventListener('click', () => setMenu(false));
menu?.addEventListener('click', e => {
  if (e.target.closest('a')) setMenu(false);
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && menu?.classList.contains('open')) setMenu(false);
});

/* ==========================================================================
   CURSOR
   ========================================================================== */
const cursor = document.getElementById('cursor');
const cursorDot = document.getElementById('cursorDot');
const cursorRing = document.getElementById('cursorRing');
const cursorLabel = document.getElementById('cursorLabel');

if (cursor && matchMedia('(hover:hover) and (pointer:fine)').matches && !reduced()) {
  doc.classList.add('has-cursor');

  if (canAnimate) {
    const dotX = gsap.quickTo(cursorDot, 'x', { duration: 0.12, ease: 'power2' });
    const dotY = gsap.quickTo(cursorDot, 'y', { duration: 0.12, ease: 'power2' });
    const ringX = gsap.quickTo(cursorRing, 'x', { duration: 0.55, ease: 'power3' });
    const ringY = gsap.quickTo(cursorRing, 'y', { duration: 0.55, ease: 'power3' });

    window.addEventListener('pointermove', e => {
      dotX(e.clientX); dotY(e.clientY);
      ringX(e.clientX); ringY(e.clientY);
    }, { passive: true });

    window.addEventListener('pointerdown', () => cursor.classList.add('is-down'));
    window.addEventListener('pointerup', () => cursor.classList.remove('is-down'));

    const labels = () => document.querySelectorAll('[data-cursor-label]');
    labels().forEach(el => {
      el.addEventListener('pointerenter', () => {
        cursor.classList.add('is-link');
        if (cursorLabel) cursorLabel.textContent = el.dataset.cursorLabel || 'View';
      });
      el.addEventListener('pointerleave', () => {
        cursor.classList.remove('is-link');
        if (cursorLabel) cursorLabel.textContent = '';
      });
    });
  }
}

/* ==========================================================================
   SCROLL PROGRESS
   ========================================================================== */
const progressEl = document.getElementById('progress');
if (progressEl) {
  if (canAnimate && ScrollTrigger) {
    gsap.to(progressEl, {
      scaleX: 1, ease: 'none',
      scrollTrigger: { start: 0, end: 'max', scrub: 0.2 },
    });
  } else {
    progressEl.style.display = 'none';
  }
}

/* ==========================================================================
   REVEALS
   ========================================================================== */
if (canAnimate && ScrollTrigger) {
  ScrollTrigger.batch('[data-reveal]', {
    start: 'top 90%',
    once: true,
    onEnter: batch => gsap.to(batch, {
      opacity: 1, y: 0, duration: 0.95, stagger: 0.06, ease: 'power3.out', overwrite: true,
    }),
  });

  /* headlines start visible in CSS; only hide them once we know we can animate */
  gsap.utils.toArray('.split').forEach(el => {
    const lines = el.querySelectorAll('.line > span');
    if (!lines.length) return;
    gsap.set(lines, { yPercent: 110 });
    const play = () => gsap.to(lines, { yPercent: 0, duration: 1.1, stagger: 0.08, ease: 'expo.out', overwrite: true });
    if (!('IntersectionObserver' in window)) { play(); return; }
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { play(); io.disconnect(); }
      });
    }, { threshold: 0.15 });
    io.observe(el);
  });

  gsap.utils.toArray('.sec-title').forEach(el => {
    gsap.from(el, {
      y: 26, autoAlpha: 0, duration: 1, ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 92%', once: true },
    });
  });
} else {
  document.querySelectorAll('[data-reveal]').forEach(el => {
    el.style.opacity = '1';
    el.style.transform = 'none';
  });
}

/* ==========================================================================
   COUNTERS
   ========================================================================== */
document.querySelectorAll('[data-count]').forEach(el => {
  const target = Number(el.dataset.count) || 0;
  const pad = Number(el.dataset.pad) || 0;
  const render = v => { el.textContent = pad ? String(v).padStart(pad, '0') : String(v); };
  if (!canAnimate || !ScrollTrigger) { render(target); return; }

  const obj = { v: 0 };
  render(0);
  gsap.to(obj, {
    v: target, duration: 1.5, ease: 'power2.out',
    scrollTrigger: { trigger: el, start: 'top 92%', once: true },
    onUpdate: () => render(Math.round(obj.v)),
  });
});

/* ==========================================================================
   HORIZONTAL WORK GALLERY
   ========================================================================== */
if (canAnimate && ScrollTrigger) {
  const mm = gsap.matchMedia();
  mm.add('(min-width: 861px)', () => {
    const wrap = document.getElementById('workWrap');
    const track = document.getElementById('workTrack');
    if (!wrap || !track) return;

    const distance = () => Math.max(0, track.scrollWidth - document.documentElement.clientWidth);
    if (distance() < 40) return;

    const tween = gsap.to(track, {
      x: () => -distance(),
      ease: 'none',
      scrollTrigger: {
        trigger: wrap,
        start: 'top top',
        end: () => '+=' + Math.max(320, distance()),
        pin: true,
        scrub: 1,
        anticipatePin: 1,
        invalidateOnRefresh: true,
      },
    });

    return () => {
      tween.scrollTrigger?.kill();
      tween.kill();
      gsap.set(track, { clearProps: 'x' });
    };
  });
}

/* ==========================================================================
   HOVER: MAGNETIC + TILT
   ========================================================================== */
if (!reduced() && matchMedia('(hover:hover) and (pointer:fine)').matches) {
  document.querySelectorAll('.magnet').forEach(el => magnetize(el, 0.18, 10));
  document.querySelectorAll('[data-tilt]').forEach(el => tilt(el, 6));
}

/* ==========================================================================
   TEMPLATE FILTERS
   ========================================================================== */
const filterBar = document.querySelector('.filters');
if (filterBar) {
  const buttons = [...filterBar.querySelectorAll('.filter')];
  const cards = [...document.querySelectorAll('.tpl')];
  const count = document.querySelector('[data-tpl-count]');

  const apply = f => {
    let shown = 0;
    cards.forEach(card => {
      const match = f === 'all' || card.dataset.cat === f;
      card.hidden = !match;
      if (match) shown++;
    });
    if (count) count.textContent = `${String(shown).padStart(2, '0')} direction${shown === 1 ? '' : 's'}`;
    if (canAnimate) {
      const visible = cards.filter(c => !c.hidden);
      gsap.fromTo(visible, { opacity: 0, y: 12 }, {
        opacity: 1, y: 0, duration: 0.5, stagger: 0.04, ease: 'power2.out', overwrite: true, clearProps: 'transform',
      });
    }
    if (ScrollTrigger) ScrollTrigger.refresh();
  };

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b === btn)));
      apply(btn.dataset.filter || 'all');
    });
  });
}

/* ==========================================================================
   CONTACT FORM
   ========================================================================== */
const form = document.getElementById('projectForm');
const formCard = document.getElementById('formCard');
const formStatus = document.getElementById('formStatus');
const successMail = document.getElementById('successMail');
const successWa = document.getElementById('successWa');

if (form) {
  const EMAIL = 'ayushdanthta@gmail.com';
  const WA = '918353011030';
  const setError = (name, message) => {
    const slot = form.querySelector(`[data-err="${name}"]`);
    if (slot) slot.textContent = message || '';
    const input = form.elements[name];
    if (input) input.setAttribute('aria-invalid', message ? 'true' : 'false');
  };

  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (!formCard) return;
    const data = Object.fromEntries(new FormData(form).entries());
    const errors = {};

    if (!data.name || data.name.trim().length < 2) errors.name = 'Please add your name';
    if (!data.email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email.trim())) errors.email = 'A valid email, please';
    if (!data.message || data.message.trim().length < 10) errors.message = 'A sentence or two is enough';

    ['name', 'email', 'message'].forEach(k => setError(k, errors[k]));
    if (Object.keys(errors).length) {
      if (formStatus) { formStatus.classList.remove('ok'); formStatus.textContent = 'Check the highlighted fields.'; }
      form.elements[Object.keys(errors)[0]]?.focus();
      return;
    }

    if (formStatus) { formStatus.classList.remove('ok'); formStatus.textContent = 'Preparing your brief…'; }

    const summary = [
      `Name: ${data.name}`,
      `Email: ${data.email}`,
      `Project: ${data.type || '—'}`,
      `Timeline: ${data.when || '—'}`,
      '',
      data.message,
    ].join('\n');

    const endpoint = form.dataset.endpoint?.trim();

    if (endpoint) {
      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error('Request failed: ' + res.status);
        if (successMail) successMail.href = `mailto:${EMAIL}`;
        if (successWa) successWa.href = `https://wa.me/${WA}?text=${encodeURIComponent(summary)}`;
        formCard.classList.add('is-sent');
        if (formStatus) formStatus.textContent = '';
        return;
      } catch (err) {
        if (formStatus) {
          formStatus.classList.remove('ok');
          formStatus.textContent = 'That endpoint did not answer. Sending by email instead.';
        }
      }
    }

    const mailto = `mailto:${EMAIL}?subject=${encodeURIComponent('Project enquiry — ' + data.name)}&body=${encodeURIComponent(summary)}`;
    const wa = `https://wa.me/${WA}?text=${encodeURIComponent(summary)}`;

    if (successMail) successMail.href = mailto;
    if (successWa) successWa.href = wa;
    formCard.classList.add('is-sent');
    if (formStatus) formStatus.textContent = '';
    setTimeout(() => { window.location.href = mailto; }, 80);
  });

  form.addEventListener('input', e => {
    const name = e.target.name;
    if (name) setError(name, '');
  });
}

/* ==========================================================================
   CLOCK / MOTION PREFERENCE
   ========================================================================== */
const clock = document.getElementById('clock');
function paintClock() {
  if (!clock) return;
  const now = new Date().toLocaleTimeString('en-GB', {
    timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', hour12: false,
  });
  clock.textContent = now;
}
paintClock();
setInterval(paintClock, 30000);

const motionToggle = document.getElementById('motionToggle');
if (motionToggle) {
  const stored = localStorage.getItem('wz-motion');
  if (stored === 'off') {
    doc.dataset.motion = 'off';
    motionToggle.setAttribute('aria-pressed', 'false');
    motionToggle.textContent = 'Off';
  }

  motionToggle.addEventListener('click', () => {
    const off = doc.dataset.motion !== 'off';
    doc.dataset.motion = off ? 'off' : 'on';
    localStorage.setItem('wz-motion', off ? 'off' : 'on');
    motionToggle.setAttribute('aria-pressed', String(!off));
    motionToggle.textContent = off ? 'Off' : 'On';

    if (off) {
      ScrollTrigger?.getAll().forEach(t => t.kill());
      gsap?.globalTimeline.pause();
      document.querySelectorAll('[data-reveal]').forEach(el => {
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
      document.querySelectorAll('.split .line > span').forEach(el => { el.style.transform = 'none'; });
      document.getElementById('workTrack')?.style.setProperty('transform', 'none');
      doc.classList.remove('has-cursor');
    } else {
      location.reload();
    }
  });
}

/* re-measure once webfonts settle */
window.addEventListener('load', () => ScrollTrigger?.refresh());
if (document.fonts) document.fonts.ready.then(() => ScrollTrigger?.refresh());

/* expose for debugging / the effects page */
window.WZ = { gsap, ScrollTrigger, effectsCount: 112, motionOff, clamp };
