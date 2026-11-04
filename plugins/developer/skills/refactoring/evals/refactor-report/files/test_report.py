import unittest

from report import render


class RenderTest(unittest.TestCase):
    ROWS = [("a", 1.5), ("b", 1.2)]

    def test_text(self):
        self.assertEqual(render("text", "sales", self.ROWS), "SALES\na: 1.50\nb: 1.20\nTOTAL: 3")

    def test_csv(self):
        self.assertEqual(render("csv", "sales", self.ROWS), "title,sales\na,1.50\nb,1.20\ntotal,2")

    def test_unknown(self):
        with self.assertRaises(ValueError):
            render("xml", "sales", self.ROWS)


if __name__ == "__main__":
    unittest.main()
