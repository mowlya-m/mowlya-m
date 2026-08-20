# Setup

## 1. Push the profile repo

```
cd ~/Downloads/"PERSONAL PROJECT"/mowlya-m
git add .
git commit -m "feat: update profile readme"
git push
```

Asset URLs point at `.../mowlya-m/main/assets/...`. If your default branch is
`master`, run `sed -i '' 's|/mowlya-m/main/|/mowlya-m/master/|g' README.md` first.

## 2. Make the GitHub Stats cards work

The stats section is empty until you create a second repo. This is the card that
counts stars, forks, all-time contributions, lines changed, repository views, and
renders the language percentage bar.

### a. Make a classic personal access token
Settings, Developer settings, Personal access tokens, Tokens (classic),
Generate new token (classic).

Tick exactly three scopes: `read:user`, `user:email`, `repo`.
Set expiration to No expiration. Copy the token, you cannot view it again.

### b. Create the repo from the template
Open https://github.com/jstrieb/github-stats/generate and name the new repo
exactly `github-stats` under your own account. Use the template, do not fork.

### c. Add the token
In the new repo: Settings, Secrets and variables, Actions, New repository secret.
Name it `ACCESS_TOKEN`, paste the token as the value.

### d. Optional exclusions
Add a secret `EXCLUDE_REPOS` with value `mowlya-m/github-stats` so the stats repo
does not count itself.

### e. Generate
Actions tab, Generate Stats Images, Run workflow. The images land on the
`generated` branch and refresh every 24 hours.

The README already points at:
```
https://github.com/mowlya-m/github-stats/raw/generated/overview.svg
https://github.com/mowlya-m/github-stats/raw/generated/languages.svg
```

Lines changed and view counts are approximate. GitHub will not count lines for
repos with more than 10,000 commits, and repos you lack view permission on count
as zero views.

## 3. Turn on the Activity overview graph

This is a GitHub profile setting, not part of the README.

1. Go to your profile page, github.com/mowlya-m
2. Above the green contributions grid, open the **Contribution settings** dropdown
3. Tick **Activity overview**

That adds the panel showing which repositories you are most active in and the
commits / issues / pull requests / code review breakdown.

## 4. Editing the animated assets

```
pip install cairosvg
python3 gen.py
```

Palettes live in the `THEMES` dict at the top of `gen.py`. Header topology,
intro card copy and the quote are each their own function.

Every asset is a hand written SVG using SMIL animation, which is the only
animation technique that survives GitHub's camo image proxy. Animations share
one duration with fractional keyTimes so the whole scene loops in sync. Light
and dark variants are swapped with `<picture>` and `prefers-color-scheme`.
