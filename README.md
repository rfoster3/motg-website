# Magicians on the Green (MotG) — Website Mockup

A hand-built visual mockup of the MotG storefront. It is **not live on Shopify
yet** — it is a clickable design draft, structured page-for-page and
section-for-section so it can be rebuilt on Shopify when the store is purchased.

## How to view it

Open `index.html` in any browser (double-click it), then click through the nav.
No build step, no server needed. Fonts load from Google Fonts (needs internet).

## What's here

| File | Purpose | Shopify equivalent |
|------|---------|--------------------|
| `index.html` | Home | Theme home with sections |
| `shop.html` | Product catalog | Collection page (filters = tags/types) |
| `product.html` | Product detail (Magic Stick example) | Product template + variants |
| `donate.html` | Direct giving | Page + preset donation products |
| `tournament.html` | Magic on the Greens event | Page + entry products |
| `sponsors.html` | Sponsor tiers | Page + sponsor-tier products |
| `story.html` | Our Story / The Team | Page |
| `css/brand.css` | All brand colors, fonts, components | Theme settings / CSS |

The little dark `Shopify: …` notes on each page are build hints for the rebuild.
Delete them (search the HTML for `sf-note`) before showing anyone the polished version.

## Swapping in the real images

Drop the real files into `assets/` using these exact names and the placeholders
fill in automatically (every image has an `onerror` fallback, so missing files
just show a labeled placeholder):

| Filename | What it is |
|----------|------------|
| `logo-m.png` | Ornate script "M" logomark (transparent PNG) — used in the header circle |
| `wizard-mascot.png` | Golf-wizard mascot, transparent PNG — home + story hero |
| `cap-star-m.png` | Star "M" cap |
| `cap-purple-m.jpg` | Purple performance "M" cap |
| `magic-stick-headcovers.jpg` | Magic Stick driver/3-wood headcovers — featured + product page |
| `magic-stick-3wood.jpg` | Fairway headcover alt shot |
| `team-shirt.jpg` | Cream team button-up |
| `wizard-tee.jpg`, `quarter-zip.jpg`, `towel.jpg` | Other shop items |
| `team-photo.jpg` | Group team photo — home "The Team" band |
| `player-photo.jpg`, `player-1/2/3.jpg`, `coach.jpg` | Story / sponsor photos |

Tip: the wizard mascot and the "M" logo look best as **transparent PNGs** so they
sit cleanly on the purple backgrounds.

## Brand system (edit in `css/brand.css`)

- Purple `#4B2A7F`, Deep purple `#2E1A4F`, Gold `#C9A24B`, Cream `#F5F0E1`.
- Fonts: Cinzel (display serif), Allura (script accent), Anton (loud labels),
  Figtree (body). Change them in one place at the top of `brand.css`.

## Ways to give (all three are built in)

1. **Merch** — hats, shirts, Magic Stick headcovers (`shop.html` / `product.html`).
2. **Donations** — preset tiers + name-your-amount (`donate.html`).
3. **Tournament entries** — Team $1,500 (cap 15) + Individual $300 (`tournament.html`).
4. **Sponsors** — Friend / Cart / Hole / Title + Sponsor-a-Player (`sponsors.html`).

## When Shopify is ready (next steps)

1. Buy the Shopify plan and pick a clean theme (Dawn or a premium golf/retail theme).
2. Rebuild each page above using Shopify sections; paste brand colors into theme
   settings and add the fonts.
3. Donations: Shopify has no native "name your price," so use a donation app
   (e.g. a tip/donation app) or create preset donation products.
4. Tournament: make **Team Entry** and **Individual Entry** products; cap the team
   product's inventory at 15. Collect player names via order notes or a form app.
5. Sponsors: one product per tier; capture logos via an order note / cart attribute
   or a follow-up form.
6. Wire payments, shipping, and a confirmation email. Final copy + SEO pass.

## Note on the source flyer

Tournament details (dates, schedule, venue, prices, lodging, contact) are taken
straight from the event flyer and can be edited in `tournament.html`.
