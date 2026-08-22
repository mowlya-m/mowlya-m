import os

THEMES = {
    "dark":  dict(bg1="#0d1117", bg2="#11161d", dot="#1b2430", body="#c9d1d9",
                  mute="#7d8590", faint="#586069", ring="#21262d",
                  a1="#22d3ee", a2="#a78bfa", chip="#161b22", chipb="#262d38"),
    "light": dict(bg1="#ffffff", bg2="#f6f8fa", dot="#e4e8ed", body="#1f2328",
                  mute="#6e7781", faint="#8c959f", ring="#d8dee4",
                  a1="#0891b2", a2="#7c3aed", chip="#f6f8fa", chipb="#d8dee4"),
}

W, H = 1000, 300
CYCLE = 16.0
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "Segoe UI,Helvetica Neue,Helvetica,Arial,sans-serif"

NAME = "Hiii, I'm Mowlya"
ABOUT = "I turn messy data into pipelines, models and decisions."
QUOTE = "I have no special talent. I am only passionately curious."
WHO = "Albert Einstein"
CHIPS = ["Data Engineering", "Machine Learning", "AWS", "Melbourne, AU"]


def wmono(txt, size):
    return len(txt) * size * 0.601


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def hand(x, y, t):
    g = [f'<g transform="translate({x},{y}) scale(0.95)">']
    g.append('<animateTransform attributeName="transform" type="rotate" additive="sum" '
             'values="0;-17;14;-17;14;0;0" keyTimes="0;0.045;0.09;0.135;0.18;0.225;1" '
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
         f'role="img" aria-label="Hi, I am Mowlya, Data and Machine Learning Engineer">']
    o.append('<defs>')
    o.append(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{t["bg1"]}"/><stop offset="55%" stop-color="{t["bg2"]}"/>'
             f'<stop offset="100%" stop-color="{t["bg1"]}"/></linearGradient>')
    o.append(f'<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["a1"]}"/><stop offset="50%" stop-color="{t["a2"]}"/>'
             f'<stop offset="100%" stop-color="{t["a1"]}"/>'
             f'<animateTransform attributeName="gradientTransform" type="translate" '
             f'values="-1 0;1 0;-1 0" dur="9s" repeatCount="indefinite"/></linearGradient>')
    o.append(f'<radialGradient id="g1"><stop offset="0%" stop-color="{t["a2"]}" stop-opacity="0.20"/>'
             f'<stop offset="100%" stop-color="{t["a2"]}" stop-opacity="0"/></radialGradient>')
    o.append(f'<radialGradient id="g2"><stop offset="0%" stop-color="{t["a1"]}" stop-opacity="0.17"/>'
             f'<stop offset="100%" stop-color="{t["a1"]}" stop-opacity="0"/></radialGradient>')
    o.append(f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
             f'<circle cx="1.2" cy="1.2" r="1.2" fill="{t["dot"]}"/></pattern>')

    lines = [dict(txt=NAME, x=70, y=126, size=44, start=0.5, dur=1.9),
             dict(txt=ABOUT, x=70, y=172, size=17, start=2.9, dur=2.0)]
    for i, ln in enumerate(lines):
        wpx = wmono(ln["txt"], ln["size"]) + 8
        s, d = ln["start"] / CYCLE, ln["dur"] / CYCLE
        o.append(f'<clipPath id="c{i}"><rect x="{ln["x"]}" y="{ln["y"]-ln["size"]}" '
                 f'height="{ln["size"]*1.5}" width="0">'
                 f'<animate attributeName="width" values="0;0;{wpx:.0f};{wpx:.0f};0;0" '
                 f'keyTimes="0;{s:.4f};{s+d:.4f};0.945;0.97;1" dur="{CYCLE}s" repeatCount="indefinite"/>'
                 f'</rect></clipPath>')
    o.append('</defs>')

    o.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>')
    o.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#dots)" opacity="0.75"/>')
    o.append(f'<circle cx="880" cy="60" r="210" fill="url(#g1)">'
             f'<animate attributeName="r" values="185;225;185" dur="11s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="90" cy="290" r="190" fill="url(#g2)">'
             f'<animate attributeName="r" values="205;170;205" dur="11s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{t["ring"]}"/>')

    for i, c in enumerate([t["a1"], t["a2"], t["faint"]]):
        o.append(f'<circle cx="{70+i*18}" cy="48" r="5" fill="{c}" opacity="0.6"/>')
    o.append(f'<text x="{70+3*18+14}" y="53" font-family="{MONO}" font-size="12" letter-spacing="1.8" '
             f'fill="{t["faint"]}">mowlya-m . profile</text>')

    cx, cy = 858, 152
    for k, (r, tilt, dur) in enumerate([(64, 0, 14), (64, 60, 18), (64, 120, 22)]):
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*0.36:.0f}" fill="none" '
                 f'stroke="{t["a2"] if k%2 else t["a1"]}" stroke-opacity="0.30" '
                 f'transform="rotate({tilt} {cx} {cy})"/>')
        path = f'M {cx-r},{cy} a {r},{r*0.36:.0f} 0 1,0 {2*r},0 a {r},{r*0.36:.0f} 0 1,0 {-2*r},0'
        o.append(f'<g transform="rotate({tilt} {cx} {cy})"><circle r="4.5" '
                 f'fill="{t["a1"] if k%2 else t["a2"]}">'
                 f'<animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}"/></circle></g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="13" fill="{t["a1"]}" opacity="0.9">'
             f'<animate attributeName="r" values="11;15;11" dur="3.2s" repeatCount="indefinite"/></circle>')

    o.append(hand(556, 104, t))
    o.append(f'<g clip-path="url(#c0)"><text x="70" y="126" font-family="{MONO}" font-size="44" '
             f'font-weight="700" fill="url(#shine)">{esc(NAME)}</text></g>')
    o.append(f'<g clip-path="url(#c1)"><text x="70" y="172" font-family="{SANS}" font-size="17" '
             f'fill="{t["body"]}">{esc(ABOUT)}</text></g>')

    x = 70
    for i, c in enumerate(CHIPS):
        cw = len(c) * 6.9 + 26
        b = 5.4 + i * 0.28
        o.append(f'<g opacity="0"><rect x="{x}" y="192" width="{cw:.0f}" height="27" rx="13.5" '
                 f'fill="{t["chip"]}" stroke="{t["chipb"]}"/>'
                 f'<circle cx="{x+14}" cy="205.5" r="3.4" fill="{t["a1"] if i%2==0 else t["a2"]}"/>'
                 f'<text x="{x+24}" y="210" font-family="{SANS}" font-size="12.5" fill="{t["mute"]}">'
                 f'{esc(c)}</text>'
                 f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                 f'keyTimes="0;{b/CYCLE:.4f};{(b+0.4)/CYCLE:.4f};0.945;0.97;1" dur="{CYCLE}s" '
                 f'repeatCount="indefinite"/></g>')
        x += cw + 10

    qy = 250
    o.append(f'<g opacity="0"><rect x="70" y="{qy-17}" width="3" height="48" rx="1.5" fill="{t["a2"]}"/>'
             f'<text x="88" y="{qy}" font-family="{SANS}" font-size="15" font-style="italic" '
             f'fill="{t["mute"]}">"{esc(QUOTE)}"</text>'
             f'<text x="88" y="{qy+23}" font-family="{MONO}" font-size="11.5" '
             f'letter-spacing="1.6" fill="{t["faint"]}">- {esc(WHO)}</text>'
             f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
             f'keyTimes="0;0.4375;0.4875;0.945;0.97;1" dur="{CYCLE}s" repeatCount="indefinite"/></g>')
    o.append('</svg>')
    return "\n".join(o)


os.makedirs("assets", exist_ok=True)
for n in THEMES:
    open(f"assets/hero-{n}.svg", "w").write(build(n))
    print("wrote assets/hero-%s.svg" % n)
