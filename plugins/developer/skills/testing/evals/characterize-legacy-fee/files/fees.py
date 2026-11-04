def late_fee(days, balance, premium=False):
    if premium:
        return balance * 0.01 * days
    fee = balance * 0.02 * days
    if fee > 500:
        fee = 500
    return fee
