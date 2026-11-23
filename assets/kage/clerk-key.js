/* Clerk's publishable key. It is public by design — the same value the
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY environment variable carries — and Clerk
   requires the browser to hold it before it will render the sign-in form.
   The secret key is never part of this site: it lives only in the Vercel
   environment as CLERK_SECRET_KEY, where api/admin.mjs reads it. */
window.CLERK_PUBLISHABLE_KEY = 'pk_test_dGVuZGVyLWFtb2ViYS02ODcwLmNsZXJrLmFjY291bnRzLmRldiQ';
