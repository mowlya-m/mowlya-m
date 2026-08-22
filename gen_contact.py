import os

THEMES = {
    "dark":  dict(bg1="#0d1117", bg2="#11161d", dot="#1b2430", body="#c9d1d9",
                  mute="#8b949e", faint="#6e7681", ring="#21262d", panel="#161b22",
                  a1="#22d3ee", a2="#a78bfa", ok="#3fb950"),
    "light": dict(bg1="#ffffff", bg2="#f6f8fa", dot="#e4e8ed", body="#1f2328",
                  mute="#57606a", faint="#8c959f", ring="#d8dee4", panel="#f6f8fa",
                  a1="#0891b2", a2="#7c3aed", ok="#1a7f37"),
}

W, H = 1000, 206
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "Segoe UI,Helvetica Neue,Helvetica,Arial,sans-serif"

FACTS = [
    ("Based in", "Melbourne, AU", "open to Sydney and remote"),
    ("Work rights", "Full, no sponsorship", "subclass 485 post study visa"),
    ("Reply time", "Within 24 hours", "every message, every time"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme):
    t = THEMES[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Open to data and machine learning engineering roles">']
    o.append('<defs>')
    o.append(f'<linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{t["bg1"]}"/><stop offset="60%" stop-color="{t["bg2"]}"/>'
             f'<stop offset="100%" stop-color="{t["bg1"]}"/></linearGradient>')
    o.append(f'<linearGradient id="cshine" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["a1"]}"/><stop offset="50%" stop-color="{t["a2"]}"/>'
             f'<stop offset="100%" stop-color="{t["a1"]}"/>'
             f'<animateTransform attributeName="gradientTransform" type="translate" '
             f'values="-1 0;1 0;-1 0" dur="9s" repeatCount="indefinite"/></linearGradient>')
    o.append(f'<pattern id="cdots" width="24" height="24" patternUnits="userSpaceOnUse">'
             f'<circle cx="1.2" cy="1.2" r="1.2" fill="{t["dot"]}"/></pattern>')
    o.append('</defs>')
    o.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#cbg)"/>')
    o.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#cdots)" opacity="0.7"/>')
    o.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{t["ring"]}"/>')
    o.append(f'<rect x="16" y="16" width="4" height="{H-32}" rx="2" fill="url(#cshine)"/>')
    o.append(f'<circle cx="52" cy="45" r="6" fill="{t["ok"]}"/>')
    o.append(f'<circle cx="52" cy="45" r="6" fill="none" stroke="{t["ok"]}" stroke-width="2">'
             f'<animate attributeName="r" values="6;16;16" keyTimes="0;0.7;1" dur="2.4s" '
             f'repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0.75;0;0" keyTimes="0;0.7;1" dur="2.4s" '
             f'repeatCount="indefinite"/></circle>')
    o.append(f'<text x="70" y="50" font-family="{SANS}" font-size="19" font-weight="600" '
             f'fill="{t["body"]}">Let\'s build something</text>')
    o.append(f'<text x="70" y="74" font-family="{SANS}" font-size="14" fill="{t["mute"]}">'
             f'Open to Data and Machine Learning Engineering roles. I reply to every message, whether '
             f'it is a role, a collaboration or a question about a repo.</text>')
    px, pw, gap = 52, 292, 14
    for i, (label, value, note) in enumerate(FACTS):
        x = px + i * (pw + gap)
        o.append(f'<rect x="{x}" y="100" width="{pw}" height="80" rx="10" fill="{t["panel"]}" '
                 f'stroke="{t["ring"]}"/>')
        o.append(f'<rect x="{x}" y="100" width="3" height="80" rx="1.5" '
                 f'fill="{t["a1"] if i % 2 == 0 else t["a2"]}" opacity="0.85"/>')
        o.append(f'<text x="{x+20}" y="126" font-family="{MONO}" font-size="10.5" letter-spacing="2" '
                 f'fill="{t["faint"]}">{esc(label.upper())}</text>')
        o.append(f'<text x="{x+20}" y="150" font-family="{SANS}" font-size="15.5" font-weight="600" '
                 f'fill="{t["body"]}">{esc(value)}</text>')
        o.append(f'<text x="{x+20}" y="170" font-family="{SANS}" font-size="12" '
                 f'fill="{t["mute"]}">{esc(note)}</text>')
    o.append('</svg>')
    return "\n".join(o)


os.makedirs("assets", exist_ok=True)
for n in THEMES:
    open(f"assets/contact-{n}.svg", "w").write(build(n))
    print("wrote assets/contact-%s.svg" % n)
