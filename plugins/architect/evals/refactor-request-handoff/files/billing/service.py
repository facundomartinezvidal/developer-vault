def quote(items, coupon_code, repository):
    discount_pct = repository.discount_pct(coupon_code) if coupon_code else 0
    subtotal_minor = sum(item["unit_price_minor"] * item["quantity"] for item in items)
    discount_minor = subtotal_minor * discount_pct // 100
    return {"subtotal_minor": subtotal_minor, "discount_minor": discount_minor, "total_minor": subtotal_minor - discount_minor}
