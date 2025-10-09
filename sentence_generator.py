from file_parser import *
import random


def generate(symbol: str, grammar: dict, terminals: dict):
    if symbol not in grammar.keys():
        return random.choice(terminals[symbol])
    result = []
    new_symbols = random.choice(grammar[symbol])
    for s in new_symbols:
        result.extend(generate(s, grammar, terminals))
    return result


def generate_sentence(grammar: dict, terminals: dict, first_symbol='ПРЕДЛОЖЕНИЕ'):
    result = generate(first_symbol, grammar, terminals)
    sentence = ' '.join(result)
    return sentence


if __name__ == '__main__':
    grammar = parse_file('grammar.txt')
    terminals = parse_file('terminals.txt')
    print(generate_sentence(grammar, terminals))
