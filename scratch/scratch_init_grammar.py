from .grammar_rule import GrammarRule
from .grammar_designing import Grammar


def grammar_factory():
    return Grammar(grammar_id="[GRAMMAR_AS_OF_2024_06_13]")


def init_grammar(grammar):
    # (NOTE: augmented each instance of a 'GrammarRule' in order to prepare
    #        for parse table construction)

    # (NOTE: check docstring at top of this module for the test grammar
    #        definition, just below the end line, where states "TEST GRAMMAR")


    # Augmented initial/starting production
    # NOTE: determine if this is automatically added to grammar ('Grammar')
    #       instance or if it's something that you have to do yourself.
    #       Ideally, the 'Grammar' object should be able to represent
    #       grammar for any type of parser/lexer, with the (no currently
    #       designed/implemented but will-be-or-should-be-soon) 'GrammarRules'
    #       object acting as the 'implementation' to the 'Grammar'
    #       abstraction, utilizing the bridge pattern in order to ensure
    #       compatibility/portability with other designs
    _initial_item = GrammarRule("$", ["S"])
    _initial_item.augment()
    grammar.add_rule(_initial_item)

    _S_rule = GrammarRule("S", ["a", "A"])
    _S_rule.augment()
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("A", ["b"])
    _S_rule.augment()
    grammar.add_rule(_S_rule)


if __name__ == "__main__":
    pass
