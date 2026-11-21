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
# the moon: a pale Himalayan moon instead of the vermilion one
sub("new THREE.MeshBasicMaterial({ map: tx(texMoon()), color: hdr(3.6, .64, .61),",
    "new THREE.MeshBasicMaterial({ map: tx(texMoon()), color: hdr(1.08, .98, .84),")
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

OUT.write_text(s, encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} — {len(s):,} bytes "
      f"(source {len(original):,}), {s.count(chr(10)) + 1} lines")
