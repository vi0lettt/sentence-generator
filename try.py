import random

def choose_terminal(options):
    return random.choice(options.split('|')).strip()

# Простейшие наборы слов из твоей грамматики
subjects = ["I", "He", "She", "We", "They", "Robert", "Alice"]
verbs = ["walks", "runs", "eats", "plays", "sings", "jumps", "drinks"]
objects = ["cake", "bread", "juice", "fish", "pasta", "smoothie"]
places = ["in the park", "on the street", "by the river", "at the cafe"]
adverbs = ["quickly", "slowly", "happily", "gracefully"]

def line(subjects, verbs, objects, places, adverbs):
    subj = random.choice(subjects)
    verb = random.choice(verbs)
    obj = random.choice(objects)
    place = random.choice(places)
    adv = random.choice(adverbs)
    return f"{subj} {verb} {obj} {place} {adv}"

def generate_limerick():
    # строки A
    line1 = line(subjects, verbs, objects, places, adverbs)
    line2 = line(subjects, verbs, objects, places, adverbs)
    # строки B
    line3 = line(subjects, verbs, objects, places, adverbs)
    line4 = line(subjects, verbs, objects, places, adverbs)
    # строка A
    line5 = line(subjects, verbs, objects, places, adverbs)
    return f"{line1}\n{line2}\n{line3}\n{line4}\n{line5}"

print(generate_limerick())
