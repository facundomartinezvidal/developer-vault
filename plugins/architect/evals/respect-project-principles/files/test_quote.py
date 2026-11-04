import unittest
from billing import quote

class Repository:
    def discount_pct(self, code):
        if code == "FAIL":
            raise RuntimeError("coupon lookup failed")
        return 15

class QuoteContract(unittest.TestCase):
    def test_rounding_and_public_shape(self):
        self.assertEqual(quote([{"unit_price_minor": 101, "quantity": 3}], "PROMO", Repository()), {"subtotal_minor": 303, "discount_minor": 45, "total_minor": 258})
    def test_without_coupon_does_not_read_repository(self):
        self.assertEqual(quote([{"unit_price_minor": 99, "quantity": 1}], None, None)["total_minor"], 99)
    def test_empty_input(self):
        self.assertEqual(quote([], None, None)["total_minor"], 0)
    def test_repository_failure_is_not_a_price(self):
        with self.assertRaises(RuntimeError):
            quote([{"unit_price_minor": 100, "quantity": 1}], "FAIL", Repository())

if __name__ == "__main__":
    unittest.main()
