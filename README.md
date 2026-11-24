# Ayush Danthta — a Himalayan 3D portfolio

One continuous climb through Himachal Pradesh, rendered live in WebGL: a deodar
forest, a slate-roofed Bhimakali tower above the valley, the ridge behind Shimla.
Five chapters, keyed to scroll, built on the ThreeUI *Kage* engine and re-themed
from Kyoto to Sarahan.

The page is a single static `index.html` with no build step and no runtime
framework. Clerk adds the account layer on top, and one serverless function
serves the private admin register.

## Run it

```bash
python3 -m http.server 3000        # from the repository root
# http://localhost:3000
```

Any static server works. Debug query parameters:

| Parameter | Effect |
|---|---|
| `?shot=0…5` | Jump to a deterministic chapter (0 ridge, 1 atmosphere, 2 temple, 3 forest, 4 arrival, 5 footer) |
| `?q=low` | Half the trees, sprays, leaves and particles; no MSAA |
| `?dpr=1.4` | Cap device pixel ratio |
| `?post=0` | Skip bloom and the composite pass |

## How the page is built

`index.html` is **generated**. `tools/theme_kage.py` rewrites the canonical
engine in `vendor/kage/kage.html` — geometry, copy, textures, palette, the
Himachali temple, the deodar forest and the portrait section. Every edit asserts
that it matched exactly once, so a change upstream fails loudly instead of
silently drifting.

```bash
python3 tools/theme_kage.py       # rebuild index.html
```

Do not hand-edit `index.html`: the next run overwrites it. Change
`tools/theme_kage.py` instead.

```
vendor/kage/kage.html      canonical ThreeUI engine (reference copy)
tools/theme_kage.py        every Himachal edit, in order
tools/make_fg.py           foreground cut-outs (ridge, grass) from the photos
tools/make_grove.py        the deodar treeline band
tools/prepare_portrait.py  studio photo → clean cut-out
tools/*.py                 Python 3 + Pillow + numpy
```

Assets live under `assets/`. The supplied field photographs are in
`assets/img/hp/`; the 3D textures and foreground cut-outs are in
`assets/kage/`.

## The portrait

`assets/img/portrait-source.png` is the original studio frame. Run:

```bash
python3 tools/prepare_portrait.py
```

It floods the white field from the border, drops the two-pixel halo that a plain
binary mask leaves around the hair, rebuilds that rim from pixel darkness,
un-composites white from the soft edge, trims, and writes:

```
assets/img/portrait-cutout.webp       up to 1400px tall
assets/img/portrait-cutout@800.webp   800px tall
```

Options: `--tolerance 26`, `--erode 3`, `--feather 0.9`, `--height 1400`.
On the page the print is stacked with a second, brighter copy revealed through a
mask that follows the pointer, plus a small counter-rotation — the cursor
behaves like a lantern crossing the photograph.

## Accounts and the admin register

The nav carries Clerk's account control (`Sign in`, then the avatar). It is
loaded lazily from the instance's own frontend API host by
`assets/kage/clerk-boot.js` after the scene has started, so nothing third-party
delays the first paint.

The loader asks for ClerkJS `@6` plus the Core 3 UI bundle (`@clerk/ui@1`) and
hands the UI to `Clerk.load()`. That is not cosmetic: instances created after
November 2026 refuse ClerkJS older than 6.40 and answer "This app uses an
outdated version of Clerk", and since Core 3 the prebuilt UI is a separate
package that `openSignIn()` needs.

- `assets/kage/clerk-key.js` holds the **publishable** key. That key is public by
  design (the same value as `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`).
- The **secret** key never enters this repository. Set it in Vercel:

  | Variable | Where | Value |
  |---|---|---|
  | `CLERK_SECRET_KEY` | Vercel → Settings → Environment Variables → Production (and Preview) | Clerk secret key for the project |

`admin.html` at `/admin.html` is the register. It is inert until someone signs
in; `api/admin.mjs` then:

1. verifies the Clerk session token against the instance JWKS (RS256, `exp`,
   `nbf`, `iss`, `azp`),
2. loads that user and requires a **verified** `ayushdanthta@gmail.com`,
3. returns a trimmed list of accounts and four counters, `no-store`.

Anyone else gets `403`. If `CLERK_SECRET_KEY` is missing the endpoint answers
`503` with the fix, and the page prints it rather than failing silently.

To change who may open the register, edit `ADMIN_EMAIL` in `api/admin.mjs` and
`assets/kage/clerk-boot.js` together. To hide the admin link but keep the page,
remove the `href` — but the API check is the real gate, not the link.

The site deploys as a static project with one Vercel Node function: no build
command, no framework preset required. On a files-only host such as GitHub Pages
the portfolio and sign-in work, but `api/admin` does not exist, so the register
says so and stays empty. Open the Vercel deployment for the register, or point
the page at one with `window.CLERK_ADMIN_API = 'https://your-app.vercel.app/api/admin'`
loaded before `admin.html`'s module script.

## Checks used

- `python3 tools/theme_kage.py` regenerates cleanly and every substitution
  asserts.
- The inline page script, `assets/kage/*.js`, `api/admin.mjs` and the admin
  script pass `node --check`.
- The page boots with no console or page errors in a WebGL2 browser; the
  portrait, forest, temple joinery, Clerk sign-in dialog and admin gate were
  exercised on the preview host.
- The admin endpoint was smoke-tested for its `503` (no secret) and `401`
  (bad token) paths; a full signed-in read needs the deployed secret key.

## Known limits

- The development Clerk instance shows a "Development mode" ribbon until the
  application is claimed and moved to a production instance.
- Bloom and the high-quality path need a GPU; the preview used the low-quality
  software path, so the high-quality post stack is verified by code only.
- `Hp Img/` holds the original photographs and is not used by the page at
  runtime.
