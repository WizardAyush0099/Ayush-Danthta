WZ STUDIO — IMAGE ASSETS
========================

The site is one generated page (index.html) with its scene, shaders and CSS
inline. There is no assets/js or assets/css runtime in the shipped page; the
3-D engine is assets/kage/three.min.js.

PORTRAIT
--------
    assets/img/portrait-source.png   original studio photograph (white paper)
    assets/img/portrait-cutout.webp      up to 1400px tall
    assets/img/portrait-cutout@800.webp  800px tall

Regenerate both cut-outs with:

    python3 tools/prepare_portrait.py

It floods the white field from the border (so white clothing and highlights
inside the subject survive), removes the white halo the flood fill leaves around
hair, un-composites white from the soft edge, trims to the subject and writes
both sizes. Options: --tolerance 26, --erode 3, --feather 0.9, --height 1400.
Requires Pillow and numpy.

The page uses a srcset of both files; keep their dimensions in step with the
width/height attributes in tools/theme_kage.py if you replace them.

FOREGROUND CUT-OUTS
-------------------
    assets/kage/fg/hill.webp           slate ridge, drawn from assets/img/hp/ridge.webp
    assets/kage/fg/tall-grass.webp     Himalayan grass and bracken
    assets/kage/fg/deodar-tree.webp    one mature deodar
    assets/kage/fg/deodar-spray.webp   the 3-D spray texture
    assets/kage/fg/deodar-grove.webp   the forest band
    assets/kage/fg/hp-slate-stones.webp

Regenerate the first two with:

    python3 tools/make_fg.py

Keep the filenames and pixel sizes: the HTML width/height attributes and the
aspect boxes are built around them.

FIELD PHOTOGRAPHS
-----------------
    assets/img/hp/temple.webp   Bhimakali temple, Sarahan
    assets/img/hp/ridge.webp    the snow line
    assets/img/hp/forest.webp   deodar forest, Manali
    assets/img/hp/fir.webp      deodar forest, Manali
    assets/img/hp/canopy.webp   deodar crown

Originals live in Hp Img/. The planted woodland in the scene is built from
assets/kage/fg/deodar-spray.webp, not from these photographs.

VENDOR
------
assets/kage/three.min.js   Three.js r1xx build used by the engine (MIT)
assets/kage/fonts.css      Onest and the display face

The scene has no third-party runtime dependency. Clerk's browser SDK is fetched
from its CDN only when the account control is used (see assets/kage/clerk-boot.js).

Reduced motion is respected: the scroll reveal, the portrait lantern tilt and
the particle systems stand down, and every chapter stays readable.
