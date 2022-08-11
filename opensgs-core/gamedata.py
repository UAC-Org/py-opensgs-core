def load_cards(fp: str = "cards.txt") -> list[str]:
    cards = []
    with open(fp, encoding="utf-8") as f:
        for line in f:
            cards.append(line.strip())
    return cards


def load_generals(fp: str = "generals.txt") -> dict[str, int]:
    generals = {}
    with open(fp, encoding="utf-8") as f:
        for line in f:
            k, v = line.strip().split(',', 1)
            generals[k] = int(v)
    return generals