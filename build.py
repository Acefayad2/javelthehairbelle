#!/usr/bin/env python3
"""Generates index.html. Every gallery item points at the Instagram post it came from."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
DIMS = json.loads((ROOT / "assets/dims.json").read_text())
IG = "https://www.instagram.com/javelthehairbelle/"
DM = "https://ig.me/m/javelthehairbelle"
DM_ALT = "https://ig.me/m/javelxo"


def icon(name):
    return (ROOT / f"assets/icons/{name}.svg").read_text().replace("<svg ", '<svg class="icon" aria-hidden="true" ', 1)


# (photo id, group, caption from the post, alt text describing the photo)
LOCS, BRAIDS, WIGS = "locs", "braids", "wigs"
GALLERY = [
    ("Ddz5wMfick7_i1", BRAIDS, "Boho Braids never disappoint", "Long boho braids with curly pieces, seen from behind"),
    ("De4iuTrFjDi_i0", LOCS, "It's getting tooooo icy out here", "Fresh retwist with clean zigzag parts, seen from above"),
    ("Ddg3wsXlnAs_i2", WIGS, "Wig Install on the CEO @javelxo", "Javel smiling in a honey blonde curled wig with bangs"),
    ("DeUgit7ljA8_i1", LOCS, "Two Strand Retwist", "Two strand retwist on shoulder length locs"),
    ("DeCutHTJZ0e_i0", BRAIDS, "Highlighted boho braids", "Long highlighted boho braids in golden blonde and black"),
    ("De0pLo7Fg4z_i1", LOCS, "Two Strand Retwist", "Two strand retwist with neat parts, seen from above"),
    ("DeW0W3KBqu6_i0", f"{BRAIDS} {WIGS}", "Fulani Braids + Half Wig Install", "Fulani braids at the front with a curly half wig"),
    ("Ddl0-rFB58I_i0", LOCS, "We heard winters coming so we had to bring out the ice", "Chunky black twists with clean square parts"),
    ("DdANRCtiXlJ_i0", LOCS, "Good reliable retwist", "Retwisted locs with straight parts, seen from behind"),
    ("DeZpnrmBKJW_i0", BRAIDS, "This color", "Boho braids with golden brown highlights and crisp parts"),
    ("De4iTuHhBvc_i0", LOCS, "Rate the retwist 1-10", "Retwist with zigzag parts on locs"),
    ("Ddg3wsXlnAs_i0", WIGS, "Wig Install on the CEO @javelxo", "Side view of a honey blonde wig with soft curls"),
    ("DeUgit7ljA8_i0", LOCS, "Two Strand Retwist", "Two strand retwist seen from behind in a living room"),
    ("Ddz5wMfick7_i0", BRAIDS, "Boho Braids never disappoint", "Boho braids with curly ends, close view from behind"),
    ("De4RaWKBJGE_i0", LOCS, "Retwist Szn", "Retwisted locs in warm window light, side view"),
    ("De4iuTrFjDi_i2", LOCS, "It's getting tooooo icy out here", "Close view of a retwist with detailed parts"),
    ("De0pLo7Fg4z_i0", LOCS, "Two Strand Retwist", "Two strand retwist from the side"),
    ("DdANRCtiXlJ_i1", LOCS, "Good reliable retwist", "Retwisted locs with neat parts, angled from the front"),
    ("Ddg3wsXlnAs_i1", WIGS, "Wig Install on the CEO @javelxo", "Javel posing in a blonde curled wig with bangs"),
    ("De4iuTrFjDi_i1", LOCS, "It's getting tooooo icy out here", "Retwist with zigzag parts, side angle"),
    ("DdANRCtiXlJ_i2", LOCS, "Good reliable retwist", "Long locs freshly retwisted, seen from behind"),
]
REELS = {"De4iTuHhBvc", "De4RaWKBJGE", "DeZpnrmBKJW", "DeW0W3KBqu6", "DeCutHTJZ0e", "Ddl0-rFB58I"}

CLIPS = [
    ("De4iuTrFjDi_v0", "Retwist close-up video"),
    ("DeUgit7ljA8_v0", "Two strand retwist close-up video"),
    ("Ddz5wMfick7_v0", "Boho braids close-up video"),
    ("De0pLo7Fg4z_v0", "Two strand retwist video from the side"),
]


def style_for(caption):
    """Which booking option a gallery photo preselects, based on its caption."""
    c = caption.lower()
    for key, style in (("highlighted", "Highlighted boho braids"), ("boho", "Boho braids"), ("this color", "Boho braids"),
                       ("fulani", "Fulani braids"), ("wig", "Wig install"), ("two strand", "Two strand retwist"),
                       ("winters", "Twists")):
        if key in c:
            return style
    return "Retwist"


# Every option comes from a caption or hashtag on her posts.
STYLES = ["Retwist", "Two strand retwist", "Twists", "Boho braids", "Highlighted boho braids",
          "Fulani braids", "Wig install", "Half wig install", "Something else"]


def post_url(pid):
    sc = pid.rsplit("_", 1)[0]
    return f"https://www.instagram.com/{'reel' if sc in REELS else 'p'}/{sc}/"


def gallery_html():
    out = []
    for i, (pid, group, cap, alt) in enumerate(GALLERY):
        w, h = DIMS[pid]
        out.append(
            f'<figure class="shot" data-group="{group}">'
            f'<button type="button" data-index="{i}" data-full="assets/photos/{pid}-lg.webp" '
            f'data-post="{post_url(pid)}" data-caption="{escape(cap, quote=True)}" data-style="{style_for(cap)}" aria-label="Open photo: {escape(alt, quote=True)}">'
            f'<img src="assets/photos/{pid}.webp" alt="{escape(alt, quote=True)}" width="{w}" height="{h}" loading="lazy" decoding="async">'
            f"</button></figure>"
        )
    return "\n        ".join(out)


def comb_svg():
    teeth = "".join(f'<rect x="{14 + i * 16}" y="34" width="8" height="150" rx="4"/>' for i in range(39))
    return (
        '<svg class="comb" viewBox="0 0 640 190" aria-hidden="true"><defs><linearGradient id="chrome" x1="0" y1="0" x2="1" y2=".25">'
        '<stop offset="0" stop-color="#6f737c"/><stop offset=".3" stop-color="#eef0f3"/><stop offset=".52" stop-color="#8e929b"/>'
        '<stop offset=".75" stop-color="#f7f8fa"/><stop offset="1" stop-color="#6f737c"/></linearGradient></defs>'
        f'<g fill="url(#chrome)">{teeth}<rect width="640" height="52" rx="24"/></g>'
        '<rect x="20" y="20" width="600" height="6" rx="3" fill="#e58db5"/></svg>'
    )


def style_options():
    return "\n            ".join(
        f'<label class="chip"><input type="radio" name="style" value="{s}" required><span>{s}</span></label>' for s in STYLES
    )


def clips_html():
    return "\n        ".join(
        f'<video muted loop playsinline preload="none" poster="assets/clips/{c}.jpg" aria-label="{escape(l, quote=True)}">'
        f'<source src="assets/clips/{c}.mp4" type="video/mp4"></video>'
        for c, l in CLIPS
    )


SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "HairSalon",
    "name": "Javel The Hair Belle",
    "description": "Hairstylist based in Silver Spring, MD. Retwists, braids and wig installs.",
    "areaServed": "Silver Spring, MD",
    "sameAs": [IG],
})

PAGE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Javel The Hair Belle | Hairstylist in Silver Spring, MD</title>
<meta name="description" content="Retwists, braids and wig installs by Javel, a teen beginner stylist based in Silver Spring, MD. See her work and request an appointment.">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#ffffff">
<meta property="og:title" content="Javel The Hair Belle">
<meta property="og:description" content="Retwists, braids and wig installs in Silver Spring, MD. Request an appointment online.">
<meta property="og:type" content="website">
<meta property="og:image" content="https://javelthehairbelle.netlify.app/assets/clips/De4iuTrFjDi_v0.jpg">
<link rel="icon" href="assets/brand/icon-180.png">
<link rel="apple-touch-icon" href="assets/brand/icon-180.png">
<link rel="preload" href="assets/fonts/BodoniModa-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/photos/De4iuTrFjDi_i0-lg.webp" as="image">
<link rel="preload" href="assets/brand/logo-intro.webp" as="image">
<link rel="stylesheet" href="styles.css">
<script>try{{if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&!sessionStorage.getItem('intro-seen'))document.documentElement.classList.add('play-intro')}}catch(e){{}}</script>
<script type="application/ld+json">{SCHEMA}</script>
</head>
<body>
<div class="intro">
  <svg width="0" height="0" aria-hidden="true"><filter id="tangle"><feTurbulence type="fractalNoise" baseFrequency=".018 .05" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="34" xChannelSelector="R" yChannelSelector="G"/></filter></svg>
  <div class="intro-stage">
    <img class="intro-tangled" src="assets/brand/logo-intro.webp" alt="" width="745" height="340">
    <img class="intro-clean" src="assets/brand/logo-intro.webp" alt="Javel The Hair Belle" width="745" height="340">
    <span class="intro-shine"></span>
    <div class="intro-track">{comb_svg()}</div>
  </div>
  <button class="intro-skip" type="button">Skip intro</button>
</div>

<a class="skip" href="#main">Skip to content</a>

<header class="top">
  <div class="wrap top-row">
    <a class="logo" href="#main" aria-label="Javel The Hair Belle, back to top"><img src="assets/brand/logo.png" alt="Javel The Hair Belle logo" width="149" height="68"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">{icon("list")}</button>
    <nav id="nav" aria-label="Main">
      <a href="#styles">Styles</a>
      <a href="#work">Work</a>
      <a href="#about">About</a>
      <a class="btn btn-small" href="#book">Book</a>
    </nav>
  </div>
</header>

<main id="main">
  <section class="hero wrap">
    <div class="hero-copy">
      <h1>Retwists, braids and <em>wig installs</em></h1>
      <p>Styled by Javel, a teen beginner stylist based in Silver Spring, MD.</p>
      <div class="actions">
        <a class="btn" href="#book">Book now</a>
        <a class="btn btn-ghost" href="#work">See the work</a>
      </div>
    </div>
    <div class="hero-art">
      <img class="a" src="assets/photos/De4iuTrFjDi_i0-lg.webp" alt="Fresh retwist with clean zigzag parts, seen from above" width="1050" height="1400" fetchpriority="high">
      <img class="b" src="assets/photos/DeCutHTJZ0e_i0.webp" alt="Long highlighted boho braids in golden blonde and black" width="360" height="640">
      <img class="c" src="assets/photos/Ddg3wsXlnAs_i2.webp" alt="Javel smiling in a honey blonde curled wig with bangs" width="480" height="640">
    </div>
  </section>

  <section class="styles wrap" id="styles">
    <h2>Styles on her page</h2>
    <p class="lede">Everything here comes from Javel's own posts. Prices and availability aren't posted, so ask when you book.</p>
    <div class="bento">
      <a class="tile t1" href="#work" data-filter="locs">
        <img src="assets/photos/DeUgit7ljA8_i1-lg.webp" alt="" loading="lazy" width="720" height="960">
        <span class="tile-text"><strong>Locs and twists</strong>Retwists, two strand retwists, twists</span>
      </a>
      <a class="tile t2" href="#work" data-filter="braids">
        <img src="assets/photos/Ddz5wMfick7_i1-lg.webp" alt="" loading="lazy" width="1050" height="1400">
        <span class="tile-text"><strong>Braids</strong>Boho, highlighted boho, Fulani</span>
      </a>
      <a class="tile t3" href="#work" data-filter="wigs">
        <img src="assets/photos/Ddg3wsXlnAs_i1-lg.webp" alt="" loading="lazy" width="1050" height="1400">
        <span class="tile-text"><strong>Wigs</strong>Wig installs, half wig installs</span>
      </a>
    </div>
  </section>

  <section class="work wrap" id="work">
    <h2>Recent work</h2>
    <div class="filters" role="group" aria-label="Filter photos by style">
      <button type="button" data-filter="all" aria-pressed="true">All</button>
      <button type="button" data-filter="locs" aria-pressed="false">Locs and twists</button>
      <button type="button" data-filter="braids" aria-pressed="false">Braids</button>
      <button type="button" data-filter="wigs" aria-pressed="false">Wigs</button>
    </div>
    <div class="grid">
        {gallery_html()}
    </div>
    <a class="more" href="{IG}" target="_blank" rel="noopener">More on @javelthehairbelle {icon("arrow-right")}</a>
  </section>

  <section class="clips" aria-labelledby="clips-title">
    <div class="wrap">
      <h2 id="clips-title">Up close</h2>
    </div>
    <div class="clip-row">
        {clips_html()}
    </div>
  </section>

  <section class="about wrap" id="about">
    <img src="assets/photos/Ddg3wsXlnAs_i2-lg.webp" alt="Javel smiling in a honey blonde curled wig with bangs" loading="lazy" width="1050" height="1400">
    <div>
      <h2>Meet Javel</h2>
      <blockquote>All Glory to God | D(M)V Based</blockquote>
      <p>That's the first line of her Instagram bio. Javel is a teen beginner stylist in Silver Spring, MD, and the CEO of Javel The Hair Belle.</p>
    </div>
  </section>

  <section class="book" id="book">
    <div class="wrap">
      <img class="book-logo" src="assets/brand/logo.png" alt="" width="149" height="68">
      <h2>Book your style</h2>
      <p>Send a request and Javel will contact you to confirm. Your appointment isn't set until she does.</p>
      <form name="booking" method="POST" action="/thanks.html" data-netlify="true" netlify-honeypot="company" class="book-form">
        <input type="hidden" name="form-name" value="booking">
        <p class="hp"><label>Leave this empty <input name="company" tabindex="-1" autocomplete="off"></label></p>
        <fieldset class="full field" data-error="Choose a style to continue.">
          <legend>What would you like?</legend>
          <div class="chips">
            {style_options()}
          </div>
          <small class="err"></small>
        </fieldset>
        <div class="field" data-error="Enter your name.">
          <label for="f-name">Your name</label>
          <input id="f-name" name="name" required autocomplete="name">
          <small class="err"></small>
        </div>
        <div class="field" data-error="Enter your Instagram or phone number so Javel can reach you.">
          <label for="f-contact">Instagram or phone number</label>
          <input id="f-contact" name="contact" required autocomplete="off">
          <small class="err"></small>
        </div>
        <div class="field" data-error="Choose today or a later date.">
          <label for="f-date">Preferred date</label>
          <input id="f-date" type="date" name="preferred-date" required>
          <small class="err"></small>
        </div>
        <div class="field">
          <label for="f-notes">Notes (optional)</label>
          <input id="f-notes" name="notes" autocomplete="off">
        </div>
        <button class="btn full" type="submit">Send request</button>
        <p class="form-status full" role="status" aria-live="polite"></p>
      </form>
      <div class="book-done" hidden tabindex="-1">
        <h3></h3>
        <p class="done-summary"></p>
        <p>Javel will contact you at <strong class="done-contact"></strong> to confirm. Your appointment isn't set until she does.</p>
        <button class="btn btn-ghost" type="button">Send another request</button>
      </div>
      <p class="alt">Prefer Instagram? <a href="{DM}" target="_blank" rel="noopener">DM @javelthehairbelle</a> or, if that's not working, <a href="{DM_ALT}" target="_blank" rel="noopener">@javelxo</a></p>
    </div>
  </section>
</main>

<footer class="foot wrap">
  <span>Javel The Hair Belle, Silver Spring, MD</span>
  <a href="{IG}" target="_blank" rel="noopener">{icon("instagram-logo")}@javelthehairbelle</a>
</footer>

<a class="sticky-book" href="#book">Book now</a>

<dialog class="box" aria-label="Photo viewer">
  <button class="box-close" type="button" aria-label="Close">{icon("x")}</button>
  <button class="box-nav prev" type="button" aria-label="Previous photo">{icon("caret-left")}</button>
  <figure>
    <img alt="">
    <figcaption><span></span><a target="_blank" rel="noopener">View post {icon("arrow-right")}</a><button class="book-this" type="button">Book this style</button></figcaption>
  </figure>
  <button class="box-nav next" type="button" aria-label="Next photo">{icon("caret-right")}</button>
</dialog>

<script src="script.js" defer></script>
</body>
</html>
"""

(ROOT / "index.html").write_text(PAGE)
print("index.html written,", len(GALLERY), "photos")
