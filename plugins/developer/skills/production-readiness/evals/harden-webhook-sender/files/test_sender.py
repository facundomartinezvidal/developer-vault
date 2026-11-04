import json
import unittest
from unittest.mock import patch

import sender


class SendTest(unittest.TestCase):
    @patch("sender.urlopen")
    def test_posts_invoice(self, urlopen):
        sender.send({"id": 1})
        self.assertEqual(json.loads(urlopen.call_args.args[0].data), {"id": 1})


if __name__ == "__main__":
    unittest.main()
