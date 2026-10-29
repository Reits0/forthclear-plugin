# ForthClear

![ForthClear](assets/logo.png)

[ForthClear](https://forthclear.io) is a B2B marketplace for surplus, overstock, and
returned inventory. This plugin connects Cursor and Grok Bot to ForthClear's
hosted MCP server so an agent can search the live catalogue, request bulk
quotes, and — after the user signs in — read orders or run a seller account.

The repository is the plugin. It has no application code and no credentials.
`mcp.json` points at `https://app.forthclear.io/mcp`. Cursor treats `type: http`
as remote streamable HTTP, the same shape as other marketplace plugins. The
server announces OAuth through
`https://app.forthclear.io/.well-known/oauth-protected-resource`. Nothing in
this repo is an API key, client secret, or token.

## Install

To try the plugin before a marketplace listing, clone this repo, load it as a
local Cursor plugin, and reload the window. Open the plugin and connect
**ForthClear**. The host runs OAuth 2.1
(authorization code, S256 PKCE, dynamic client registration) in the browser.
Sign in on `app.forthclear.io` and approve only the scopes you want.

If the plugin is listed in the Cursor Marketplace later, you can install it
there instead.

## What works without an account

Catalogue search, product details, and pricing suggestions need no sign-in.
`request_quote` also works without an account when you pass `buyer_email` (the
address the seller replies to). Anonymous quotes are limited to 5 per hour.
Keep the returned `status_token` and pass it to `get_quote_status`.

## Sign-in

Account tools need a connected ForthClear user. Supported scopes:

| Scope | Allows |
| --- | --- |
| `buyer:read` | Read your orders and quote status |
| `buyer:write` | Request quotes, open disputes, and save searches |
| `buyer:purchase` | Start instant checkout |
| `seller:read` | Read your quote inbox and export your orders |
| `seller:write` | Create and update listings, respond to quotes, and mark orders shipped |

Seller scopes are offered only to seller accounts. A connection lasts 30 days.
Revoke it at <https://app.forthclear.io/oauth/connections>. Do not paste a
password or token into the chat.

## Tools

These are the tools the server advertises. Prices on catalogue, quote, and
listing tools are integer cents. `bulk_update_listings` `price_set` is a USD
dollar amount.

| Tool | Access | What it does |
| --- | --- | --- |
| `search_inventory` | none | Search by keyword, category, condition, or maximum price in cents |
| `search_inventory_semantic` | none | Rank listings against an everyday-language description |
| `get_product_details` | none | Read one listing, including whether instant checkout is available |
| `get_pricing_recommendation` | none | Suggest a wholesale unit price from category, condition, and retail price |
| `request_quote` | none, or `buyer:write` | Ask a seller to price a bulk order |
| `get_quote_status` | status token, or `buyer:read` | Read a quote and the seller's reply |
| `quick_buy` | `buyer:purchase` | Start checkout when the listing allows instant purchase |
| `get_order_status` | `buyer:read` | Status, tracking, and inspection deadline for your order |
| `open_dispute` | `buyer:write` | Report a problem on a delivered order waiting for confirmation |
| `subscribe_to_query` | `buyer:write` | Save a search and receive new matches by email, webhook, or poll |
| `create_listing` | `seller:write` | Publish a surplus lot |
| `get_quote_requests` | `seller:read` | List quote requests buyers sent you |
| `seller_inbox_summarise` | `seller:read` | Pending quotes, ship-by risk, and reported problems |
| `bulk_export_orders` | `seller:read` | Download your orders as CSV |
| `respond_to_quote` | `seller:write` | Accept, counter, or decline a quote |
| `bulk_update_listings` | `seller:write` | Replace price or minimum quantity on up to 200 listings |
| `bulk_mark_shipped` | `seller:write` | Mark up to 200 of your orders shipped |

`bulk_update_listings` and `bulk_mark_shipped` replace existing values. The
server marks them destructive.

The server also exposes two resources, which are not tools:
`forthclear://categories` (catalogue categories) and `forthclear://stats`
(marketplace statistics).

## Try it

- "Find surplus electronics under $200 a unit."
- "Request a quote for 200 units of that listing. My email is …"
- "What is waiting in my ForthClear seller inbox?"

## Privacy

Tool calls go to `https://app.forthclear.io` over HTTPS. The server receives
the tool name and the arguments the agent sends (search text, product ids,
quantities, a quote email, and similar), plus ordinary request metadata. It
does not receive the rest of the chat. Card numbers are not collected here.
Stripe processes payment.

- Privacy policy: <https://forthclear.io/privacy> (same document as <https://forthclear.io/privacy-policy>)
- Terms of service: <https://forthclear.io/terms>
- Support: info@forthclear.io

The live MCP metadata advertises <https://forthclear.io/privacy> and
<https://forthclear.io/terms>. <https://forthclear.io/privacy-policy> is the
same privacy policy.

## License

MIT. See [LICENSE](LICENSE).
