def page_count(total, per_page):
    return total // per_page + 1


def format_price(cents):
    return "$" + str(cents / 100)
