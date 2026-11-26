# Install the ForthClear MCP server

ForthClear is a B2B marketplace for surplus, overstock and returned goods. This repository configures a remote MCP server. There is no local server process to build or run.

## Endpoint

Use this URL in any MCP client that supports streamable HTTP:

`https://app.forthclear.io/mcp`

## What works without a key

Catalogue search, listing details, supplier search and price suggestions work without signing in. Quote requests also work without an account if you pass `buyer_email`.

## Sign-in

Account tools (orders, checkout, saved searches, and seller actions) need a connected ForthClear user.

OAuth 2.1 is the usual method for hosted assistants. The server advertises it at `https://app.forthclear.io/.well-known/oauth-protected-resource`. The client should follow that metadata, register itself, and open the browser so the user can approve scopes.

API keys are also supported:

- Buyer key: create one at https://app.forthclear.io/account-settings and send it in the `X-Agent-Token` header.
- Seller key: create one at https://app.forthclear.io/seller/settings and send it in the `X-MCP-API-Key` header.

Do not put a key, password or token in the chat, the README, or this file.

## Cline

Add a remote MCP server named `forthclear` with URL `https://app.forthclear.io/mcp`. You do not need to clone this repository to run the server. If Cline asks how to install from this repo, point it at this file and the README, then use the remote URL above. After the server is connected, use OAuth if the client supports it, or an API key as described above.

## Other clients

The same URL works in VS Code, Cursor, Perplexity, Claude and other MCP clients that accept a hosted streamable HTTP endpoint. Docs: https://app.forthclear.io/developers/mcp

## Check the connection

Ask the agent to search for surplus electronics or another ordinary category. It should return current lots from the live catalogue. If the catalogue has no match, it should say so rather than invent inventory.
