/* /api/admin — the only server-side piece of the portfolio.
 *
 * It does two things and nothing else:
 *   1. verifies the Clerk session token the browser sends in the
 *      Authorization header, against the instance's published JWKS;
 *   2. if that user's verified address is Ayush's, asks Clerk's Backend API
 *      for the account list and returns a trimmed, read-only summary.
 *
 * No dependencies: Node's crypto verifies the RS256 signature and fetch talks
 * to Clerk. The secret key stays in the Vercel environment.
 */
import crypto from 'node:crypto';

const ADMIN_EMAIL = 'ayushdanthta@gmail.com';
/* Public key, duplicated from assets/kage/clerk-key.js so this function is
   self-contained. It only identifies the Frontend API / issuer. */
const PUBLISHABLE_KEY =
  process.env.CLERK_PUBLISHABLE_KEY ||
  process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ||
  'pk_test_dGVuZGVyLWFtb2ViYS02ODcwLmNsZXJrLmFjY291bnRzLmRldiQ';

const SECRET_KEY = process.env.CLERK_SECRET_KEY || '';
const API = 'https://api.clerk.com/v1';

function frontendApi() {
  const raw = PUBLISHABLE_KEY.replace(/^pk_(test|live)_/, '');
  const decoded = Buffer.from(raw, 'base64').toString('utf8').replace(/\$$/, '');
  return decoded.startsWith('http') ? decoded : `https://${decoded}`;
}

function send(res, status, body) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store, max-age=0');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.end(JSON.stringify(body));
}

function bearer(req) {
  const h = req.headers.authorization || req.headers.Authorization || '';
  const m = /^Bearer\s+(.+)$/i.exec(String(h));
  return m ? m[1].trim() : '';
}

function b64urlJson(part) {
  return JSON.parse(Buffer.from(part, 'base64url').toString('utf8'));
}

/* Clerk publishes the signing keys at the Frontend API's well-known JWKS.
   Cached per lambda instance: the set rotates rarely and every admin request
   would otherwise pay for it. */
let jwksCache = { at: 0, keys: [] };

async function signingKey(kid) {
  const now = Date.now();
  if (!jwksCache.keys.length || now - jwksCache.at > 10 * 60 * 1000) {
    const res = await fetch(`${frontendApi()}/.well-known/jwks.json`, {
      headers: { Accept: 'application/json' }
    });
    if (!res.ok) throw new Error(`jwks ${res.status}`);
    const body = await res.json();
    jwksCache = { at: now, keys: Array.isArray(body.keys) ? body.keys : [] };
  }
  return jwksCache.keys.find((k) => k.kid === kid) || jwksCache.keys[0] || null;
}

function hostOf(value) {
  if (!value) return '';
  try {
    return new URL(value.includes('://') ? value : `https://${value}`).hostname.toLowerCase();
  } catch {
    return String(value).toLowerCase();
  }
}

async function verifySession(token, req) {
  const parts = String(token).split('.');
  if (parts.length !== 3) throw new Error('malformed token');
  const header = b64urlJson(parts[0]);
  const payload = b64urlJson(parts[1]);
  if (header.alg !== 'RS256') throw new Error('unexpected algorithm');

  const jwk = await signingKey(header.kid);
  if (!jwk) throw new Error('no signing key');

  const key = crypto.createPublicKey({ key: jwk, format: 'jwk' });
  const ok = crypto.verify(
    'RSA-SHA256',
    Buffer.from(`${parts[0]}.${parts[1]}`),
    key,
    Buffer.from(parts[2], 'base64url')
  );
  if (!ok) throw new Error('bad signature');

  const now = Math.floor(Date.now() / 1000);
  if (typeof payload.exp === 'number' && payload.exp < now - 5) throw new Error('expired');
  if (typeof payload.nbf === 'number' && payload.nbf > now + 5) throw new Error('not yet valid');
  if (payload.iss && hostOf(payload.iss) !== hostOf(frontendApi())) throw new Error('wrong issuer');

  /* azp pins the token to the origin that requested it. Clerk omits it for
     empty origins, so only reject a claim we can read and that is foreign. */
  if (payload.azp) {
    const allowed = new Set([hostOf(req.headers['x-forwarded-host'] || req.headers.host), 'localhost', '127.0.0.1']);
    if (!allowed.has(hostOf(payload.azp))) throw new Error('foreign origin');
  }
  return payload;
}

async function clerkGet(path) {
  const res = await fetch(`${API}${path}`, {
    headers: {
      Authorization: `Bearer ${SECRET_KEY}`,
      Accept: 'application/json'
    }
  });
  if (!res.ok) throw new Error(`clerk ${res.status}`);
  return res.json();
}

function primaryEmail(user) {
  const list = user.email_addresses || [];
  const primary = list.find((e) => e.id === user.primary_email_address_id) || list[0];
  return primary ? primary.email_address : '';
}

function trimUser(user) {
  const list = user.email_addresses || [];
  const verified = list.some((e) => e.verification && e.verification.status === 'verified');
  return {
    id: user.id,
    name: [user.first_name, user.last_name].filter(Boolean).join(' ') || user.username || '',
    email: primaryEmail(user),
    avatar: user.image_url || '',
    created: user.created_at || null,
    lastSeen: user.last_sign_in_at || null,
    verified,
    twoFactor: !!user.two_factor_enabled,
    banned: !!user.banned
  };
}

export default async function handler(req, res) {
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return send(res, 405, { error: 'method_not_allowed' });
  }
  if (!SECRET_KEY) {
    return send(res, 503, {
      error: 'not_configured',
      message: 'Add CLERK_SECRET_KEY to this project in Vercel (Settings → Environment Variables) and redeploy.'
    });
  }

  let claims;
  try {
    claims = await verifySession(bearer(req), req);
  } catch {
    return send(res, 401, { error: 'unauthorized' });
  }

  try {
    const me = await clerkGet(`/users/${encodeURIComponent(claims.sub)}`);
    const emails = (me.email_addresses || []).filter(
      (e) => String(e.email_address).toLowerCase() === ADMIN_EMAIL
    );
    const allowed = emails.some((e) => e.verification && e.verification.status === 'verified');
    if (!allowed) return send(res, 403, { error: 'forbidden' });
  } catch {
    return send(res, 502, { error: 'clerk_unreachable' });
  }

  try {
    const [list, count, active] = await Promise.all([
      clerkGet('/users?limit=100&order_by=-created_at&offset=0'),
      clerkGet('/users/count'),
      clerkGet('/sessions?status=active&limit=1')
    ]);

    const users = (Array.isArray(list) ? list : []).map(trimUser).sort((a, b) => (b.created || 0) - (a.created || 0));
    const week = Math.floor(Date.now() / 1000) - 7 * 24 * 60 * 60;
    const total = typeof count.total_count === 'number' ? count.total_count : users.length;
    const activeCount =
      typeof active.total_count === 'number' ? active.total_count : Array.isArray(active) ? active.length : 0;

    return send(res, 200, {
      admin: { email: ADMIN_EMAIL },
      stats: {
        total,
        newThisWeek: users.filter((u) => (u.created || 0) >= week).length,
        active: activeCount,
        verified: users.filter((u) => u.verified).length
      },
      users,
      fetchedAt: new Date().toISOString()
    });
  } catch {
    return send(res, 502, { error: 'clerk_unreachable' });
  }
}
