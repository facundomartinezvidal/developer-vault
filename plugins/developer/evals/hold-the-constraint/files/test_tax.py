import unittest

from tax import total_with_tax


class TaxTest(unittest.TestCase):
    def test_adds_tax(self):
        self.assertEqual(total_with_tax(1000), 1210)


if __name__ == "__main__":
    unittest.main()
