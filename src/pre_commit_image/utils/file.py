def get_extension(path: str) -> str:
    return str(path).split(".")[-1]


def get_readable_byte_size(value: int) -> str:
    units = [
        {"str": "B", "from": 0, "to": 1024},
        {"str": "KiB", "from": 1024, "to": 1024**2},
        {"str": "MiB", "from": 1024**2, "to": 1024**3},
        {"str": "GiB", "from": 1024**3, "to": 1024**4},
        {"str": "TiB", "from": 1024**4, "to": 1024**5},
    ]
    unit = next((u for u in units if u["from"] <= value < u["to"]), units[-1])
    return f"{value / (unit['from'] or 1):,.1f} {unit['str']}".replace(".0", "")
