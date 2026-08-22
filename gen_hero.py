import os

THEMES = {
    "dark":  dict(bg1="#0d1117", bg2="#11161d", dot="#1b2430", body="#c9d1d9",
                  mute="#7d8590", ring="#21262d", a1="#22d3ee", a2="#a78bfa"),
    "light": dict(bg1="#ffffff", bg2="#f6f8fa", dot="#e4e8ed", body="#1f2328",
                  mute="#6e7781", ring="#d8dee4", a1="#0891b2", a2="#7c3aed"),
}

W, H = 1000, 268
CYCLE = 16.0
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

L4 = "Albert Einstein"
LINES = [
    dict(txt="Hiii, I'm Mowlya", x=70, y=112, size=44, weight="700",
         fill="url(#shine)", start=0.6, type_dur=2.0),
    dict(txt="I build data pipelines and ML systems that reach production.",
         x=70, y=160, size=17, weight="400", fill="BODY", start=3.0, type_dur=2.2),
    dict(txt='"I have no special talent. I am only passionately curious."',
         x=70, y=206, size=16, weight="400", fill="MUTE", start=5.8, type_dur=2.6),
]


def w_of(txt, size):
    return len(txt) * size * 0.601


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme):
    t = THEMES[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Hi, I am Mowlya. I build data pipelines and ML systems.">']
    o.append('<defs>')
    o.append(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{t["bg1"]}"/><stop offset="55%" stop-color="{t["bg2"]}"/>'
             f'<stop offset="100%" stop-color="{t["bg1"]}"/></linearGradient>')
    o.append(f'<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["a1"]}"/><stop offset="50%" stop-color="{t["a2"]}"/>'
             f'<stop offset="100%" stop-color="{t["a1"]}"/>'
             f'<animateTransform attributeName="gradientTransform" type="translate" '
             f'values="-1 0;1 0;-1 0" dur="9s" repeatCount="indefinite"/></linearGradient>')
    o.append(f'<radialGradient id="glow"><stop offset="0%" stop-color="{t["a2"]}" stop-opacity="0.17"/>'
             f'<stop offset="100%" stop-color="{t["a2"]}" stop-opacity="0"/></radialGradient>')
    o.append(f'<radialGradient id="glow2"><stop offset="0%" stop-color="{t["a1"]}" stop-opacity="0.15"/>'
             f'<stop offset="100%" stop-color="{t["a1"]}" stop-opacity="0"/></radialGradient>')
    o.append(f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
             f'<circle cx="1.2" cy="1.2" r="1.2" fill="{t["dot"]}"/></pattern>')

    for i, ln in enumerate(LINES):
        wpx = w_of(ln["txt"], ln["size"]) + 6
        s, d = ln["start"] / CYCLE, ln["type_dur"] / CYCLE
        o.append(f'<clipPath id="clip{i}"><rect x="{ln["x"]}" y="{ln["y"]-ln["size"]}" '
                 f'height="{ln["size"]*1.5}" width="0">'
                 f'<animate attributeName="width" values="0;0;{wpx:.0f};{wpx:.0f};0;0" '
                 f'keyTimes="0;{s:.4f};{s+d:.4f};0.94;0.965;1" dur="{CYCLE}s" '
                 f'repeatCount="indefinite"/></rect></clipPath>')
    o.append('</defs>')

    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>')
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#dots)" opacity="0.75"/>')
    o.append(f'<circle cx="880" cy="72" r="200" fill="url(#glow)">'
             f'<animate attributeName="r" values="175;215;175" dur="11s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="120" cy="250" r="180" fill="url(#glow2)">'
             f'<animate attributeName="r" values="200;160;200" dur="11s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{t["ring"]}"/>')

    for i, c in enumerate([t["a1"], t["a2"], t["mute"]]):
        o.append(f'<circle cx="{70+i*18}" cy="46" r="5" fill="{c}" opacity="0.55"/>')
    o.append(f'<text x="{70+3*18+14}" y="51" font-family="{MONO}" font-size="12" letter-spacing="1.6" '
             f'fill="{t["mute"]}">mowlya-m . profile</text>')

    for i, ln in enumerate(LINES):
        fill = ln["fill"].replace("BODY", t["body"]).replace("MUTE", t["mute"])
        style = "italic" if i == 2 else "normal"
        o.append(f'<g clip-path="url(#clip{i})"><text x="{ln["x"]}" y="{ln["y"]}" font-family="{MONO}" '
                 f'font-size="{ln["size"]}" font-weight="{ln["weight"]}" font-style="{style}" '
                 f'fill="{fill}">{esc(ln["txt"])}</text></g>')

    car = [(l["start"], l["start"] + l["type_dur"], l["x"], l["y"], l["size"],
            w_of(l["txt"], l["size"])) for l in LINES]
    for idx, (s, e, x, y, size, tw) in enumerate(car):
        hold = 0.999 if idx == len(car) - 1 else (car[idx + 1][0] - 0.25) / CYCLE
        o.append(f'<rect x="{x}" y="{y-size+3}" width="{max(8,size*0.55):.0f}" height="{size*0.95:.0f}" '
                 f'fill="{t["a1"]}" opacity="0">'
                 f'<animate attributeName="x" values="{x};{x+tw:.0f}" keyTimes="{s/CYCLE:.4f};{e/CYCLE:.4f}" '
                 f'dur="{CYCLE}s" repeatCount="indefinite" calcMode="linear"/>'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{s/CYCLE:.4f};{(s+0.01)/CYCLE:.4f};{hold:.4f};{min(hold+0.004,0.9995):.4f};1" '
                 f'dur="{CYCLE}s" repeatCount="indefinite"/></rect>')

    o.append(f'<text x="70" y="234" font-family="{MONO}" font-size="12" letter-spacing="2" '
             f'fill="{t["mute"]}" opacity="0">- {esc(L4)}'
             f'<animate attributeName="opacity" values="0;0;0.9;0.9;0" keyTimes="0;0.535;0.575;0.94;0.96" '
             f'dur="{CYCLE}s" repeatCount="indefinite"/></text>')
    o.append('</svg>')
    return "\n".join(o)


os.makedirs("assets", exist_ok=True)
for name in THEMES:
    open(f"assets/hero-{name}.svg", "w").write(build(name))
    print("wrote assets/hero-%s.svg" % name)
