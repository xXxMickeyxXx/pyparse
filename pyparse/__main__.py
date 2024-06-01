# from .runtime import main


# if __name__ == "__main__":
#     main()



"""


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

I4:
    S ---> aA.


EXAMPLE INPUT:

    ab

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


from .core import Tokenizer
from .utils import apply_color, underline_text, bold_text, center_text


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
    "E": [("E", "+", "E"), ("E", "*", "E"), ("LEFT_PARENTHESIS", "E", "RIGHT_PARENTHESIS"), ("NUMBER",)]}


# grammar = {
#     "E":
# }

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
        print(f"CURRENT STATE ---> {state}")
        print(f"CURRENT TOKEN ---> {token}")
        _item = 
        if token in parse_table[state]:
            # Shift action
            state_stack.append(parse_table[state][token])
            token_stack.append(token)

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


# Example usage
INPUT = """(1 + 5) * 2"""
input_tokens = create_test_tokens(INPUT)
display_test_tokens(input_tokens)
input_valid = shift_reduce_parse(input_tokens) is True
print(f"INPUT:\n  • {INPUT}")  # Output: Accept
