import unittest

from invoice import subtotal


class SubtotalTest(unittest.TestCase):
    def test_sums_lines(self):
        self.assertEqual(subtotal([{"cents": 150, "qty": 2}]), 300)


if __name__ == "__main__":
    unittest.main()
