#!/usr/bin/env python3
"""Build index.html from the canonical ThreeUI Kage page.

The engine (Three.js scene, camera rig, scroll wiring, shaders, post pipeline)
is kept byte-for-byte; only identity, copy, image assets and a few material
tints are redirected for the Himachal Pradesh portfolio.

    python3 tools/theme_kage.py

Source of truth: vendor/kage/kage.html (fetched from
threeui.com/source-code/kage-landing-page.json).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "vendor" / "kage" / "kage.html"
OUT = ROOT / "index.html"

s = SRC.read_text(encoding="utf-8")
original = s


def sub(old: str, new: str, count: int = 1):
    """Replace `old` exactly `count` times, loudly."""
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} match(es), found {n} for:\n{old[:160]!r}")
    s = s.replace(old, new)


# ---------------------------------------------------------------- head / meta
s = re.sub(r"<head><script>function __threeuiStorageImage.*?</script>", "<head>", s,
           count=1, flags=re.S)

sub("<title>Kage — Where stillness reveals the unseen</title>",
    "<title>Ayush Danthta — A Himalayan 3D portfolio</title>")

sub('<meta name="description" content="A five-chapter night walk through a Kyoto mountain temple. '
    'Charred cypress, lantern light and a vermilion moon, rendered live in WebGL.">',
    '<meta name="description" content="Ayush Danthta — designer and developer in Shimla, '
    'Himachal Pradesh. A cinematic five-chapter climb through deodar forest and a slate-roofed '
    'mountain temple, rendered live in WebGL.">')

sub('<link rel="stylesheet" href="secret-pathways-assets/fonts.css">',
    '<link rel="stylesheet" href="assets/kage/fonts.css">')
sub('<script src="secret-pathways-assets/three.min.js"></script>',
    '<script src="assets/kage/three.min.js"></script>')

# ---------------------------------------------------------------- preloader
sub('<div class="pre-jp jp">影の道</div>', '<div class="pre-jp dv">HIMACHAL</div>')
sub('<span>Raising the mountain temple</span>', '<span>Building the mountain</span>')

# ---------------------------------------------------------------- nav
sub('<span class="brand-tx"><b>KAGE</b><i>HIDDEN REALMS OF KYOTO</i></span>',
    '<span class="brand-tx"><b>AYUSH DANTHTA</b><i>DESIGNER · DEVELOPER · MOTION</i></span>')

# ---------------------------------------------------------------- the mark
# The original mark is a torii: two lintels and a post. At 34 px it says Kyoto
# before a word of the page is read. Himachal's mark is a Bhimakali tower —
# three storeys of deodar stepping out under level slate pents, a whitewashed
# plinth, one lit door, and a trishul above the whole thing.
MARK = '''<svg viewBox="0 0 44 44" fill="none" aria-hidden="true">
  <!-- trishul on the finial -->
  <path d="M22 3.4v7.6M19.5 5.2v5.6M24.5 5.2v5.6"
        stroke="#dfe7e0" stroke-width="1.5" stroke-linecap="round"/>
  <circle cx="22" cy="10.9" r="1" fill="#dfe7e0"/>
  <!-- the slate pent, thrown wide past the walls -->
  <path d="M11.4 11.9h21.2l4.6 5.4H6.8Z" fill="#dfe7e0"/>
  <!-- whitewashed wall behind the deodar frame -->
  <rect x="11.2" y="17.3" width="21.6" height="12.3" fill="#dfe7e0" fill-opacity=".32"/>
  <rect x="10" y="17.7" width="2.6" height="11.9" fill="#dfe7e0"/>
  <rect x="31.4" y="17.7" width="2.6" height="11.9" fill="#dfe7e0"/>
  <!-- the lit door -->
  <rect x="19.2" y="22.4" width="5.6" height="7.2" fill="#e0231c"/>
  <!-- the plinth it stands on -->
  <rect x="6.6" y="30.2" width="30.8" height="3" fill="#dfe7e0" fill-opacity=".78"/>
</svg>'''
sub('''    <svg viewBox="0 0 44 44" fill="none" aria-hidden="true">
      <circle cx="22" cy="25" r="8.6" fill="#e0231c" fill-opacity=".9"/>
      <path d="M5 13h34M9 18.4h26M22 8.5v27" stroke="#dfe7e0" stroke-width="1.5"/>
      <path d="M14 35.5h16" stroke="#dfe7e0" stroke-width="1.2" stroke-opacity=".6"/>
    </svg>''', '    ' + MARK)
sub('''      <svg viewBox="0 0 44 44" fill="none" aria-hidden="true">
        <circle cx="22" cy="24" r="9.5" stroke="#e0231c" stroke-width="1.2"/>
        <path d="M6 12h32M9.5 17h25M22 8v28" stroke="#dfe7e0" stroke-width="1.2"/>
      </svg>''', '      ' + MARK)
sub('''      <svg viewBox="0 0 44 44" fill="none" width="34" height="34" aria-hidden="true">
        <circle cx="22" cy="25" r="8.6" fill="#e0231c" fill-opacity=".9"/>
        <path d="M5 13h34M9 18.4h26M22 8.5v27" stroke="#dfe7e0" stroke-width="1.5"/>
      </svg>''',
    '      ' + MARK.replace('fill="none"', 'fill="none" width="34" height="34"'))

sub('''    <a class="nav-link" href="#gate" data-cursor><span>Temples</span><span class="alt">伽藍</span></a>
    <a class="nav-link" href="#pathways" data-cursor><span>Gardens</span><span class="alt">庭園</span></a>
    <a class="nav-link" href="#lessons" data-cursor><span>Rituals</span><span class="alt">神事</span></a>
    <a class="nav-link" href="#eternity" data-cursor><span>Afterlight</span><span class="alt">残光</span></a>''',
    '''    <a class="nav-link" href="#gate" data-cursor><span>Atmosphere</span><span class="alt">Shimla</span></a>
    <a class="nav-link" href="#pathways" data-cursor><span>Temple</span><span class="alt">Sarahan</span></a>
    <a class="nav-link" href="#lessons" data-cursor><span>Forest</span><span class="alt">Deodar</span></a>
    <a class="nav-link" href="#eternity" data-cursor><span>Arrival</span><span class="alt">Ridge</span></a>''')

# ---------------------------------------------------------------- hero
sub('<span class="dot"></span> Chapter 00 — The Hidden Gate',
    '<span class="dot"></span> Chapter 01 — The Ridge')

sub('''      <span class="mask-line"><span>Where stillness</span></span>
      <span class="mask-line"><span>reveals the</span></span>
      <span class="mask-line"><span>unseen.</span></span>''',
    '''      <span class="mask-line"><span>Design that</span></span>
      <span class="mask-line"><span>holds its</span></span>
      <span class="mask-line"><span>ground.</span></span>''')

sub('''    <p class="hero-sub body" data-rv="up">Enter Kyoto through its quiet thresholds, where ritual,
      craft, and memory shape the path.</p>''',
    '''    <p class="hero-sub body" data-rv="up">Ayush Danthta — designer and developer in Shimla.
      Interfaces, motion and 3D built with the patience of a mountain temple.</p>''')

sub('''      <div class="chip" data-chip="0" data-rv="up" data-cursor><span class="num">01</span>
        <span class="tx"><b>Thresholds</b><p>Discover the hidden gates that open on to deeper paths.</p></span></div>
      <div class="chip" data-chip="1" data-rv="up" data-cursor><span class="num">02</span>
        <span class="tx"><b>Still Gardens</b><p>Witness the courts where silence gently unfolds.</p></span></div>
      <div class="chip" data-chip="2" data-rv="up" data-cursor><span class="num">03</span>
        <span class="tx"><b>Sacred Craft</b><p>Embrace the hands and heritage that shape devotion.</p></span></div>
      <div class="chip" data-chip="3" data-rv="up" data-cursor><span class="num">04</span>
        <span class="tx"><b>Night Rituals</b><p>Explore the rites that awaken when the day is done.</p></span></div>''',
    '''      <div class="chip" data-chip="0" data-rv="up" data-cursor><span class="num">01</span>
        <span class="tx"><b>The Ridge</b><p>The valley opens before anything is built on it.</p></span></div>
      <div class="chip" data-chip="1" data-rv="up" data-cursor><span class="num">02</span>
        <span class="tx"><b>Atmosphere</b><p>Thin air, long shadows, and the work that lives in them.</p></span></div>
      <div class="chip" data-chip="2" data-rv="up" data-cursor><span class="num">03</span>
        <span class="tx"><b>The Temple</b><p>Deodar, slate, and a frame you can read.</p></span></div>
      <div class="chip" data-chip="3" data-rv="up" data-cursor><span class="num">04</span>
        <span class="tx"><b>The Forest</b><p>Five lessons the deodar taught the interface.</p></span></div>''')

sub('<b class="jp">山門</b><i>Sanmon — before the bell</i>',
    '<b class="dv">BHIMAKALI</b><i>Sarahan — before the bell</i>')

# the gate is a dwara now, not a sanmon: the rail tooltip and the peek card
# were still naming it after the hall the engine shipped with
sub("const names = ['The Hidden Gate', 'The Sanmon', 'Still Gardens', 'Sacred Craft', 'Afterlight', 'Colophon'];",
    "const names = ['The Hidden Gate', 'The Dwara', 'Still Gardens', 'Sacred Craft', 'Afterlight', 'Colophon'];")
sub('aria-label="Preview: Sanmon, before the bell"',
    'aria-label="Preview: the temple dwara, before the bell"')

sub('<div class="word-fb" aria-hidden="true">KAGE</div>',
    '<div class="word-fb" aria-hidden="true">AYUSH</div>')
sub('<span class="v jp">影の道</span>', '<span class="v dv">HIMACHAL</span>')

# ---------------------------------------------------------------- chapter 02 · atmosphere
sub('''    <span class="k"><b>01</b> — The Sanmon</span><span class="rule"></span><span class="k jp">山門</span>''',
    '''    <span class="k"><b>02</b> — Atmosphere</span><span class="rule"></span><span class="k dv">SHIMLA · 31°N</span>''')

sub('''    <h2 class="display h-sec" data-rv="up">Charred cypress, worn stone, one gate left open.</h2>''',
    '''    <h2 class="display h-sec" data-rv="up">Thin air, long shadows, a room that breathes.</h2>''')

sub('''      <p class="lead" data-rv="up">Kage begins where the city stops: a mountain gate of cedar burned black,
        standing in its own weather. The soot is not decoration. It is how a board is taught to survive a
        hundred rainy seasons, and the first thing this place asks you to understand.</p>
      <p class="body" data-rv="up">Climb the worn steps and the worship hall lifts out of the mist, its paper
        screens lit from inside like a lantern the size of a house. Above the eaves a vermilion moon holds
        its place, patient, half hidden. Nothing here is in a hurry. Neither, for the next ninety minutes,
        are you.</p>
      <a class="arrowlink" href="#pathways" data-rv="fade" data-cursor>
        <span>Cross the threshold</span>''',
    '''      <p class="lead" data-rv="up">I am Ayush Danthta — a designer and developer working out of Shimla,
        in the Himalaya. I build interfaces, motion and 3D for people who would rather be remembered
        than merely clicked.</p>
      <p class="body" data-rv="up">Atmosphere is the part of the work nobody can name: the weight of a
        shadow, the half-second a surface takes to settle, the silence between a click and its answer.
        I start there and draw the structure around it — type, timing and light, until a screen feels
        like a place rather than a page.</p>
      <a class="arrowlink" href="#pathways" data-rv="fade" data-cursor>
        <span>See the structure</span>''')

sub('''  <div class="gate-stats" data-rv="up">
    <div><b>05</b><span>Chapters</span></div>
    <div><b>92</b><span>Minutes</span></div>
    <div><b>1611</b><span>Hall raised</span></div>
    <div><b>∞</b><span>Stillness</span></div>
  </div>''',
    '''  <div class="gate-stats" data-rv="up">
    <div><b>WZ</b><span>Independent studio</span></div>
    <div><b>HP</b><span>Based in Himachal</span></div>
    <div><b>01</b><span>Person, start to finish</span></div>
    <div><b>∞</b><span>Attention to detail</span></div>
  </div>''')

# the single portrait, in the atmosphere chapter only
sub('''  <div class="sec-head" data-rv="fade">
    <span class="k"><b>02</b> — Atmosphere</span><span class="rule"></span><span class="k dv">SHIMLA · 31°N</span>
  </div>''',
    '''  <div class="sec-head" data-rv="fade">
    <span class="k"><b>02</b> — Atmosphere</span><span class="rule"></span><span class="k dv">SHIMLA · 31°N</span>
  </div>
  <figure class="portrait-band" data-rv="up">
    <figcaption>
      <b>Ayush Danthta</b>
      <span>Shimla — Himachal Pradesh</span>
      <p class="body">Designer, developer and motion. Interfaces, 3D, and the quiet
        mechanics of attention.</p>
    </figcaption>
    <img src="assets/img/portrait-cutout@800.webp" alt="Portrait of Ayush Danthta"
         width="900" height="1200" loading="lazy" decoding="async">
  </figure>''')

# ---------------------------------------------------------------- chapter 03 · temple
sub('''    <span class="k"><b>02</b> — Still Gardens</span><span class="rule"></span><span class="k jp">庭園</span>''',
    '''    <span class="k"><b>03</b> — The Temple</span><span class="rule"></span><span class="k dv">SARAHAN</span>''')

sub('<b>Approach</b><span class="jp">参道</span>', '<b>Approach</b><span class="dv">THE CLIMB</span>')
sub('<b>Lanterns</b><span class="jp">灯籠</span>', '<b>Deodar</b><span class="dv">THE FOREST</span>')
sub('<b>Moonwater</b><span class="jp">月影</span>', '<b>Canopy</b><span class="dv">ABOVE</span>')
sub('<span>The long climb</span><span>01 / 03</span>', '<span>Temple · forest · canopy</span><span>01 / 03</span>')
sub('<span>Lantern court</span><span>02 / 03</span>', '<span>Deodar forest</span><span>02 / 03</span>')
sub('<span>The wet court</span><span>03 / 03</span>', '<span>Himalayan canopy</span><span>03 / 03</span>')

# ---------------------------------------------------------------- chapter 04 · forest
sub('''    <span class="k"><b>03</b> — Sacred Craft</span><span class="rule"></span><span class="k jp">手業</span>''',
    '''    <span class="k"><b>04</b> — The Forest</span><span class="rule"></span><span class="k dv">DEODAR</span>''')

sub('''    <h2 class="display h-sec" data-rv="up">Five chapters. Ninety minutes. One quiet mind.</h2>
    <p class="body-lg" data-rv="up">Each chapter is a walk, not a lecture. You arrive at the gate, climb the
      steps, sit with the lantern, and leave with one thing worth keeping.</p>''',
    '''    <h2 class="display h-sec" data-rv="up">Five things the deodar taught the interface.</h2>
    <p class="body-lg" data-rv="up">The deodar grows slowly, holds the slope, and gives the valley its
      shade. Every rule I build by came out of walking under it — not out of a design system.</p>''')

sub('''      <h3>The Hidden Gate<em class="jp">山門</em></h3>
      <p>Why a gate is a sentence, and what you agree to when you walk under one.</p>
      <span class="t">14 min</span><i class="bar"></i>''',
    '''      <h3>Deep roots<em class="dv">STRUCTURE</em></h3>
      <p>The frame has to carry the whole tree before the first branch is drawn.</p>
      <span class="t">Structure</span><i class="bar"></i>''')

sub('''      <h3>Borrowed Scenery<em class="jp">借景</em></h3>
      <p>Shakkei: composing with a mountain you will never own.</p>
      <span class="t">18 min</span><i class="bar"></i>''',
    '''      <h3>Borrowed scenery<em class="dv">DEPTH</em></h3>
      <p>Composing with a mountain you will never own — and letting it stay the hero.</p>
      <span class="t">Depth</span><i class="bar"></i>''')

sub('''      <h3>Charred Cypress<em class="jp">焼杉</em></h3>
      <p>Yakisugi: burning a board black so the weather will let it live.</p>
      <span class="t">21 min</span><i class="bar"></i>''',
    '''      <h3>Weathering<em class="dv">MATERIAL</em></h3>
      <p>Deodar silvering in the rain. Surfaces should age, not peel.</p>
      <span class="t">Material</span><i class="bar"></i>''')

sub('''      <h3>Lantern Light<em class="jp">灯籠</em></h3>
      <p>How a single ember decides the scale of everything around it.</p>
      <span class="t">17 min</span><i class="bar"></i>''',
    '''      <h3>Lantern light<em class="dv">FOCUS</em></h3>
      <p>One warm source decides the scale of everything around it. So does one accent.</p>
      <span class="t">Focus</span><i class="bar"></i>''')

sub('''      <h3>The Vermilion Moon<em class="jp">朱月</em></h3>
      <p>Why the moon burns red over the valley, and what the garden does with it.</p>
      <span class="t">22 min</span><i class="bar"></i>''',
    '''      <h3>Clearings<em class="dv">REST</em></h3>
      <p>Where the eye is allowed to stop. Space is the loudest thing you can draw.</p>
      <span class="t">Rest</span><i class="bar"></i>''')

# ---------------------------------------------------------------- chapter 05 · arrival
sub('<div class="eyebrow" data-rv="fade">Chapter 04 — Afterlight</div>',
    '<div class="eyebrow" data-rv="fade">Chapter 05 — Arrival</div>')
sub('<h2 class="display" data-rv="up">Afterlight</h2>',
    '<h2 class="display" data-rv="up">Arrival</h2>')
sub('''  <p class="body-lg" data-rv="up">The gate does not close behind you. Take the walk whenever the noise
    gets loud — it is always the same path, and never the same light.</p>
  <a class="cta" href="#top" data-rv="fade" data-cursor>
    <i></i><span>Begin the walk</span>''',
    '''  <p class="body-lg" data-rv="up">The ridge does not close behind you. Take the climb whenever the
    noise gets loud — it is always the same path, and never the same light.</p>
  <a class="cta" href="mailto:ayushdanthta@gmail.com?subject=Project%20enquiry" data-rv="fade" data-cursor>
    <i></i><span>Start a project</span>''')

# ---------------------------------------------------------------- footer
sub('''      <p>A five-chapter night walk through a Kyoto mountain temple. Three illustrated garden field notes
        sit inside a live Three.js sanctuary.</p>''',
    '''      <p>A portfolio built as one continuous climb through Himachal Pradesh: deodar forest, a
        slate-roofed temple above the valley, and the ridge behind Shimla.</p>''')

sub('''      <li><a href="#gate" data-cursor>The Sanmon</a></li>
      <li><a href="#pathways" data-cursor>Still Gardens</a></li>
      <li><a href="#lessons" data-cursor>Sacred Craft</a></li>
      <li><a href="#eternity" data-cursor>Afterlight</a></li>''',
    '''      <li><a href="#gate" data-cursor>Atmosphere</a></li>
      <li><a href="#pathways" data-cursor>The Temple</a></li>
      <li><a href="#lessons" data-cursor>The Forest</a></li>
      <li><a href="#eternity" data-cursor>Arrival</a></li>''')

sub('''    <div><h4>Practice</h4><ul>
      <li><a href="#lessons" data-cursor>Borrowed scenery</a></li>
      <li><a href="#lessons" data-cursor>Lantern light</a></li>
      <li><a href="#lessons" data-cursor>Charred cypress</a></li>
      <li><a href="#lessons" data-cursor>Raked gravel</a></li>
    </ul></div>
    <div><h4>Elsewhere</h4><ul>
      <li><a href="#top" data-cursor>Journal</a></li>
      <li><a href="#top" data-cursor>Field notes</a></li>
      <li><a href="#top" data-cursor>Colophon</a></li>
    </ul></div>''',
    '''    <div><h4>Work</h4><ul>
      <li><a href="mailto:ayushdanthta@gmail.com" data-cursor>Email</a></li>
      <li><a href="https://wa.me/918353011030" target="_blank" rel="noopener noreferrer" data-cursor>WhatsApp</a></li>
      <li><a href="https://wzayush.vercel.app/" target="_blank" rel="noopener noreferrer" data-cursor>Portfolio</a></li>
    </ul></div>
    <div><h4>Elsewhere</h4><ul>
      <li><a href="https://wa.me/918353011030" target="_blank" rel="noopener noreferrer" data-cursor>Commissions</a></li>
      <li><a href="mailto:ayushdanthta@gmail.com?subject=Hello" data-cursor>Say hello</a></li>
      <li><a href="#top" data-cursor>Back to the ridge</a></li>
    </ul></div>''')

sub('''    <span>© 2026 Kage — Kage no Michi</span>
    <span class="jp">静けさは一つの技である</span>
    <span>WebGL · Onest · Kyoto</span>''',
    '''    <span>© 2026 Ayush Danthta</span>
    <span class="dv">SHIMLA · HIMACHAL PRADESH</span>
    <span>WebGL · Onest · Shimla</span>''')

# ---------------------------------------------------------------- plates
sub("url('https://ublctyddhtbgaersvxxb.supabase.co/storage/v1/object/public/threeui-media/"
    "scene-images/6884c5281949d2c3530ad4cf/kage-sanmon-preview.webp') center / cover no-repeat;",
    "url('assets/img/hp/ridge.webp') center 42% / cover no-repeat;")
sub("url('https://ublctyddhtbgaersvxxb.supabase.co/storage/v1/object/public/threeui-media/"
    "scene-images/6884c5281949d2c3530ad4cf/kage-approach.webp') center / cover no-repeat;",
    "url('assets/img/hp/temple.webp') center 38% / cover no-repeat;")
sub("url('https://ublctyddhtbgaersvxxb.supabase.co/storage/v1/object/public/threeui-media/"
    "scene-images/6884c5281949d2c3530ad4cf/kage-lantern-court.webp') center / cover no-repeat;",
    "url('assets/img/hp/forest.webp') center / cover no-repeat;")
sub("url('https://ublctyddhtbgaersvxxb.supabase.co/storage/v1/object/public/threeui-media/"
    "scene-images/6884c5281949d2c3530ad4cf/kage-moonwater.webp') center / cover no-repeat;",
    "url('assets/img/hp/canopy.webp') center / cover no-repeat;")

# ---------------------------------------------------------------- near-plane cut-outs
FG = {
    "gate": '''  <div class="fg" data-fg="gate" aria-hidden="true">
    <span class="fg-el fg-pine" data-fg-in="right">
      <img src="assets/kage/fg/deodar-tree.webp" alt="" width="1024" height="1438" loading="lazy" decoding="async">
    </span>
    <span class="fg-el fg-grass" data-fg-in="up">
      <img src="assets/kage/fg/tall-grass.webp" alt="" width="1717" height="916" loading="lazy" decoding="async">
    </span>
  </div>
''',
    "pathways": '''  <div class="fg" data-fg="pathways" aria-hidden="true">
    <span class="fg-el fg-hill" data-fg-in="up">
      <img src="assets/kage/fg/hill.webp" alt="" width="1774" height="887" loading="lazy" decoding="async">
    </span>
    <span class="fg-el fg-stones" data-fg-in="left">
      <img src="assets/kage/fg/hp-slate-stones.webp" alt="" width="952" height="554" loading="lazy" decoding="async">
    </span>
  </div>
''',
    "lessons": '''  <div class="fg" data-fg="lessons" aria-hidden="true">
    <span class="fg-el fg-stones" data-fg-in="up">
      <img src="assets/kage/fg/hp-slate-stones.webp" alt="" width="952" height="554" loading="lazy" decoding="async">
    </span>
    <span class="fg-el fg-grass" data-fg-in="up">
      <img src="assets/kage/fg/tall-grass.webp" alt="" width="1717" height="916" loading="lazy" decoding="async">
    </span>
    <span class="fg-el fg-grove" data-fg-in="up">
      <img src="assets/kage/fg/deodar-grove.webp" alt="" width="2600" height="820" loading="lazy" decoding="async">
    </span>
  </div>
''',
    "eternity": '''  <div class="fg" data-fg="eternity" aria-hidden="true">
    <span class="fg-el fg-hill" data-fg-in="up">
      <img src="assets/kage/fg/hill.webp" alt="" width="1774" height="887" loading="lazy" decoding="async">
    </span>
    <span class="fg-el fg-grass" data-fg-in="up">
      <img src="assets/kage/fg/tall-grass.webp" alt="" width="1717" height="916" loading="lazy" decoding="async">
    </span>
  </div>
''',
    "foot": '''  <div class="fg" data-fg="foot" aria-hidden="true">
    <span class="fg-el fg-grass" data-fg-in="up">
      <img src="assets/kage/fg/tall-grass.webp" alt="" width="1717" height="916" loading="lazy" decoding="async">
    </span>
    <span class="fg-el fg-stones" data-fg-in="up">
      <img src="assets/kage/fg/hp-slate-stones.webp" alt="" width="952" height="554" loading="lazy" decoding="async">
    </span>
  </div>
''',
}
for key, block in FG.items():
    pattern = re.compile(r'  <div class="fg" data-fg="%s".*?\n  </div>\n' % key, re.S)
    s, n = pattern.subn(block, s, count=1)
    if n != 1:
        sys.exit(f"fg block {key}: {n} matches")

# ---------------------------------------------------------------- field notes
# The forest chapter argued its rules in type alone. Three frames of the
# supplied Himachali photographs give the deodar belt a face before the rules
# begin: the belt itself, the snow line it grows under, and one crown.
FIELD_NOTES = '''  <div class="field-notes" data-rv="fade">
    <figure>
      <span class="fn-fr"><img src="assets/img/hp/fir.webp" alt="Deodar and fir on the slope above Shimla" loading="lazy" decoding="async"></span>
      <figcaption><b>The belt</b><span>2,300 m</span></figcaption>
    </figure>
    <figure>
      <span class="fn-fr"><img src="assets/img/hp/ridge.webp" alt="The snow line along a Himalayan ridge" loading="lazy" decoding="async" style="object-position:22% 45%; filter:saturate(.72) contrast(1.22) brightness(.58)"></span>
      <figcaption><b>The snow line</b><span>Dhauladhar</span></figcaption>
    </figure>
    <figure>
      <span class="fn-fr"><img src="assets/img/hp/canopy.webp" alt="A deodar crown lit against the dark forest" loading="lazy" decoding="async" style="object-position:50% 32%"></span>
      <figcaption><b>The crown</b><span>Sarahan</span></figcaption>
    </figure>
  </div>
'''
# set under the closing chapter's call to action: the page ends on the work
# itself rather than on another paragraph
sub('</section>\n\n<!-- ============================================================ footer -->',
    FIELD_NOTES + '</section>\n\n<!-- ============================================================ footer -->')

# ---------------------------------------------------------------- 3-D wordmark
sub("  const word = 'KAGE', gl = [];", "  const word = 'AYUSH', gl = [];")

# ---------------------------------------------------------------- material grade
# the moon: a pale Himalayan moon instead of the vermilion one. Its sourced
# disc carries crater noise that reads as mould behind a bloom, so the body is
# a soft-edged glow and the light comes from the halo around it.
sub("new THREE.MeshBasicMaterial({ map: tx(texMoon()), color: hdr(3.6, .64, .61),",
    "new THREE.MeshBasicMaterial({ map: tx(texGlow('rgba(255,251,240,1)', 'rgba(206,222,236,.42)')), color: hdr(1.24, 1.18, 1.04),")
sub("texGlow('rgba(255,124,112,.90)', 'rgba(206,52,48,.26)')",
    "texGlow('rgba(255,240,214,.88)', 'rgba(206,176,124,.24)')")
sub("const moonKey = new THREE.DirectionalLight(0xff6a42, .52);",
    "const moonKey = new THREE.DirectionalLight(0xffd2a0, .46);")
sub("const moonL = new THREE.PointLight(0xff3a1c, 3.0, 46, 2);",
    "const moonL = new THREE.PointLight(0xffd9ac, 1.7, 46, 2);")

# the falling drifts: pine needles, not maple embers
sub("    color: 0x40080a, roughness: .84, metalness: 0,",
    "    color: 0x35441f, roughness: .84, metalness: 0,")
sub("    emissive: 0x780200, emissiveIntensity: .72",
    "    emissive: 0x0b1407, emissiveIntensity: .28")

# temple: deodar timber and slate, not charred cypress and black tile
sub("{ color: 0x565150, normal: 1.5 }", "{ color: 0x6b523f, normal: 1.5 }")
sub("{ color: 0x8a746d, normal: 1.05, metalness: .03 }",
    "{ color: 0x8b6a4c, normal: 1.05, metalness: .03 }")
sub("{ color: 0x2b343a, roughness: .74, metalness: .10, normal: 1.4 }",
    "{ color: 0x3b444c, roughness: .74, metalness: .10, normal: 1.4 }")

# --------------------------------------------------------- the deodar forest
# The engine's tree is a maple: a short forked trunk carrying five-lobed
# leaves, and a foreground bough of the same. That is autumn Kyoto, not a
# Himalayan hillside. A deodar is the opposite silhouette — one tall straight
# leader, whorls of near-horizontal boughs that droop at the tips, and narrow
# blue-green sprays. The chestnut is replaced, not retinted.
TEX_NEEDLE = r"""function texLeaf() {
  /* A deodar sprig: a tapered feather of needles, widest a third of the way
     out and drawn to a point. The body is filled and then combed apart with
     transparent cuts, so it holds together at distance — fine strokes alone
     mip away to nothing and leave the crown looking bare. White on
     transparent: the material tint decides the green. */
  const S = 256, c = cvs(S, S), x = c.getContext('2d');
  const rnd = mulberry32(7);
  const y0 = S * .5, x0 = S * .04, x1 = S * .96;

  x.beginPath();
  x.moveTo(x0, y0);
  for (let i = 0; i <= 24; i++) {
    const u = i / 24;
    const px = x0 + (x1 - x0) * u;
    x.lineTo(px, y0 - S * .235 * Math.pow(Math.sin(Math.PI * Math.pow(u, .70)), .75));
  }
  for (let i = 24; i >= 0; i--) {
    const u = i / 24;
    const px = x0 + (x1 - x0) * u;
    x.lineTo(px, y0 + S * .215 * Math.pow(Math.sin(Math.PI * Math.pow(u, .76)), .80));
  }
  x.closePath();
  x.fillStyle = '#fff'; x.fill();

  /* comb the body into needles with transparent splits fanning off the midrib */
  x.globalCompositeOperation = 'destination-out';
  const N = 52;
  for (let i = 0; i < N; i++) {
    const u = (i + .5) / N;
    const px = x0 + (x1 - x0) * u;
    for (let sd = -1; sd <= 1; sd += 2) {
      x.beginPath(); x.moveTo(px, y0 + sd * S * .008);
      x.lineTo(px + S * .045, y0 + sd * S * .255);
      x.lineWidth = 1.0 + rnd() * 1.5; x.stroke();
    }
  }
  for (let i = 0; i < 9; i++) {
    x.beginPath();
    x.moveTo(x1 - S * .09 + rnd() * S * .04, y0);
    x.lineTo(x1 + S * .04, y0 - S * .14 + rnd() * S * .28);
    x.lineWidth = 1.2 + rnd() * 1.6; x.stroke();
  }
  x.globalCompositeOperation = 'source-over';

  /* the midrib stays solid */
  x.beginPath(); x.moveTo(x0, y0);
  x.quadraticCurveTo(S * .5, y0 - S * .015, x1, y0);
  x.lineWidth = S * .012; x.strokeStyle = '#fff'; x.lineCap = 'round'; x.stroke();
  return c;
}
"""

s, _tn = re.subn(r"function texLeaf\(\) \{.*?\n\}\n\n/\* the night sky itself",
                lambda m: TEX_NEEDLE + "\n/* the night sky itself", s, count=1, flags=re.S)
if _tn != 1:
    sys.exit("texLeaf: the engine maple-leaf texture was not found exactly once")

DEODAR = r"""function buildDeodar(seed, x, z, scale, far) {
  /* Cedrus deodara: one straight leader carrying whorls of near-horizontal
     boughs that droop at the tips, under a narrow conical crown of blue-green
     sprays. Height and spread follow the engine's maple so nothing else about
     the court moves. `far` is the ridge belt: a third of the whorls, because
     at sixty metres only the silhouette ever resolves. */
  const rnd = mulberry32(seed);
  const g = new THREE.Group();
  const H = 8.4 + rnd() * 3.2;                 /* deodars are tall */
  const R0 = 1.25 + rnd() * .50;               /* reach of the lowest whorl */

  /* ---- the leader, in tapered segments so it can carry a slight lean ---- */
  const parts = [];
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), UP = new THREE.Vector3(0, 1, 0);
  const dir = new THREE.Vector3(), pos = new THREE.Vector3();
  const SEG = 8;
  let lx = 0, lz = 0;
  for (let i = 0; i < SEG; i++) {
    lx += (rnd() - .5) * .13; lz += (rnd() - .5) * .13;
    const y0 = H * i / SEG, y1 = H * (i + 1) / SEG;
    const from = new THREE.Vector3(lx, y0, lz), to = new THREE.Vector3(lx, y1, lz);
    dir.subVectors(to, from);
    const len = dir.length(); dir.normalize();
    const r0 = .28 * (1 - i / SEG * .88), r1 = .28 * (1 - (i + 1) / SEG * .88);
    const geo = new THREE.CylinderGeometry(r1, r0, len, 7, 1, false);
    Q.setFromUnitVectors(UP, dir);
    pos.addVectors(from, to).multiplyScalar(.5);
    M.compose(pos, Q, new THREE.Vector3(1, 1, 1));
    geo.applyMatrix4(M);
    parts.push(geo);
  }
  const trunk = new THREE.Mesh(mergeGeos(parts),
    new THREE.MeshStandardMaterial({ color: 0x191410, roughness: .95, metalness: 0 }));
  trunk.castShadow = true; trunk.receiveShadow = true; g.add(trunk);

  /* ---- the sprays: two crossed planes per bough ---- */
  const frond = new THREE.PlaneGeometry(1.9, 1.35, 1, 1);
  frond.translate(.95, 0, 0);            /* rooted at the bough, not its middle */
  /* the sprays are cut from the same deodar specimen as the page's foreground
     tree, so the 3-D wood and the flat cut-out are the same species */
  if (!WORLD.deodarSpray) {
    WORLD.deodarSpray = new THREE.TextureLoader().load('assets/kage/fg/deodar-spray.webp');
    WORLD.deodarSpray.encoding = THREE.sRGBEncoding;
    WORLD.deodarSpray.anisotropy = Math.min(8, maxAniso);
  }
  /* one leaf material for the whole hillside: the canopy is now twenty trees
     deep, and a material per tree meant twenty copies of the same shader */
  if (!WORLD.deodarMats) {
    const spray = (col, emit) => new THREE.MeshStandardMaterial({
      map: WORLD.deodarSpray, color: col, alphaTest: .30,
      side: THREE.DoubleSide, roughness: .84, metalness: 0,
      emissive: emit, emissiveIntensity: .12
    });
    /* deodar green, not the pale blue the specimen was keyed against; the far
       wood runs a shade colder so the ridge sits behind the court */
    WORLD.deodarMats = { near: spray(0x6a785f, 0x020403), far: spray(0x4d5d54, 0x010202) };
  }
  const needle = far ? WORLD.deodarMats.far : WORLD.deodarMats.near;
  const TIER = far ? (LOW ? 4 : 6) : (LOW ? 10 : 14);
  const sprays = [];
  for (let t = 0; t < TIER; t++) {
    const u = t / (TIER - 1);                    /* 0 lowest whorl, 1 the tip */
    const y = .26 * H + u * .66 * H;
    const r = R0 * Math.pow(1 - u, .72) + .16;
    const n = Math.max(4, Math.round(9 - u * 5));
    for (let k = 0; k < n; k++) {
      const a = (k / n) * TAU + t * .55 + rnd() * .22;
      const rr = r * (.84 + rnd() * .24);
      sprays.push({
        px: lx * u + Math.cos(a) * rr, py: y + (rnd() - .5) * .18, pz: lz * u + Math.sin(a) * rr,
        a: a, droop: -.12 - rnd() * .22,
        s: (.92 + .46 * (1 - u)) * (.85 + rnd() * .3)
      });
    }
  }
  for (let k = 0; k < (far ? 2 : 4); k++) {
    const a = k / (far ? 2 : 4) * TAU + .6;
    sprays.push({ px: lx + Math.cos(a) * .14, py: H * .965, pz: lz + Math.sin(a) * .14,
                  a: a, droop: -.04, s: .36 });
  }

  const inst = new THREE.InstancedMesh(frond, needle, sprays.length * 2);
  const dummy = new THREE.Object3D();
  const qYaw = new THREE.Quaternion(), qDroop = new THREE.Quaternion(), qRoll = new THREE.Quaternion();
  const YAW = new THREE.Vector3(0, 1, 0), PITCH = new THREE.Vector3(0, 0, 1), ROLL = new THREE.Vector3(1, 0, 0);
  let vi = 0;
  sprays.forEach(o => {
    [-1, 1].forEach(face => {
      qYaw.setFromAxisAngle(YAW, -o.a);
      qDroop.setFromAxisAngle(PITCH, o.droop);
      qRoll.setFromAxisAngle(ROLL, face * Math.PI * .5 + (rnd() - .5) * .20);
      dummy.position.set(o.px, o.py, o.pz);
      dummy.quaternion.copy(qYaw).multiply(qDroop).multiply(qRoll);
      dummy.scale.set(o.s, o.s, o.s);
      dummy.updateMatrix();
      inst.setMatrixAt(vi++, dummy.matrix);
    });
  });
  inst.instanceMatrix.needsUpdate = true;
  inst.frustumCulled = false;
  g.add(inst);

  g.position.set(x, 0, z);
  g.scale.setScalar(scale || 1);
  g.rotation.y = rnd() * TAU;
  scene.add(g);
  WORLD.deodars = WORLD.deodars || [];
  WORLD.deodars.push(g);

  /* the sprays move in the wind, a beat behind the grass */
  needle.onBeforeCompile = sh => {
    sh.uniforms.uT = WORLD.uT;
    sh.vertexShader = 'uniform float uT;\n' + sh.vertexShader.replace('#include <begin_vertex>',
      '#include <begin_vertex>\n' +
      'vec3 wp = (instanceMatrix * vec4(0.0,0.0,0.0,1.0)).xyz;\n' +
      'float ph = wp.x*1.4 + wp.z*1.1 + wp.y*.55;\n' +
      'transformed.y += sin(uT*.9 + ph)*.035;\n' +
      'transformed.x += sin(uT*.7 + ph*1.4)*.045;\n');
  };
  return g;
}
"""

s, _dd = re.subn(r"function buildMaple\(seed, x, z, scale\) \{.*?\n\}\n\nfunction buildRocks\(\) \{",
                lambda m: DEODAR + "\nfunction buildRocks() {", s, count=1, flags=re.S)
if _dd != 1:
    sys.exit("buildDeodar: the engine buildMaple was not found exactly once")

sub("    buildMaple(71, 12.6, -13.0, 1.05); buildMaple(72, -11.8, -9.4, .95);",
    "    buildDeodar(71, 12.6, -13.0, .84); buildDeodar(72, -11.8, -9.4, .76);")
sub("    buildMaple(73, 9.2, -19.0, .82);   buildMaple(74, -14.5, -17.5, 1.0);",
    "    buildDeodar(73, 9.2, -19.0, .66);   buildDeodar(74, -14.5, -17.5, .80);")
sub("  ['Growing the maples', () => {", "  ['Growing the deodar', () => {")
sub("    buildMaple(75, 16.5, -6.0, .88);",
    '''    buildDeodar(75, 16.5, -6.0, .70);

    /* The court five are the engine's own placements. Around them, the
       hillside the photographs show: a wood on either flank of the flight,
       and the belt that closes the ridge behind the tower. */
    const flank = [[76, 18.4, -26.0, .92], [77, -19.2, -28.0, .88],
                   [78, 22.0, -37.0, 1.02], [79, -22.6, -39.5, .96],
                   [80, 20.6, -48.0, 1.08], [81, -21.4, -50.0, 1.02],
                   [82, 17.6, -8.0, .74], [83, -17.9, -12.5, .72]];
    const belt = [[84, -30, -59, 1.30], [85, -20, -64, 1.22], [86, -10, -68, 1.34],
                  [87, 0, -71, 1.26], [88, 10, -67, 1.36], [89, 20, -63, 1.24],
                  [90, 30, -58, 1.32], [91, -39, -55, 1.18], [92, 39, -54, 1.20]];
    flank.forEach(t => buildDeodar(t[0], t[1], t[2], t[3]));
    belt.forEach(t => buildDeodar(t[0], t[1], t[2], t[3], true));''')

ROCKS = r"""function buildRocks() {
  /* Himachal roadsides are banked with split slate, not smooth wet granite:
     flat beds prised out of the mountain and stacked, the top slab canted.
     Each engine position becomes a small pile so the silhouette gains the
     stepped, layered profile one icosahedron never had. */
  const stone = new THREE.MeshStandardMaterial({
    color: 0x3c474e, roughness: .89, metalness: .03, flatShading: true
  });
  const moss = new THREE.MeshStandardMaterial({
    color: 0x2c3a26, roughness: .98, metalness: 0, flatShading: true
  });
  const rnd = mulberry32(404), n = noise2D(88);
  const spots = [[-6.2, -5.4, .95], [-7.4, -2.1, .7], [6.6, -7.2, .8], [8.0, -4.0, 1.05],
                 [-9.0, -8.4, 1.15], [9.6, -9.2, .9], [3.4, -7.8, .55], [-3.2, -8.6, .6]];
  spots.forEach((s, i) => {
    const g = new THREE.Group();
    const slabs = 2 + (rnd() * 3 | 0);
    for (let k = 0; k < slabs; k++) {
      const sc = s[2] * (1 - k * .15);
      const geo = new THREE.IcosahedronGeometry(sc * (.85 + rnd() * .4), 1);
      const p = geo.attributes.position;
      for (let v = 0; v < p.count; v++) {
        const vx = p.getX(v), vy = p.getY(v), vz = p.getZ(v);
        const d = 1 + .18 * fbm(n, vx * 2.2 + i * 7 + k * 3, vz * 2.2 + vy, 3, 2.2, .5);
        p.setXYZ(v, vx * d * 1.15, vy * d * .46, vz * d);
      }
      geo.computeVertexNormals();
      const m = new THREE.Mesh(geo, stone);
      m.position.set((rnd() - .5) * s[2], s[2] * .18 + k * s[2] * .36, (rnd() - .5) * s[2] * .8);
      m.rotation.set((rnd() - .5) * .2, rnd() * TAU, (rnd() - .5) * .16);
      m.castShadow = true; m.receiveShadow = true;
      g.add(m);
    }
    /* a little moss bedded on the top slab */
    if (rnd() > .45) {
      const cap = new THREE.Mesh(new THREE.SphereGeometry(s[2] * (.18 + rnd() * .14), 8, 5), moss);
      cap.scale.y = .38;
      cap.position.set((rnd() - .5) * s[2] * .5, s[2] * (.1 + slabs * .36), (rnd() - .5) * s[2] * .4);
      cap.castShadow = true;
      g.add(cap);
    }
    g.position.set(s[0], 0, s[1]);
    g.rotation.y = rnd() * TAU;
    scene.add(g);
  });
}
"""

s, _rk = re.subn(r"function buildRocks\(\) \{.*?\n\}\n\n/\* ------------------------------- the transparent-PNG",
                lambda m: ROCKS + "\n/* ------------------------------- the transparent-PNG", s, count=1, flags=re.S)
if _rk != 1:
    sys.exit("buildRocks: the engine builder was not found exactly once")

ROCK_TEX = r"""/* Himachali slate: bedded grey-blue rock split into slabs, lichen on the dry
   faces, moss where it meets the ground */
function texRockCutout(seed, opt) {
  opt = opt || {};
  const W = opt.w || 1536, H = opt.h || 1024;
  const c = cvs(W, H), x = c.getContext('2d');
  const rnd = mulberry32(seed), n = noise2D(seed * 7 + 11);
  const blobs = opt.blobs || [[.30, .70, .40, .34], [.66, .82, .38, .28], [.46, .96, .52, .34]];

  blobs.forEach((b, bi) => {
    const cx2 = b[0] * W, cy = b[1] * H, rx = b[2] * W * .5, ry = b[3] * H * .8;

    x.beginPath();
    for (let a = 0; a <= 160; a++) {
      const t = a / 160 * TAU;
      const ledge = Math.sin(t * 6 + bi * 2.3) * .018;
      const k = 1 + .14 * fbm(n, Math.cos(t) * 1.7 + bi * 9, Math.sin(t) * 1.7, 4, 2.1, .55) + ledge;
      const px = cx2 + Math.cos(t) * rx * k, py = cy + Math.sin(t) * ry * k;
      a === 0 ? x.moveTo(px, py) : x.lineTo(px, py);
    }
    x.closePath();
    const g = x.createLinearGradient(cx2 - rx, cy - ry, cx2 + rx * .4, cy + ry);
    g.addColorStop(0, hex(72, 84, 90));
    g.addColorStop(.34, hex(41, 51, 57));
    g.addColorStop(.72, hex(24, 31, 36));
    g.addColorStop(1, hex(13, 18, 22));
    x.fillStyle = g; x.fill();
    x.save(); x.clip();

    /* the bedding: courses of slate, each a little off level */
    let y = cy - ry * 1.1;
    const rows = 12 + bi * 3;
    for (let r = 0; r < rows; r++) {
      const bh = ry * 2.2 / rows * (.7 + rnd() * .7);
      const tilt = (rnd() - .5) * .09;
      const x0 = cx2 - rx * 1.4, x1 = cx2 + rx * 1.4;
      const y0a = y + (x0 - cx2) * tilt, y0b = y + (x1 - cx2) * tilt;
      const y1a = y0a + bh, y1b = y0b + bh;
      x.beginPath();
      x.moveTo(x0, y0a); x.lineTo(x1, y0b); x.lineTo(x1, y1b); x.lineTo(x0, y1a);
      x.closePath();
      const sh = .4 + rnd() * .6;
      x.fillStyle = hex(26 + 26 * sh, 34 + 34 * sh, 40 + 38 * sh);
      x.globalAlpha = .22 + rnd() * .42;
      x.fill();
      x.globalAlpha = 1;
      x.beginPath(); x.moveTo(x0, y0a); x.lineTo(x1, y0b);
      x.strokeStyle = 'rgba(7,11,14,' + (.26 + rnd() * .42) + ')';
      x.lineWidth = .8 + rnd() * 2.6; x.stroke();
      x.beginPath(); x.moveTo(x0, y0a + 1.2); x.lineTo(x1, y0b + 1.2);
      x.strokeStyle = 'rgba(172,190,194,' + (.03 + rnd() * .11) + ')';
      x.lineWidth = 1 + rnd() * 1.6; x.stroke();
      y += bh;
    }

    /* joint cracks down the face */
    for (let f = 0; f < 10; f++) {
      const jx = cx2 + (rnd() - .5) * rx * 1.7;
      let jy = cy - ry * .95;
      x.beginPath(); x.moveTo(jx, jy);
      for (let s2 = 0; s2 < 4; s2++) { jy += ry * .5; x.lineTo(jx + (rnd() - .5) * 24, jy); }
      x.strokeStyle = 'rgba(5,8,10,' + (.18 + rnd() * .34) + ')';
      x.lineWidth = .7 + rnd() * 1.8; x.stroke();
    }

    /* lichen: pale sage on the weathered tops, rust on the sheltered faces */
    for (let i = 0; i < 260; i++) {
      const lx = cx2 + (rnd() - .5) * rx * 1.75, ly = cy + (rnd() - .65) * ry * 1.5;
      const rad = 1.5 + rnd() * 8;
      x.beginPath();
      for (let a2 = 0; a2 <= 12; a2++) {
        const t2 = a2 / 12 * TAU;
        const rr2 = rad * (.55 + .75 * rnd());
        const px2 = lx + Math.cos(t2) * rr2, py2 = ly + Math.sin(t2) * rr2 * .7;
        a2 === 0 ? x.moveTo(px2, py2) : x.lineTo(px2, py2);
      }
      x.closePath();
      x.fillStyle = rnd() > .42 ? 'rgba(139,152,124,.11)' : 'rgba(150,106,62,.10)';
      x.fill();
    }

    /* moss at the foot, where the rock holds the melt */
    x.globalCompositeOperation = 'source-atop';
    for (let i = 0; i < 3000; i++) {
      const px = rnd() * W, py = H - Math.pow(rnd(), 1.9) * H * .55;
      x.fillStyle = 'rgba(' + (48 + rnd() * 42 | 0) + ',' + (74 + rnd() * 48 | 0) + ',' + (38 + rnd() * 28 | 0) + ',' + (.05 + rnd() * .23) + ')';
      x.fillRect(px, py, 1.4 + rnd() * 2.4, 3 + rnd() * 9);
    }
    x.globalCompositeOperation = 'source-over';
    x.restore();

    /* the lit rim, cold — high stone under a Himalayan moon */
    x.lineWidth = 2 + rnd() * 3;
    x.strokeStyle = 'rgba(180,198,202,.15)';
    x.beginPath();
    for (let a3 = 0; a3 <= 70; a3++) {
      const t3 = Math.PI + a3 / 70 * Math.PI * .82;
      const k3 = 1 + .16 * fbm(n, Math.cos(t3) * 1.7 + bi * 9, Math.sin(t3) * 1.7, 4, 2.1, .55);
      const px3 = cx2 + Math.cos(t3) * rx * k3 * .97, py3 = cy + Math.sin(t3) * ry * k3 * .97;
      a3 === 0 ? x.moveTo(px3, py3) : x.lineTo(px3, py3);
    }
    x.stroke();
  });

  /* cool grade: slate reads blue in this light */
  x.globalCompositeOperation = 'source-atop';
  const cg = x.createLinearGradient(W, 0, 0, H);
  cg.addColorStop(0, 'rgba(104,132,150,.15)'); cg.addColorStop(.65, 'rgba(0,0,0,0)');
  x.fillStyle = cg; x.fillRect(0, 0, W, H);
  x.globalCompositeOperation = 'source-over';
  return c;
}
"""

s, _rt = re.subn(r"/\* wet foreground boulders \*/\nfunction texRockCutout\(seed, opt\) \{.*?\n\}\n\n/\* a maple bough leaning into the top of frame \*/",
                lambda m: ROCK_TEX + "\n/* a deodar bough leaning into the top of frame */", s, count=1, flags=re.S)
if _rt != 1:
    sys.exit("texRockCutout: the engine boulder texture was not found exactly once")

BOUGH = r"""/* a deodar bough leaning into the top of frame */
function texBranchCutout(seed) {
  const W = 1536, H = 1024;
  const c = cvs(W, H), x = c.getContext('2d');
  const rnd = mulberry32(seed);

  /* a cedar frond is needles hung off a woody midrib; the midrib is drawn
     first, then the needle fans along it, so the spray has a spine */
  function needleFan(px, py, ang, rad) {
    x.save(); x.translate(px, py); x.rotate(ang);
    for (let i = 0; i < 30; i++) {
      const sd = i % 2 ? 1 : -1;
      const off = (rnd() - .5) * 30;
      const spread = sd * (.5 + rnd() * 1.0);
      const L = rad * (.42 + rnd() * .85);
      const ex = off + Math.cos(spread) * L * .6, ey = Math.sin(spread) * L;
      x.beginPath(); x.moveTo(off, 0);
      x.quadraticCurveTo(off + Math.cos(spread) * L * .28, ey * .5, ex, ey);
      const v = rnd();
      x.strokeStyle = 'rgba(' + (28 + v * 26 | 0) + ',' + (54 + v * 32 | 0) + ',' + (36 + v * 22 | 0) + ',' + (.5 + .42 * rnd()) + ')';
      x.lineWidth = 1 + rnd() * 2.1;
      x.lineCap = 'round';
      x.stroke();
    }
    x.restore();
  }

  function bough(px, py, ang, len, wid, depth) {
    const steps = 8;
    let cx2 = px, cy = py, a = ang;
    const pts = [];
    x.beginPath(); x.moveTo(cx2, cy);
    for (let s = 0; s < steps; s++) {
      a += (rnd() - .5) * .18;
      cx2 += Math.cos(a) * len / steps;
      cy += Math.sin(a) * len / steps + len / steps * .08;   /* it hangs */
      x.lineTo(cx2, cy);
      pts.push([cx2, cy, a, s / steps]);
    }
    x.lineCap = 'round'; x.lineWidth = wid;
    x.strokeStyle = 'rgba(' + (40 + depth * 5 | 0) + ',' + (31 + depth * 4 | 0) + ',' + (25 + depth * 3 | 0) + ',1)';
    x.stroke();
    pts.forEach(p => needleFan(p[0], p[1], p[2], (32 + 34 * (1 - p[3])) * (1 - depth * .10)));
    if (depth < 3 && len > 150) {
      for (let i = 0; i < 2; i++)
        bough(cx2, cy, a + (rnd() - .5) * 1.2, len * (.5 + rnd() * .16), wid * .55, depth + 1);
    }
  }

  bough(W * 1.01, H * .03, Math.PI * .82, 480, 24, 0);
  bough(W * .87, H * .02, Math.PI * .63, 350, 15, 1);
  bough(W * .96, H * .34, Math.PI * .96, 300, 12, 1);
  return c;
}
"""

s, _bg = re.subn(r"/\* a deodar bough leaning into the top of frame \*/\nfunction texBranchCutout\(seed\) \{.*?\n\}\n/\* =+ 4 · gl \*/",
                lambda m: BOUGH + "\n/* ================================================================= 4 · gl */", s, count=1, flags=re.S)
if _bg != 1:
    sys.exit("texBranchCutout: the engine maple bough was not found exactly once")

# ---------------------------------------------------------------- the gate
# ---------------------------------------------------------------- the gate
# The engine's gate is a torii: two round columns, two lifted lintels, and
# nothing between them. Re-tinting that frame deodar left the frame standing,
# and the frame is what reads Japanese. A Himachali temple entrance is a wall,
# not a frame — whitewashed stone either side of a studded deodar door, square
# posts carrying a carved frieze and a jali band, corbels, and a hipped slate
# roof with the temple bell hanging under it. So the whole builder is replaced;
# the engine keeps its original torii untouched.
GATE_NEW = r"""function buildTorii() {
  const timber = surface(postWood(), [2, 2],
    { color: hdr(1.10, .90, .68), roughness: .88, metalness: .03, normal: .95 });
  const board = surface(postWood(), [1.4, 2.2],
    { color: hdr(.50, .37, .26), roughness: .92, metalness: .02, normal: 1.05 });
  const lime = surface(texPlaster(), [2.6, 1.3],
    { color: 0xe4e3d6, roughness: .95, metalness: .01, normal: .30 });
  const stone = surface(texPlaster(), [4, 2.5],
    { color: 0x8a8a82, roughness: .96, metalness: .01, normal: 1.15 });
  const slate = surface(texSlate(), [1, 1],
    { color: 0x8d959b, roughness: .86, metalness: .06, normal: 1.05 });
  const brass = new THREE.MeshStandardMaterial({ color: 0x6f4f27, roughness: .40, metalness: .66 });
  const iron  = new THREE.MeshStandardMaterial({ color: 0x2b2521, roughness: .56, metalness: .44 });
  const jali  = new THREE.MeshStandardMaterial({
    map: tx(texJali(), { wrap: THREE.RepeatWrapping, repeat: [6, 1] }),
    color: 0xb6a78b, roughness: .90, metalness: .02,
    transparent: true, alphaTest: .30, side: THREE.DoubleSide });

  const g = new THREE.Group();
  const BASE = .58, HALF = 6.0, IN = 1.50, HEAD = BASE + 3.30, Z = -.55;

  function box(w, h, d, x, y, z, m, cast) {
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
    mesh.position.set(x, y, z);
    mesh.receiveShadow = true;
    if (cast !== false) mesh.castShadow = true;
    g.add(mesh); return mesh;
  }
  /* a bell on its chain: four links, a flared body, a lip and a clapper */
  function bell(px, top, len, r) {
    const c = new THREE.Group();
    for (let i = 0; i < 4; i++) {
      const l = new THREE.Mesh(new THREE.TorusGeometry(.05, .017, 6, 12), brass);
      l.position.y = -i * .15; c.add(l);
    }
    const body = new THREE.Mesh(new THREE.CylinderGeometry(r * .60, r, r * 1.55, 20), brass);
    body.position.y = -len; body.castShadow = true; c.add(body);
    const lip = new THREE.Mesh(new THREE.TorusGeometry(r * .97, .034, 6, 22), brass);
    lip.rotation.x = Math.PI / 2; lip.position.y = -len - r * .78; c.add(lip);
    const clap = new THREE.Mesh(new THREE.SphereGeometry(r * .22, 10, 8), iron);
    clap.position.y = -len - r * .96; c.add(clap);
    c.position.set(px, top, 2.30); g.add(c);
  }

  /* --- the platform: dressed stone, two risers down to the court */
  box(12.60, BASE, 5.60, 0, BASE / 2, -.10, stone);
  box(5.20, .20, .70, 0, .10, 2.86, stone);
  box(4.80, .20, .70, 0, .30, 2.60, stone);

  /* --- the wall. Whitewash over stone, a slate string course, stone again:
     the banding every temple wall in the valley is built from. */
  const SEG = HALF - IN, SX = IN + SEG / 2;
  [-1, 1].forEach(s => {
    box(SEG, .58, .56, s * SX, BASE + .29, Z, stone);
    box(SEG, 1.66, .52, s * SX, BASE + 1.41, Z, lime);
    box(SEG, .20, .64, s * SX, BASE + 2.34, Z, stone);
    box(SEG, 2.12, .50, s * SX, BASE + 3.50, Z, lime);
    /* a framed niche in each flank, the way the walls of a dwara are panelled */
    box(1.46, 1.42, .06, s * 3.70, 3.30, -.285, board, false);
    box(1.62, .13, .16, s * 3.70, 4.06, -.27, timber);
    box(1.62, .13, .16, s * 3.70, 2.54, -.27, timber);
    box(.13, 1.42, .16, s * 3.70 + s * .745, 3.30, -.27, timber);
    box(.13, 1.42, .16, s * 3.70 - s * .745, 3.30, -.27, timber);
  });
  /* the panel over the door, between the carved lintel and the jali band */
  box(3.00, .66, .50, 0, 4.81, Z, lime);
  box(12.10, .22, .58, 0, 5.25, Z, stone);

  /* --- the jali band: lattice over a dark board, mullions and rails in front */
  box(12.10, .94, .30, 0, 5.83, Z + .02, board);
  const jp = new THREE.Mesh(new THREE.PlaneGeometry(11.60, .90), jali);
  jp.position.set(0, 5.83, Z + .20); g.add(jp);
  for (let x = -5.50; x <= 5.51; x += 1.000) box(.11, .94, .16, x, 5.83, -.25, timber);
  box(12.10, .14, .20, 0, 5.43, -.25, timber);
  box(12.10, .14, .20, 0, 6.24, -.25, timber);

  /* --- the carved frieze, its dentil course and three brass medallions */
  box(12.30, .70, .74, 0, 6.71, Z + .06, timber);
  for (let x = -5.90; x <= 5.91; x += .46) box(.20, .20, .24, x, 6.26, -.055, timber);
  [-4.00, 0, 4.00].forEach(x => {
    box(.62, .62, .05, x, 6.71, -.115, board, false);
    const m = new THREE.Mesh(new THREE.TorusGeometry(.26, .05, 8, 22), brass);
    m.position.set(x, 6.71, -.085); g.add(m);
    box(.11, .11, .05, x, 6.71, -.08, brass);
  });

  /* --- the wall plate the roof lands on */
  box(12.60, .24, 1.05, 0, 7.16, Z + .14, timber);

  /* --- the porch: four square deodar posts, capitals, a beam and a purlin */
  [2.15, 4.75].forEach(ax => [-1, 1].forEach(s => {
    const px = s * ax;
    box(.44, .30, .44, px, BASE + .15, 2.30, stone);
    box(.38, 5.96, .38, px, BASE + 3.28, 2.30, timber);
    box(.58, .18, .58, px, 6.90, 2.30, timber);
  }));
  box(11.00, .30, .44, 0, 7.09, 2.30, timber);
  box(11.80, .22, .30, 0, 7.18, 3.28, timber);

  /* --- the roof: a shallow hipped pitch of slate slabs. No flare: the lift at
     the corners is what makes a roof read as a pagoda, and a Himachali pitch
     is dead flat with a heavy eave. */
  const roof = new THREE.Mesh(roofGeo(6.80, 2.55, 5.50, 1.38, .30, 0), slate);
  roof.position.set(0, 7.30, .95); roof.castShadow = true; roof.receiveShadow = true; g.add(roof);
  box(11.80, .22, .44, 0, 8.62, .95, slate);
  [-5.35, 5.35].forEach(x => box(.28, .26, .46, x, 8.68, .95, slate));

  /* --- the trishul on the ridge, the one mark the temple shares */
  (function trishul() {
    const t = new THREE.Group();
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(.035, .035, 1.40, 8), brass);
    shaft.position.y = .70; t.add(shaft);
    const bar = new THREE.Mesh(new THREE.BoxGeometry(.54, .05, .06), brass);
    bar.position.y = 1.06; t.add(bar);
    [-1, 0, 1].forEach(i => {
      const p = new THREE.Mesh(new THREE.CylinderGeometry(.028, .020, .54, 8), brass);
      p.position.set(i * .14, 1.32 - Math.abs(i) * .05, 0);
      p.rotation.z = -i * .22; t.add(p);
    });
    const k = new THREE.Mesh(new THREE.SphereGeometry(.075, 10, 8), brass);
    k.position.y = .28; t.add(k);
    t.position.set(0, 8.68, .95); t.scale.setScalar(.92); g.add(t);
  })();

  /* --- the doorway: pegged deodar jambs, a carved lintel, studded leaves */
  [-1, 1].forEach(s => {
    box(.34, 3.52, .74, s * 1.63, BASE + 1.76, Z + .02, timber);
    box(.30, .22, .86, s * 1.63, HEAD + .30, Z + .04, timber);
  });
  box(4.00, .40, .80, 0, 4.26, Z + .02, timber);
  for (let x = -1.75; x <= 1.76; x += .45) box(.16, .16, .18, x, 3.96, -.055, timber);
  box(3.20, .09, .06, 0, 4.26, -.125, brass);

  box(3.40, .16, .92, 0, BASE + .08, Z + .14, stone);

  [-1, 1].forEach(s => {
    const lx = s * .68;
    box(1.34, 3.18, .14, lx, BASE + 1.60, Z + .16, board);
    /* five raised boards a leaf, the way the door in the photograph is cut */
    for (let i = 0; i < 5; i++) box(.20, 2.96, .06, lx + (i - 2) * .25, BASE + 1.60, -.275, board);
    /* iron studs and two hinge straps */
    for (let r = 0; r < 6; r++) [-1, 1].forEach(c =>
      box(.09, .09, .07, lx + c * .40, BASE + .62 + r * .38, -.27, iron));
    box(.36, .12, .05, lx, BASE + 2.55, -.27, iron);
    box(.36, .12, .05, lx, BASE + 1.05, -.27, iron);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.14, .030, 8, 18), brass);
    ring.position.set(s * .42, BASE + 1.50, -.26); ring.castShadow = true; g.add(ring);
  });

  /* --- the bells under the porch, the gate's own voice */
  bell(0, 7.18, .90, .29);
  bell(-2.60, 7.14, .58, .18);
  bell(2.60, 7.14, .58, .18);

  /* --- the wall ends: low slate-capped piers, no outrigger wall */
  [-1, 1].forEach(s => {
    box(.72, 3.20, 1.05, s * 6.15, BASE + 1.60, Z, stone);
    box(.94, .18, 1.26, s * 6.15, BASE + 3.29, Z, slate);
  });

  /* the moon is behind the gate, so without a raking lamp in front the whole
     entrance renders as a black rectangle. This one is cool: the night is
     blue, and the warm light belongs to the two lamps on the door. */
  const face = new THREE.PointLight(0xbcc9d2, 2.40, 26, 1.7);
  face.position.set(0, 6.20, 11.0); g.add(face);
  const lamp = new THREE.PointLight(0xffb478, 1.20, 14, 1.9);
  lamp.position.set(0, 4.40, 1.70); g.add(lamp);
  const sill = new THREE.PointLight(0xff9a52, .55, 6.0, 2);
  sill.position.set(0, 2.00, 1.30); g.add(sill);
  /* the porch lamp thrown up into the rafters, so the slate soffit reads as
     stone slabs overhead instead of a black band */
  const eave = new THREE.PointLight(0xffbc84, .85, 8.5, 2);
  eave.position.set(0, 6.55, 2.60); g.add(eave);

  /* the group's own origin is the court, so the plinth sits on it */
  const GS = .62;
  g.position.set(0, 0, -8.6); g.scale.setScalar(GS);
  scene.add(g); WORLD.gate = g; WORLD.torii = g;
}

"""

s, _gn = re.subn(r"function buildTorii\(\) \{.*?\n\}\n\nfunction buildLantern",
                GATE_NEW + "\nfunction buildLantern", s, count=1, flags=re.S)
if _gn != 1:
    sys.exit("gate: the engine buildTorii was not found exactly once")

# ---------------------------------------------------------------- the lamps
# The engine's lantern is a Japanese stone toro: round base, round post, a
# pagoda cap and a finial. A Himachali approach is lit by a square stone pillar
# under a flat slate slab, so the silhouette changes while the glow, the light
# and every placement stay exactly as authored.
sub("""  const base = new THREE.Mesh(new THREE.CylinderGeometry(.44, .52, .26, 20), stone);
  base.position.y = .13; base.castShadow = true; g.add(base);
  const post = new THREE.Mesh(new THREE.CylinderGeometry(.15, .18, 1.02, 16), stone);
  post.position.y = .77; post.castShadow = true; g.add(post);
  const shelf = new THREE.Mesh(new THREE.CylinderGeometry(.42, .34, .13, 20), stone);
  shelf.position.y = 1.34; shelf.castShadow = true; g.add(shelf);

  const box = new THREE.Mesh(new THREE.BoxGeometry(.50, .50, .50), dark);
  box.position.y = 1.66; box.castShadow = true; g.add(box);
  const paneMat = new THREE.MeshBasicMaterial({ color: hdr(2.3, .30, .085), fog: false, toneMapped: false });
  [[0, 0, .256, 0], [0, 0, -.256, Math.PI], [.256, 0, 0, Math.PI / 2], [-.256, 0, 0, -Math.PI / 2]].forEach(p => {
    const pane = new THREE.Mesh(new THREE.PlaneGeometry(.34, .34), paneMat);
    pane.position.set(p[0], 1.66, p[2]); pane.rotation.y = p[3]; g.add(pane);
  });
  WORLD.lanternPane = WORLD.lanternPane || paneMat;

  const roof = new THREE.Mesh(new THREE.CylinderGeometry(.10, .62, .34, 4, 1), stone);
  roof.position.y = 2.06; roof.rotation.y = Math.PI / 4; roof.castShadow = true; g.add(roof);
  const brim = new THREE.Mesh(new THREE.CylinderGeometry(.66, .70, .07, 4, 1), stone);
  brim.position.y = 1.93; brim.rotation.y = Math.PI / 4; g.add(brim);
  const knob = new THREE.Mesh(new THREE.SphereGeometry(.09, 12, 10), stone);
  knob.position.y = 2.28; g.add(knob);
  const tip = new THREE.Mesh(new THREE.ConeGeometry(.055, .16, 10), stone);
  tip.position.y = 2.4; g.add(tip);""",
    """  const plinth = new THREE.Mesh(new THREE.BoxGeometry(.68, .10, .68), stone);
  plinth.position.y = .05; plinth.receiveShadow = true; g.add(plinth);
  const base = new THREE.Mesh(new THREE.BoxGeometry(.54, .22, .54), stone);
  base.position.y = .11; base.castShadow = true; base.receiveShadow = true; g.add(base);
  const post = new THREE.Mesh(new THREE.BoxGeometry(.24, 1.06, .24), stone);
  post.position.y = .76; post.castShadow = true; g.add(post);
  const collar = new THREE.Mesh(new THREE.BoxGeometry(.34, .10, .34), stone);
  collar.position.y = 1.30; collar.castShadow = true; g.add(collar);
  const shelf = new THREE.Mesh(new THREE.BoxGeometry(.48, .08, .48), stone);
  shelf.position.y = 1.38; shelf.castShadow = true; g.add(shelf);

  const box = new THREE.Mesh(new THREE.BoxGeometry(.46, .48, .46), dark);
  box.position.y = 1.66; box.castShadow = true; g.add(box);
  const paneMat = new THREE.MeshBasicMaterial({ color: hdr(2.2, 1.05, .50), fog: false, toneMapped: false });
  [[0, 0, .236, 0], [0, 0, -.236, Math.PI], [.236, 0, 0, Math.PI / 2], [-.236, 0, 0, -Math.PI / 2]].forEach(p => {
    const pane = new THREE.Mesh(new THREE.PlaneGeometry(.32, .32), paneMat);
    pane.position.set(p[0], 1.66, p[2]); pane.rotation.y = p[3]; g.add(pane);
  });
  WORLD.lanternPane = WORLD.lanternPane || paneMat;

  /* one slate slab over the cage, and a second course of stone above it */
  const roof = new THREE.Mesh(new THREE.BoxGeometry(.70, .10, .70), stone);
  roof.position.y = 1.94; roof.castShadow = true; g.add(roof);
  const brim = new THREE.Mesh(new THREE.BoxGeometry(.54, .09, .54), stone);
  brim.position.y = 2.03; brim.castShadow = true; g.add(brim);""")

sub("texGlow('rgba(255,120,60,.9)', 'rgba(255,60,24,.28)')",
    "texGlow('rgba(255,196,128,.9)', 'rgba(255,146,64,.28)')")
sub("new THREE.PointLight(0xff5a24, 2.6, 9, 2)",
    "new THREE.PointLight(0xffa552, 2.3, 9, 2)")

# --- the wordmark: smaller and higher, so the hall keeps its silhouette
sub("  const fill = narrow ? .96 : 1.00;", "  const fill = narrow ? .74 : .64;")
sub("  const base = hit(0, narrow ? -.16 : -.585);", "  const base = hit(0, narrow ? -.26 : -.42);")
# a ghosted wordmark: it belongs behind the hall, not on top of its steps
sub("        depthWrite: false, side: THREE.DoubleSide, fog: true, opacity: 1 }));",
    "        depthWrite: false, side: THREE.DoubleSide, fog: true, opacity: .58 }));")

# ---------------------------------------------------------------- stale prose
sub("/* ================================================= foreground layers (KAGE)",
    "/* ============================================ foreground layers (HIMALAYA)")
sub("   The transparent PNG library in secret-pathways-assets/foreground/png is",
    "   The transparent cut-out library in assets/kage/fg is")
sub('''   KAGE — a live Kyoto mountain temple, after dark.
   Everything on this page is generated at runtime: no photographs,
   no video, no external assets beyond three.js and two subset fonts.''',
    '''   HIMALAYA — a live mountain temple, a deodar forest and a ridge, after dark.
   The engine is the canonical ThreeUI Kage implementation; the world, lighting,
   camera rig and scroll wiring are generated at runtime exactly as authored.
   Only the plates, cut-outs, copy and material tints are Himachal.''')  

# ---------------------------------------------------------------- added styles
sub("opacity: .44 }));\n  halo.position.set(MOON.x, MOON.y, MOON.z - .3);",
    "opacity: .30 }));\n  halo.position.set(MOON.x, MOON.y, MOON.z - .3);")

PORTRAIT_CSS = '''
/* ====================================================== atmosphere portrait
   The one photograph of Ayush on the page: chapter 02. It stands in the live
   scene as a cut-out rather than sitting in a card, so the temple, mist and
   stone keep moving behind it. */
.dv{ font-family:'Onest',system-ui,-apple-system,sans-serif; font-weight:500; letter-spacing:.24em; }
.portrait-band{
  position:relative; display:grid; grid-template-columns:minmax(0,1fr) minmax(0,.82fr);
  gap:clamp(18px,4vw,58px); align-items:end;
  margin:0 0 clamp(34px,6vh,74px); padding-top:clamp(4px,1.4vh,16px);
}
.portrait-band figcaption{ max-width:36ch; padding-bottom:clamp(4px,2vh,26px); }
.portrait-band figcaption b{
  display:block; font-size:clamp(17px,1.55vw,23px); font-weight:400; letter-spacing:.01em;
  text-shadow:0 2px 22px rgba(3,6,8,.9);
}
.portrait-band figcaption > span{
  display:block; margin-top:9px; font-size:10px; font-weight:500; letter-spacing:.24em;
  text-transform:uppercase; color:var(--muted);
}
.portrait-band figcaption p{ margin:16px 0 0; max-width:34ch; }
/* The photographs are files, not renders: they arrive brighter than the scene
   they hang in, so the live windows take a light wash of the page ink. */
.peek-fr, .card-fr{ box-shadow:inset 0 0 0 999px rgba(4,7,10,.22); }
.portrait-band > img{
  width:min(100%,400px); height:auto; justify-self:end;
  filter:drop-shadow(0 28px 54px rgba(3,6,8,.78));
  /* the cut-out ends at the waist: fade the last band so the crop reads as the
     scene taking over rather than as a photograph sliced off */
  -webkit-mask-image:linear-gradient(#000 80%, transparent 99%);
          mask-image:linear-gradient(#000 80%, transparent 99%);
}
/* Chapter 02's near plane is the one place the cut-outs would stand in front of
   a paragraph rather than the frame: the pine goes, the grass drops below the
   last line of copy. */
[data-fg="gate"] .fg-pine{ display:none; }
[data-fg="gate"] .fg-grass{ left:-10%; bottom:-250px; width:clamp(380px,52vw,900px); }
@media (max-width:1080px){
  .portrait-band{ grid-template-columns:minmax(0,1fr) minmax(0,.9fr); }
  .portrait-band > img{ width:min(100%,330px); }
}
@media (max-width:820px){
  .portrait-band{ grid-template-columns:1fr; gap:14px; margin-bottom:clamp(28px,5vh,48px); }
  .portrait-band > img{ justify-self:start; order:-1; width:min(72vw,300px); }
  .portrait-band figcaption{ padding-bottom:0; }
}

/* ============================================================ deodar belt
   Two things the page was missing: trees at the edge of the frame, and the
   forest under the chapter named after one. The belt is composited from the
   same deodar specimen as the single tree and cropped by object-fit, so only
   the crowns and the first trunks show — it frames the page instead of
   standing on the reading. */
[data-fg="lessons"] .fg-grove{
  left:-5%; right:-5%; bottom:-12px; height:clamp(130px,20vh,230px);
}
[data-fg="lessons"] .fg-grove > img{
  width:100%; height:100%; object-fit:cover; object-position:50% 14%;
  filter:saturate(.70) brightness(.54);
}

/* ===================================================== forest field notes
   Three frames of the supplied photographs, graded into the night so the
   daylight belt does not arrive as a lit panel in a dark room. */
.field-notes{
  display:grid; grid-template-columns:repeat(3,minmax(0,1fr));
  gap:clamp(10px,1.6vw,26px);
  width:100%; max-width:min(100%,940px); margin:clamp(38px,6.5vh,78px) auto 0;
}
.field-notes figure{ margin:0; }
.fn-fr{
  display:block; position:relative; overflow:hidden; aspect-ratio:4/3;
  background:#080d10; box-shadow:inset 0 0 0 1px rgba(223,231,224,.13);
}
.fn-fr img{
  width:100%; height:100%; object-fit:cover; display:block;
  filter:saturate(.50) brightness(.50) contrast(1.12);
  transition:filter .8s var(--ease), transform 1.6s var(--ease-out);
}
.field-notes figure:hover .fn-fr img{ filter:saturate(.72) brightness(.74) contrast(1.04); transform:scale(1.05); }
.fn-fr::after{
  content:''; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(180deg, rgba(4,7,10,.06), rgba(4,7,10,.30) 62%, rgba(4,7,10,.66));
}
.field-notes figcaption{
  display:flex; justify-content:space-between; gap:10px; margin-top:10px;
  font-size:10px; letter-spacing:.18em; text-transform:uppercase; color:var(--muted);
}
.field-notes figcaption b{ font-weight:500; color:#a9b4ad; }
/* the closing chapter is a two-column grid whose right column carries the
   vertical ARRIVAL; the strip takes a row of its own across both columns */
body[data-layout-closing="b"] .fin .field-notes{
  grid-column:1 / -1; grid-row:4; justify-self:center;
  width:100%; max-width:min(100%,940px);
}
@media (max-width:820px){
  .field-notes{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; }
  .field-notes figure:first-child{ grid-column:1 / -1; }
  .field-notes figure:first-child .fn-fr{ aspect-ratio:16/10; }
  .field-notes figcaption span{ display:none; }
}
'''
sub("</style>\n</head>", PORTRAIT_CSS + "</style>\n</head>")

TOWER = r'''/* ---------------------------------------------------- the Bhimakali tower
   What the Sarahan photograph shows, in order: a whitewashed stone plinth, a
   square tower of deodar boarding five storeys tall, every storey stepping in
   under a shallow slate pent that projects past its own walls, and a brass
   finial above the last one. The eaves run dead level all the way round — the
   lift is in the stone coursing, not in the corners — which is the whole
   difference between this building and the swept-eave hall below it. */

/* the carved deodar jali a Himachali window carries: three mullions, a
   transom or two, and a row of teeth cut along the head. Mostly transparent,
   so the lamp behind it comes through the gaps. */
function texJali() {
  const W = 256, H = 320, c = cvs(W, H), x = c.getContext('2d');
  x.clearRect(0, 0, W, H);
  x.strokeStyle = 'rgba(16,11,7,.94)'; x.fillStyle = 'rgba(16,11,7,.94)';
  x.lineWidth = 22; x.strokeRect(11, 11, W - 22, H - 22);
  x.lineWidth = 9;
  [W / 4, W / 2, W * 3 / 4].forEach(v => {
    x.beginPath(); x.moveTo(v, 0); x.lineTo(v, H); x.stroke();
  });
  x.lineWidth = 8;
  [H * .42, H * .70].forEach(v => {
    x.beginPath(); x.moveTo(0, v); x.lineTo(W, v); x.stroke();
  });
  x.beginPath();
  for (let i = 0; i < 8; i++) {
    const w = W / 8, l = i * w;
    x.moveTo(l, 24); x.lineTo(l + w / 2, 58); x.lineTo(l + w, 24);
  }
  x.fill();
  return c;
}

/* quarried slate, not charred tile: lift the engine's near-black roof map to
   the pale grey the Sarahan photograph shows, keeping its ribs and relief */
function texSlate() {
  const src = lib('roof', () => texRoof());
  const W = src.map.width, H = src.map.height;
  const c = cvs(W, H), x = c.getContext('2d');
  x.drawImage(src.map, 0, 0);
  /* soften the glazed-tile ribs: under an eave they read as corrugated metal */
  x.globalAlpha = .40; x.fillStyle = '#7c7871'; x.fillRect(0, 0, W, H); x.globalAlpha = 1;
  x.globalCompositeOperation = 'lighter';
  x.fillStyle = 'rgba(96,94,88,.56)';
  x.fillRect(0, 0, W, H);
  x.globalCompositeOperation = 'source-over';
  return { map: c, normal: src.normal, rough: src.rough };
}

/* lime-washed stone — the plinth, the parapet and every eave fascia */
function texPlaster() {
  const W = 512, H = 512, c = cvs(W, H), x = c.getContext('2d');
  x.fillStyle = '#b8b4a7'; x.fillRect(0, 0, W, H);
  x.globalAlpha = .55; x.globalCompositeOperation = 'multiply';
  x.drawImage(fbmCanvas(W, H, 311, 5, 4, 1.2), 0, 0);
  x.globalAlpha = 1; x.globalCompositeOperation = 'source-over';
  const rnd = mulberry32(71);
  for (let i = 0; i < 46; i++) {
    const sx = rnd() * W, ww = 1 + rnd() * 6, top = rnd() * H * .4, len = H * (.2 + rnd() * .6);
    const g = x.createLinearGradient(0, top, 0, top + len);
    g.addColorStop(0, 'rgba(60,58,50,0)');
    g.addColorStop(.4, 'rgba(60,58,50,.10)');
    g.addColorStop(1, 'rgba(60,58,50,0)');
    x.fillStyle = g; x.fillRect(sx, top, ww, len);
  }
  const h = cvs(W, H), hx = h.getContext('2d');
  hx.fillStyle = '#8a8a8a'; hx.fillRect(0, 0, W, H);
  hx.globalAlpha = .5; hx.drawImage(fbmCanvas(W, H, 57, 5, 7, 1.1), 0, 0);
  return { map: c, normal: normalFromHeight(h, 1.4) };
}

function buildTempleHimachal() {
  const g = new THREE.Group();
  const F = PODIUM;

  /* The photograph reads as a light timber grid over dark boarding: pale
     deodar posts and rails, near-black panels, grey slate above. Held dark
     and close, the tower turns into a cardboard cut-out at forty metres. */
  const board = surface(wallWood(), [4, 2], { color: hdr(1.22, .94, .68), normal: 1.45 });
  const post  = surface(postWood(), [1, 1], { color: hdr(2.30, 1.86, 1.36), normal: 1.10, metalness: .03 });
  const beam  = surface(postWood(), [1, 1], { color: 0x2c2116, normal: 1.30 });
  /* the engine's roof map is charred tile: near-black by design. The temple
     borrows its relief, not its albedo. */
  const slate = surface(texSlate(), [1, 1],
    { color: 0xd2cec4, roughness: .86, metalness: .04, normal: .90 });
  const white = surface(texPlaster(), [3.6, 1.8], { color: 0xdedacd, roughness: .93, metalness: .01 });
  const stone = surface(texPlaster(), [3, 2], { color: 0x8c8d87, roughness: .95, metalness: .01 });
  const brass = new THREE.MeshStandardMaterial({ color: 0x9a7a34, roughness: .34, metalness: .82,
    emissive: 0x140e04, emissiveIntensity: .60 });

  /* The lamps. Every opening is a warm plane with a carved jali hung in front
     of it; both are merged at the end, so forty windows cost two draw calls. */
  const paper = new THREE.MeshBasicMaterial({ color: hdr(.46, .22, .085), fog: true, toneMapped: false });
  const jali  = new THREE.MeshBasicMaterial({ map: tx(texJali()), transparent: true,
    depthWrite: false, fog: true, opacity: .94 });
  WORLD.paper = paper;

  const glowG = [], jaliG = [], woodG = [], beamG = [], slateG = [], brassG = [], whiteG = [];

  /* One opening: jambs, a carved lintel, a deep sill, a centre mullion and two
     little brackets. ry turns the whole frame on to a side face. */
  function win(w, h, x, y, z, ry) {
    const t = .16, d = .28;
    const bar = (bw, bh, bd, ox, oy) => {
      const q = new THREE.BoxGeometry(bw, bh, bd);
      q.translate(ox, oy, 0); q.rotateY(ry); q.translate(x, y, z); woodG.push(q);
    };
    bar(w + t * 2.2, t * 1.15, d, 0,  h / 2 + t * .58);
    bar(w + t * 2.2, t * 1.55, d * 1.4, 0, -h / 2 - t * .78);
    bar(t, h, d, -w / 2 - t * .5, 0);
    bar(t, h, d,  w / 2 + t * .5, 0);
    bar(t * .55, h, d * .8, 0, 0);
    bar(.34, .20, d * 1.1, -w / 2 - t * 1.3, h / 2 - .12);
    bar(.34, .20, d * 1.1,  w / 2 + t * 1.3, h / 2 - .12);
    const p = new THREE.PlaneGeometry(w, h);
    p.rotateY(ry); p.translate(x, y, z); glowG.push(p);
    const j = new THREE.PlaneGeometry(w, h);
    j.rotateY(ry); j.translate(x + Math.sin(ry) * .045, y, z + Math.cos(ry) * .045); jaliG.push(j);
  }

  function mergeInto(list, mat, cast, order) {
    if (!list.length) return null;
    const m = new THREE.Mesh(mergeGeos(list), mat);
    m.castShadow = !!cast; m.receiveShadow = true;
    if (order) m.renderOrder = order;
    g.add(m); return m;
  }

  const TZ = TEMPLE_Z;

  /* ---- the terrace: one long stone platform, whitewashed at its edge,
          carrying the tower and both wings ------------------------------- */
  const terrace = new THREE.Mesh(new THREE.BoxGeometry(33, 1.7, 17.6), stone);
  terrace.position.set(0, F + .85, TZ + .6);
  terrace.castShadow = true; terrace.receiveShadow = true; g.add(terrace);
  whiteG.push(new THREE.BoxGeometry(33.3, .42, 17.9).translate(0, F + 1.50, TZ + .6));
  /* the last four risers, coming up off the head of the long flight */
  const risers = [];
  for (let i = 0; i < 4; i++) {
    const hh = 1.66 - i * .41;
    risers.push(new THREE.BoxGeometry(6.2 + i * .26, hh, .62)
      .translate(0, F + hh / 2, TZ + 9.45 + i * .60));
  }
  const riser = new THREE.Mesh(mergeGeos(risers), stone);
  riser.castShadow = true; riser.receiveShadow = true; g.add(riser);
  /* the low stone parapet either side of those risers */
  [-1, 1].forEach(s => {
    const pw = 9.8;
    const par = new THREE.Mesh(new THREE.BoxGeometry(pw, .62, .46), stone);
    par.position.set(s * (3.1 + pw / 2), F + 2.01, TZ + 9.4);
    par.castShadow = true; par.receiveShadow = true; g.add(par);
    slateG.push(new THREE.BoxGeometry(pw + .16, .13, .60)
      .translate(s * (3.1 + pw / 2), F + 2.38, TZ + 9.4));
  });

  /* ---- the tower base: one more whitewashed course under the boarding -- */
  const baseY = F + 2.45;
  const podium2 = new THREE.Mesh(new THREE.BoxGeometry(23, .75, 12.4), white);
  podium2.position.set(0, F + 2.08, TZ);
  podium2.castShadow = true; podium2.receiveShadow = true; g.add(podium2);

  /* ---- the tower: five storeys, each stepping out under its own pent ---- */
  const TIERS = [[9.4, 3.2, 2.05], [8.7, 2.7, 1.85], [8.0, 2.4, 1.65], [7.2, 2.1, 1.50], [6.4, 1.9, 1.35]];
  let y = baseY, apexY = 0;
  TIERS.forEach((t, i) => {
    const w = t[0], h = t[1], ov = t[2], hw = w / 2;
    const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, w), board);
    body.position.set(0, y + h / 2, TZ);
    body.castShadow = true; body.receiveShadow = true; g.add(body);

    /* the whitewashed floor band, the head beam, four corner posts and two
       mid posts a face — the frame the photograph reads first */
    whiteG.push(new THREE.BoxGeometry(w + .38, .20, w + .38).translate(0, y + .10, TZ));
    beamG.push(new THREE.BoxGeometry(w + .36, .18, w + .36).translate(0, y + h - .09, TZ));
    [-1, 1].forEach(sx => [-1, 1].forEach(sz =>
      woodG.push(new THREE.BoxGeometry(.34, h, .34).translate(sx * hw, y + h / 2, TZ + sz * hw))));
    const mid = hw * .52;
    [-1, 1].forEach(s => {
      woodG.push(new THREE.BoxGeometry(.24, h, .22).translate(s * mid, y + h / 2, TZ + hw));
      woodG.push(new THREE.BoxGeometry(.24, h, .22).translate(s * mid, y + h / 2, TZ - hw));
      woodG.push(new THREE.BoxGeometry(.22, h, .24).translate(hw, y + h / 2, TZ + s * mid));
      woodG.push(new THREE.BoxGeometry(.22, h, .24).translate(-hw, y + h / 2, TZ + s * mid));
    });

    /* the openings: two a face low down, one a face above */
    const wn = i < 2 ? 2 : 1;
    const ww = Math.min(1.46, w * .17), wh = Math.min(1.62, h * .52);
    for (let k = 0; k < wn; k++) {
      const off = (k - (wn - 1) / 2) * (ww + 1.30);
      win(ww, wh, off, y + h * .54, TZ + hw + .03, 0);
      win(ww, wh, off, y + h * .54, TZ - hw - .03, Math.PI);
      for (const s of [-1, 1])
        win(ww, wh, s * (hw + .03), y + h * .54, TZ + off, s > 0 ? Math.PI / 2 : -Math.PI / 2);
    }

    /* the carved corbel band that throws the pent out past the wall. Deodar,
       not black: as silhouettes these read as a comb of slots, not brackets. */
    const nb = Math.max(4, Math.round(w / 1.18));
    for (let k = 0; k < nb; k++) {
      const bx = -hw + .62 + k * ((w - 1.24) / (nb - 1));
      woodG.push(new THREE.BoxGeometry(.22, .34, ov * .92).translate(bx, y + h - .20, TZ + hw + ov * .34));
      woodG.push(new THREE.BoxGeometry(.22, .34, ov * .92).translate(bx, y + h - .20, TZ - hw - ov * .34));
      woodG.push(new THREE.BoxGeometry(ov * .92, .34, .22).translate(hw + ov * .34, y + h - .20, TZ + bx));
      woodG.push(new THREE.BoxGeometry(ov * .92, .34, .22).translate(-hw - ov * .34, y + h - .20, TZ + bx));
    }

    /* eave fascia, then the pent itself — dead level, quarried slate, thrown
       well past the wall so it lays a hard shadow across the boarding */
    const ew = w + ov * 2, pitch = i < 2 ? .88 : .80, rim = hw + ov - .06;
    /* the eave edge: a thick stone fascia with a thin slate cap over it, so
       seen from below the pent has a body and not just a line */
    slateG.push(new THREE.BoxGeometry(ew + .14, .28, .18).translate(0, y + h + .02, TZ + rim));
    slateG.push(new THREE.BoxGeometry(ew + .14, .28, .18).translate(0, y + h + .02, TZ - rim));
    slateG.push(new THREE.BoxGeometry(.18, .28, ew + .14).translate(rim, y + h + .02, TZ));
    slateG.push(new THREE.BoxGeometry(.18, .28, ew + .14).translate(-rim, y + h + .02, TZ));
    whiteG.push(new THREE.BoxGeometry(ew + .04, .10, .12).translate(0, y + h + .17, TZ + rim));
    whiteG.push(new THREE.BoxGeometry(ew + .04, .10, .12).translate(0, y + h + .17, TZ - rim));
    whiteG.push(new THREE.BoxGeometry(.12, .10, ew + .04).translate(rim, y + h + .17, TZ));
    whiteG.push(new THREE.BoxGeometry(.12, .10, ew + .04).translate(-rim, y + h + .17, TZ));
    const roof = new THREE.Mesh(roofGeo(ew / 2, ew / 2, 0, pitch, .44, .02), slate);
    roof.position.set(0, y + h, TZ); roof.castShadow = true; g.add(roof);

    /* a brass spike stands at each corner of every pent, the way the small
       finials do in the photograph */
    [-1, 1].forEach(sx => [-1, 1].forEach(sz =>
      brassG.push(new THREE.ConeGeometry(.05, .58, 5)
        .translate(sx * rim, y + h + .28, TZ + sz * rim))));

    /* two rails tie the posts: the horizontal half of the timber grid */
    [.24, .80].forEach(f => {
      woodG.push(new THREE.BoxGeometry(w + .06, .10, .17).translate(0, y + h * f, TZ + hw + .03));
      woodG.push(new THREE.BoxGeometry(w + .06, .10, .17).translate(0, y + h * f, TZ - hw - .03));
      woodG.push(new THREE.BoxGeometry(.17, .10, w + .06).translate(hw + .03, y + h * f, TZ));
      woodG.push(new THREE.BoxGeometry(.17, .10, w + .06).translate(-hw - .03, y + h * f, TZ));
    });

    apexY = y + h + pitch;
    y += h + pitch * .62;
  });

  /* the finial: lotus, mast, kalash, trishul — the one bright thing up here */
  brassG.push(new THREE.CylinderGeometry(.55, .82, .30, 12).translate(0, apexY + .12, TZ));
  brassG.push(new THREE.CylinderGeometry(.10, .15, 2.5, 10).translate(0, apexY + 1.52, TZ));
  brassG.push(new THREE.SphereGeometry(.38, 14, 10).translate(0, apexY + 2.34, TZ));
  brassG.push(new THREE.CylinderGeometry(.09, .09, .26, 10).translate(0, apexY + 2.73, TZ));
  brassG.push(new THREE.CylinderGeometry(.045, .045, 1.4, 6).translate(0, apexY + 3.45, TZ));
  brassG.push(new THREE.BoxGeometry(.72, .05, .05).translate(0, apexY + 3.52, TZ));
  [-.30, 0, .30].forEach((dx, k) =>
    brassG.push(new THREE.ConeGeometry(.052, k ? 1.10 : .80, 6)
      .translate(dx, apexY + 3.9 + (k ? -.24 : 0), TZ)));
  WORLD.templeTop = apexY + 4.9;

  /* ---- the door: a deep carved opening, under a veranda that carries the
          lowest pent across the width of the front ---------------------- */
  const dY = baseY, dH = 2.7, dW = 2.15, dZ = TZ + 4.7;
  const doorTrim = new THREE.Mesh(mergeGeos([
    new THREE.BoxGeometry(dW + .90, .34, .52).translate(0, dY + dH + .17, dZ + .10),
    new THREE.BoxGeometry(.34, dH + .10, .52).translate(-(dW / 2 + .42), dY + dH / 2, dZ + .10),
    new THREE.BoxGeometry(.34, dH + .10, .52).translate( (dW / 2 + .42), dY + dH / 2, dZ + .10),
    new THREE.BoxGeometry(dW + 1.0, .18, .62).translate(0, dY + dH + .38, dZ + .14)
  ]), beam);
  doorTrim.castShadow = true; g.add(doorTrim);
  [-1, 1].forEach(s => {
    const leaf = new THREE.Mesh(new THREE.BoxGeometry(dW / 2 - .04, dH, .14), beam);
    leaf.position.set(s * dW / 4, dY + dH / 2, dZ + .05); leaf.castShadow = true; g.add(leaf);
    for (let r = 0; r < 3; r++)
      brassG.push(new THREE.SphereGeometry(.045, 6, 5)
        .translate(s * dW / 4, dY + .62 + r * .74, dZ + .14));
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.13, .022, 6, 12), brass);
    ring.position.set(s * .30, dY + 1.45, dZ + .16); g.add(ring);
  });

  /* the veranda posts, tucked under the first pent's outer edge */
  const vTop = baseY + 3.16;
  [-1, 1].forEach(s => {
    const vp = new THREE.Mesh(new THREE.BoxGeometry(.32, vTop - (F + 1.7), .32), post);
    vp.position.set(s * 2.8, (vTop + F + 1.7) / 2, dZ + 1.9); vp.castShadow = true; g.add(vp);
    const cap = new THREE.Mesh(new THREE.BoxGeometry(.58, .20, .58), beam);
    cap.position.set(s * 2.8, vTop - .10, dZ + 1.9); g.add(cap);
    const foot = new THREE.Mesh(new THREE.BoxGeometry(.54, .26, .54), white);
    foot.position.set(s * 2.8, F + 1.7 + .13, dZ + 1.9); g.add(foot);
  });
  const vBeam = new THREE.Mesh(new THREE.BoxGeometry(6.4, .26, .34), beam);
  vBeam.position.set(0, vTop - .30, dZ + 1.9); vBeam.castShadow = true; g.add(vBeam);
  /* two lamps hanging from it, at the door */
  [-1, 1].forEach(s => {
    brassG.push(new THREE.CylinderGeometry(.016, .016, .34, 5).translate(s * 1.55, vTop - .58, dZ + 1.9));
    brassG.push(new THREE.CylinderGeometry(.13, .19, .32, 9).translate(s * 1.55, vTop - .90, dZ + 1.9));
    brassG.push(new THREE.SphereGeometry(.055, 7, 5).translate(s * 1.55, vTop - 1.10, dZ + 1.9));
  });

  /* ---- the wings: long low halls either side, on the same terrace ---- */
  [-1, 1].forEach(s => {
    const len = 11, hgt = 3.3, dep = 5.2;
    const cx = s * 10.9, cz = TZ + 2.1, wy = F + 1.7;
    const wbase = new THREE.Mesh(new THREE.BoxGeometry(len + .5, .55, dep + .5), stone);
    wbase.position.set(cx, wy + .275, cz);
    wbase.castShadow = true; wbase.receiveShadow = true; g.add(wbase);
    const wing = new THREE.Mesh(new THREE.BoxGeometry(len, hgt, dep), board);
    wing.position.set(cx, wy + .55 + hgt / 2, cz);
    wing.castShadow = true; wing.receiveShadow = true; g.add(wing);
    /* the whitewashed lower wall, with the deodar posts standing proud of it */
    whiteG.push(new THREE.BoxGeometry(len + .03, .95, dep + .03)
      .translate(cx, wy + .55 + .475, cz));

    /* the boarded wall is framed: sill, head, and a post every bay */
    beamG.push(new THREE.BoxGeometry(len + .30, .20, dep + .34).translate(cx, wy + .66, cz));
    beamG.push(new THREE.BoxGeometry(len + .30, .18, dep + .34).translate(cx, wy + .55 + hgt - .08, cz));
    const bays = 4;
    for (let k = 0; k <= bays; k++)
      woodG.push(new THREE.BoxGeometry(.26, hgt, .26)
        .translate(cx - len / 2 + k * (len / bays), wy + .55 + hgt / 2, cz + dep / 2));
    const bw = 1.30, bh = 1.55;
    for (let k = 0; k < bays; k++) {
      const wx = cx + (k - (bays - 1) / 2) * (len / bays);
      win(bw, bh, wx, wy + .55 + hgt * .52, cz + dep / 2 + .03, 0);
    }
    /* the pent, level, with its own corbel band and a bell at each end */
    const ov = 1.15, ew2 = len + ov * 2, ed = dep + ov * 2;
    for (let k = 0; k < 7; k++) {
      const bx = cx - len / 2 + .8 + k * ((len - 1.6) / 6);
      beamG.push(new THREE.BoxGeometry(.24, .40, ov * .9)
        .translate(bx, wy + .55 + hgt - .22, cz + dep / 2 + ov * .34));
    }
    const wr = new THREE.Mesh(roofGeo(ew2 / 2, ed / 2, 1.4, 1.10, .30, .03), slate);
    wr.position.set(cx, wy + .55 + hgt, cz); wr.castShadow = true; g.add(wr);
    slateG.push(new THREE.BoxGeometry(ew2 + .1, .24, .14)
      .translate(cx, wy + .55 + hgt + .07, cz + ed / 2 - .06));
    [-1, 1].forEach(e => {
      const bx = cx + e * (len / 2 - .5), bz = cz + dep / 2 + ov * .55;
      brassG.push(new THREE.CylinderGeometry(.015, .015, .36, 5).translate(bx, wy + .55 + hgt - .10, bz));
      brassG.push(new THREE.CylinderGeometry(.09, .13, .22, 9).translate(bx, wy + .55 + hgt - .36, bz));
    });
  });

  mergeInto(woodG, post, true);
  mergeInto(beamG, beam, true);
  mergeInto(slateG, slate, false);
  mergeInto(brassG, brass, false);
  mergeInto(whiteG, white, true);
  mergeInto(glowG, paper, false);
  mergeInto(jaliG, jali, false, 3);

  /* one warm lamp at the door, so the veranda has depth under the pent */
  const doorLamp = new THREE.PointLight(0xffa860, .42, 11, 2);
  doorLamp.position.set(0, dY + 2.5, dZ + 2.2); g.add(doorLamp);
  /* a low raking fill on the facade only. The moon is behind the tower, so
     without it the posts, the slate and the window frames are a silhouette;
     kept below the eaves, it also lights the rafters from underneath. */
  const facade = new THREE.PointLight(0xc2ab8e, 4.0, 38, 1.8);
  facade.position.set(2, F + 4.6, TZ + 16); g.add(facade);
  /* and the warm spill the lamps throw up the boarding above the veranda */
  const wash = new THREE.PointLight(0xff9a52, 1.9, 16, 1.7);
  wash.position.set(0, baseY + 3.2, dZ + 3.0); g.add(wash);

  scene.add(g); WORLD.temple = g;

  const spill = new THREE.Mesh(new THREE.PlaneGeometry(30, 16),
    new THREE.MeshBasicMaterial({ map: tx(texGlow('rgba(255,150,66,.80)', 'rgba(240,96,26,.24)')),
      transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, fog: false, opacity: .30 }));
  spill.position.set(0, F + 3.0, TEMPLE_Z + 5.6); spill.renderOrder = 2;
  scene.add(spill); WORLD.hallHalo = spill;

  const mist = new THREE.Mesh(new THREE.PlaneGeometry(64, 20),
    new THREE.MeshBasicMaterial({ map: tx(texGlow('rgba(150,178,190,.62)', 'rgba(104,138,154,.20)')),
      transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, fog: false, opacity: .17 }));
  mist.position.set(0, F - 1.4, TEMPLE_Z + 10); mist.renderOrder = 2; scene.add(mist);

  return true;
}

'''

sub("function buildTemple() {\n  const g = new THREE.Group();",
    TOWER + "function buildTemple() {\n  if (buildTempleHimachal()) return;\n  const g = new THREE.Group();")

OUT.write_text(s, encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} — {len(s):,} bytes "
      f"(source {len(original):,}), {s.count(chr(10)) + 1} lines")
