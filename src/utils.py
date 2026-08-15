def format_inr(number) -> str:
    """
    Formats transaction amounts according to the Indian Numbering System (INR):
    e.g. 500000 -> INR 5,00,000 (5 Lakhs)
    e.g. 1500000 -> INR 15,00,000 (15 Lakhs)
    e.g. 150000 -> INR 1,50,000 (1 Lakh 50 Thousand)
    e.g. 10000000 -> INR 1,00,00,000 (1 Crore)
    """
    if number is None:
        return "N/A"
    try:
        val = int(round(float(number)))
        s = str(val)
        if len(s) <= 3:
            return f"INR {s}"
        last_three = s[-3:]
        other = s[:-3]
        groups = []
        while len(other) > 2:
            groups.append(other[-2:])
            other = other[:-2]
        if other:
            groups.append(other)
        groups.reverse()
        formatted_other = ",".join(groups)
        return f"INR {formatted_other},{last_three}"
    except Exception:
        return f"INR {number}"
