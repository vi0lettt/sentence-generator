
def parse_grammar_file(filename: str):
    grammar = {}

    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        if "->" not in line:
            continue

        left, right = line.split("->", 1)
        left = left.strip()

        variants = [alt.strip().split() for alt in right.split("|")]

        grammar[left] = variants

    return grammar


if __name__ == "__main__":
    filename = "grammar.txt"  
    grammar = parse_grammar_file(filename)

    for nonterm, rules in grammar.items():
        print(f"{nonterm}:")
        for r in rules:
            print("   ", r)