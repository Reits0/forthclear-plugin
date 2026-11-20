"""Offline USD lot-cost arithmetic. Standard library; no network or account access."""
import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


def money(value, name):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError(f'{name} must be a decimal string or integer dollars')
    if not re.fullmatch(r'\d+(?:\.\d{1,2})?', str(value)):
        raise ValueError(f'{name} must be nonnegative USD with at most two decimal places')
    number = Decimal(str(value))
    if number > Decimal('1000000000'):
        raise ValueError(f'{name} exceeds the example calculator limit')
    return number


def units(value, name, allow_zero=False):
    if type(value) is not int or value < (0 if allow_zero else 1) or value > 1000000000:
        raise ValueError(f'{name} must be a whole-number quantity within range')
    return value


def display(value):
    return str(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def calculate(data):
    if not isinstance(data, dict) or data.get('currency') != 'USD':
        raise ValueError('This example requires currency USD; it does not convert currencies')
    quantity = units(data.get('ordered_units'), 'ordered_units')
    price = money(data.get('unit_price'), 'unit_price')
    usable = data.get('usable_units')
    if usable is not None:
        usable = units(usable, 'usable_units', allow_zero=True)
        if usable > quantity:
            raise ValueError('usable_units cannot exceed ordered_units')
    missing = [key for key in ('freight_total', 'other_costs_total') if data.get(key) is None]
    known = {key: money(data[key], key) for key in ('freight_total', 'other_costs_total') if key not in missing}
    result = {'currency': 'USD', 'ordered_units': quantity, 'usable_units_assumption': usable,
              'goods_subtotal': display(price * quantity), 'complete_buying_cost': not missing,
              'missing_cost_inputs': missing, 'total_buying_cost': None,
              'cost_per_ordered_unit': None, 'cost_per_usable_unit': None}
    if missing:
        return result
    total = price * quantity + sum(known.values(), Decimal(0))
    result.update(total_buying_cost=display(total), cost_per_ordered_unit=display(total / quantity))
    if usable:
        result['cost_per_usable_unit'] = display(total / usable)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='JSON file of explicit dollar amounts and quantities')
    args = parser.parse_args()
    try:
        result = calculate(json.loads(args.input.read_text(encoding='utf-8-sig')))
    except (OSError, ValueError, InvalidOperation) as exc:
        print(f'Invalid input: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result['complete_buying_cost'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
