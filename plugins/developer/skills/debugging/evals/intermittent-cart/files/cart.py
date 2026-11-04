class Cart:
    def __init__(self, items=[]):
        self.items = items

    def add(self, name, price):
        self.items.append((name, price))

    def total(self):
        return sum(price for _, price in self.items)
