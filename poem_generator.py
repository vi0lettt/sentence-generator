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

            # проверка рифмы и чтобы слово не совпадало с rhyme_word
            if rhyme_word is not None:
                if w.lower() == rhyme_word.lower():
                    continue
                if not rhyme_matches(w, rhyme_word):
                    continue

            valid.append(w)

        # фоллбэк: если нет валидных слов — берём любые варианты
        if not valid:
            valid = [normalize_word(w) for w in options if normalize_word(w) is not None]

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
        line = generate_line(symbol, grammar, terminals, max_syllables, rhyme_word=rhyme_word)
        if not line:
            continue

        if rhyme_word is not None:
            last_word = line[-1]
            if last_word.lower() == rhyme_word.lower():
                continue
            if not rhyme_matches(last_word, rhyme_word):
                continue

        return line
    return []

def generate_limerick_once(grammar, terminals, max_attempts_per_line=100):
    """Генерируем один лимерик с ограничением на количество попыток для каждой строки"""
    
    # --- Линия 1 ---
    line1 = []
    attempts = 0
    while not line1 and attempts < max_attempts_per_line:
        line1 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 120)
        attempts += 1
    rhyme_A = line1[-1] if line1 else None

    # --- Линия 2 (рифмуется с A) ---
    line2 = []
    attempts = 0
    while not line2 and attempts < max_attempts_per_line and rhyme_A:
        line2 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 120, rhyme_word=rhyme_A)
        attempts += 1

    # --- Линия 3 ---
    line3 = []
    attempts = 0
    while not line3 and attempts < max_attempts_per_line:
        line3 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 120)
        attempts += 1
    rhyme_B = line3[-1] if line3 else None

    # --- Линия 4 (рифмуется с B) ---
    line4 = []
    attempts = 0
    while not line4 and attempts < max_attempts_per_line and rhyme_B:
        line4 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 120, rhyme_word=rhyme_B)
        attempts += 1

    # --- Линия 5 (рифмуется с A) ---
    line5 = []
    attempts = 0
    while not line5 and attempts < max_attempts_per_line and rhyme_A:
        line5 = safe_generate_line("ПРЕДЛОЖЕНИЕ", grammar, terminals, 120, rhyme_word=rhyme_A)
        attempts += 1

    # Собираем результат, убирая пустые строки
    lines = []
    for line in [line1, line2, line3, line4, line5]:
        if line:
            lines.append(" ".join(line).capitalize())

    return lines if lines else None

def generate_limerick(grammar, terminals, max_attempts=900):
    """Генерируем готовый лимерик"""
    for _ in range(max_attempts):
        poem = generate_limerick_once(grammar, terminals)
        if poem is not None and len(poem) == 5:
            return "\n".join(poem)
    return "Failed to generate a valid limerick"
