from pyparse import Tokenizer
from .utils import underline_text, apply_color, bold_text


class TestDateTokenizer(Tokenizer):

    # _valid_years = {str(i) for i in range(1950, 2100)}
    # _valid_months = [str(i) for i in range(0, 13)] + ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
    # _valid_days = [str(i) for i in range(1, 32)] + ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
    _valid_numbers = [str(i) for i in range(10)]

    def __init__(self, input=None):
        super().__init__(input=input)
        self.on_loop(self._tokenize())

    def _tokenize(self):

        def _tokenize_():
            if self.can_consume:
                char = self.consume()
                if char.isdigit():
                    char += self.consume_until(lambda x: x.peek() in {"-", "/"})
                    self.push_token(("YEAR", char))
                    char = ""
                if self.expect("-"):
                    self.push_token(("DELIMITER", self.expect("-", consume=True)))
                if self.peek() is not None and self.peek() in self._valid_numbers:
                    char += self.consume_until(lambda x: x.peek() in ("-", "/"))
                    self.push_token(("MONTH", char))
                    char = ""
                if self.expect("-"):
                    self.push_token(("DELIMITER", self.expect("-", consume=True)))
                if self.peek() is not None and self.peek() in self._valid_numbers:
                    char += self.consume_until(lambda x: not x.can_consume)
                    self.push_token(("DAY", char))
                    char = ""
            else:
                _EOF_token = ("EOF", "")
                self.push_token(_EOF_token)
                self.quit()

        return _tokenize_


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
                _EOF_token = ("EOF", "")
                self.push_token(_EOF_token)
                self.quit()

        return _tokenize_

    # @staticmethod
    # def _consume_words(tokenizer):
    #     return tokenizer.peek() in {*tokenizer._words, *".,!@#$%^&*()_;:- "}

    # @staticmethod
    # def _consume_numbers(tokenizer):
    #     return tokenizer.peek() in tokenizer._numbers


def create_test_math_tokens(input):
    tokenizer = TestMathTokenizer(input=input)
    return [i for i in tokenizer.tokenize()]


def create_test_date_tokens(input):
    tokenizer = TestDateTokenizer(input=input)
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


def test_math_token_runner():
    TEST_INPUT = "(1 + 7) * 8"
    _test_tokens = create_test_math_tokens(TEST_INPUT)
    display_test_tokens(_test_tokens)


def test_date_token_runner():
    TEST_INPUT = "2024-07-01"
    _test_tokens = create_test_date_tokens(TEST_INPUT)
    display_test_tokens(_test_tokens)


if __name__ == "__main__":
    # test_math_token_runner()
    test_date_token_runner()


# class Token:
#     def __init__(self, type, value):
#         self.type = type
#         self.value = value

#     def __repr__(self):
#         return f'Token({self.type}, {repr(self.value)})'

# class Tokenizer:
#     def __init__(self, text):
#         self.text = text
#         self.pos = 0
#         self.length = len(text)

#     def tokenize(self):
#         while self.pos < self.length:
#             char = self.text[self.pos]
#             if char in ' \t\n\r':
#                 self.pos += 1  # Skip whitespace
#             elif char == '{':
#                 yield Token('LBRACE', char)
#                 self.pos += 1
#             elif char == '}':
#                 yield Token('RBRACE', char)
#                 self.pos += 1
#             elif char == '[':
#                 yield Token('LBRACKET', char)
#                 self.pos += 1
#             elif char == ']':
#                 yield Token('RBRACKET', char)
#                 self.pos += 1
#             elif char == ':':
#                 yield Token('COLON', char)
#                 self.pos += 1
#             elif char == ',':
#                 yield Token('COMMA', char)
#                 self.pos += 1
#             elif char == '"':
#                 yield self._string()
#             elif char in '-0123456789':
#                 yield self._number()
#             elif char == 't' and self.text[self.pos:self.pos+4] == 'true':
#                 yield Token('TRUE', 'true')
#                 self.pos += 4
#             elif char == 'f' and self.text[self.pos:self.pos+5] == 'false':
#                 yield Token('FALSE', 'false')
#                 self.pos += 5
#             elif char == 'n' and self.text[self.pos:self.pos+4] == 'null':
#                 yield Token('NULL', 'null')
#                 self.pos += 4
#             else:
#                 raise ValueError(f'Unexpected character: {char}')

#     def _string(self):
#         start = self.pos
#         self.pos += 1  # Skip the opening quote
#         while self.pos < self.length:
#             char = self.text[self.pos]
#             if char == '"':
#                 self.pos += 1  # Skip the closing quote
#                 return Token('STRING', self.text[start:self.pos])
#             elif char == '\\':  # Handle escape sequences
#                 self.pos += 2
#             else:
#                 self.pos += 1
#         raise ValueError('Unterminated string literal')

#     def _number(self):
#         start = self.pos
#         if self.text[self.pos] == '-':
#             self.pos += 1
#         while self.pos < self.length and self.text[self.pos].isdigit():
#             self.pos += 1
#         if self.pos < self.length and self.text[self.pos] == '.':
#             self.pos += 1
#             while self.pos < self.length and self.text[self.pos].isdigit():
#                 self.pos += 1
#         if self.pos < self.length and self.text[self.pos] in 'eE':
#             self.pos += 1
#             if self.pos < self.length and self.text[self.pos] in '+-':
#                 self.pos += 1
#             while self.pos < self.length and self.text[self.pos].isdigit():
#                 self.pos += 1
#         return Token('NUMBER', self.text[start:self.pos])


# if __name__ == "__main__":
#     # Example usage
#     print()
#     json_text = '{"key": {"nestedKey": "nestedValue"}, "another_key": "value"}'
#     tokenizer = Tokenizer(json_text)
#     tokens = list(tokenizer.tokenize())
#     for token in tokens:
#         print(token)
#     print()
