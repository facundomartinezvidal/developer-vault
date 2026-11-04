def shipping_cost(order):
    if order["express"]:
        return 15 + order["weight"] * 2
    return 5 + order["weight"]
