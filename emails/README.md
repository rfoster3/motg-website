# Magicians on the Green: Email Program

Mobile-first, brand HTML built for **Shopify Email**. No em dashes or en dashes anywhere (house rule).
Paste each file's HTML into Shopify Email (see "How to set up" at the bottom).

Build order is by impact: do Abandoned checkout and Welcome first, then Tournament countdown, then post-purchase.

---

## The emails (drafted, ready to paste)

| # | File | Type | Trigger / timing | Subject | Preview text |
|---|------|------|------------------|---------|--------------|
| 1 | `1-welcome-prelaunch.html` | Automation | Subscribes via coming-soon page (before launch) | You are early. Welcome to the magic. | Founding supporters get first access to the drop and the September tournament. |
| 2 | `2-welcome-postlaunch.html` | Automation | Subscribes after launch | Welcome to Magicians on the Green | Wear the magic, fund the team, or back the tournament. Here is where to start. |
| 3 | `3-abandoned-checkout-1.html` | Automation | Checkout started, not finished. ~1 hour | You left something in your bag | Your order is still waiting, and it funds the team. Finish in one tap. |
| 4 | `4-abandoned-checkout-2.html` | Automation | Still not finished. ~24 hours | Still want to wear the magic? | Your bag is held a little longer. Every order sends the team further. |
| 5 | `5-postpurchase-merch.html` | Automation | Order placed, product type Headcover/Hat/Apparel/Accessory | Thank you. You just funded the team. | Your gear ships from Memphis soon. Here is what your order does. |
| 6 | `6-postpurchase-donor.html` | Automation | Order placed, product type Donation | You just funded a student-athlete. Thank you. | Your gift goes straight to the program. Here is what it does. |
| 7 | `7-postpurchase-tournament.html` | Automation | Order placed, product type Tournament Entry | You are in. See you on the green. | Your spot at Magic on the Greens is confirmed. Details inside. |
| 8 | `8-postpurchase-sponsor.html` | Automation | Order placed, product type Sponsorship | Thank you for backing the Magicians. | Your sponsorship fuels the program. The coach will be in touch. |

Segmentation note: the post-purchase emails branch on **product type**, which is already set on every product (Headcover, Hat, Apparel, Accessory, Donation, Tournament Entry, Sponsorship). So no manual tagging is needed; condition each automation on product type.

---

## Outlined (not yet drafted): Tournament countdown campaign

Scheduled **campaigns** (not event automations), sent to the players and sponsors segment. Anchored to the Sept 13 deadline and the 15-spot cap.

| Send | Timing | Working subject | Angle |
|------|--------|-----------------|-------|
| 1 | Launch day | The Magic on the Greens spots are open | Announce, 15 foursomes only |
| 2 | ~60 days out | The field is filling up | Scarcity, how many spots left |
| 3 | ~30 days out | Two ways to play, one way to sponsor | Individual entry + sponsor push |
| 4 | ~14 days out | Almost gone: spots for Magic on the Greens | Urgency |
| 5 | ~5 days out | Final call: last spots on the green | Last chance |
| 6 | Day after | Thank you, and save the date | Recap, photos, next year |

Say the word and I will draft these as full HTML too.

## Outlined (later): Win-back

Automation, trigger = no purchase or open in ~120 days. 3 emails: "We miss you on the green" (re-introduce the mission), "Here is what is new" (drops, the tournament), "Last call" (one clear CTA, or quietly clean the list).

---

## How to set these up in Shopify admin

1. **Marketing > Automations.** Shopify has templates for **Welcome new subscriber**, **Abandoned checkout**, and **Thank you after purchase / first purchase**. Start from those.
2. In the automation's email step, use the **email editor**. To use this custom HTML, add a **Custom Liquid** section (or replace the body), and paste the file's HTML.
3. For the **abandoned checkout** emails, insert Shopify's dynamic checkout link where the HTML has `{{ checkout.url }}` (use the editor's "complete your order" / checkout button field so the real recovery link is injected).
4. For **post-purchase**, set the automation **condition to product type** so each customer gets the right one of the four.
5. For the **Tournament countdown** and **launch announcement**, use **Marketing > Campaigns** (scheduled sends), not Automations.

## Shopify Email constraints already handled in these files
- Single column, max 600px, table-based, inline styles, **no media queries** (Shopify strips them).
- `&amp;` used for ampersands; HTML entities used for symbols to avoid mojibake.
- `{{ customer.first_name }}` is used in post-purchase emails. Confirm the exact variable name in your Shopify Email editor and add a fallback if the field can be empty.
- Shopify Email **auto-appends the required unsubscribe link and business address footer** to marketing emails, so it is not duplicated in the HTML.
- Header images load from the public site assets (`rfoster3.github.io/motg-website/assets/...`). You can re-upload them into Shopify's content library and swap the URLs if you prefer Shopify-hosted images.

## Things to finalize before sending live
- `[INSTAGRAM_URL]` in the pre-launch welcome: drop in the real handle, or remove the button.
- `[CONFIRM tax-receipt wording]` in the donor email: depends on the coach's decision about 501(c)(3) / tax receipts.
- Real **sender email** and **payments** must be set (on the coach's list) before any of these can actually send or fire.
