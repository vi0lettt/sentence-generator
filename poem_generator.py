# poem_generator.py

import random
from phoneme_utils import count_syllables, rhyme_matches

def normalize_word(w):
    """Приводим терминал к строке"""
    if isinstance(w, (list, tuple)):
        return normalize_word(w[0])
    if w is None:
        return None
    w = str(w).strip()
    # Разбиваем составное слово на слова
    parts = w.split()
    if len(parts) > 1:
        return parts[-1]  # для рифмы берём последнее слово
    return w


def generate_line(symbol, grammar, terminals, max_syllables, rhyme_word=None, current_syllables=0):
    if current_syllables > max_syllables:
        return []

    # --- терминал ---
    if symbol not in grammar:
        options = terminals.get(symbol, [symbol])
        valid = []

        for w in options:
            w = normalize_word(w)
            if w is None:
                continue

            w_lower = w.lower()  # приводим слово к нижнему регистру
            sylls = count_syllables(w_lower)

            if current_syllables + sylls > max_syllables:
                continue

            if rhyme_word is not None:
                rhyme_word_lower = rhyme_word.lower()
                print(w_lower)
                # сначала проверяем фонемы через rhyme_matches
                if not rhyme_matches(w_lower, rhyme_word_lower):
                    # fallback: проверяем совпадение последних 2-3 букв
                    if w_lower[-3:] != rhyme_word_lower[-3:]:
                        if w_lower[-2:] != rhyme_word_lower[-2:]:
                            print(1)
                            continue


            valid.append(w)

        if not valid:
            return []

        return [random.choice(valid)]


    # --- нетерминал ---
    for _ in range(10):  # попытки генерации
        variant = random.choice(grammar[symbol])[0]
        result = []
        sylls = current_syllables
        failed = False

        for s in variant:
            part = generate_line(
                s,
                grammar,
                terminals,
                max_syllables,
                rhyme_word=rhyme_word,
                current_syllables=sylls
            )
            if not part:
                failed = True
                break

            sylls += sum(count_syllables(w) for w in part)
            result.extend(part)

        if not failed and sylls <= max_syllables:
            return result

    return []

def generate_limerick(grammar, terminals):
    line1 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 9)
    if not line1:
        return "Generation failed"

    rhyme_A = line1[-1]

    line2 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 9)
    line3 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 6)
    rhyme_B = line3[-1] if line3 else None
    print(rhyme_B)
    line4 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 6, rhyme_word=rhyme_B)
    line5 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 9, rhyme_word=rhyme_A)
    print(line1, line2, line3, line4, line5)
    return "\n".join(
        " ".join(l).capitalize()
        for l in [line1, line2, line3, line4, line5]
        if l
    )

def safe_generate_line(symbol, grammar, terminals, max_syllables, rhyme_word=None, tries=30):
    for _ in range(tries):
        line = generate_line(
            symbol,
            grammar,
            terminals,
            max_syllables,
            rhyme_word=rhyme_word
        )
        if line:
            return line
    return []

