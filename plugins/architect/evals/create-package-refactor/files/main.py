from billing import quote

def preview(items, coupon, repository):
    return quote(items, coupon, repository)
