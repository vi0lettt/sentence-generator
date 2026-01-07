from file_parser import parse_file
from poem_generator import generate_limerick

grammar = parse_file("grammar.txt")
terminals = parse_file("terminals.txt")

print(generate_limerick(grammar, terminals))
