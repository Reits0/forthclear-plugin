---
name: forthclear
description: Use when the user wants surplus, overstock, returned, or wholesale inventory from ForthClear, a bulk quote, an order update, or help listing and shipping as a ForthClear seller. Covers the live MCP tools on app.forthclear.io.
---

# ForthClear

ForthClear is a B2B marketplace for surplus, overstock, and returned inventory.
Use the ForthClear MCP server for live catalogue and account data. Do not invent
stock, prices, sellers, order status, or quote replies.

The server is `https://app.forthclear.io/mcp`. Public tools need no account.
Account tools use OAuth 2.1 (authorization code, S256 PKCE, dynamic client
registration). The host opens sign-in. Never ask the user to paste a password,
API key, access token, or refresh token into the chat.

Scopes, from the server:

- `buyer:read` — read the signed-in buyer's orders and quote status
- `buyer:write` — request quotes, open disputes, and save searches
- `buyer:purchase` — start instant checkout
- `seller:read` — read that seller's quote inbox and export their orders
- `seller:write` — create and update listings, respond to quotes, and mark orders shipped

Seller scopes are only offered to seller accounts. A scope error means the
connection is missing that permission; ask the host to reconnect with the scope
the failed tool requires. Revoke connections at
https://app.forthclear.io/oauth/connections. Grants last 30 days.

On an authentication error, let the host open account linking and retry the
same operation. If a write times out, read it back with the matching status
tool before submitting it again. These tools do not take an idempotency key.

## Prices and ids

Search, product details, quote `target_price`, listing `price_per_unit`, and
pricing recommendations use integer cents. `bulk_update_listings` is different:
`price_set` takes a USD dollar amount, the percent modes take a percent, and
`moq_set` takes an integer minimum quantity. Say which unit you are using.

Catalogue tools identify listings as `product_<n>`. `bulk_update_listings`
takes integer product ids. Quote ids and order ids are integers.

## Catalogue (no sign-in)

- `search_inventory` — keyword search. Optional category, condition, maximum
  price in cents, and limit (default 20, max 100). Categories: `electronics`,
  `apparel`, `home_goods`, `beauty`, `sports`, `kitchenware`,
  `office_supplies`, `toys`, `food_beverage`, `tools`, `other`. Conditions:
  `salvage`, `customer_returns`, `shelf_pulls`, `overstock`,
  `new_or_refurbished`.
- `search_inventory_semantic` — everyday-language search. Requires `query`.
  Results include a similarity score from 0 to 1. A weak match can still be
  returned; if meaning search finds nothing, the same words are searched as
  keywords. Limit default 10, max 50.
- `get_product_details` — one listing: description, price, quantity, condition,
  photo, seller company when available, `instant_checkout`,
  `quote_quantity_threshold`, and whether a quote is required. Call this before
  a quote or a purchase. Use an id returned by search.
- `get_pricing_recommendation` — a suggested wholesale unit price from category,
  condition, original retail price in cents, and optional lot size. It is
  guidance, not a seller offer.

Empty results mean the live catalogue had no match. Broaden filters only by
saying so. Do not claim stock exists that the tools did not return.

Two resources are also public, and they are not tools: `forthclear://categories`
and `forthclear://stats`.

## Quotes

`request_quote` sends a real quote request to the seller. Required: `product_id`, `quantity`, and
`buyer_email` (where the seller replies). Optional: name, company, target price
in cents, and a message. Submit only after the user agrees to send those
details.

No sign-in is required. Anonymous requests are limited to 5 per hour. Keep the
returned `status_token` private and pass it to `get_quote_status` with
`quote_id`. A signed-in buyer with `buyer:write` can attach the quote to their
account; `buyer:read` can then read their own quotes without the token. If the
email already belongs to an account, the server refuses to bind the quote until
that account is connected. Some listings require a verified reseller or a
minimum quantity; report that refusal instead of retrying with a different
email. A quote is not an order and does not reserve stock. The server's own
reply window is 24–48 hours.

## Buyer account

These need the signed-in buyer. `buyer:read` does not include purchase.

- `get_order_status` — status, tracking, and inspection deadline for an order
  this buyer placed. `buyer:read`.
- `open_dispute` — report a problem on a delivered order that is waiting for
  confirmation. Records the issue, marks the order, and notifies ForthClear.
  Reasons: `missing_units`, `quality_issue`, `damaged`, `wrong_item`, `other`.
  Optional resolution: `refund`, `replacement`, `partial_refund`. Get the
  user's reason and explicit go-ahead before calling. `buyer:write`.
- `subscribe_to_query` — save a catalogue search and deliver new matches by
  email, a public https webhook, or a pollable `mcp_resource` feed (1–5
  channels). Use only an address the user supplied. `buyer:write`.
- `quick_buy` — start checkout for a listing whose product details say instant
  checkout is available, and only for a quantity under that listing's bulk
  threshold. Larger quantities, and listings sold only by quote, must use
  `request_quote`. Requires `buyer:purchase`, plus `product_id`, `quantity`,
  and `buyer_email`. Confirm the product, quantity, and the totals the server
  returns before treating checkout as started. Stripe handles payment through
  ForthClear. Do not collect card numbers or bank details in the chat, and do
  not say the purchase succeeded until the server says so. If the seller has
  not connected Stripe, the tool returns a contact path instead of a payment
  step.

## Seller account

These need a connected seller. Read scopes do not grant write.

- `seller_inbox_summarise` — quotes waiting for a reply, orders that may miss
  their ship-by date, and orders with reported problems. `seller:read`.
  `window_hours` defaults to 24 (max 168). An empty inbox is what the server
  returned, not proof there are no orders.
- `get_quote_requests` — quote requests sent to this seller. Filter `pending`
  (default), `responded`, or `all`. `seller:read`.
- `bulk_export_orders` — CSV of this seller's orders only (order id, product,
  buyer, quantity, total, status, date). Pass integer order ids, max 200.
  Treat the CSV as private. `seller:read`.
- `create_listing` — publish a lot. Required: name, category, condition,
  quantity, and `price_per_unit` in cents. Optional: description, original
  retail price in cents, and SKU. Do not invent condition, provenance,
  quantity, or price. Show the seller the exact listing and publish only after
  they confirm. `seller:write`.
- `respond_to_quote` — `accept`, `counter` (requires `counter_price` in cents),
  or `decline`. The buyer is notified. Confirm the quote id, action, and any
  counter price before sending. `seller:write`.
- `bulk_update_listings` — replace price or minimum order quantity on up to
  200 listings. Modes: `price_set` (USD dollars), `price_percent_increase`,
  `price_percent_decrease`, `moq_set`. Previous values are replaced
  (`destructiveHint`). Show the ids and the new values and wait for
  authorization. A request to "optimize prices" is not permission to change
  every listing. `seller:write`.
- `bulk_mark_shipped` — mark up to 200 of this seller's orders shipped.
  Optional tracking number, tracking link, and carrier apply to the whole
  batch and replace tracking already stored. Buyers are notified. Do not mark
  an order shipped without a real shipment. `seller:write`.

If a bulk call returns a partial result, report the items that succeeded and
the items that failed. Retry only the failed ids after the error is resolved.
