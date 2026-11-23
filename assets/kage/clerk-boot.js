/* One place that knows how to load Clerk, who the admin is, and how to get a
   fresh session token. The SDK is fetched from Clerk's CDN only when it is
   actually needed — the mountain should paint before any third party does. */
(function () {
  var ADMIN_EMAIL = 'ayushdanthta@gmail.com';
  var SDK = 'https://cdn.jsdelivr.net/npm/@clerk/clerk-js@5/dist/clerk.browser.js';
  var KEY = window.CLERK_PUBLISHABLE_KEY || '';
  var pending = null;

  /* the modal is the only Clerk surface the visitor sees, so it inherits the
     page's ink, bone and vermilion rather than arriving as a white card */
  var APPEARANCE = {
    variables: {
      colorPrimary: '#e0231c',
      colorBackground: '#0a0f12',
      colorText: '#dfe7e0',
      colorTextSecondary: '#9aa7a1',
      colorInputBackground: '#0d1418',
      colorInputText: '#dfe7e0',
      colorNeutral: '#dfe7e0',
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

  function loadScript() {
    return new Promise(function (resolve, reject) {
      if (window.Clerk) return resolve();
      var s = document.createElement('script');
      s.src = SDK;
      s.async = true;
      s.crossOrigin = 'anonymous';
      s.dataset.clerkPublishableKey = KEY;
      s.onload = function () { resolve(); };
      s.onerror = function () { reject(new Error('Clerk SDK failed to load')); };
      document.head.appendChild(s);
    });
  }

  function loadClerk() {
    if (!KEY) return Promise.reject(new Error('Add assets/kage/clerk-key.js first.'));
    if (window.Clerk && window.Clerk.loaded) return Promise.resolve(window.Clerk);
    if (!pending) {
      pending = loadScript()
        .then(function () { return window.Clerk.load({ appearance: APPEARANCE }); })
        .then(function () { return window.Clerk; })
        .catch(function (err) { pending = null; throw err; });
    }
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
