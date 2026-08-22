import os

THEMES = {
    "dark": dict(bg1="#0d1117", bg2="#0f141b", grid="#1b2430",
                 sub="#8b949e", tag="#6e7681", a1="#22d3ee", a2="#a78bfa", ring="#21262d"),
    "light": dict(bg1="#ffffff", bg2="#f6f8fa", grid="#e4e8ed",
                  sub="#57606a", tag="#8c959f", a1="#0891b2", a2="#7c3aed", ring="#d8dee4"),
}

W, H = 1000, 240
COLS, ROWS = 14, 7
CELL, GAP = 18, 4
GX = 636
GY = (H - (ROWS * (CELL + GAP) - GAP)) // 2

ROLES = ["Data Engineer", "Machine Learning Engineer", "Melbourne, Australia"]
CYCLE = 12.0


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def role_anim(i):
    if i == 0:
        return '0;0.31;0.35;0.96;1', '1;1;0;0;1'
    if i == 1:
        return '0;0.31;0.35;0.64;0.68;1', '0;0;1;1;0;0'
    return '0;0.64;0.68;0.96;1;1', '0;0;1;1;0;0'


def build(theme):
    t = THEMES[theme]
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
             f'role="img" aria-label="Mowlya Shree Manjunatha, Data and Machine Learning Engineer">')
    o.append('<defs>')
    o.append(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{t["bg1"]}"/><stop offset="55%" stop-color="{t["bg2"]}"/>'
             f'<stop offset="100%" stop-color="{t["bg1"]}"/></linearGradient>')
    o.append(f'<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["a1"]}"/><stop offset="50%" stop-color="{t["a2"]}"/>'
             f'<stop offset="100%" stop-color="{t["a1"]}"/>'
             f'<animateTransform attributeName="gradientTransform" type="translate" '
             f'values="-1 0;1 0;-1 0" dur="10s" repeatCount="indefinite"/></linearGradient>')
    o.append(f'<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["a1"]}" stop-opacity="0.9"/>'
             f'<stop offset="70%" stop-color="{t["a2"]}" stop-opacity="0.55"/>'
             f'<stop offset="100%" stop-color="{t["a2"]}" stop-opacity="0"/></linearGradient>')
    o.append(f'<radialGradient id="glow"><stop offset="0%" stop-color="{t["a2"]}" stop-opacity="0.20"/>'
             f'<stop offset="100%" stop-color="{t["a2"]}" stop-opacity="0"/></radialGradient>')
    o.append(f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
             f'<circle cx="1" cy="1" r="1" fill="{t["grid"]}"/></pattern>')
    o.append('</defs>')

    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>')
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#dots)" opacity="0.7"/>')
    o.append(f'<circle cx="820" cy="120" r="190" fill="url(#glow)">'
             f'<animate attributeName="r" values="170;205;170" dur="9s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{t["ring"]}"/>')

    o.append(f'<text x="60" y="72" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" '
             f'letter-spacing="3" fill="{t["tag"]}">HELLO, I AM</text>')
    o.append(f'<rect x="172" y="60" width="8" height="15" fill="{t["a1"]}">'
             f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.45;0.5;0.95;1" '
             f'dur="1.4s" repeatCount="indefinite"/></rect>')

    o.append(f'<text x="60" y="128" font-family="Segoe UI,Helvetica Neue,Helvetica,Arial,sans-serif" '
             f'font-size="46" font-weight="700" fill="url(#shine)">Mowlya Shree Manjunatha</text>')

    o.append(f'<rect x="60" y="146" height="3" rx="1.5" fill="url(#rule)" width="470">'
             f'<animate attributeName="width" values="0;470;470" keyTimes="0;0.18;1" dur="10s" '
             f'repeatCount="indefinite"/></rect>')

    for i, r in enumerate(ROLES):
        kt, vals = role_anim(i)
        o.append(f'<text x="60" y="180" font-family="Segoe UI,Helvetica Neue,Helvetica,Arial,sans-serif" '
                 f'font-size="19" fill="{t["sub"]}" opacity="{1 if i==0 else 0}">{r}'
                 f'<animate attributeName="opacity" keyTimes="{kt}" values="{vals}" dur="{CYCLE}s" '
                 f'repeatCount="indefinite"/></text>')

    o.append(f'<text x="60" y="206" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12" '
             f'letter-spacing="2.2" fill="{t["tag"]}">PIPELINES  .  MODELS  .  CLOUD</text>')

    for c in range(COLS):
        col = mix(t["a1"], t["a2"], c / (COLS - 1))
        for r in range(ROWS):
            x = GX + c * (CELL + GAP)
            y = GY + r * (CELL + GAP)
            delay = -((c * 0.16) + (r * 0.11))
            o.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="4" fill="{col}" opacity="0.12">'
                     f'<animate attributeName="opacity" values="0.12;0.95;0.12" dur="4.4s" '
                     f'begin="{delay:.2f}s" repeatCount="indefinite"/></rect>')

    o.append('</svg>')
    return "\n".join(o)


os.makedirs("assets", exist_ok=True)
for name in THEMES:
    with open(f"assets/header-{name}.svg", "w") as f:
        f.write(build(name))
    print("wrote", f"assets/header-{name}.svg")
