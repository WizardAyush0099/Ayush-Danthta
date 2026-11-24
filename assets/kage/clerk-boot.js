/* One place that knows how to load Clerk, who the admin is, and how to get a
   fresh session token. Nothing is fetched until the account control is used —
   the mountain should paint before any third party does.

   Since Clerk Core 3 the prebuilt UI is a separate package (@clerk/ui) that
   must be loaded and handed to load(); an instance created after Nov 2026 also
   refuses any ClerkJS older than 6.40, which is why the old @5 CDN build
   answered "This app uses an outdated version of Clerk". Both packages are
   served from the instance's own frontend API host, derived from the
   publishable key exactly as Clerk's own loader does, and both use a major
   range (@6 / @1) so the instance always gets a version it accepts. */
(function () {
  var ADMIN_EMAIL = 'ayushdanthta@gmail.com';
  var JS_PKG = '@clerk/clerk-js@6';
  var UI_PKG = '@clerk/ui@1';
  var KEY = window.CLERK_PUBLISHABLE_KEY || '';
  var pending = null;

  /* the modal is the only Clerk surface the visitor sees, so it inherits the
     page's ink, bone and vermilion rather than arriving as a white card */
  var APPEARANCE = {
    /* Core 3 renamed the text/input tokens (colorText → colorForeground,
       colorTextSecondary → colorMutedForeground, colorInputBackground →
       colorInput, colorInputText → colorInputForeground). With the old names
       the card stayed dark but every label fell back to Clerk's near-black
       default, which is what made the modal look washed out. */
    variables: {
      colorPrimary: '#e0231c',
      colorPrimaryForeground: '#ffffff',
      colorBackground: '#0a0f12',
      colorForeground: '#dfe7e0',
      colorMutedForeground: '#9aa7a1',
      colorInput: '#0d1418',
      colorInputForeground: '#dfe7e0',
      colorNeutral: '#dfe7e0',
      colorBorder: 'rgba(223,231,224,.18)',
      colorRing: '#e9b48a',
      /* Core 3 renders this one at full opacity, so give it a solid ink */
      colorModalBackdrop: '#05080b',
      fontFamily: "'Onest', system-ui, -apple-system, sans-serif",
      borderRadius: '2px'
    },
    elements: {
      card: { border: '1px solid rgba(223,231,224,.16)', boxShadow: '0 30px 90px rgba(0,0,0,.65)' },
      headerTitle: { letterSpacing: '.02em' },
      formButtonPrimary: {
        background: '#e0231c',
        boxShadow: 'none',
        textTransform: 'none',
        letterSpacing: '.06em'
      },
      footerActionLink: { color: '#e9b48a' },
      modalBackdrop: { background: 'rgba(3,6,8,.82)', backdropFilter: 'blur(6px)' }
    }
  };

  /* pk_test_<base64 of "host$"> — the same decode Clerk's SDK uses, so a
     development instance and a custom frontend API domain both work */
  function frontendHost() {
    var parts = String(KEY).split('_');
    if (parts.length < 3) return '';
    try {
      var raw = atob(parts[2]);
      return raw.charAt(raw.length - 1) === '$' ? raw.slice(0, -1) : raw;
    } catch (e) {
      return '';
    }
  }

  function inject(src, attrs) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.async = true;
      s.crossOrigin = 'anonymous';
      Object.keys(attrs || {}).forEach(function (k) { s.setAttribute(k, attrs[k]); });
      s.src = src;
      s.onload = function () { resolve(); };
      s.onerror = function () { reject(new Error('Could not load ' + src)); };
      document.head.appendChild(s);
    });
  }

  function loadClerk() {
    if (!KEY) return Promise.reject(new Error('Add assets/kage/clerk-key.js first.'));
    if (window.Clerk && window.Clerk.loaded) return Promise.resolve(window.Clerk);
    if (pending) return pending;

    var base = frontendHost();
    if (!base) return Promise.reject(new Error('The publishable key could not be read.'));

    pending = inject('https://' + base + '/npm/' + UI_PKG + '/dist/ui.browser.js')
      .then(function () {
        if (window.Clerk) return;
        return inject('https://' + base + '/npm/' + JS_PKG + '/dist/clerk.browser.js', {
          'data-clerk-publishable-key': KEY
        });
      })
      .then(function () {
        if (!window.Clerk || typeof window.Clerk.load !== 'function') {
          throw new Error('Clerk did not initialise');
        }
        var ui = window.__internal_ClerkUICtor;
        return window.Clerk.load(ui
          ? { appearance: APPEARANCE, ui: { ClerkUI: ui } }
          : { appearance: APPEARANCE });
      })
      .then(function () { return window.Clerk; })
      .catch(function (err) { pending = null; throw err; });
    return pending;
  }

  function isAdmin(user) {
    if (!user || !user.emailAddresses) return false;
    return user.emailAddresses.some(function (e) {
      var verified = e.verification && e.verification.status === 'verified';
      return verified && String(e.emailAddress || '').toLowerCase() === ADMIN_EMAIL;
    });
  }

  async function token() {
    var clerk = await loadClerk();
    return clerk.session ? clerk.session.getToken() : null;
  }

  function displayName(user) {
    if (!user) return '';
    var n = [user.firstName, user.lastName].filter(Boolean).join(' ');
    if (n) return n.split(' ')[0];
    if (user.username) return user.username;
    var p = user.primaryEmailAddress && user.primaryEmailAddress.emailAddress;
    return p ? p.split('@')[0] : 'Account';
  }

  window.HimachalAuth = {
    ADMIN_EMAIL: ADMIN_EMAIL,
    appearance: APPEARANCE,
    loadClerk: loadClerk,
    isAdmin: isAdmin,
    token: token,
    displayName: displayName
  };
})();
