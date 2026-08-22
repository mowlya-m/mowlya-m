import json, os, urllib.request, collections

USER = "mowlya-m"
TOP = 10
FRAMES = 16
COUNT_DUR = 1.9
EXCLUDE = {"mowlya-m"}

THEMES = {
    "dark":  dict(bg="#0d111700", ring="#21262d", title="#22d3ee",
                  body="#c9d1d9", mute="#7d8590", track="#1b2430"),
    "light": dict(bg="#ffffff00", ring="#d8dee4", title="#0891b2",
                  body="#1f2328", mute="#6e7781", track="#e9edf1"),
}

COLORS = {
    "Python": "#3572A5", "Jupyter Notebook": "#DA5B0B", "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a", "HTML": "#e34c26", "CSS": "#563d7c", "SCSS": "#c6538c",
    "Shell": "#89e051", "HCL": "#844FBA", "Dockerfile": "#384d54", "Makefile": "#427819",
    "R": "#198CE7", "Java": "#b07219", "Go": "#00ADD8", "Rust": "#dea584",
    "SQL": "#e38c00", "PLpgSQL": "#336790", "Mako": "#7e858d", "Vue": "#41b883",
    "C++": "#f34b7d", "C": "#555555", "Kotlin": "#A97BFF", "Swift": "#F05138",
}
FALLBACK = ["#22d3ee", "#a78bfa", "#3fb950", "#f778ba", "#e3b341", "#58a6ff"]

W, PAD, BAR_Y, BAR_H, ROW_H, COL_W = 620, 28, 66, 12, 30, 282


def fetch():
    tok = os.environ.get("GH_TOKEN") or os.environ.get("PAT_1")
    hdr = {"User-Agent": "langs-card"}
    if tok:
        hdr["Authorization"] = "Bearer " + tok

    def get(u):
        return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=hdr)))

    totals, page = collections.Counter(), 1
    while True:
        repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}")
        if not repos:
            break
        for r in repos:
            if r["fork"] or r["name"] in EXCLUDE:
                continue
            totals.update(get(r["languages_url"]))
        if len(repos) < 100:
            break
        page += 1
    return totals


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def color(name, i):
    return COLORS.get(name, FALLBACK[i % len(FALLBACK)])


def build(theme, langs):
    t = THEMES[theme]
    rows = (len(langs) + 1) // 2
    H = BAR_Y + BAR_H + 26 + rows * ROW_H + 14
    inner = W - PAD * 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Most used languages">']
    o.append(f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}" stroke="{t["ring"]}"/>')
    o.append(f'<text x="{PAD}" y="40" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="18" '
             f'font-weight="600" fill="{t["title"]}">Most Used Languages</text>')
    o.append(f'<rect x="{PAD}" y="{BAR_Y}" width="{inner}" height="{BAR_H}" rx="{BAR_H/2}" fill="{t["track"]}"/>')
    o.append(f'<clipPath id="barclip"><rect x="{PAD}" y="{BAR_Y}" width="{inner}" height="{BAR_H}" '
             f'rx="{BAR_H/2}"/></clipPath>')
    o.append('<g clip-path="url(#barclip)">')
    off = 0.0
    for i, (name, pct) in enumerate(langs):
        seg = inner * pct / 100.0
        o.append(f'<rect x="{PAD+off:.1f}" y="{BAR_Y}" width="0" height="{BAR_H}" fill="{color(name,i)}">'
                 f'<animate attributeName="width" values="0;{seg:.2f}" dur="{COUNT_DUR}s" begin="0.15s" '
                 f'fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.2 1"/></rect>')
        off += seg
    o.append('</g>')
    step = COUNT_DUR / FRAMES
    for i, (name, pct) in enumerate(langs):
        col, row = i % 2, i // 2
        x = PAD + col * COL_W
        y = BAR_Y + BAR_H + 46 + row * ROW_H
        o.append(f'<circle cx="{x+6}" cy="{y-5}" r="6" fill="{color(name,i)}"/>')
        o.append(f'<text x="{x+22}" y="{y}" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
                 f'font-size="13.5" fill="{t["body"]}">{esc(name)}</text>')
        px = x + COL_W - 40
        for f in range(FRAMES + 1):
            p = f / FRAMES
            v = pct * (1 - (1 - p) ** 2)
            b = 0.15 + f * step
            sets = f'<set attributeName="opacity" to="1" begin="{b:.3f}s"/>'
            if f < FRAMES:
                sets += f'<set attributeName="opacity" to="0" begin="{b+step:.3f}s"/>'
            o.append(f'<text x="{px}" y="{y}" text-anchor="end" font-family="ui-monospace,SFMono-Regular,'
                     f'Menlo,monospace" font-size="13" fill="{t["mute"]}" '
                     f'opacity="{1 if f==FRAMES else 0}">{v:.2f}%{sets}</text>')
    o.append('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    try:
        totals = fetch()
        tot = sum(totals.values())
        langs = [(k, v * 100.0 / tot) for k, v in totals.most_common(TOP)]
        json.dump(langs, open("langs_cache.json", "w"))
    except Exception as e:
        print("api failed, using cache:", e)
        langs = [(a, b) for a, b in json.load(open("langs_cache.json"))]
    os.makedirs("assets", exist_ok=True)
    for th in THEMES:
        open(f"assets/langs-{th}.svg", "w").write(build(th, langs))
        print("wrote assets/langs-%s.svg" % th)
