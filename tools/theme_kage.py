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
      <img src="assets/kage/fg/pine-tree.webp" alt="" width="1024" height="1438" loading="lazy" decoding="async">
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
      <img src="assets/kage/fg/basalt-stones.webp" alt="" width="1536" height="996" loading="lazy" decoding="async">
    </span>
  </div>
''',
    "lessons": '''  <div class="fg" data-fg="lessons" aria-hidden="true">
    <span class="fg-el fg-pine fg-el--flip" data-fg-in="right">
      <img src="assets/kage/fg/pine-tree.webp" alt="" width="1024" height="1438" loading="lazy" decoding="async">
    </span>
    <span class="fg-el fg-stones" data-fg-in="up">
      <img src="assets/kage/fg/basalt-stones.webp" alt="" width="1536" height="996" loading="lazy" decoding="async">
    </span>
    <span class="fg-el fg-grass" data-fg-in="up">
      <img src="assets/kage/fg/tall-grass.webp" alt="" width="1717" height="916" loading="lazy" decoding="async">
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
    <span class="fg-el fg-pine" data-fg-in="left">
      <img src="assets/kage/fg/pine-tree.webp" alt="" width="1024" height="1438" loading="lazy" decoding="async">
    </span>
  </div>
''',
    "foot": '''  <div class="fg" data-fg="foot" aria-hidden="true">
    <span class="fg-el fg-grass" data-fg-in="up">
      <img src="assets/kage/fg/tall-grass.webp" alt="" width="1717" height="916" loading="lazy" decoding="async">
    </span>
    <span class="fg-el fg-stones" data-fg-in="up">
      <img src="assets/kage/fg/basalt-stones.webp" alt="" width="1536" height="996" loading="lazy" decoding="async">
    </span>
  </div>
''',
}
for key, block in FG.items():
    pattern = re.compile(r'  <div class="fg" data-fg="%s".*?\n  </div>\n' % key, re.S)
    s, n = pattern.subn(block, s, count=1)
    if n != 1:
        sys.exit(f"fg block {key}: {n} matches")

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

# foliage: deodar green rather than red maple
sub("    map: tx(texLeaf()), color: 0x2b0406, alphaTest: .42, side: THREE.DoubleSide,",
    "    map: tx(texLeaf()), color: 0x24331a, alphaTest: .42, side: THREE.DoubleSide,")
sub("emissive: 0x080000, emissiveIntensity: .12",
    "emissive: 0x030703, emissiveIntensity: .12")

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

# the gate: timber and slate instead of vermilion lacquer, with its own roof
sub('''  const lac = surface(lib('lacquer', () => texLacquer()), [2, 2],
    { color: hdr(1.72, 1.02, .94), roughness: .92, metalness: .05, normal: .75 });
  const gold = new THREE.MeshStandardMaterial({ color: 0x7a5d2a, roughness: .50, metalness: .60 });''',
    '''  const lac = surface(postWood(), [2, 1],
    { color: hdr(1.16, .96, .74), roughness: .88, metalness: .03, normal: .9 });
  const gold = new THREE.MeshStandardMaterial({ color: 0x4a382a, roughness: .62, metalness: .22 });''')

# --- the gate crown: square-cut deodar instead of the torii's upward sweep
sub('''  /* shimaki + kasagi — the two crowning beams, swept upward at the ends */
  function beamPath(half, rise, power) {
    const p = [];
    for (let i = 0; i <= 26; i++) {
      const u = i / 26 * 2 - 1;
      p.push(new THREE.Vector3(u * half, Math.pow(Math.abs(u), power) * rise, 0));
    }
    return p;
  }
  const shimaki = new THREE.Mesh(sweepPoly(beamPath(5.05, .40, 2.6),
    [[-.30, -.19], [.30, -.19], [.32, .06], [.28, .21], [-.28, .21], [-.32, .06]]), lac);
  shimaki.position.set(0, BASE + H - .52, 0); shimaki.castShadow = true; g.add(shimaki);

  const kasagi = new THREE.Mesh(sweepPoly(beamPath(5.85, .62, 2.4),
    [[-.42, -.24], [.42, -.24], [.46, .04], [.30, .28], [-.30, .28], [-.46, .04]]), lac);
  kasagi.position.set(0, BASE + H + .96, 0); kasagi.castShadow = true; g.add(kasagi);
  /* a black lacquer cap along the top of the kasagi */
  const cap = new THREE.Mesh(sweepPoly(beamPath(5.95, .62, 2.4),
    [[-.48, .22], [.48, .22], [.48, .34], [-.48, .34]]),
    new THREE.MeshStandardMaterial({ color: 0x120c0c, roughness: .42, metalness: .14 }));
  cap.position.set(0, BASE + H + .96, 0); g.add(cap);''',
    '''  /* The crown. A torii lifts its lintels at the ends; a Himachali entrance is
     square-cut deodar under a slate pitch, so both beams run dead level. */
  const shimaki = new THREE.Mesh(new THREE.BoxGeometry(10.1, .34, .46), lac);
  shimaki.position.set(0, BASE + H - .52, 0); shimaki.castShadow = true; g.add(shimaki);

  const kasagi = new THREE.Mesh(new THREE.BoxGeometry(11.7, .40, .52), lac);
  kasagi.position.set(0, BASE + H + .58, 0); kasagi.castShadow = true; g.add(kasagi);
  /* the cap rail the roof sits on */
  const cap = new THREE.Mesh(new THREE.BoxGeometry(11.9, .22, .58), lac);
  cap.position.set(0, BASE + H + .96, 0); g.add(cap);''')

# --- the wordmark: smaller and higher, so the hall keeps its silhouette
sub("  const fill = narrow ? .96 : 1.00;", "  const fill = narrow ? .74 : .64;")
sub("  const base = hit(0, narrow ? -.16 : -.585);", "  const base = hit(0, narrow ? -.26 : -.42);")
# a ghosted wordmark: it belongs behind the hall, not on top of its steps
sub("        depthWrite: false, side: THREE.DoubleSide, fog: true, opacity: 1 }));",
    "        depthWrite: false, side: THREE.DoubleSide, fog: true, opacity: .58 }));")

# --- foliage: deodar green, not maple red
sub("    tx.fillStyle = hex(96 + v * 96, 14 + v * 22, 16 + v * 18);",
    "    tx.fillStyle = hex(24 + v * 30, 50 + v * 44, 22 + v * 22);")

sub('''  cap.position.set(0, BASE + H + .96, 0); g.add(cap);''',
    '''  cap.position.set(0, BASE + H + .96, 0); g.add(cap);

  /* Himachali roof over the gate. A kath-kuni entrance is a timber frame under
     a slate pitch, so the crown gets a real roof instead of the bare lintel. */
  const gateSlate = surface(lib('roof', () => texRoof()), [1, 1],
    { color: 0x3b444c, roughness: .82, metalness: .08, normal: 1.3 });
  const gateRoof = new THREE.Mesh(roofGeo(6.15, 2.55, 1.05, 1.0, .20, .30), gateSlate);
  gateRoof.position.set(0, BASE + H + 1.30, 0); gateRoof.castShadow = true; g.add(gateRoof);
  const gateRidge = new THREE.Mesh(new THREE.BoxGeometry(4.4, .26, .38), gateSlate);
  gateRidge.position.set(0, BASE + H + 2.32, 0); gateRidge.castShadow = true; g.add(gateRidge);''')

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
