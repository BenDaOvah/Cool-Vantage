# Cool Vantage Website

Static marketing website for **Cool Vantage Air Conditioning & Refrigeration LLC** (Apopka, FL) — plain HTML/CSS/JS, no frameworks required to serve it.

## Repository layout

| Path | What it is |
|---|---|
| `public/` | **The actual website.** 10 static pages (HTML), shared CSS/JS in `public/assets/`, images, `robots.txt`, `sitemap.xml`, `404.html`, `_redirects`. |
| `public/_redirects` | Clean-URL routing for Cloudflare Pages (`/services` → `/services/index.html`, root `/` → home, etc.). |
| `src/app/` | Local preview wrapper only (iframe). **Not needed in production.** |
| `next.config.ts` | Maps the same clean URLs for the local Next.js dev server. |

## Edit content

- Pages live in `public/<page>/index.html` (one file per page, single-line formatting — search inside the line).
- Shared styles: `public/assets/css/site.css`
- Shared behavior (mobile menu, FAQ accordions, footer year): `public/assets/js/site.js`
- Images: `public/assets/images/`

> Note: the contact email `info@coolvantageac.com` is a placeholder — replace it with the real mailbox (search all HTML files for `coolvantageac.com`).

## Run locally

```bash
bun install
bun run dev        # dev server on http://localhost:3000 (open / for the preview wrapper)
```

Direct static pages also work during dev: `/home`, `/about`, `/contact`, `/services`, etc.

## Deploy: GitHub → Cloudflare Pages

### 1. Push to GitHub

```bash
git remote add origin git@github.com:<your-user>/cool-vantage-website.git
git push -u origin main
```

### 2. Connect Cloudflare Pages (static — recommended)

1. Cloudflare Dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git** → pick this repo.
2. Build settings:
   - **Framework preset:** `None`
   - **Build command:** *(leave empty)*
   - **Build output directory:** `/public`
3. **Save and Deploy.** Done — no build step is needed; `public/` is the finished site.

Clean URLs (e.g. `/services/ac-repair`) are handled by `public/_redirects`; unknown routes fall back to `404.html` automatically.

### 3. Custom domain

In the Pages project → **Custom domains** → add `coolvantageac.com` (and `www`), then follow Cloudflare's DNS instructions. Update `sitemap.xml` / canonical tags only if the final domain differs from `https://coolvantageac.com/`.

### Why not deploy the Next.js app itself?

The Next.js app only exists to preview the static site inside the development sandbox. The whole site is static, so Cloudflare Pages serves it directly with zero build cost. If a full Next.js deploy is ever needed, use the Cloudflare "Workers" (OpenNext) adapter instead of Pages.
