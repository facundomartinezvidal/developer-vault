import unittest

from cart import Cart


class CartTest(unittest.TestCase):
    def test_add_one(self):
        cart = Cart()
        cart.add("pen", 3)
        self.assertEqual(cart.total(), 3)

    def test_empty_total(self):
        self.assertEqual(Cart().total(), 0)


if __name__ == "__main__":
    unittest.main()
