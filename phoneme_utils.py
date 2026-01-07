# phoneme_utils.py

import nltk
from nltk.corpus import cmudict

# загружаем cmu словарь
CMU_DICT = cmudict.dict()

def count_syllables(word):
    """
    Возвращает количество слогов у слова по CMU dict.
    Если слово не найдено — грубо оценивает как 1 слог.
    """
    w = word.lower()
    if w in CMU_DICT:
        # может быть несколько вариантов произношения — берем первый
        return [len([y for y in x if y[-1].isdigit()]) for x in CMU_DICT[w]][0]
    return 1

def get_rhyme_part(word):
    """
    Возвращает рифмовую часть слова: от последнего гласного с ударением до конца.
    """
    w = word.lower()
    if w not in CMU_DICT:
        return word[-2:]  # fallback — 2 последние буквы

    pronunciations = CMU_DICT[w][0]
    # ищем позицию последнего ударного гласного
    rhyme_idx = 0
    for i, ph in enumerate(pronunciations):
        # ударение в CMU — 1 или 2 цифра в фонеме
        if any(d in ph for d in "12"):
            rhyme_idx = i

    rhyme_part = tuple(pronunciations[rhyme_idx:])
    return rhyme_part

def rhyme_matches(w1, w2):
    """
    True, если слова рифмуются (одинаковая рифмовая часть).
    """
    return get_rhyme_part(w1) == get_rhyme_part(w2)
