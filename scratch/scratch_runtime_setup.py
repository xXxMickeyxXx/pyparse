from .test_parser_design import shift_reduce_parse_tester
from .prefix_tree import Trie
from .grammar_rule import GrammarRule
from .grammar_designing import NewGrammarDesign


def _parser_main():
	print(f"HELLO FROM PARSER MAIN ---> {__file__}")
	print(f"PARSER FUNC ---> {shift_reduce_parse_tester}")


def _prefix_tree_main():
    trie = Trie()
    trie.insert("hello")
    trie.insert("world")

    print()
    print(trie.search("hello"))  # Output: True
    print(trie.search("hell"))   # Output: False
    print(trie.starts_with("hell")) # Output: True
    print(trie.starts_with("helloa")) # Output: False
    print(trie.starts_with("world")) # Output: True
    print()


def _grammar_rule_main():
    print()
    _copy_1 = GrammarRule("S", ["a", "A"])
    _copy_1.augment()
    _copy_2 = _copy_1.copy()
    # _copy_2 = _copy_1.copy(deepcopy=True)
    print()
    print(f"COPY 1 is COPY 2 ---> {_copy_1 is _copy_2}")
    print(f"COPY 1 == COPY 2 ---> {_copy_1 == _copy_2}")
    print()


def _new_grammar_design_main():
    _new_grammar = NewGrammarDesign(grammar_id="[NEW_GRAMMAR_DESIGN]")
    
    _test_rule_1 = GrammarRule("$", ["S"])
    _test_rule_2 = GrammarRule("S", ["a", "A"])
    _test_rule_2_dupe = GrammarRule("S", ["a", "A"])
    _test_rule_3 = GrammarRule("A", ["b"])

    _new_grammar.add_rule(_test_rule_1)
    _new_grammar.add_rule(_test_rule_2)
    _new_grammar.add_rule(_test_rule_2_dupe)
    _new_grammar.add_rule(_test_rule_3)
    _new_grammar.add_rule(GrammarRule("A", ["bb"]))

    for i in _new_grammar.rules():
        print(f"{i}")

    _test_removed_by_body = _new_grammar.remove_rule(rule_body=["b"])
    print(_test_removed_by_body)
    print()
    _test_removed_by_head = _new_grammar.remove_rule(rule_head=["S"])
    print(_test_removed_by_head)
    print()


if __name__ == "__main__":
    pass
