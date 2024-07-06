from .grammar_rule import GrammarRule
from .grammar_designing import Grammar


def grammar_factory():
    return Grammar(grammar_id="[GRAMMAR_AS_OF_2024_06_13]")


def init_grammar_1(grammar):
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
    
    grammar.create_rule("$", ["S"], rule_id="INIT_RULE")
    grammar.create_rule("S", ["a", "A"], rule_id="S_rule_1")
    grammar.create_rule("S", ["b", "B"], rule_id="S_rule_2")
    grammar.create_rule("A", ["b"], rule_id="A_rule_1")
    grammar.create_rule("B", ["c"], rule_id="B_rule_1")


def init_grammar_2(grammar):
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
    
    grammar.create_rule("$", ["S"], rule_id="INIT_RULE")

    # _S_rule = GrammarRule("S", ["a", "A", "B", "C"], rule_id="S_rule")
    # grammar.add_rule(_S_rule)

    _S_rule = GrammarRule("S", ["a", "A"], rule_id="S_rule")
    grammar.add_rule(_S_rule)

    # _S_rule_2 = GrammarRule("S", ["S", "B"], rule_id="S_rule_2")
    # grammar.add_rule(_S_rule_2)

    _A_rule_1 = GrammarRule("A", ["b"], rule_id="A_rule_1")
    grammar.add_rule(_A_rule_1)

    # _S_rule = GrammarRule("B", ["c"], rule_id="B_rule_1")
    # grammar.add_rule(_S_rule)


def init_grammar_3(grammar):
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


def init_grammar_4(grammar):
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
