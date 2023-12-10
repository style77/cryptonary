def format_number(amount):
    suffixes = ["", "K", "M", "B", "T"]
    for suffix in suffixes:
        if abs(amount) < 1000:
            break
        amount /= 1000.0
    return f"{amount:.1f}{suffix}"
