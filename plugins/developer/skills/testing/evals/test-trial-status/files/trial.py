from datetime import date


def trial_status(user):
    days = (date.today() - user["signed_up"]).days
    if days > 14:
        return "expired"
    if days >= 12:
        return "ending_soon"
    return "active"
