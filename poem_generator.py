# poem_generator.py

import random
import pronouncing

def normalize_word(w):
    """Приводим терминал к строке, берём последнее слово для рифмы"""
    if isinstance(w, (list, tuple)):
        if len(w) == 0:
            return None
        return normalize_word(w[0])
    if w is None:
        return None
    w = str(w).strip()
    parts = w.split()
    return parts[-1] if len(parts) > 1 else w

def rhyme_matches(word1, word2):
    """Проверяем, рифмуются ли два слова с помощью pronouncing"""
    word1 = word1.lower()
    word2 = word2.lower()
    rhymes = pronouncing.rhymes(word2)
    if word1 in rhymes:
        return True
    # fallback: совпадение последних 2-3 букв
    return word1[-2:] == word2[-2:] or word1[-3:] == word2[-3:]

def count_syllables(word):
    """Считаем слоги через pronouncing, fallback на 1 слог если не найдено"""
    word = word.lower()
    phones = pronouncing.phones_for_word(word)
    if not phones:
        return max(1, len(word) // 3)  # грубая оценка слогов
    return pronouncing.syllable_count(phones[0])

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

            sylls = count_syllables(w)
            if current_syllables + sylls > max_syllables:
                continue

            if rhyme_word is not None and not rhyme_matches(w, rhyme_word):
                continue

            valid.append(w)

        if not valid:
            return []

        return [random.choice(valid)]

    # --- нетерминал ---
    for _ in range(15):  # попытки генерации
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

def safe_generate_line(symbol, grammar, terminals, max_syllables, rhyme_word=None, tries=50):
    for _ in range(tries):
        line = generate_line(symbol, grammar, terminals, max_syllables)
        if not line:
            continue

        if rhyme_word is not None:
            last_word = line[-1]
            if not rhyme_matches(last_word, rhyme_word):
                continue

        return line
    return []


def generate_limerick_once(grammar, terminals):
    """Генерируем один лимерик"""
    line1 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 7)
    if not line1:
        return None
    rhyme_A = line1[-1]

    line2 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 7, rhyme_word=rhyme_A)
    line3 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 6)
    if not line3:
        return None
    rhyme_B = line3[-1]

    line4 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 6, rhyme_word=rhyme_B)
    line5 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 7, rhyme_word=rhyme_A)

    if None in [line1, line2, line3, line4, line5]:
        return None

    return [
        " ".join(line1).capitalize(),
        " ".join(line2).capitalize(),
        " ".join(line3).capitalize(),
        " ".join(line4).capitalize(),
        " ".join(line5).capitalize(),
    ]

def generate_limerick(grammar, terminals, max_attempts=200):
    """Генерируем готовый лимерик"""
    for _ in range(max_attempts):
        poem = generate_limerick_once(grammar, terminals)
        if poem is not None:
            return "\n".join(poem)
    return "Failed to generate a valid limerick"
