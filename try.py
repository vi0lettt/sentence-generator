import random
from file_parser import parse_file

# -----------------------------
# Словарь терминалов с слогами и рифмой
# -----------------------------
phonemes = {
    "cat":    {"syllables": 1, "rhyme": "at"},
    "hat":    {"syllables": 1, "rhyme": "at"},
    "mat":    {"syllables": 1, "rhyme": "at"},
    "dog":    {"syllables": 1, "rhyme": "og"},
    "frog":   {"syllables": 1, "rhyme": "og"},
    "log":    {"syllables": 1, "rhyme": "og"},
    "happy":  {"syllables": 2, "rhyme": "appy"},
    "snappy": {"syllables": 2, "rhyme": "appy"},
    "chased": {"syllables": 1, "rhyme": "ased"},
    "fast":   {"syllables": 1, "rhyme": "ast"},
    "past":   {"syllables": 1, "rhyme": "ast"},
    "day":    {"syllables": 1, "rhyme": "ay"},
    "play":   {"syllables": 1, "rhyme": "ay"},
    "away":   {"syllables": 2, "rhyme": "ay"},
}

# -----------------------------
# Генерация строки с контролем слогов и рифмы
# -----------------------------
def generate_line(symbol, grammar, terminals, max_syllables, rhyme=None, current_syllables=0):
    """
    symbol       : текущий нетерминал
    grammar      : словарь грамматики
    terminals    : словарь терминалов
    max_syllables: максимальное количество слогов в строке
    rhyme        : если указана, последний терминал должен рифмоваться
    current_syllables: текущий счетчик слогов
    """
    if current_syllables >= max_syllables:
        return []

    # Если символ — терминал
    if symbol not in grammar:
        options = terminals.get(symbol, [symbol])
        # фильтруем по рифме, если указана
        valid_options = [w for w in options if phonemes[w]["syllables"] + current_syllables <= max_syllables]
        if rhyme:
            valid_options = [w for w in valid_options if phonemes[w]["rhyme"] == rhyme]
        if not valid_options:
            return []
        choice = random.choice(valid_options)
        return [choice]

    # Рекурсивно выбираем ветвь грамматики
    variant = random.choice(grammar[symbol])[0]
    result = []
    for s in variant:
        res = generate_line(
            s,
            grammar,
            terminals,
            max_syllables,
            rhyme=rhyme,
            current_syllables=current_syllables + sum(phonemes.get(w, {"syllables":1})["syllables"] for w in result)
        )
        result.extend(res)
    return result

# -----------------------------
# Генерация лимерика
# -----------------------------
def generate_limerick(grammar, terminals):
    # строки A (1,2,5) рифмуются
    line1 = generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 9)
    rhyme_A = phonemes[line1[-1]]["rhyme"]
    line2 = generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 9)
    
    # строки B (3,4) рифмуются
    line3 = generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 6)
    rhyme_B = phonemes[line3[-1]]["rhyme"]
    line4 = generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 6)
    
    # строка 5 рифмуется с первой
    line5 = generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 9, rhyme=rhyme_A)
    
    limerick = [
        " ".join(line1),
        " ".join(line2),
        " ".join(line3),
        " ".join(line4),
        " ".join(line5),
    ]
    return "\n".join(limerick)

# -----------------------------
# Пример запуска
# -----------------------------
if __name__ == "__main__":
    grammar = parse_file("grammar.txt")    # ваша грамматика
    terminals = parse_file("terminals.txt")# ваши терминалы
    poem = generate_limerick(grammar, terminals)
    print(poem)
