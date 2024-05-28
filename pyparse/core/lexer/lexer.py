class Lexer:
    """Utilize the state pattern and some sort of handler registry, then build
    an automaton to handle creating tokens for the parser to consume. Ideally,
    the parser can pull tokens from the lexer (tokenizer) one by one, lazily.
    (NOTE: this would also be ideal for making it easier to make parsing part
    of the task as opposed to be used inside of a thread - thread operation
    would only then require actually performing the operation and not any
    additional logic)
    """

    # TODO: pass tokenizer object (type: 'DictTokenizer[Tokenizer]')

    def __init__(self, tokenizer=None):
        self._tokenizer = tokenizer
        self._consumed = False

    def set_tokenizer(self, tokenizer):
        self._tokenizer = tokenizer
        self._consumed = False

    def generate(self, input):
        self._tokenizer.set_input(input)
        if self._tokenizer is None or not self._tokenizer:
            return iter([])
        _retval = [i for i in self._tokenizer.tokenize()]
        self._consumed = True
        return _retval

    def stream(self, input):
        self._tokenizer.set_input(input)
        _tokenizer = self._tokenizer.tokenize()
        for _token in _tokenizer:
            yield _token
        self._consumed = True


if __name__ == "__main__":
    pass
