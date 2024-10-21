from .grammar_rule import GrammarRule
from .grammar_designing import Grammar


def test_grammar_factory():
    return Grammar(grammar_id="[ • -^- • TEST_GRAMMAR • -^- • ]")


def init_grammar_1(grammar):
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
    grammar.create_rule("A", ["b"], rule_id="A_rule_1")


def init_grammar_2(grammar):
    grammar.create_rule("$", ["S"], rule_id="INIT_RULE")
    grammar.create_rule("S", ["a", "A", "A"], rule_id="S_rule_1")
    grammar.create_rule("S", ["a", "A"], rule_id="S_rule_2")
    # grammar.create_rule("A", ["b", "b"], rule_id="A_rule_1")
    grammar.create_rule("A", ["b"], rule_id="A_rule_2")


def init_grammar_3(grammar):
    grammar.create_rule("$", ["S"], rule_id="INIT_RULE")
    grammar.create_rule("$", ["S"], rule_id="INIT_RULE")
    grammar.create_rule("S", ["Z"], rule_id="S_rule_1")
    grammar.create_rule("S", ["T"], rule_id="S_rule_2")
    grammar.create_rule("S", ["D"], rule_id="S_rule_3")
    grammar.create_rule("T", ["a", "A", "B"], rule_id="T_rule_1")
    grammar.create_rule("D", ["a", "b", "c"], rule_id="D_rule_1")
    grammar.create_rule("Z", ["a", "A"], rule_id="Z_rule_1")
    grammar.create_rule("A", ["b"], rule_id="A_rule")
    grammar.create_rule("B", ["c"], rule_id="B_rule")


def init_grammar_4(grammar):
    grammar.create_rule("$", ["E"], rule_id="INIT_RULE")
    grammar.create_rule("E", ["E", "*", "B"], rule_id="E_rule_1")
    grammar.create_rule("E", ["E", "+", "B"], rule_id="E_rule_2")
    grammar.create_rule("E", ["B"], rule_id="E_rule_3")
    grammar.create_rule("B", ["0"], rule_id="B_rule_1")
    grammar.create_rule("B", ["1"], rule_id="B_rule_2")


def init_grammar_5(grammar):
    grammar.create_rule("$", ["S"], rule_id="INIT_RULE")
    grammar.create_rule("S", ["a", "A"], rule_id="S_rule_1")
    grammar.create_rule("S", ["S", "A"], rule_id="S_rule_2")
    grammar.create_rule("S", ["A"], rule_id="S_rule_3")
    grammar.create_rule("A", ["b"], rule_id="A_rule_1")
    grammar.create_rule("A", ["b", "A"], rule_id="A_rule_2")


def init_grammar_6(grammar):
    grammar.create_rule("$", ["S"], rule_id="INIT_RULE")
    grammar.create_rule("S", ["S", "+", "S"], rule_id="S_rule_1")
    grammar.create_rule("S", ["S", "*", "S"], rule_id="S_rule_2")
    grammar.create_rule("S", ["id"], rule_id="S_rule_3")
    grammar.create_rule("S", ["(", "S", ")"], rule_id="S_rule_3")

    # grammar.create_rule("$", ["S"], rule_id="INIT_RULE")
    # grammar.create_rule("S", ["A", "+", "A"], rule_id="S_rule_1")
    # grammar.create_rule("S", ["A", "*", "A"], rule_id="S_rule_2")
    # grammar.create_rule("A", ["id"], rule_id="A_rule_1")
    # grammar.create_rule("A", ["S"], rule_id="A_rule_2")


def init_grammar_7(grammar):
    # grammar.create_rule("$", ["E"], rule_id="INIT_RULE")
    # grammar.create_rule("E", ["E", "*", "B"], rule_id="E_rule_1")
    # grammar.create_rule("E", ["E", "/", "B"], rule_id="E_rule_2")
    # grammar.create_rule("E", ["E", "+", "B"], rule_id="E_rule_3")
    # grammar.create_rule("E", ["E", "-", "B"], rule_id="E_rule_4")
    # grammar.create_rule("E", ["B"], rule_id="E_rule_5")
    # grammar.create_rule("B", ["C"], rule_id="B_rule_1")
    # grammar.create_rule("B", ["T"], rule_id="B_rule_2")
    # grammar.create_rule("C", ["(", "E", ")"], rule_id="C_rule_1")
    # grammar.create_rule("T", ["number"], rule_id="T_rule_1")
    # grammar.create_rule("number", ["NUMBER"], rule_id="number_rule_1")
    grammar.create_rule("$", ["E"], rule_id="INIT_RULE")
    grammar.create_rule("E", ["B"], rule_id="E_rule_1")
    grammar.create_rule("B", ["B", "operator", "B"], rule_id="B_rule_1")
    grammar.create_rule("B", ["C"], rule_id="B_rule_2")
    grammar.create_rule("C", ["(", "E", ")"], rule_id="C_rule_1")
    grammar.create_rule("operator", ["+"], rule_id="operator_rule_1")
    grammar.create_rule("operator", ["-"], rule_id="operator_rule_2")
    grammar.create_rule("operator", ["*"], rule_id="operator_rule_3")
    grammar.create_rule("operator", ["/"], rule_id="operator_rule_4")


def init_grammar_8(grammar):
    # Test arithmatic grammr
    grammar.create_rule("$", ["E"], rule_id="INIT_RULE")
    grammar.create_rule("E", ["E", "operator", "E"], rule_id="E_1")
    grammar.create_rule("E", ["B"], rule_id="E_2")
    grammar.create_rule("B", ["C"], rule_id="B_1")
    grammar.create_rule("B", ["number"], rule_id="B_2")
    grammar.create_rule("C", ["(", "E", ")"], rule_id="C_1")
    grammar.create_rule("number", ["NUMBER"], rule_id="C_1")
    grammar.create_rule("operator", ["+"], rule_id="operator_1")
    grammar.create_rule("operator", ["-"], rule_id="operator_2")
    grammar.create_rule("operator", ["*"], rule_id="operator_3")
    grammar.create_rule("operator", ["/"], rule_id="operator_4")

    
def init_grammar_9(grammar):
    # Simple test grammar in order to help in making the 
    grammar.create_rule("#", ["S"], rule_id="INIT_RULE")
    grammar.create_rule("S", ["a", "A"], rule_id="S_rule_1")
    grammar.create_rule("A", ["B"], rule_id="A_rule_1")
    grammar.create_rule("B", ["b"], rule_id="B_rule_1")
    grammar.create_rule("B", ["C"], rule_id="B_rule_2")
    grammar.create_rule("C", ["(", "S", ")"], rule_id="C_rule_1")


_grammar_initializers = {
    1: init_grammar_1,
    2: init_grammar_2,
    3: init_grammar_3,
    4: init_grammar_4,
    5: init_grammar_5,
    6: init_grammar_6,
    7: init_grammar_7,
    8: init_grammar_8,
    9: init_grammar_9
}


def init_grammar(grammar, initializer_key, initializers=_grammar_initializers):
    _initializer = initializers[initializer_key]
    _initializer(grammar)


if __name__ == "__main__":
    pass
