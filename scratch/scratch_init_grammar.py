from .grammar_rule import GrammarRule
from .grammar_designing import Grammar


def grammar_factory():
    return Grammar(grammar_id="[GRAMMAR_AS_OF_2024_06_13]")


def init_grammar_1(grammar, augmented_rule=GrammarRule("$", ["S"], rule_id="INIT_ITEM")):
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
    grammar.add_rule(augmented_rule)

    _S_rule = GrammarRule("S", ["a", "A"], rule_id="S_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("A", ["b"], rule_id="A_rule_1")
    grammar.add_rule(_S_rule)

    # _S_rule = GrammarRule("A", ["b", "b"], rule_id="A_rule_2")
    # grammar.add_rule(_S_rule)


def init_grammar_2(grammar, augmented_rule=GrammarRule("$", ["S"], rule_id="INIT_ITEM")):
    grammar.add_rule(augmented_rule)

    _S_rule = GrammarRule("S", ["a", "A"], rule_id="S_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("A", ["b", "B"], rule_id="A_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("B", ["c", "C"], rule_id="B_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("C", ["d", "D"], rule_id="C_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("D", ["e"], rule_id="D_rule")
    grammar.add_rule(_S_rule)


def init_grammar_3(grammar, augmented_rule=GrammarRule("$", ["E"], rule_id="INIT_ITEM")):
    grammar.add_rule(augmented_rule)

    _S_rule = GrammarRule("E", ["E", "+", "T"], rule_id="S_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("E", ["T"], rule_id="S_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("T", ["T", "*", "F"], rule_id="S_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("T", ["F"], rule_id="S_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("F", ["(", "E", ")"], rule_id="S_rule")
    grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("E", ["id"], rule_id="S_rule")
    grammar.add_rule(_S_rule)


if __name__ == "__main__":
    pass
