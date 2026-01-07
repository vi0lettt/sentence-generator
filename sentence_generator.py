from file_parser import parse_file
import random

def choose_variant(variants, probabilistic=False):
    """Выбираем вариант продукции грамматики"""
    if probabilistic:
        symbols, probs = zip(*[(v, p if p is not None else 0) for v, p in variants])
        total = sum(probs)
        if total == 0:
            return random.choice(symbols)
        probs = [p / total for p in probs]
        return random.choices(symbols, weights=probs, k=1)[0]
    else:
        return random.choice([v for v, _ in variants])

def flatten_words(words):
    """Рекурсивно расплющиваем списки и кортежи в список строк"""
    flat = []
    for w in words:
        if isinstance(w, tuple):
            # кортеж (symbols, prob)
            w = w[0]
        if isinstance(w, list):
            flat.extend(flatten_words(w))
        else:
            flat.append(str(w))
    return flat

def generate(symbol, grammar, terminals, probabilistic=False):
    """Генерируем список слов для символа"""
    if symbol not in grammar:
        t_options = terminals.get(symbol, [symbol])
        choice = random.choice(t_options)
        # если терминал — список слов, возвращаем как есть
        return choice if isinstance(choice, list) else [choice]

    variant = choose_variant(grammar[symbol], probabilistic)
    # иногда choose_variant возвращает кортеж (symbols, prob)
    if isinstance(variant, tuple):
        variant = variant[0]

    result = []
    for s in variant:
        result.extend(generate(s, grammar, terminals, probabilistic))
    return result

def generate_sentence(grammar, terminals, first_symbol='ПРЕДЛОЖЕНИЕ', probabilistic=False):
    words = generate(first_symbol, grammar, terminals, probabilistic)
    words = flatten_words(words)  # расплющиваем все вложенные списки/кортежи
    sentence = ' '.join(words)
    sentence = ' '.join(sentence.split())  # удаляем лишние пробелы
    return sentence[0].upper() + sentence[1:] + '.'

if __name__ == '__main__':
    probabilistic = True
    grammar = parse_file('grammar.txt', probabilistic=probabilistic)
    terminals = parse_file('terminals.txt')

    for i in range(20):
        sentence = generate_sentence(grammar, terminals, probabilistic=probabilistic)
        print(f"{i+1}: {sentence}")
