def header(fmt, title):
    if fmt == "text":
        return title.upper()
    elif fmt == "csv":
        return "title," + title
    raise ValueError(fmt)


def line(fmt, name, amount):
    if fmt == "text":
        return f"{name}: {amount:.2f}"
    elif fmt == "csv":
        return f"{name},{amount:.2f}"
    raise ValueError(fmt)


def total(fmt, amounts):
    if fmt == "text":
        return f"TOTAL: {round(sum(amounts))}"
    elif fmt == "csv":
        return f"total,{int(sum(amounts))}"
    raise ValueError(fmt)


def render(fmt, title, rows):
    out = [header(fmt, title)]
    for name, amount in rows:
        out.append(line(fmt, name, amount))
    out.append(total(fmt, [amount for _, amount in rows]))
    return "\n".join(out)
