# file_parser.py
def parse_file(filename: str, probabilistic=False):
    """
    Парсер файла грамматики или терминалов.
    Если probabilistic=True, парсит вероятности после [0.2]
    """
    result = {}

    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        if "->" not in line:
            continue

        left, right = line.split("->", 1)
        left = left.strip()
        variants = []

        for alt in right.split("|"):
            alt = alt.strip()
            if probabilistic:
                # ищем вероятность в конце [0.2]
                if "[" in alt and "]" in alt:
                    prob_str = alt[alt.rfind("[")+1 : alt.rfind("]")]
                    prob = float(prob_str)
                    symbols = alt[:alt.rfind("[")].strip().split()
                else:
                    prob = None
                    symbols = alt.split()
                variants.append((symbols, prob))
            else:
                symbols = alt.split()
                if "[" in alt and "]" in alt:
                    symbols = symbols[:-1]
                variants.append((symbols, None))

        result[left] = variants

    return result
