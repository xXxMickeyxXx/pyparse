

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'

class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def tokenize(self):
        while self.pos < self.length:
            char = self.text[self.pos]
            if char in ' \t\n\r':
                self.pos += 1  # Skip whitespace
            elif char == '{':
                yield Token('LBRACE', char)
                self.pos += 1
            elif char == '}':
                yield Token('RBRACE', char)
                self.pos += 1
            elif char == '[':
                yield Token('LBRACKET', char)
                self.pos += 1
            elif char == ']':
                yield Token('RBRACKET', char)
                self.pos += 1
            elif char == ':':
                yield Token('COLON', char)
                self.pos += 1
            elif char == ',':
                yield Token('COMMA', char)
                self.pos += 1
            elif char == '"':
                yield self._string()
            elif char in '-0123456789':
                yield self._number()
            elif char == 't' and self.text[self.pos:self.pos+4] == 'true':
                yield Token('TRUE', 'true')
                self.pos += 4
            elif char == 'f' and self.text[self.pos:self.pos+5] == 'false':
                yield Token('FALSE', 'false')
                self.pos += 5
            elif char == 'n' and self.text[self.pos:self.pos+4] == 'null':
                yield Token('NULL', 'null')
                self.pos += 4
            else:
                raise ValueError(f'Unexpected character: {char}')

    def _string(self):
        start = self.pos
        self.pos += 1  # Skip the opening quote
        while self.pos < self.length:
            char = self.text[self.pos]
            if char == '"':
                self.pos += 1  # Skip the closing quote
                return Token('STRING', self.text[start:self.pos])
            elif char == '\\':  # Handle escape sequences
                self.pos += 2
            else:
                self.pos += 1
        raise ValueError('Unterminated string literal')

    def _number(self):
        start = self.pos
        if self.text[self.pos] == '-':
            self.pos += 1
        while self.pos < self.length and self.text[self.pos].isdigit():
            self.pos += 1
        if self.pos < self.length and self.text[self.pos] == '.':
            self.pos += 1
            while self.pos < self.length and self.text[self.pos].isdigit():
                self.pos += 1
        if self.pos < self.length and self.text[self.pos] in 'eE':
            self.pos += 1
            if self.pos < self.length and self.text[self.pos] in '+-':
                self.pos += 1
            while self.pos < self.length and self.text[self.pos].isdigit():
                self.pos += 1
        return Token('NUMBER', self.text[start:self.pos])


if __name__ == "__main__":
    # Example usage
    print()
    json_text = '{"key": {"nestedKey": "nestedValue"}, "another_key": "value"}'
    tokenizer = Tokenizer(json_text)
    tokens = list(tokenizer.tokenize())
    for token in tokens:
        print(token)
    print()
