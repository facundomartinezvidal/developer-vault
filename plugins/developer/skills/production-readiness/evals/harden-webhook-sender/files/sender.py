import json
from urllib.request import Request, urlopen

URL = "https://billing.internal/notify"


def send(invoice):
    try:
        body = json.dumps(invoice).encode()
        urlopen(Request(URL, data=body, headers={"Content-Type": "application/json"}))
    except Exception:
        pass
