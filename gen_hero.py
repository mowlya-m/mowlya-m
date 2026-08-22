import math, os, random

THEMES = {
    "dark":  dict(bg1="#0d1117", bg2="#11161d", body="#c9d1d9", mute="#7d8590",
                  faint="#586069", ring="#21262d", a1="#22d3ee", a2="#a78bfa",
                  node="#b6c2cf", edge="#c9d6e2"),
    "light": dict(bg1="#ffffff", bg2="#f6f8fa", body="#1f2328", mute="#57606a",
                  faint="#8c959f", ring="#d8dee4", a1="#0891b2", a2="#7c3aed",
                  node="#8c959f", edge="#aab4bf"),
}

W, H = 1000, 234
CYCLE = 16.0
DRIFT = 17.0
NODES = 32
KEYS = 8
LINK = 165
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

LINES = [
    dict(txt="Hiii there! I'm Mowlya", x=176, y=112, size=34, weight="700",
         fill="SHINE", start=0.6, dur=2.0),
    dict(txt="I build data pipelines and ML systems that reach production.",
         x=176, y=148, size=15, weight="400", fill="BODY", start=3.0, dur=2.2),
    dict(txt='"I have no special talent. I am only passionately curious."',
         x=176, y=180, size=14, weight="400", fill="MUTE", start=5.8, dur=2.6),
    dict(txt="- Albert Einstein", x=674, y=206, size=11, weight="400",
         fill="FAINT", start=8.6, dur=0.9, anchor="end"),
]


def w_of(txt, size):
    return len(txt) * size * 0.601


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def constellation(t):
    rng = random.Random(7)
    base = [(rng.uniform(24, W - 24), rng.uniform(20, H - 20)) for _ in range(NODES)]
    xs, ys = [], []
    for (bx, by) in base:
        px, py = [bx], [by]
        for _ in range(KEYS - 1):
            px.append(min(W - 12, max(12, bx + rng.uniform(-46, 46))))
            py.append(min(H - 12, max(12, by + rng.uniform(-34, 34))))
        px.append(bx)
        py.append(by)
        xs.append(px)
        ys.append(py)
    edges = [(i, j, math.dist(base[i], base[j]))
             for i in range(NODES) for j in range(i + 1, NODES)
             if math.dist(base[i], base[j]) < LINK]
    o = ['<g opacity="0.9">']
    for i, j, d in edges:
        op = max(0.14, 0.55 * (1 - d / LINK))
        vx1 = ";".join(f"{v:.1f}" for v in xs[i])
        vy1 = ";".join(f"{v:.1f}" for v in ys[i])
        vx2 = ";".join(f"{v:.1f}" for v in xs[j])
        vy2 = ";".join(f"{v:.1f}" for v in ys[j])
        o.append(f'<line x1="{xs[i][0]:.1f}" y1="{ys[i][0]:.1f}" x2="{xs[j][0]:.1f}" '
                 f'y2="{ys[j][0]:.1f}" stroke="{t["edge"]}" stroke-opacity="{op:.2f}" '
                 f'stroke-width="1.2">'
                 f'<animate attributeName="x1" values="{vx1}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y1" values="{vy1}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="x2" values="{vx2}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y2" values="{vy2}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'</line>')
    for i in range(NODES):
        r = 2.4 + (i % 4) * 0.7
        c = t["a1"] if i % 5 == 0 else (t["a2"] if i % 7 == 0 else t["node"])
        op = 0.95 if c != t["node"] else 0.7
        vx = ";".join(f"{v:.1f}" for v in xs[i])
        vy = ";".join(f"{v:.1f}" for v in ys[i])
        o.append(f'<circle cx="{xs[i][0]:.1f}" cy="{ys[i][0]:.1f}" r="{r:.1f}" fill="{c}" '
                 f'opacity="{op}">'
                 f'<animate attributeName="cx" values="{vx}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="cy" values="{vy}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="r" values="{r:.1f};{r*1.75:.1f};{r:.1f}" '
                 f'dur="{2.6 + (i % 5) * 0.55:.2f}s" repeatCount="indefinite"/>'
                 f'</circle>')
    o.append('</g>')
    return "".join(o)


def hand(x, y, s=1.0):
    skin, shade, line = "#f3bd8d", "#e0a473", "#22d3ee"
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    for r, dl in [(40, 0.0), (52, 0.4)]:
        g.append(f'<path d="M {r},-20 A {r},{r} 0 0 1 {r},20" fill="none" stroke="{line}" '
                 f'stroke-width="2.6" stroke-linecap="round" opacity="0">'
                 f'<animate attributeName="opacity" values="0;0;0.6;0;0" '
                 f'keyTimes="0;0.05;0.15;0.28;1" dur="4.2s" begin="{dl}s" repeatCount="indefinite"/>'
                 f'</path>')
    g.append('<g>')
    g.append('<animateTransform attributeName="transform" type="rotate" '
             'values="0 0 34;-19 0 34;15 0 34;-19 0 34;15 0 34;0 0 34;0 0 34" '
             'keyTimes="0;0.05;0.10;0.15;0.20;0.26;1" dur="4.2s" repeatCount="indefinite"/>')
    g.append(f'<rect x="-13" y="24" width="26" height="18" rx="9" fill="{shade}"/>')
    g.append(f'<g transform="rotate(-48 -18 12)">'
             f'<rect x="-27" y="0" width="11" height="26" rx="5.5" fill="{shade}"/></g>')
    for fx, tip in [(-20, -30), (-9, -37), (2, -33), (13, -22)]:
        g.append(f'<rect x="{fx}" y="{tip}" width="10" height="{10 - tip}" rx="5" fill="{skin}"/>')
    g.append(f'<rect x="-22" y="-6" width="45" height="36" rx="16" fill="{skin}"/>')
    g.append('</g></g>')
    return "".join(g)


def build(theme):
    t = THEMES[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Hi there, I am Mowlya. I build data pipelines and ML systems.">']
    o.append('<defs>')
    o.append(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{t["bg1"]}"/><stop offset="55%" stop-color="{t["bg2"]}"/>'
             f'<stop offset="100%" stop-color="{t["bg1"]}"/></linearGradient>')
    o.append(f'<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["a1"]}"/><stop offset="50%" stop-color="{t["a2"]}"/>'
             f'<stop offset="100%" stop-color="{t["a1"]}"/>'
             f'<animateTransform attributeName="gradientTransform" type="translate" '
             f'values="-1 0;1 0;-1 0" dur="9s" repeatCount="indefinite"/></linearGradient>')
    o.append(f'<radialGradient id="gA"><stop offset="0%" stop-color="{t["a2"]}" stop-opacity="0.16"/>'
             f'<stop offset="100%" stop-color="{t["a2"]}" stop-opacity="0"/></radialGradient>')
    o.append(f'<radialGradient id="gB"><stop offset="0%" stop-color="{t["a1"]}" stop-opacity="0.14"/>'
             f'<stop offset="100%" stop-color="{t["a1"]}" stop-opacity="0"/></radialGradient>')
    for i, ln in enumerate(LINES):
        ls = 1.5 * len(ln["txt"]) if ln.get("anchor") == "end" else 0
        wpx = w_of(ln["txt"], ln["size"]) + ls + 14
        cx0 = ln["x"] - wpx if ln.get("anchor") == "end" else ln["x"]
        s, d = ln["start"] / CYCLE, ln["dur"] / CYCLE
        o.append(f'<clipPath id="clip{i}"><rect x="{cx0}" y="{ln["y"]-ln["size"]}" '
                 f'height="{ln["size"]*1.5}" width="0">'
                 f'<animate attributeName="width" values="0;0;{wpx:.0f};{wpx:.0f};0;0" '
                 f'keyTimes="0;{s:.4f};{s+d:.4f};0.94;0.965;1" dur="{CYCLE}s" '
                 f'repeatCount="indefinite"/></rect></clipPath>')
    o.append('</defs>')
    o.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>')
    o.append(f'<circle cx="860" cy="40" r="170" fill="url(#gA)">'
             f'<animate attributeName="r" values="150;185;150" dur="11s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="110" cy="224" r="155" fill="url(#gB)">'
             f'<animate attributeName="r" values="170;140;170" dur="11s" repeatCount="indefinite"/></circle>')
    o.append(constellation(t))
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{t["ring"]}"/>')
    o.append(hand(106, 84, 1.15))
    for i, ln in enumerate(LINES):
        fill = (ln["fill"].replace("SHINE", "url(#shine)").replace("BODY", t["body"])
                .replace("MUTE", t["mute"]).replace("FAINT", t["faint"]))
        style = "italic" if i == 2 else "normal"
        sp = ' letter-spacing="1.5"' if i == 3 else ''
        an = ' text-anchor="end"' if ln.get("anchor") == "end" else ''
        o.append(f'<g clip-path="url(#clip{i})"><text x="{ln["x"]}" y="{ln["y"]}" font-family="{MONO}" '
                 f'font-size="{ln["size"]}" font-weight="{ln["weight"]}" font-style="{style}"{sp}{an} '
                 f'fill="{fill}">{esc(ln["txt"])}</text></g>')
    o.append('</svg>')
    return "\n".join(o)


os.makedirs("assets", exist_ok=True)
for n in THEMES:
    open(f"assets/hero-{n}.svg", "w").write(build(n))
    print("wrote assets/hero-%s.svg" % n, os.path.getsize(f"assets/hero-{n}.svg"), "bytes")
