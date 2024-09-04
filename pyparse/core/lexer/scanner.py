from abc import ABC, abstractmethod

from ...utils import generate_id
from ...errors import ScannerError


class Scanner(ABC):

    """Objects of this class are esponsible for managing logic associated
    with managing the input stream as it's fed into the tokenizer. Object
    spends it's lifetime working within the tokenizer design and
    should not be interacted with directly; the logic implemented here is
    to separate conerns between managing the tokenizing process and
    reading/getting/streaming the input
    

    """

    def __init__(self, input="", scanner_id=None):
        self._scanner_id = scanner_id or generate_id()
        self._input = input
        self._pointer = 0

    @property
    def scanner_id(self):
        return self._scanner_id

    @property
    def input(self):
        return self._input

    @property
    def input_len(self):
        return len(self.input)

    @property
    def can_consume(self):
        return self._input is not None and self.pointer < self.input_len

    @property
    def current_char(self):
        _input = self._input
        _pointer = self._pointer
        return _input[_pointer] if _input and self.can_consume else None

    @property
    def pointer(self):
        return self._pointer

    def set_input(self, input):
        self._input = input

    def reset(self):
        self.set_input("")
        self.update_pointer(0)

    def update_pointer(self, idx):
        if self.input_len > 0:
            if idx >= self.input_len:
                _error_details = f"unable to update pointer to position of input at index: {idx} as that is out of the input's index bounds (max: {len(self.input) - 1 if len(self.input) > 0 else 0})..."
                raise ScannerError(details=_error_details)
        self._pointer = idx

    def peek(self, offset=1):
        _tmp_pointer = self.pointer + offset
        if _tmp_pointer < self.input_len:
                return self._input[_tmp_pointer]
        return None

    def peek_range(self, start=0, until=-1, step=1):
        if self.can_consume:
            return self._input[self.pointer + start::step] if (until == -1 or until <=0) else self._input[self.pointer + start: until: steps]
        return None

    def advance(self):
        if self.can_consume:
            self._pointer += 1

    def consume(self):
        _current_char = self.current_char
        self.advance()
        return _current_char

    def cond_consume(self, condition):
        _lexeme = ""
        _current_char = self.current_char
        while self.can_consume:
            if condition(_current_char, _lexeme, self):
                break
            _lexeme += _current_char
            self.advance()
            _current_char = self.current_char
        return _lexeme

    def expect(self, value):
        _peek_val = self.peek()
        if _peek_val is not None and _peek_val == value:
            return self.consume()
        return False

    def expect_at(self, value, offset=1):
        return self.peek(offset=offset) == value

    def input_at(self, index):
        if index >= self.input_len:
            # TODO: create and raise custom error here
            _error_details = f"unable to access token at index: {index} as it exceeds the bounds of tokens container..."
            raise IndexError(_error_details)
        return self.input[index]

    def input_range(self, *slice_args):
        _slicer = slice(*slice_args)
        return self.input[_slicer]


if __name__ == "__main__":
    _scanner = Scanner(input="HI", scanner_id="TEST_SCANNER")
    print(f"SCANNER ID: {_scanner.scanner_id}")
    print(_scanner.peek())
    print(_scanner.current_char)
