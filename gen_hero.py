import math, os, random

THEMES = {
    "dark":  dict(bg1="#0d1117", bg2="#11161d", body="#c9d1d9", mute="#7d8590",
                  faint="#586069", ring="#21262d", a1="#22d3ee", a2="#a78bfa",
                  node="#8b949e", edge="#8b949e"),
    "light": dict(bg1="#ffffff", bg2="#f6f8fa", body="#1f2328", mute="#57606a",
                  faint="#8c959f", ring="#d8dee4", a1="#0891b2", a2="#7c3aed",
                  node="#6e7781", edge="#8c959f"),
}

W, H = 1000, 300
CYCLE = 16.0
DRIFT = 17.0
NODES = 34
KEYS = 8
LINK = 170
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

LINES = [
    dict(txt="Hi there! I'm Mowlya", x=196, y=150, size=40, weight="700",
         fill="SHINE", start=0.6, dur=2.0),
    dict(txt="I build data pipelines and ML systems that reach production.",
         x=196, y=192, size=16, weight="400", fill="BODY", start=3.0, dur=2.2),
    dict(txt='"I have no special talent. I am only passionately curious."',
         x=196, y=228, size=15, weight="400", fill="MUTE", start=5.8, dur=2.6),
    dict(txt="- Albert Einstein", x=728, y=254, size=12, weight="400",
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
    o = ['<g opacity="0.55">']
    for i, j, d in edges:
        op = max(0.06, 0.34 * (1 - d / LINK))
        vx1 = ";".join(f"{v:.1f}" for v in xs[i])
        vy1 = ";".join(f"{v:.1f}" for v in ys[i])
        vx2 = ";".join(f"{v:.1f}" for v in xs[j])
        vy2 = ";".join(f"{v:.1f}" for v in ys[j])
        o.append(f'<line x1="{xs[i][0]:.1f}" y1="{ys[i][0]:.1f}" x2="{xs[j][0]:.1f}" '
                 f'y2="{ys[j][0]:.1f}" stroke="{t["edge"]}" stroke-opacity="{op:.2f}" '
                 f'stroke-width="1">'
                 f'<animate attributeName="x1" values="{vx1}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y1" values="{vy1}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="x2" values="{vx2}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y2" values="{vy2}" dur="{DRIFT}s" repeatCount="indefinite"/>'
                 f'</line>')
    for i in range(NODES):
        r = 2.4 + (i % 4) * 0.7
        c = t["a1"] if i % 5 == 0 else (t["a2"] if i % 7 == 0 else t["node"])
        op = 0.75 if c != t["node"] else 0.5
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


def hand(x, y, s=1.35):
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    g.append('<animateTransform attributeName="transform" type="rotate" additive="sum" '
             'values="0;-18;15;-18;15;0;0" keyTimes="0;0.04;0.08;0.12;0.16;0.2;1" '
             'dur="4.5s" repeatCount="indefinite"/>')
    skin, shade = "#f6c193", "#e8ab77"
    for i, fx in enumerate([-14.5, -5, 4.5, 14]):
        h = [24, 27, 26, 21][i]
        g.append(f'<rect x="{fx}" y="{-h}" width="8.6" height="{h+10}" rx="4.3" fill="{skin}"/>')
    g.append(f'<g transform="rotate(-42 -17 12)"><rect x="-25" y="2" width="8.6" height="20" rx="4.3" '
             f'fill="{shade}"/></g>')
    g.append(f'<rect x="-19" y="4" width="38" height="30" rx="12" fill="{skin}"/>')
    g.append('</g>')
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
        wpx = w_of(ln["txt"], ln["size"]) + 6
        cx0 = ln["x"] - wpx if ln.get("anchor") == "end" else ln["x"]
        s, d = ln["start"] / CYCLE, ln["dur"] / CYCLE
        o.append(f'<clipPath id="clip{i}"><rect x="{cx0}" y="{ln["y"]-ln["size"]}" '
                 f'height="{ln["size"]*1.5}" width="0">'
                 f'<animate attributeName="width" values="0;0;{wpx:.0f};{wpx:.0f};0;0" '
                 f'keyTimes="0;{s:.4f};{s+d:.4f};0.94;0.965;1" dur="{CYCLE}s" '
                 f'repeatCount="indefinite"/></rect></clipPath>')
    o.append('</defs>')
    o.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>')
    o.append(f'<circle cx="860" cy="52" r="200" fill="url(#gA)">'
             f'<animate attributeName="r" values="175;215;175" dur="11s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="110" cy="286" r="185" fill="url(#gB)">'
             f'<animate attributeName="r" values="200;168;200" dur="11s" repeatCount="indefinite"/></circle>')
    o.append(constellation(t))
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{t["ring"]}"/>')
    o.append(hand(112, 128))
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
