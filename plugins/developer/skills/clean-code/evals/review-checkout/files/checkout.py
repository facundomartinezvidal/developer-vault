from gateway import charge, save_order


def process(d, flag):
    try:
        total = 0
        for x in d["items"]:
            total += x["price"] * x["qty"]
        if flag:
            total = total * 0.9
        receipt = charge(d["card_token"], total)
        save_order(d["id"], total, receipt)
        return True
    except:
        return False


def item_count(order):
    return sum(item["qty"] for item in order["items"])
