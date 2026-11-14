# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static, single-professional website for Débora Araújo dos Reis (aromatherapist), in Brazilian Portuguese. Built with Python (Jinja2, as a static site generator only — never a runtime server) + plain HTML/CSS/JS. No JS framework, no CSS framework, no client-side build tooling.

The full design/content brief (benchmarking, palette rationale, typography, IA decisions, SEO/LGPD requirements, blog editorial plan) lives in `docs/proposta-site-debora.md` — read it before making structural or visual changes, since most design decisions are justified there rather than in code comments.

## Commands

```powershell
uv sync                      # install deps (jinja2, markdown, python-frontmatter, pillow)
uv run python build.py       # renders templates/ + content/blog/*.md into dist/
```

There is no lint, format, or test suite configured in this project.

`dist/` **must** be served over HTTP to preview — internal links are root-relative (`/static/...`, `/blog/...`) and will not resolve via `file://`, and won't resolve correctly either if the server root isn't `dist/` itself (e.g. serving from the repo root and browsing to `/dist/index.html` breaks every `/static/...` link). Use the built-in serve mode, which always gets this right:

```powershell
uv run python build.py --serve   # builds, then serves dist/ at http://localhost:8000/index.html
```

Equivalent manual steps, if needed: `uv run python build.py` then `cd dist && uv run python -m http.server 8000`.

The most common "site loads with no CSS" report is a leftover `$env:BASE_PATH` from a previous deploy build in the same PowerShell session (see below) — `--serve` prints a warning when `BASE_PATH` is set, since in that case the site expects to be served from `/aromoterapia/...`, not from the root.

### Deploying to GitHub Pages

The site is published from a `gh-pages` branch containing only the built `dist/` output (a separate, disposable git history from `master`/source) — the standard static-site-generator deploy pattern. `master` never contains `dist/` (gitignored).

Because the live site is a GitHub Pages *project* site (`wilsonreis.github.io/aromoterapia/`, not a bare user site or custom domain), the build must be run with `BASE_PATH` set to the repo path, or all internal links break (404 on CSS/images):

```powershell
$env:BASE_PATH = "/aromoterapia"
uv run python build.py
# then commit dist/ contents as the root of the gh-pages branch and force-push
Remove-Item Env:BASE_PATH   # unset immediately — PowerShell env vars persist for the rest of the session
```

Omit `BASE_PATH` (default `""`) for local preview or if the site ever moves to a custom domain / bare `*.github.io` root.

## Architecture

**Build pipeline** (`build.py`, ~150 lines, single file, no other build code):
- Jinja2 `Environment` renders `templates/*.html` into `dist/`.
- Blog posts are Markdown files with YAML front-matter in `content/blog/*.md`, loaded via `python-frontmatter` and converted with the `markdown` package. Files whose name starts with `_` (e.g. `_exemplo-de-artigo.md`) are treated as drafts/reference and skipped by `carregar_posts()` — that's how you keep an authoring template in the repo without publishing it.
- `preparar_saida()` deliberately does **not** `shutil.rmtree(dist/)` before rebuilding — on Windows, a directory that's the cwd of a running `http.server` (or otherwise open) cannot be removed, so the build only copies static assets with `dirs_exist_ok=True` and prunes blog post HTML files whose slug no longer exists in `content/blog/`.
- All site-wide config (business name, WhatsApp number/message, email, Instagram, canonical domain, theme color, `BASE_PATH`) is centralized at the top of `build.py` in the `SITE` dict and the `NUMERO_WHATSAPP`/`BASE_PATH` constants — that is the single place to update contact info, not the templates.
- `base` (= `BASE_PATH`) is passed into every template render and prefixes every internal URL (`{{ base }}/static/...`, `{{ base }}/blog/...`). `site.url` (the absolute canonical domain) is a separate concept used only for `<link rel="canonical">`, Open Graph tags, and `sitemap.xml` — both get combined as `{{ site.url }}{{ base }}...` where an absolute URL is required.

**Templates** (`templates/`):
- `base.html` is the shell (`<head>`, header/footer/WhatsApp-float includes, Google Fonts, theme-color) that every page extends via Jinja2 blocks (`titulo`, `description`, `og_titulo`, `og_descricao`, `conteudo`).
- `templates/partials/` (`header.html`, `footer.html`, `whatsapp-float.html`) are `{% include %}`d from `base.html`, not extended.
- `index.html` is the entire home page as one-page sections with anchor IDs (`#sobre`, `#aromaterapia`, `#servicos`, `#depoimentos`, `#faq`, `#contato`) — this is an intentional IA decision (see the proposal doc, section 4): institutional content is one-page, but blog posts and the privacy policy are real separate pages for SEO/shareability.
- `blog_index.html` / `blog_post.html` render the `posts` list / a single `post` dict assembled in `build.py`.

**Styling** (`static/css/`):
- `tokens.css` — only CSS custom properties (light/dark palette, fonts, radii, shadow). Dark mode is driven by `[data-tema="escuro"|"claro"]` on `<html>` (explicit user choice, persisted to `localStorage`) falling back to `@media (prefers-color-scheme: dark)` when no explicit choice was made ("Automático").
- `estilos.css` — every component, numbered in sections by comment headers, mobile-first (unprefixed base styles = mobile; `@media (min-width: ...)` adds complexity for tablet/desktop). Uses `clamp()` for fluid type/spacing instead of fixed breakparately-tuned sizes, and CSS grid `repeat(auto-fill, minmax(...))` so card grids (services, benefits, testimonials, blog) reflow without per-breakpoint column rules.
- **Known footgun**: watch CSS specificity when adding a new modifier class meant to override a component's base display/layout (e.g. hiding something below a breakpoint) — a same-specificity single-class rule declared *earlier* in the file can lose to one declared *later* (e.g. `.botao { display: inline-flex }` vs `.topo__cta { display: none }`) regardless of which one is "more specific in intent". Prefer a compound selector (`.parent .child`) for override rules instead of relying on file order.

**JS** (`static/js/`, all vanilla IIFEs, zero dependencies):
- `app.js` — theme cycling (auto → claro → escuro, `localStorage`), footer year, copy-email button.
- `menu.js` — mobile hamburger nav toggle.
- `faq.js` — accordion (single-open) for the FAQ section.

**Images** (`static/img/`): `debora-avatar.jpg`/`.webp` (hero) and `debora-avatar-mini.*` (header brand mark) were produced from a source photo via a one-off Pillow crop/rotate/enhance script (not part of `build.py` — there's no repeatable image pipeline yet, so new photos need the same manual treatment).

## Content policy

- Testimonial cards in `templates/index.html` are explicitly placeholder ("depoimento de exemplo", commented as such) and must be replaced with real, authorized patient testimonials before the site is considered launch-ready — do not treat them as real content.
- Copy must keep the "complementary practice, not medical treatment" disclaimer (`.aviso` block + footer) intact — this is a deliberate LGPD/ethics decision from the proposal doc, not boilerplate to trim.
