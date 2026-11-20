import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lot_cost', ROOT/'examples/lot_cost.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SAMPLE = json.loads((ROOT/'examples/illustrative-lot.json').read_text())


class LotCostTests(unittest.TestCase):
    def test_worked_example_matches_content(self):
        result = module.calculate(SAMPLE)
        self.assertEqual(result['total_buying_cost'], '750.00')
        self.assertEqual(result['cost_per_ordered_unit'], '3.75')
        self.assertEqual(result['cost_per_usable_unit'], '5.00')

    def test_unknown_shipping_never_becomes_free(self):
        result = module.calculate({**SAMPLE, 'freight_total': None})
        self.assertFalse(result['complete_buying_cost'])
        self.assertEqual(result['missing_cost_inputs'], ['freight_total'])
        self.assertIsNone(result['total_buying_cost'])
        self.assertIsNone(result['cost_per_usable_unit'])

    def test_explicit_zero_shipping_is_valid(self):
        self.assertEqual(module.calculate({**SAMPLE, 'freight_total': '0.00'})['total_buying_cost'], '630.00')

    def test_unknown_and_zero_usable_quantities_remain_unpriced(self):
        for value in (None, 0):
            self.assertIsNone(module.calculate({**SAMPLE, 'usable_units': value})['cost_per_usable_unit'])

    def test_invalid_quantities_are_rejected(self):
        for field, value in [('ordered_units', 0), ('ordered_units', True), ('usable_units', 201), ('usable_units', -1), ('usable_units', 1.5)]:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                module.calculate({**SAMPLE, field: value})

    def test_money_requires_finite_nonnegative_explicit_decimal_inputs(self):
        for value in ('NaN', 'Infinity', '-1', '3.001', 3.0, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                module.calculate({**SAMPLE, 'unit_price': value})

    def test_currency_is_not_silently_converted(self):
        with self.assertRaises(ValueError):
            module.calculate({**SAMPLE, 'currency': 'EUR'})

    def test_decimal_rounding_is_consistent(self):
        result = module.calculate({**SAMPLE, 'ordered_units': 3, 'usable_units': 3, 'unit_price':'0.10', 'freight_total':'0.01', 'other_costs_total':'0.00'})
        self.assertEqual(result['total_buying_cost'], '0.31')
        self.assertEqual(result['cost_per_ordered_unit'], '0.10')

    def test_cli_signals_incomplete_quote(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'lot.json'
            path.write_text(json.dumps({**SAMPLE, 'other_costs_total': None}))
            result = subprocess.run([sys.executable, str(ROOT/'examples/lot_cost.py'), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIsNone(json.loads(result.stdout)['total_buying_cost'])


if __name__ == '__main__':
    unittest.main()
