def subtotal(lines):
    return sum(line["cents"] * line["qty"] for line in lines)
