import unittest

from pagination import page_count


class PageCountTest(unittest.TestCase):
    def test_partial_page(self):
        self.assertEqual(page_count(11, 5), 3)


if __name__ == "__main__":
    unittest.main()
