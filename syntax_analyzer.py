import sys
from file_parser import parse_file
from graphviz import Digraph


class Node:
    def __init__(self, symbol, children=None, value=None):
        self.symbol = symbol
        self.children = children if children else []
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.symbol}: '{self.value}'"
        return self.symbol

    def to_graphviz(self, graph=None, parent_id=None, node_id=0):
        if graph is None:
            graph = Digraph(comment='Parse Tree', format='png')
            graph.attr('node', shape='box',
                       style='rounded,filled', color='lightblue2')
        label = f"{self.symbol}\n'{self.value}'" if self.value else self.symbol
        current_id = str(node_id)
        graph.node(current_id, label=label)
        if parent_id is not None:
            graph.edge(parent_id, current_id)
        next_id = node_id + 1
        for child in self.children:
            graph, next_id = child.to_graphviz(graph, current_id, next_id)

        return graph, next_id

    def save_tree_image(self, filename='tree.png'):
        graph, _ = self.to_graphviz()
        graph.render(filename, view=False, cleanup=True)
        print(f"Дерево сохранено в {filename}")



class SyntaxAnalyzer:
    def __init__(self, grammar_file, terminals_file):
        self.grammar = parse_file(grammar_file, probabilistic=True)
        self.terminals = parse_file(terminals_file, probabilistic=False)
        self.rules = {}
        for d in [self.grammar, self.terminals]:
            for key, values in d.items():
                if key not in self.rules:
                    self.rules[key] = []
                cleaned_variants = [v[0] for v in values]
                self.rules[key].extend(cleaned_variants)

    def parse(self, sentence):
        clean_sentence = sentence.strip().rstrip('.')
        tokens = clean_sentence.split()
        success, next_pos, tree = self._match('ПРЕДЛОЖЕНИЕ', tokens, 0)
        if success and next_pos == len(tokens):
            return True, tree
        else:
            return False, None

    def _match(self, symbol, tokens, pos):
        if pos > len(tokens):
            return False, pos, None
        
        if symbol not in self.rules:
            if pos < len(tokens):
                token_to_check = tokens[pos].lower(
                ) if pos == 0 else tokens[pos]
                if token_to_check == symbol.lower():
                    return True, pos + 1, Node("WORD", value=tokens[pos])
            return False, pos, None

        variants = self.rules[symbol]
        for variant in variants:
            if len(variant) == 1 and variant[0] not in self.rules:
                target_word = variant[0]
                if pos < len(tokens):
                    current_token = tokens[pos]
                    check_token = current_token.lower() if pos == 0 else current_token
                    check_target = target_word.lower()

                    if check_token == check_target:
                        return True, pos + 1, Node(symbol, value=current_token)
                continue 
            current_pos = pos
            children = []
            sequence_match = True
            for sub_symbol in variant:
                res_ok, res_pos, res_node = self._match(
                    sub_symbol, tokens, current_pos)
                if not res_ok:
                    sequence_match = False
                    break
                current_pos = res_pos
                children.append(res_node)
            if sequence_match:
                return True, current_pos, Node(symbol, children=children)
        return False, pos, None


if __name__ == "__main__":
    analyzer = SyntaxAnalyzer('grammar.txt', 'terminals.txt')

    sentence = 'Birds clean the feathers on the tree quietly.'
    if sentence[-1] == '.':
        sentence = sentence[:-1]
    sentence = sentence.lower()
    
    is_valid, tree = analyzer.parse(sentence)
    if is_valid:
        print(f"Результат: принадлежит языку")
        tree.save_tree_image('parse_tree')
    else:
        print("Результат: не принадлежит языку")
