# Edison Sheppard — Project Portfolio

A static, GitHub Pages-hosted engineering and maker portfolio.

## Site structure

- `site/` — the **only** directory published to the internet.
- `site/data/projects.json` — vetted project summaries shown on the site (empty until approved projects are imported).
- `tools/check_publish.py` — pre-publication checks for dangerous assets, credentials, and suspicious text.
- `tools/build.py` — validates project data and builds `dist/` from `site/`.
- `config/project-sources.json` — placeholder registry for project repositories (do not put private details or credentials here).
- `docs/` — project metadata and security guidelines.
- `.github/workflows/pages.yml` — build, scan and GitHub Pages deployment.

## One-time setup

1. Go to **Settings → Pages → Build and deployment** and select **GitHub Actions**.
2. Push or re-run the **Publish portfolio** workflow on the Actions tab.
3. Open your published project website at `https://edisonsheppard.github.io/edisonSheppardWebsiteCV/`.

This repository is public. **Never commit private reports, access tokens, API keys, raw sensitive datasets or other source files that should not become public.** Publish *selected, vetted* project details and selected images only.

## Adding projects

Each project can keep its own private repository. Suggested structure:

```text
My-Project/
  Portfolio/
    README.md
    project.yml
    images/
    supporting/   # private reports, CAD, spreadsheets, etc.
```

Supporting materials are sources for review, **not automatic public downloads**. A future import/AI review process will read them with approved credentials, prepare a proposed project page, check sensitive content, and open a pull request for approval. This initial site setup does *not* yet fetch private repositories or use AI.

See [project format](docs/PROJECTS.md) and [publishing safety](docs/SECURITY.md).

## Local checks

```bash
python3 tools/check_publish.py
python3 tools/build.py
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000` to preview.

## Design

About section first, no navigation bar, responsive project cards, and a static placeholder instead of a 3D model. No front-end framework or external analytics required.
