/* The nav's account control. Signed out it offers one quiet "Sign in"; signed
   in it becomes the avatar, and the Admin link appears only for Ayush's own
   verified address. Nothing here blocks the first paint: the SDK is warmed
   when the browser is idle, and immediately if someone asks for it. */
(function () {
  var A = window.HimachalAuth;
  if (!A) return;

  var signIn = document.getElementById('clerkSignIn');
  var userBtn = document.getElementById('clerkUser');
  var avatar = document.getElementById('clerkAvatar');
  var name = document.getElementById('clerkName');
  var admin = document.getElementById('clerkAdmin');
  if (!signIn || !userBtn) return;

  var clerk = null;

  function render(user) {
    var signedIn = !!user;
    signIn.hidden = signedIn;
    userBtn.hidden = !signedIn;
    if (admin) admin.hidden = !A.isAdmin(user);
    if (signedIn) {
      var url = user.imageUrl || user.profileImageUrl || '';
      if (url) {
        avatar.src = url;
        avatar.alt = '';
      }
      name.textContent = A.displayName(user);
      userBtn.setAttribute('aria-label', 'Account — ' + name.textContent);
    }
  }

  function wire(c) {
    clerk = c;
    render(c.user);
    c.addListener(function (state) { render(state.user); });
  }

  function boot() {
    if (clerk) return Promise.resolve(clerk);
    return A.loadClerk().then(wire).catch(function () {
      /* Clerk unreachable (offline, blocked, or a key mismatch): leave the
         page exactly as it was rather than showing a dead button. */
      signIn.hidden = true;
    });
  }

  signIn.addEventListener('click', function () {
    signIn.disabled = true;
    A.loadClerk()
      .then(function (c) {
        wire(c);
        c.openSignIn({ appearance: A.appearance });
      })
      .catch(function () {
        signIn.textContent = 'Sign-in unavailable';
      })
      .finally(function () { signIn.disabled = false; });
  });

  userBtn.addEventListener('click', function () {
    if (!clerk) return boot().then(function () {
      if (clerk) clerk.openUserProfile({ appearance: A.appearance });
    });
    clerk.openUserProfile({ appearance: A.appearance });
  });

  // Keep the signed-in state honest on other tabs.
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden && clerk) render(clerk.user);
  });

  // Warm the SDK after the scene has had a chance to build.
  var idle = window.requestIdleCallback || function (fn) { return setTimeout(fn, 2600); };
  idle(function () { boot(); });
})();
