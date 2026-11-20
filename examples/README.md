# Wholesale lot cost: a small offline example

Work out the buying cost per ordered unit and per usable unit using numbers
you supply. This example supports USD and Python 3.10 or newer. It uses the
standard library and makes no network requests.

From the repository root:

```sh
python examples/lot_cost.py examples/illustrative-lot.json
python -m unittest discover -s tests -v
```

The included file is fictional. It contains 200 ordered units at USD 3.00,
USD 120 freight, USD 30 other buying costs, and an assumption of 150 usable
units. The output is USD 750 total, USD 3.75 per ordered unit and USD 5.00 per
usable unit. Usable quantity is an input, not a prediction.

All money inputs here are dollar amounts written as decimal strings, such as
`"3.00"`. The example has its own input format. The MCP catalogue's integer
cents must be converted before using them here; do not paste `price: 300`
into `unit_price` and treat it as USD 3.00.

Include known buying charges in `other_costs_total`. Set freight or other
costs to `null` when they are unknown. The calculator then leaves the buying
total and per-unit costs unset and exits with code 2. Supply `"0.00"` only
when that charge is known to be zero. Invalid inputs exit with code 1.

Omit `usable_units`, or set it to `null`, when no usable-quantity assumption
is available. The ordered-unit calculation still works. A zero usable
quantity has no finite cost per usable unit; its output is `null`.

These calculations cover the supplied buying costs. A resale plan separately
needs realistic proceeds and the applicable testing, storage, packaging,
selling, delivery and return costs. No resale profit is calculated here.

See the [buyer walkthrough](buyer-walkthrough.md) to use the live ForthClear
plugin to find and compare actual lots before contacting a seller.
