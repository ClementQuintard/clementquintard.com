# clementquintard.com

Static site for clementquintard.com, deployed on Cloudflare (Workers static assets).

## Layout
- `posts/*.md` — blog posts. Front matter (title, date, image, excerpt, optional alt, optional `format: html`), then the body in Markdown (or HTML when `format: html`). Math works with `\( ... \)` inline and `$$ ... $$` display.
- `pubs.json` — publications list (year, title, authors, venue, doi/url, lead, type, status).
- `page-research.md` — full background page.
- `img/` — images. `cv.pdf` — the CV served at /cv.pdf.
- `style.css`, `site.js` — design and the hero animation.
- `build.py` — generates `site/` from the above. `pip install markdown`, then `python3 build.py`.

## Deploy
Cloudflare Workers Builds runs `pip install markdown && python3 build.py`, then `npx wrangler deploy` publishes `site/` as static assets (see `wrangler.jsonc`).
