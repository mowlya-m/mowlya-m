import os

THEMES = {
    "dark":  dict(body="#e6edf3", mute="#7d8590", a1="#22d3ee", a2="#a78bfa",
                  env="#22d3ee", env2="#0e7490"),
    "light": dict(body="#1f2328", mute="#57606a", a1="#0891b2", a2="#7c3aed",
                  env="#0891b2", env2="#164e63"),
}

W, H = 560, 104
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "Segoe UI,Helvetica Neue,Helvetica,Arial,sans-serif"

HEART = ("M 0,3 C 0,0.6 -1.9,-0.9 -3.6,-0.2 C -5,0.4 -5.4,2.1 -4.6,3.4 "
         "L 0,9 L 4.6,3.4 C 5.4,2.1 5,0.4 3.6,-0.2 C 1.9,-0.9 0,0.6 0,3 Z")


def build(theme):
    t = THEMES[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Reach me at">']
    o.append('<defs>')
    o.append(f'<linearGradient id="rg" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="{t["a1"]}"/><stop offset="50%" stop-color="{t["a2"]}"/>'
             f'<stop offset="100%" stop-color="{t["a1"]}"/>'
             f'<animateTransform attributeName="gradientTransform" type="translate" '
             f'values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/></linearGradient>')
    o.append('</defs>')
    for i, (dx, delay, sc) in enumerate([(0, 0, 1.0), (-13, 1.1, 0.72), (12, 2.2, 0.85)]):
        o.append(f'<g transform="translate({58+dx},40) scale({sc})" opacity="0">'
                 f'<path d="{HEART}" fill="{t["a2"] if i % 2 else t["a1"]}"/>'
                 f'<animateTransform attributeName="transform" type="translate" additive="sum" '
                 f'values="0 0;0 -26" dur="3.3s" begin="{delay}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;0.95;0" dur="3.3s" begin="{delay}s" '
                 f'repeatCount="indefinite"/></g>')
    o.append(f'<g transform="translate(58,60)">'
             f'<animateTransform attributeName="transform" type="translate" additive="sum" '
             f'values="0 0;0 -4;0 0" dur="2.6s" repeatCount="indefinite"/>'
             f'<rect x="-25" y="-16" width="50" height="34" rx="6" fill="{t["env"]}"/>'
             f'<path d="M -25,-11 L 0,6 L 25,-11" fill="none" stroke="{t["env2"]}" '
             f'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
             f'<rect x="-25" y="-16" width="50" height="34" rx="6" fill="none" '
             f'stroke="{t["env2"]}" stroke-width="2"/></g>')
    o.append(f'<text x="112" y="52" font-family="{SANS}" font-size="27" font-weight="700" '
             f'fill="url(#rg)">Reach me at</text>')
    o.append(f'<text x="114" y="76" font-family="{MONO}" font-size="12" letter-spacing="1.4" '
             f'fill="{t["mute"]}">i reply to every message</text>')
    o.append(f'<rect x="{114 + 23*12*0.74 + 8:.0f}" y="66" width="7" height="13" fill="{t["a1"]}">'
             f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.45;0.5;0.95;1" '
             f'dur="1.3s" repeatCount="indefinite"/></rect>')
    o.append('</svg>')
    return "\n".join(o)


def logo_m(theme):
    t = THEMES[theme]
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" '
         'role="img" aria-label="Portfolio">']
    o.append(f'<defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{t["a1"]}"/><stop offset="100%" stop-color="{t["a2"]}"/>'
             f'</linearGradient>'
             f'<linearGradient id="ms" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>'
             f'<stop offset="50%" stop-color="#ffffff" stop-opacity="0.55"/>'
             f'<stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>'
             f'<animateTransform attributeName="gradientTransform" type="translate" '
             f'values="-1 0;1 0;-1 0" dur="4.5s" repeatCount="indefinite"/></linearGradient>'
             f'<clipPath id="mc"><rect x="6" y="6" width="84" height="84" rx="24"/></clipPath></defs>')
    o.append('<rect x="6" y="6" width="84" height="84" rx="24" fill="url(#mg)">'
             '<animate attributeName="rx" values="24;30;24" dur="4s" repeatCount="indefinite"/></rect>')
    o.append('<text x="48" y="66" text-anchor="middle" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
             'font-size="46" font-weight="800" fill="#ffffff">m</text>')
    o.append('<rect x="6" y="6" width="84" height="84" fill="url(#ms)" clip-path="url(#mc)"/>')
    o.append('<circle cx="76" cy="22" r="3.4" fill="#ffffff" opacity="0.9">'
             '<animate attributeName="opacity" values="0.2;1;0.2" dur="2.2s" repeatCount="indefinite"/>'
             '</circle>')
    o.append('</svg>')
    return "\n".join(o)


os.makedirs("assets", exist_ok=True)
for n in THEMES:
    open(f"assets/reachme-{n}.svg", "w").write(build(n))
    open(f"assets/logo-m-{n}.svg", "w").write(logo_m(n))
    print("wrote reachme + logo-m", n)
