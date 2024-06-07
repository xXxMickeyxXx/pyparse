# from .runtime import main


# if __name__ == "__main__":
#     main()



"""

__________LR(0) AUTOMATON__________


    TEST GRAMMAR:
        S ---> aA
        A ---> b


    AUGMENTED TEST GRAMMAR:
        S ---> .S
        S ---> .aA
        A ---> .b


        I0:
            S ---> .S
            S ---> .aA
            A ---> .b

        I1:
            S ---> S.

        I2:
            S ---> a.A
            A ---> .b

        I3:
            A ---> b.


        EXAMPLE INPUT ---> ab

                INITIALIZE:
                    [(0, $)]
                
                STEP:
                    [(0, $), (2, a)]

                STEP:
                    [(0, $), (2, a), (3, b)]

                STEP:
                    [(0, $), (2, a), (4, A)]

                STEP:
                    [(0, $), (1, S)]


        EXAMPLE INPUT 2 ---> abbA

                INITIALIZE:
                    [(0, $)]
                
                STEP:
                    [(0, $), (2, a)]

                STEP:
                    [(0, $), (2, a), (3, b)]

                STEP:
                    [(0, $), (2, a), (4, A)]

                STEP:
                    [(0, $), (2, a), (3, A)]

                STEP:
                    [(0, $), (2, a)]

                STEP:
                    [(0, $), (2, a), (4, A)]

                STEP:
                    [(0, $), (1, S)]


"""


"""

__________LR(0) AUTOMATON__________


    TEST GRAMMAR:
        E ---> E * B
        E ---> E + B
        E ---> B
        B ---> 0
        B ---> 1
        B ---> (E)


    TEST AUGMENTED GRAMMAR:
        S ---> .E
        E ---> .E * B
        E ---> .E + B
        E ---> .B
        B ---> .0
        B ---> .1
        B ---> .(E)


        I0:
            KERNEL
                S ---> .E
            CLOSURE
                E ---> .E * B
                E ---> .E + B
                E ---> .B
                B ---> .0
                B ---> .1
                B ---> .(E)
            TRANSITIONS
                GOTO(0, E) = 1
                GOTO(0, B) = 4


        I1:
            KERNEL
                S ---> E.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)
                REDUCE(I1, S) = ACCEPT

        I2:
            KERNEL
                E ---> E .* B
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)

        I3:
            KERNEL
                E ---> E .+ B
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


        I4:
            KERNEL:
                E ---> B.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)
                REDUCE(4, E)

        I5:
            KERNEL
                B ---> 0.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


        I6:
            KERNEL
                B ---> 1.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)

        I7:
            KERNEL
                B ---> (.E)
            CLOSURE
                E ---> .E * B
                E ---> .E + B
                E ---> .B
            TRANSITIONS
                NONE
            ACTION(S)

        I8:
            KERNEL
                E ---> E * .B
            CLOSURE
                B ---> .0
                B ---> .1
            TRANSITIONS
                GOTO(7, B) = 9
            ACTION(S)


        I9:
            KERNEL
                E ---> E + .B
            CLOSURE
                B ---> .0
                B ---> .1
            TRANSITIONS
                GOTO(8, B) = 10
            ACTION(S)


        I10:
            KERNEL
                E ---> E * B.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


        I11:
            KERNEL
                E ---> E + B.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


"""


"""

    INIT:

        • Parser initializes, adding initial state/accept symbol to the stack

    PARSE

        • Parser 


"""


"""

__________LR(0) AUTOMATON__________


    TEST GRAMMAR:
        E ---> E * B
        E ---> E + B
        E ---> B
        B ---> number
        B ---> (E)


    TEST AUGMENTED GRAMMAR:
        E ---> .E
        E ---> .E * B
        E ---> .E + B
        E ---> .B
        B ---> .NUMBER
        B ---> .(E)


         I0:
            E ---> .E (augmented grammar start symbol)
            E ---> .E * B
            E ---> .E + B
            E ---> .B
            B ---> .NUMBER
            B ---> .(E)

                TRANSITIONS (from I0)
                    GOTO(0, E) = 1
                    GOTO(0, B) = 4
                    GOTO(0, NUMBER) = 


        I1:
            E ---> E.
                
                ACTION: ACCEPT


        I2:
            E ---> E .* B










"""


"""
    In regards to 'apply_color':

        RED     --> 1 or 9
        GREEN   --> 2 or 10
        YELLOW   --> 3 or 11

"""

from abc import ABC, abstractmethod
from enum import IntEnum, StrEnum, auto

from pyparse import Grammar, Tokenizer, ShiftReduceParser, Parser
from pyparse.library import PySignal
from .utils import generate_id, apply_color, underline_text, bold_text, center_text


# NOTE rexample  grammar 
# RAW_GRAMMAR = [["S", ["a", "A"]], ["A", ["b"]]]
RAW_GRAMMAR = {"S": ["a", "A"], "A": ["b"]}


class TestResult(StrEnum):

    PASSED = bold_text(apply_color(10, f"TEST PASSED"))
    FAILED = bold_text(apply_color(9, f"TEST FAILED"))


class TestCaseID(StrEnum):

    GRAMMAR_CHECK = auto()


# class ParseState:

#     def __init__(self, parser=None, state_id=None):
#         self._parser = parser
#         self._state_id = state_id or generate_id()

#     @property
#     def parser(self):
#         # NOTE: potentially add an additional check for the '_parser' attribute, such
#         #       as 'isinstance' to ensure it's of the parser type
#         if self._parser is None:
#             # TODO: create and raise custom errors here
#             _error_details = f"unable to access 'parser' as a reference has not yet been associated with this {self.__class__.__name__} instance..."
#             raise ValueError(_error_details)
#         return self._parser

#     @property
#     def state_id(self):
#         return self._state_id

#     def copy(self):
#         raise NotImplementedError


class LRItem:

    __slots__ = ("_item_id", "_data", "_signal")

    def __init__(self, item_id=None):
        self._item_id = item_id or generate_id()
        self._data = data
        self._signal = PySignal(signal_id=self._item_id)

    @property
    def item_id(self):
        return self._item_id

    @property
    def data(self):
        return self._data

    @property
    def signal(self):
        if self._signal is None:
            self._signal = PySignal(signal_id=self.item_id)
        return self._signal

    def register(self, receiver, receiver_id=None, overwrite=False):
        self.signal.register(receiver, receiver_id=receiver_id, overwrite=overwrite)

    def remove(self, receiver_id):
        return self.signal.remove(receiver_id)

    def emit(self, *args, **kwargs):
        return self.signal.emit(*args, **kwargs)


class LRItems(LRItem):

    __slots__ = ("_items",)

    def __init__(self, data=None, item_id=None):
        super().__init__(data=data, item_id=item_id)
        self._items = {}

    def add(self, lr_item: "LRItem | LRItems", overwrite: bool = False) -> None:
        _lr_item_id = lr_item.item_id
        if _lr_item_id not in self._items or overwrite:
            self._items[_lr_item_id] = lr_item

    def remove(self, item_id: str) -> "LRItem | LRItems | None":
        return self._items.get(item_id, None)

    def get(self, item_id, default=None):
        return self._items.get(item_id, default)

    def traverse(self):
        yield from self._items.items()


class TestGrammarDesign(Grammar):

    __slots__ = ("_augmented_grammar",)

    def __init__(self, grammar_id=None):
        super().__init__(grammar_id=grammar_id)
        self._augmented_grammar = []

    def create_items(self):
        raise NotImplementedError


class TestMathTokenizer(Tokenizer):

    _numbers = {str(i) for i in range(10)}

    def __init__(self, input=None):
        super().__init__(input=input)
        self.on_loop(self._tokenize())

    def consume_ws(self):
        if self.current_char is not None:
            while self.peek() != None and self.current_char.isspace() or self.current_char in {"\r\n", "\r", "\n", "\t"}:
                yield self.consume()

    def consume_number(self, number):
        number += self.consume_until(lambda x: x.peek() in x._numbers)
        if not number.isdigit():
            _error_details = f"unable to consume and create 'NUMBER' token as the consumed number aggregate: {number} contains one or more invalid characters that prevent casting as a valid number object... as one or more characters in the 'number' aggregate is not a digit/number/etc..."
            raise TypeError(_error_details)
        _next_token = ("NUMBER", int(number))
        self.push_token(_next_token)

    def _tokenize(self):


        def _tokenize_():
            _next_token = None
            if self.can_consume:

                char = self.consume()

                if char == " " or char in {"\n", "\r", "\r\n", "\t"}:
                    self.consume_ws()
                elif char.isdigit():
                    self.consume_number(char)
                elif char == "*":
                    _next_token = ("MULTIPLY", "*")
                elif char == "+":
                    _next_token = ("PLUS", "+")
                elif char == "(":
                    _next_token = ("LEFT_PARENTHESIS", "(")
                elif char == ")":
                    _next_token = ("RIGHT_PARENTHESIS", ")")
                else:
                    _error_details = f"invalid character: {char}; does not belong to provided grammar..."
                    raise RuntimeError(_error_details)

                if _next_token is not None:
                    self.push_token(_next_token)
            else:
                self.quit()

        return _tokenize_

    @staticmethod
    def _consume_words(tokenizer):
        return tokenizer.peek() in {*tokenizer._words, *".,!@#$%^&*()_;:- "}

    @staticmethod
    def _consume_numbers(tokenizer):
        return tokenizer.peek() in tokenizer._numbers


class SRParser(ShiftReduceParser):
    pass


##### DESIGN TESTING BELOW ##### DESIGN TESTING BELOW ##### DESIGN TESTING BELOW #####


def create_test_tokens(input):
    tokenizer = TestMathTokenizer(input=input)
    return [i for i in tokenizer.tokenize()]


def display_test_tokens(tokens):
    print()
    print(underline_text(bold_text(apply_color(5, f"TEST TOKENS:"))))
    print(f"    |")
    print(f"    |")
    print(f"    |")
    print(f"    • ----> ", end="")
    for idx, i in enumerate(tokens, start=0):
        if idx == 0:
            print(f"\t{i}")
        else:
            print(f"\t\t{i}")
    print()


grammar = {
    "E": [("E", "*", "E"), ("E", "+", "E"), ("LEFT_PARENTHESIS", "E", "RIGHT_PARENTHESIS"), ("NUMBER",)]}


parse_table = {
    0: {"(": 1, "num": 2, "E": 3},
    1: {"(": 1, "num": 2, "E": 3},
    2: {"+": 4, "*": 5},
    3: {"+": 6, "*": 7, ")": 8},
    4: {"(": 1, "num": 2, "E": 3},
    5: {"(": 1, "num": 2, "E": 3},
    6: {"(": 1, "num": 2, "E": 3},
    7: {"(": 1, "num": 2, "E": 3},
    8: {"+": 9, "*": 10},
    9: {"(": 1, "num": 2, "E": 3},
    10: {"(": 1, "num": 2, "E": 3},
}


def shift_reduce_parse(tokens):
    state_stack = [0]  # Initialize the state stack with the initial state
    token_stack = []  # Initialize the token stack as empty

    stack = [(0, "$")]

    # Start parsing loop
    for token in tokens:
        state = stack[-1][0]
        _token = token[1]
        print(f"CURRENT STATE ---> {state}")
        print(f"CURRENT TOKEN ---> {token}")
        if _token in parse_table[state]:
            _item = parse_table[state][_token]
            print(f"ITEM ---> {_item}")
            state_stack.append(parse_table[state][_token])
            token_stack.append(_token)

        else:
            # Reduce action
            for production in grammar:
                if token in parse_table[state]:
                    # Replace the right-hand side of the production with the left-hand side
                    for _ in grammar[production]:
                        state_stack.pop()
                        token_stack.pop()
                    state = state_stack[-1]
                    state_stack.append(parse_table[state][production])
                    token_stack.append(production)
                    break
            else:
                # Error: No valid action found
                return "Syntax Error"

    # Check if the parsing process completes successfully
    if len(state_stack) == 2 and state_stack[1] == 3:
        return True
    else:
        return False


def test_parsing_setup(**kwargs):
    """
    EXECUTION STEPS

        1.) Instantiate and initialize grammar object

            a.) Define al grammar rules/productions, conceptually
            b.) Add them all using the 'grammar_instance.add_rule'
                method, with a positional 'rule_id: str' and
                'rule: callable' parameters 

        2.) Generate parser items, i.e. the state/symbol associations
                that encodes how the parser handles the state/symbol
                combinations
            
            (NOTE: the parser items, in effect, represent the parse table
            for a given grammar, though it doesn't and ideally shouldn't
            solely depend upon the parsing approach. I'm not sure if this
            understanding is feasible without really testing out the
            different approaches to parsing)

        3.) Instantiate and initialize parser object


    """

    _grammar_obj = kwargs.get("grammar")


def display_test_results(test_results):
    print()
    print(bold_text(f"TEST CASE RESULTS"))
    for test_key, test_case_result in test_results.items():
        print(f"    |")
        print(f"    |")
        print(f"    • ----> ", end="")
        print(f"[{test_key.upper()}]\n\t\t{test_case_result}")
        print()
    print()


def automaton_testing_main():
    INPUT = """(1 + 5) * 2"""
    input_tokens = create_test_tokens(INPUT)
    display_test_tokens(input_tokens)
    input_valid = bold_text(apply_color(10, f"INPUT IS VALID")) if shift_reduce_parse(input_tokens) else bold_text(apply_color(9, f"INPUT IS INVALID"))
    print(f"INPUT ---> {INPUT}")
    print(input_valid)
    print()


# def _add_start_production(grammar):
#     for prod_head, prod_body in grammar:


# def augment_grammar_rules(grammar):
#     for k

#     DOT = "."
#     if DOT not in item:
#         item.insert(0, DOT)


def update_parser_item(item):
    _test_item = []


def _main():
    """
        EXAMPLE TEST GRAMMAR:

            S ---> aA
            A ---> b

        AUGMENTED TEST GRAMMAR:
        
            $ ---> .s
            S ---> .aA
            A ---> .b


        TEST GRAMMAR ITEM SETS/STATES:

            $ ---> .s
            S ---> .aA
            A ---> .b

    """



    # Constants and test pieces
    ARROW_SYMBOL = bold_text(apply_color(15, "--->"))
    TEST_RESULT_MESSAGES = {}
    GRAMMAR_ID = "TESTING_FOR_GRAMMAR_DESIGN"

    # Primary lib/package   design structure setup and initialization
    grammar = TestGrammarDesign(grammar_id=GRAMMAR_ID)
    grammar.add_rule("$", ["S"])
    grammar.add_rule("S", ["a", "A"])
    grammar.add_rule("A", ["b"])
    _actual_grammar = grammar.rules()

    _grammar_check_test_passed = RAW_GRAMMAR == _actual_grammar
    _grammar_check_test_passed = TestResult.PASSED if _grammar_check_test_passed else TestResult.FAILED
    _grammar_check_msg = apply_color(11, f"Grammar generated from grammar object (ID: {grammar.grammar_id})")
    _grammar_check_pass = f"{_grammar_check_msg} {ARROW_SYMBOL} {_grammar_check_test_passed}"
    TEST_RESULT_MESSAGES[TestCaseID.GRAMMAR_CHECK] = _grammar_check_pass


    display_test_results(TEST_RESULT_MESSAGES)


def _main_2():
    _grammar_tesst_obj = Grammar(grammar_id="TESTING_GRAMMAR_OBJECT_1")
    _grammar_tesst_obj.add_rule("$", ["S"])
    _grammar_tesst_obj.add_rule("S", ["a", "A"])
    _grammar_tesst_obj.add_rule("S", ["b", "B"])
    _grammar_tesst_obj.add_rule("A", ["b"])
    _grammar_tesst_obj.add_rule("B", ["c"])
    _grammar_rules = _grammar_tesst_obj.rules()
    _inverted_grammar_rules = _grammar_tesst_obj.inverted_rules()
    print()
    for k, v in _grammar_rules.items():
        print(f"{k} ---> {v}")
    print()
    for i, e in _inverted_grammar_rules.items():
        print(f"{i} ---> {e}")


def scratch_runner(runner):
    return runner()


if __name__ == "__main__":
    pass
