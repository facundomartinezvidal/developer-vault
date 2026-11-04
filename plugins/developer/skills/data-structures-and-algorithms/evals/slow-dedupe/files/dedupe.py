def dedupe(emails):
    seen = []
    result = []
    for email in emails:
        key = email.lower()
        if key not in seen:
            seen.append(key)
            result.append(email)
    return result
