#!/usr/bin/env python3
"""Generate hand-authored animated SVG assets for the mowlya-m GitHub profile.

Every animation uses SMIL with dur=TOTAL + repeatCount="indefinite" and keyTimes
expressed as fractions of the total loop, so the whole scene restarts cleanly.
This is the pattern that survives GitHub's camo image proxy.
"""
import os, html, math

OUT = "/home/claude/build/assets"
os.makedirs(OUT, exist_ok=True)

MONO = "'JetBrains Mono','Fira Code','SF Mono',Menlo,Consolas,'Courier New',monospace"
SANS = "'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"

THEMES = {
    "dark": dict(
        bg="#0d1117", panel="#0f141b", panel2="#161b22", border="#26303b",
        text="#e6edf3", muted="#8b949e", dim="#6e7681",
        cyan="#22d3ee", violet="#a78bfa", green="#3fb950", yellow="#e3b341",
        red="#ff7b72", pink="#f778ba", grid="#ffffff", glow_o="0.16",
        grid_o="0.05", chip="#161b22", chipb="#2b3441",
    ),
    "light": dict(
        bg="#ffffff", panel="#f6f8fa", panel2="#eef2f6", border="#d0d7de",
        text="#1f2328", muted="#59636e", dim="#818b98",
        cyan="#0b7285", violet="#6d28d9", green="#1a7f37", yellow="#9a6700",
        red="#cf222e", pink="#bf3989", grid="#000000", glow_o="0.10",
        grid_o="0.06", chip="#ffffff", chipb="#d0d7de",
    ),
}


def esc(s):
    return html.escape(s, quote=True)


def kt(vals):
    """format keyTimes list"""
    return ";".join(f"{v:.5f}".rstrip("0").rstrip(".") or "0" for v in vals)


def mono_text(s, x, y, size, fill, weight="400", opacity="1", extra=""):
    w = len(s) * size * 0.6
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" opacity="{opacity}" xml:space="preserve" '
            f'textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs" {extra}>{esc(s)}</text>')



def mono_rich(parts, x, y, size, weight="400"):
    """One <text> with coloured <tspan>s and a single enforced textLength."""
    total = sum(len(t) for t, _ in parts)
    w = total * size * 0.6
    inner = "".join(f'<tspan fill="{col}">{esc(t)}</tspan>' for t, col in parts)
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" '
            f'xml:space="preserve" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs">{inner}</text>')

def mono_w(s, size):
    return len(s) * size * 0.6


# ─────────────────────────────────────────────────────────────────────────────
# 1. HEADER  — hero banner with a flowing data pipeline motif
# ─────────────────────────────────────────────────────────────────────────────
def header(theme):
    c = THEMES[theme]
    W, H, TOTAL = 1000, 240, 12.0
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Mowlya Shree Manjunatha, Data and Machine Learning Engineer">']
    s.append(f"""<defs>
  <linearGradient id="bgg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{c['bg']}"/><stop offset="60%" stop-color="{c['panel']}"/><stop offset="100%" stop-color="{c['bg']}"/>
  </linearGradient>
  <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{c['cyan']}"/><stop offset="50%" stop-color="{c['violet']}"/><stop offset="100%" stop-color="{c['cyan']}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="9s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{c['cyan']}" stop-opacity="0"/>
    <stop offset="45%" stop-color="{c['cyan']}" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="{c['violet']}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="blobA"><stop offset="0%" stop-color="{c['cyan']}" stop-opacity="{c['glow_o']}"/><stop offset="45%" stop-color="{c['cyan']}" stop-opacity="{float(c['glow_o'])*0.3:.3f}"/><stop offset="100%" stop-color="{c['cyan']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="blobB"><stop offset="0%" stop-color="{c['violet']}" stop-opacity="{c['glow_o']}"/><stop offset="45%" stop-color="{c['violet']}" stop-opacity="{float(c['glow_o'])*0.3:.3f}"/><stop offset="100%" stop-color="{c['violet']}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
    <path d="M28 0H0V28" fill="none" stroke="{c['grid']}" stroke-opacity="{c['grid_o']}" stroke-width="1"/>
  </pattern>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>""")
    s.append('<g clip-path="url(#frame)">')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#bgg)"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    s.append(f'<ellipse cx="150" cy="40" rx="320" ry="190" fill="url(#blobA)">'
             f'<animate attributeName="cx" values="120;340;120" dur="15s" repeatCount="indefinite"/></ellipse>')
    s.append(f'<ellipse cx="880" cy="210" rx="330" ry="200" fill="url(#blobB)">'
             f'<animate attributeName="cx" values="900;680;900" dur="17s" repeatCount="indefinite"/></ellipse>')

    # name: quick fade + slide, no character typing
    name = "Mowlya Shree Manjunatha"
    s.append(f'<g opacity="0" transform="translate(0,14)">'
             f'<animate attributeName="opacity" values="0;1;1" keyTimes="0;0.06;1" dur="{TOTAL}s" repeatCount="indefinite"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0 14;0 0;0 0" '
             f'keyTimes="0;0.07;1" dur="{TOTAL}s" repeatCount="indefinite"/>'
             f'<text x="46" y="104" font-family="{SANS}" font-size="44" font-weight="800" '
             f'fill="url(#shine)" letter-spacing="-0.5">{esc(name)}</text></g>')

    s.append(f'<rect x="46" y="122" width="0" height="3" rx="1.5" fill="url(#rule)">'
             f'<animate attributeName="width" values="0;0;540;540" keyTimes="0;0.05;0.14;1" '
             f'dur="{TOTAL}s" repeatCount="indefinite"/></rect>')

    # subtitle
    sub = "Data Engineer  ·  Machine Learning Engineer  ·  Melbourne, Australia"
    s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.10;0.16;1" '
             f'dur="{TOTAL}s" repeatCount="indefinite"/>'
             f'<text x="48" y="154" font-family="{SANS}" font-size="17" font-weight="500" '
             f'fill="{c["muted"]}">{esc(sub)}</text></g>')

    # status pill
    s.append(f'<g opacity="0" transform="translate(46,178)">'
             f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.14;0.20;1" dur="{TOTAL}s" repeatCount="indefinite"/>'
             f'<rect width="196" height="32" rx="16" fill="{c["panel2"]}" stroke="{c["border"]}"/>'
             f'<circle cx="19" cy="16" r="5" fill="{c["green"]}">'
             f'<animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/></circle>'
             f'<text x="34" y="21" font-family="{SANS}" font-size="13" font-weight="600" '
             f'fill="{c["muted"]}">Open to new opportunities</text></g>')

    # right side: a data pipeline with packets flowing along it
    nodes = [(700, 70), (790, 118), (700, 166), (880, 70), (880, 166), (955, 118)]
    edges = [(0, 1), (1, 2), (0, 3), (2, 4), (3, 5), (4, 5), (1, 5)]
    s.append('<g opacity="0"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.16;0.26;1" '
             f'dur="{TOTAL}s" repeatCount="indefinite"/>')
    for a, b in edges:
        x1, y1 = nodes[a]; x2, y2 = nodes[b]
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["border"]}" stroke-width="1.5"/>')
    for i, (a, b) in enumerate(edges):
        x1, y1 = nodes[a]; x2, y2 = nodes[b]
        col = c['cyan'] if i % 2 == 0 else c['violet']
        s.append(f'<circle r="3.4" fill="{col}">'
                 f'<animate attributeName="cx" values="{x1};{x2}" dur="{2.6 + i*0.35:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="{y1};{y2}" dur="{2.6 + i*0.35:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.85;1" '
                 f'dur="{2.6 + i*0.35:.2f}s" repeatCount="indefinite"/></circle>')
    for i, (x, y) in enumerate(nodes):
        r = 9 if i in (0, 5) else 7
        col = c['cyan'] if i in (0, 5) else c['violet']
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c["panel2"]}" stroke="{col}" stroke-width="2">'
                 f'<animate attributeName="r" values="{r};{r+1.6};{r}" dur="{3 + i*0.4:.1f}s" repeatCount="indefinite"/></circle>')
    s.append('</g>')
    s.append('</g>')
    s.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{c["border"]}"/>')
    s.append('</svg>')
    return "\n".join(s)


# ─────────────────────────────────────────────────────────────────────────────
# 2. INTRO — identity card, fully readable within ~2s
# ─────────────────────────────────────────────────────────────────────────────
def intro(theme):
    c = THEMES[theme]
    W, H, TOTAL = 1000, 288, 12.0
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Introduction card for Mowlya Shree Manjunatha">']
    s.append(f"""<defs>
  <linearGradient id="icard" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{c['panel']}"/><stop offset="100%" stop-color="{c['bg']}"/>
  </linearGradient>
  <linearGradient id="iring" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{c['cyan']}"/><stop offset="100%" stop-color="{c['violet']}"/>
  </linearGradient>
  <linearGradient id="imono" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{c['cyan']}"/><stop offset="100%" stop-color="{c['violet']}"/>
  </linearGradient>
  <radialGradient id="iglow"><stop offset="0%" stop-color="{c['violet']}" stop-opacity="{c['glow_o']}"/><stop offset="100%" stop-color="{c['violet']}" stop-opacity="0"/></radialGradient>
  <clipPath id="iframe"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>""")
    s.append('<g clip-path="url(#iframe)">')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#icard)"/>')
    s.append(f'<ellipse cx="820" cy="60" rx="300" ry="180" fill="url(#iglow)"/>')

    # monogram with a rotating gradient ring
    cx, cy = 116, 118
    s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1;1" keyTimes="0;0.05;1" dur="{TOTAL}s" repeatCount="indefinite"/>'
             f'<circle cx="{cx}" cy="{cy}" r="56" fill="{c["panel2"]}" stroke="{c["border"]}"/>'
             f'<circle cx="{cx}" cy="{cy}" r="56" fill="none" stroke="url(#iring)" stroke-width="3" '
             f'stroke-linecap="round" stroke-dasharray="120 232">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" '
             f'dur="9s" repeatCount="indefinite"/></circle>'
             f'<text x="{cx}" y="{cy+13}" text-anchor="middle" font-family="{SANS}" font-size="38" '
             f'font-weight="800" fill="url(#imono)">MM</text></g>')

    # name + role
    s.append(f'<g opacity="0" transform="translate(0,10)">'
             f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;0.04;0.10;1" dur="{TOTAL}s" repeatCount="indefinite"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0 10;0 0;0 0" keyTimes="0;0.11;1" dur="{TOTAL}s" repeatCount="indefinite"/>'
             f'<text x="206" y="78" font-family="{SANS}" font-size="30" font-weight="800" fill="{c["text"]}">Hi, I am Mowli.</text>'
             f'<text x="206" y="112" font-family="{SANS}" font-size="17" font-weight="500" fill="{c["muted"]}">'
             f'I build data platforms that keep running when nobody is watching.</text></g>')

    # fact rows
    facts = [
        (c['cyan'],   "Master of Data Science, Monash University"),
        (c['violet'], "AWS Certified Machine Learning Engineer, Associate"),
        (c['green'],  "Melbourne, Australia. Full working rights, no sponsorship needed"),
    ]
    for i, (col, txt) in enumerate(facts):
        y = 152 + i * 30
        t = 0.12 + i * 0.035
        s.append(f'<g opacity="0" transform="translate(10,0)">'
                 f'<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{t:.3f};{t+0.03:.3f};1" dur="{TOTAL}s" repeatCount="indefinite"/>'
                 f'<animateTransform attributeName="transform" type="translate" values="10 0;0 0;0 0" '
                 f'keyTimes="0;{t+0.035:.3f};1" dur="{TOTAL}s" repeatCount="indefinite"/>'
                 f'<circle cx="212" cy="{y-5}" r="4.5" fill="{col}"/>'
                 f'<text x="230" y="{y}" font-family="{SANS}" font-size="15.5" fill="{c["text"]}">{esc(txt)}</text></g>')

    # pills
    pills = [("Streaming", c['cyan']), ("Lakehouse", c['violet']), ("MLOps", c['green']), ("Agentic AI", c['yellow'])]
    x = 206
    for i, (label, col) in enumerate(pills):
        w = len(label) * 8.2 + 30
        t = 0.24 + i * 0.025
        s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{t:.3f};{t+0.025:.3f};1" '
                 f'dur="{TOTAL}s" repeatCount="indefinite"/>'
                 f'<rect x="{x:.0f}" y="234" width="{w:.0f}" height="30" rx="15" fill="{c["chip"]}" stroke="{col}" stroke-opacity="0.55"/>'
                 f'<text x="{x + w/2:.0f}" y="254" text-anchor="middle" font-family="{SANS}" font-size="13" '
                 f'font-weight="600" fill="{col}">{esc(label)}</text></g>')
        x += w + 10

    s.append('</g>')
    s.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{c["border"]}"/>')
    s.append('</svg>')
    return "\n".join(s)


# ─────────────────────────────────────────────────────────────────────────────
# 4. DIVIDER — animated pulse line
# ─────────────────────────────────────────────────────────────────────────────
def divider(theme):
    c = THEMES[theme]
    W, H = 1000, 12
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="divider">']
    s.append(f'''<defs><linearGradient id="dv" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{c['cyan']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{c['violet']}" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="{c['cyan']}" stop-opacity="0"/></linearGradient></defs>''')
    s.append(f'<rect x="0" y="5" width="{W}" height="1.5" rx="0.75" fill="url(#dv)" opacity="0.5"/>')
    s.append(f'''<circle cx="0" cy="5.75" r="3.5" fill="{c['cyan']}">
      <animate attributeName="cx" values="0;{W};0" dur="9s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="9s" repeatCount="indefinite"/></circle>''')
    s.append('</svg>')
    return "\n".join(s)



# ─────────────────────────────────────────────────────────────────────────────
# 5. QUOTE — starfield with a typed quotation
# ─────────────────────────────────────────────────────────────────────────────
def quote(theme):
    import random
    c = THEMES[theme]
    W, H, TOTAL = 1000, 210, 16.0
    lines = ["I have no special talents.",
             "I am only passionately curious."]
    FS = 24
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Quote: I have no special talents. I am only passionately curious. Albert Einstein">']
    s.append(f"""<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{c['bg']}"/>
    <stop offset="70%" stop-color="{c['panel']}"/>
    <stop offset="100%" stop-color="{c['panel2']}"/>
  </linearGradient>
  <linearGradient id="qg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{c['cyan']}"/><stop offset="100%" stop-color="{c['violet']}"/>
  </linearGradient>
  <clipPath id="qframe"><rect width="{W}" height="{H}" rx="12"/></clipPath>
</defs>""")
    s.append('<g clip-path="url(#qframe)">')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')

    # deterministic starfield
    random.seed(7)
    for i in range(90):
        x = random.uniform(0, W); y = random.uniform(0, H * 0.88)
        r = random.choice([0.7, 0.9, 1.1, 1.4])
        d = random.uniform(2.5, 6.0)
        o = random.uniform(0.15, 0.55)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c["text"]}" opacity="{o:.2f}">'
                 f'<animate attributeName="opacity" values="{o:.2f};{min(o*2.4,0.95):.2f};{o:.2f}" '
                 f'dur="{d:.1f}s" begin="{random.uniform(0,4):.1f}s" repeatCount="indefinite"/></circle>')

    # shooting star
    s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" '
             f'keyTimes="0;0.42;0.46;0.52;1" dur="{TOTAL}s" repeatCount="indefinite"/>'
             f'<line x1="0" y1="0" x2="46" y2="26" stroke="{c["cyan"]}" stroke-width="1.4" stroke-linecap="round">'
             f'<animateTransform attributeName="transform" type="translate" values="700 8;830 82" '
             f'keyTimes="0;1" dur="{TOTAL*0.10:.2f}s" begin="{TOTAL*0.42:.2f}s" repeatCount="indefinite"/>'
             f'</line></g>')

    # ridgeline silhouette
    s.append(f'<path d="M0 {H} L0 176 L118 150 L196 168 L288 122 L352 146 L436 96 L520 134 '
             f'L604 108 L688 152 L772 126 L866 158 L940 138 L{W} 164 L{W} {H} Z" '
             f'fill="{c["panel2"]}" opacity="0.9"/>')
    s.append(f'<path d="M0 {H} L0 190 L140 172 L250 186 L360 164 L470 184 L590 166 L700 188 '
             f'L820 170 L920 186 L{W} 178 L{W} {H} Z" fill="{c["border"]}" opacity="0.55"/>')

    # opening quote mark
    s.append(f'<text x="34" y="76" font-family="{SANS}" font-size="70" font-weight="700" '
             f'fill="url(#qg)" opacity="0.35">&#8220;</text>')

    # typed lines
    t = 0.06
    for i, ln in enumerate(lines):
        y = 74 + i * 40
        wid = mono_w(ln, FS)
        dur = len(ln) * 0.011
        cid = f"ql{i}"
        s.append(f'<defs><clipPath id="{cid}"><rect x="78" y="{y-FS-4}" width="0" height="{FS*1.8:.0f}">'
                 f'<animate attributeName="width" values="0;0;{wid:.1f};{wid*1.06:.1f}" '
                 f'keyTimes="0;{t:.4f};{t+dur:.4f};1" dur="{TOTAL}s" repeatCount="indefinite"/>'
                 f'</rect></clipPath></defs>')
        s.append(f'<g clip-path="url(#{cid})">{mono_text(ln, 78, y, FS, c["text"], weight="500")}</g>')
        s.append(f'<rect x="78" y="{y-FS+2}" width="11" height="{FS+2}" fill="{c["cyan"]}" opacity="0">'
                 f'<animate attributeName="x" values="78;78;{78+wid:.1f};{78+wid:.1f}" '
                 f'keyTimes="0;{t:.4f};{t+dur:.4f};1" dur="{TOTAL}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{t-0.01:.4f};{t:.4f};{t+dur+0.02:.4f};{t+dur+0.03:.4f};1" '
                 f'dur="{TOTAL}s" repeatCount="indefinite"/></rect>')
        t += dur + 0.05

    # attribution slides in
    attr = "Albert Einstein"
    aw = mono_w(attr, 14)
    s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1" '
             f'keyTimes="0;{t:.4f};{t+0.03:.4f};1" dur="{TOTAL}s" repeatCount="indefinite"/>'
             f'<rect x="78" y="152" width="0" height="2" rx="1" fill="url(#qg)">'
             f'<animate attributeName="width" values="0;0;54;54" keyTimes="0;{t:.4f};{t+0.04:.4f};1" '
             f'dur="{TOTAL}s" repeatCount="indefinite"/></rect>'
             f'{mono_text(attr, 146, 158, 14, c["muted"], weight="600")}</g>')
    s.append('</g>')
    s.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{c["border"]}"/>')
    s.append('</svg>')
    return "\n".join(s)


ASSETS = {
    "header": header,
    "intro": intro,
    "divider": divider,
    "quote": quote,
}

if __name__ == "__main__":
    for name, fn in ASSETS.items():
        for theme in ("dark", "light"):
            path = os.path.join(OUT, f"{name}-{theme}.svg")
            with open(path, "w") as f:
                f.write(fn(theme))
            print(f"wrote {path}  ({os.path.getsize(path):,} bytes)")
