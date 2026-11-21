WZ STUDIO — IMAGE ASSETS
========================

PORTRAIT
--------
The hero and the about section are built for a cut-out portrait of Ayush.

1. Save the original photograph (white background) as:

       assets/img/portrait-source.png

2. Run the background remover from the project root:

       python3 tools/prepare_portrait.py

   It floods the white field from the border (so white clothing and highlights
   inside the subject survive), feathers the edge, removes the white fringe,
   trims to the subject and writes:

       assets/img/portrait-cutout.webp      up to 1400px tall
       assets/img/portrait-cutout@800.webp  800px tall

   Options: --tolerance 18 (raise for off-white studio paper), --feather 0.8,
   --height 1400. Requires Pillow and numpy.

3. Reload the site. `assets/js/app.js` adds `html.has-photo` once the cut-out
   loads; the monogram plate is replaced automatically. No HTML edits needed.

Until the file exists, the hero shows an art-directed WZ plate and the about
section shows a monogram plate — never a broken image.

OTHER IMAGES
------------
The project posters and template posters are CSS compositions, not screenshots.
They stay sharp at every size and add no network weight. Real screenshots can
replace them later by swapping the `.poster` / `.work-poster` contents for an
`<img>` while keeping the same aspect ratios.

VENDOR
------
assets/vendor/three.module.js      three r169 (MIT)
assets/vendor/gsap.min.js          GSAP 3.12.5 (standard licence)
assets/vendor/ScrollTrigger.min.js ScrollTrigger 3.12.5

These are vendored so the site works offline and has no third-party runtime
dependency. The fonts are loaded from Google Fonts with a system fallback.

FIELD NOTES — THE SCROLL WORLD
------------------------------
assets/js/journey3d.js builds the pinned 3D stretch between the hero and the
studio section: photographs sit at real depths and a camera dollies through
them along a spline, keyed to scroll. Styles live in assets/css/journey.css.

  assets/img/hp/temple.webp   Bhimakali temple, Sarahan
  assets/img/hp/ridge.webp    blurred crop of that frame, used for the far ridge
  assets/img/hp/forest.webp   deodar forest, Manali
  assets/img/hp/fir.webp      deodar forest, Manali
  assets/img/hp/canopy.webp   crop of that frame, used as foreground canopy

Originals live in Hp Img/. The pine-forest stock frame there carries a
watermark across the whole image, so it is not used anywhere on the site.

Every plate is graded in the fragment shader (desaturate, push shadows into the
page ink, highlights toward cream) so photographs taken in different light read
as one place. Swapping a file keeps its path — no JS edits needed.

Reduced motion, `data-motion="off"` and a missing WebGL context all fall back to
a static composition where every chapter stays readable.
