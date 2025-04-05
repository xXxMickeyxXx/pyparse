from .grammar_rule import GrammarRule
from .grammar_designing import Grammar
from .scratch_cons import LanguageType


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
    grammar.create_rule("E", ["(", ")"], rule_id="E_3")
    grammar.create_rule("B", ["C"], rule_id="B_1")
    grammar.create_rule("B", ["number"], rule_id="B_2")
    grammar.create_rule("C", ["(", "E", ")"], rule_id="C_1")
    grammar.create_rule("C", ["(", "C", ")"], rule_id="C_2")
    grammar.create_rule("number", ["NUMBER"], rule_id="number")
    grammar.create_rule("operator", ["+"], rule_id="operator_1")
    grammar.create_rule("operator", ["-"], rule_id="operator_2")
    grammar.create_rule("operator", ["*"], rule_id="operator_3")
    grammar.create_rule("operator", ["/"], rule_id="operator_4")
    # grammar.create_rule("$", ["expression"], rule_id="INIT_RULE")
    # grammar.create_rule("expression", ["term"], rule_id="exp_term")
    # grammar.create_rule("expression", ["expression", "+", "term"], rule_id="exp_plus_term")
    # grammar.create_rule("expression", ["expression", "-", "term"], rule_id="exp_minus_term")
    # grammar.create_rule("term", ["factor"], rule_id="term_factor")
    # grammar.create_rule("term", ["term", "*", "factor"], rule_id="term_mult_fact")
    # grammar.create_rule("term", ["term", "/", "factor"], rule_id="term_div_fact")
    # grammar.create_rule("factor", ["number"], rule_id="fact_num")
    # grammar.create_rule("factor", ["(", "expression", ")"], rule_id="fact_exp")
    # grammar.create_rule("factor", ["(", ")"], rule_id="fact_empty_exp")
    # grammar.create_rule("number", ["NUMBER"], rule_id="num")

    
def init_grammar_9(grammar):
    # Simple test grammar in order to help in making the 
    grammar.create_rule("#", ["S"], rule_id="INIT_RULE")
    grammar.create_rule("S", ["a", "A"], rule_id="S_rule_1")
    grammar.create_rule("S", ["S", "!"], rule_id="S_rule_2")
    grammar.create_rule("S", ["C"], rule_id="S_rule_3")
    grammar.create_rule("A", ["B"], rule_id="A_rule_1")
    grammar.create_rule("B", ["b"], rule_id="B_rule_1")
    grammar.create_rule("C", ["(", "S", ")"], rule_id="C_rule_1")


def init_date_lang_grammar_v0_0_1(grammar):
    # Date grammar for parsing and facilitating the usage of date
    grammar.create_rule("#", ["date"], rule_id="INIT_RULE")
    grammar.create_rule("date", ["year_format"], rule_id="date_format1")
    grammar.create_rule("date", ["month_format"], rule_id="date_format2")
    grammar.create_rule("date", ["day_format"], rule_id="date_format3t")
    
    grammar.create_rule("year_format", ["year", "DELIM", "month", "DELIM", "day"], rule_id="year_format")
    grammar.create_rule("month_format", ["month", "DELIM", "day", "DELIM", "year"], rule_id="month_format")
    grammar.create_rule("day_format", ["day", "DELIM", "month", "DELIM", "year"], rule_id="day_format")
    
    grammar.create_rule("year", ["year_4"], rule_id="year4")
    grammar.create_rule("year", ["year_2"], rule_id="year2")
    
    grammar.create_rule("year_4", ["digit", "digit", "digit", "digit"], rule_id="year_4digits")
    grammar.create_rule("year_2", ["digit", "digit"], rule_id="year_2digits")

    grammar.create_rule("month", ["digit", "digit"], rule_id="month")
    grammar.create_rule("day", ["digit", "digit"], rule_id="day")
    grammar.create_rule("digit", ["0"], rule_id="digit0")
    grammar.create_rule("digit", ["1"], rule_id="digit1")
    grammar.create_rule("digit", ["2"], rule_id="digit2")
    grammar.create_rule("digit", ["3"], rule_id="digit3")
    grammar.create_rule("digit", ["4"], rule_id="digit4")
    grammar.create_rule("digit", ["5"], rule_id="digit5")
    grammar.create_rule("digit", ["6"], rule_id="digit6")
    grammar.create_rule("digit", ["7"], rule_id="digit7")
    grammar.create_rule("digit", ["8"], rule_id="digit8")
    grammar.create_rule("digit", ["9"], rule_id="digit9")


def init_simple_lang_grammar_v0_0_1(grammar):
    """
    Simple-lang grammar - a super small grammar spec to truly begin
    designing and building this whole shebang. This language is essentialy
    a summation language where each number, separated by a (consistent)
    delimiter (either a newline, '\\n', or a comma, ',') gets added to a
    running total, wich gets printed out at program exit (NOTE: language
    is left-associative).
    

    EXAMPLE VALID SENTENCES (each enumerated line number is followed by '.)'
                             meaning the first byte at index zero of the input
                             occurs directly after the ')'  within an input
                             text):

        1.)123
        2.)36
        3.)593

    which prints out upon exit:
        
        #(EMPTY LINE)
        #TOTAL: 752
        #(EMPTY LINE)

    OR

        1.)123,
        2.)1034,
        3.)593

    which prints out upon exit:
        
        #(EMPTY LINE)
        #TOTAL: 1750
        #(EMPTY LINE)


    """

    grammar.create_rule("#", ["S"], rule_id="INIT_RULE")
    grammar.create_rule("S", ["A"], rule_id="S_rule_1")
    grammar.create_rule("A", ["B"], rule_id="A_rule_1")
    grammar.create_rule("B", ["C"], rule_id="B_rule_1")
    grammar.create_rule("B", ["C", "DELIM", "C"], rule_id="B_rule_2")
    grammar.create_rule("C", ["NUMBER"], rule_id="C_rule_1")
    grammar.create_rule("C", ["B", "DELIM"], rule_id="C_rule_2")


def init_todo_grammar_v0_0_1(grammar):
    # First real use-case mini-language for building/constructing TO-DO lists by
    # within a python project by embedding mini-language using comments.
    #
    # Since python disregards source text when it starts with a pound symbol (#),
    # and since it allows mult-line text when surrounded by triple-quotes (also
    # referred to as a 'docstring') we can easily embed the mini-language by
    # prefixing every statement with the pound (#) symbol before adding whatever
    # language specific qualifiers, declarations, expressions, etc.
    #
    # For example (NOTE: spacing only included to draw visual attention to the example text directly below):
    # 
    #         @TODO<Syntax for a 'TODO' data structure>
    #         @NOTE<Syntax for a 'NOTE' data structure>
    #
    grammar.create_rule("$", ["todo_lang"], rule_id="INIT_RULE")
    grammar.create_rule("todo_lang", ["todo_@_symbol", "todo_type", "todo_body"], rule_id="todo_lang")
    grammar.create_rule("todo_type", ["TODO"], rule_id="todo_type_TODO")
    grammar.create_rule("todo_type", ["NOTE"], rule_id="todo_type_NOTE")
    grammar.create_rule("todo_body", ["todo_l_angle", "todo_body_text", "todo_r_angle"], rule_id="todo_body")
    grammar.create_rule("todo_body_text", ["TEXT"], rule_id="todo_body_text")
    grammar.create_rule("todo_l_angle", ["<"], rule_id="todo_l_angle")
    grammar.create_rule("todo_r_angle", [">"], rule_id="todo_r_angle")
    grammar.create_rule("todo_@_symbol", ["@"], rule_id="todo_@_symbol")


_grammar_initializers = {
    1: init_grammar_1,
    2: init_grammar_2,
    3: init_grammar_3,
    4: init_grammar_4,
    5: init_grammar_5,
    6: init_grammar_6,
    7: init_grammar_7,
    8: init_grammar_8,
    9: init_grammar_9,
    # 10: init_grammar_10,
    "date_lang_v0_0_1": init_date_lang_grammar_v0_0_1,
    "todo_lang_v0_0_1": init_todo_grammar_v0_0_1,
    "simple_lang_v0_0_1": init_simple_lang_grammar_v0_0_1
}


def init_grammar(grammar, initializer_key, initializers=None):
    if initializers is None:
        initializers = _grammar_initializers
    _initializer = initializers[initializer_key]
    _initializer(grammar)
    return grammar


if __name__ == "__main__":
    pass
