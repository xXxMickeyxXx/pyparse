"""

	_____TO-DO_____

		A.) Cleanup module and remove designing testing code
			(AS-OF-SUNDAY: 2024-09-01)

"""


from abc import ABC, abstractmethod
from typing import (
    Protocol,
    Callable,
    Union,
    Any,
    List,
    Dict,
    Tuple,
    LiteralString,
    Type,
    Optional,
    runtime_checkable
)

from .scanner import Scanner
from ..token import Token
from ...utils import generate_id
from ...errors import TimeOutError


class Tokens(ABC):
	"""Represents the object that contains and manages token list access and
	is also what the parser interface expects to receive when it's 'parse'
	method is called. Will likely interact with the 'Scanner' design as well,
	though that should only happen in the 'Tokenizer' class so as to prevent
	un-needed dependency
	"""


# class Tokenizer:

# 	def __init__(self, input=None, tokenizer_id=None):
# 		self._tokenizer_id = tokenizer_id or generate_id()
# 		self._input = input
# 		self._pointer = 0
# 		self._tokens = []
# 		self._scanner = None
# 		self._input_len = len(self._input) if self._input is not None else 0

# 	@property
# 	def tokenizer_id(self):
# 		return self._tokenizer_id

# 	@property
# 	def can_consume(self):
# 		return self.scanner.can_consume

# 	@property
# 	def current_char(self):
# 		_input = self._input
# 		_pointer = self._pointer
# 		return _input[_pointer] if _input and self.can_consume else None

# 	@property
# 	def tokens(self):
# 		return self._tokens

# 	@property
# 	def token_count(self):
# 		return len(self._tokens)

# 	@property
# 	def scanner(self):
# 		if self._scanner is None:
# 			self._scanner = self.create_scanner(self._input, scanner_id=self.tokenizer_id)
# 		return self._scanner

# 	@property
# 	def input(self):
# 		return self.scanner.input

# 	def create_scanner(self, input=None, scanner_id=None):
# 		return self.scanner_factory(input=input, scanner_id=scanner_id)

# 	def scanner_factory(self, *args, **kwargs):
# 		return Scanner(*args, **kwargs)

# 	def create_token(self, token_type, token_val, token_id=None):
# 		return self.token_factory(token_type, token_val, token_id=token_id)

# 	def token_factory(self, *args, **kwargs):
# 		return Token(*args, **kwargs)

# 	def set_input(self, input):
# 		self.scanner.set_input(input)

# 	def reset(self, auto_flush=False):
# 		if auto_flush:
# 			self.flush_tokens()
# 		elif self.token_count < 1 and not auto_flush:
# 			# TODO: create and raise custom error here
# 			_error_details = f"unable to reset instance of '{self.__class__.__name__}' as tokens are still present in the token buffer (i.e. the '_tokens' field); please flush buffer via the 'flush_tokens' method prior to calling the 'reset' or pass 'True' to the 'auto_flush' kwarg in either 'reset' (if resetting) or 'tokenize' method (if tokenizing input)..."
# 			raise RuntimeError(_error_details)
# 		self.scanner.reset()

# 	def flush_tokens(self):
# 		_retval = []
# 		while self.tokens:
# 			_next_token = self.tokens.pop(0)
# 			_retval.append(_next_token)
# 		assert len(self.tokens) == 0, "an error occured when attempting to flush token buffer (i.e. the '_tokens' field); please review and try again..."
# 		return _retval

# 	def peek(self, offset=0):
# 		return self.scanner.peek(offset=offset)

# 	def peek_range(self, start=0, until=-1, step=1):
# 		return self.scanner.peek_range(start=start, until=until, step=step)

# 	def advance(self):
# 		return self.scanner.advance()

# 	def consume(self):
# 		return self.scanner.consume()

# 	def cond_consume(self, condition):
# 		return self.scanner.cond_consume(condition)

# 	def expect(self, value):
# 		return self.scanner.expect(value)

# 	def expect_at(self, value, offset=1):
# 		return self.scanner.expect_at(value, offset=offset)

# 	def add_token(self, token_type, token_val, token_id=None):
# 		# TODO: consider adding the 'block=False, timeout=None' params, like how the
# 		# 		built-in 'Queue' object does it
# 		_new_token = self.create_token(token_type, token_val, token_id=token_id)
# 		self.tokens.append(_new_token)

# 	def pop_token(self, idx=-1):
# 		if not self.tokens or len(self.tokens) <= 0:
# 			# TODO: create and raise custom error here
# 			_error_details = f"unable to 'pop' token from token container, as it's currently empty..."
# 			raise IndexError(_error_details)
# 		return self.tokens.pop(idx)

# 	def input_at(self, index):
# 		if index >= self._input_len:
# 			# TODO: create and raise custom error here
# 			_error_details = f"unable to access token at index: {index} as it exceeds the bounds of tokens container..."
# 			raise IndexError(_error_details)
# 		return self.input[index]

# 	def input_range(self, *slice_args):
# 		_slicer = slice(*slice_args)
# 		return self.input[_slicer]

# 	def token_at(self, index):
# 		if index >= self._input_len:
# 			# TODO: create and raise custom error here
# 			_error_details = f"unable to access token at index: {index} as it exceeds the bounds of tokens container..."
# 			raise IndexError(_error_details)
# 		return self._tokens[index]

# 	def token_range(self, *slice_args):
# 		_slicer = slice(*slice_args)
# 		return self.tokens[_slicer]

# 	def tokenize(self, handler, *, auto_flush=False):
# 		handler.set_tokenizer(self)
# 		handler.handle()
# 		if auto_flush:
# 			_tokens = self.flush_tokens()
# 		else:
# 			_tokens = self.tokens
# 		return _tokens


class Tokenizer:

	def __init__(self, input=None, token_factory=Token, tokenizer_id=None):
		self._tokenizer_id = tokenizer_id or generate_id()
		self._scanner = None
		self._input = input or ""
		# self._pointer = 0
		self._tokens = []
		# self._input_len = len(self._input)
		self._token_factory = token_factory

	@property
	def tokenizer_id(self):
		return self._tokenizer_id

	@property
	def scanner(self):
		if self._scanner is None:
			self._scanner = self.scanner_factory(scanner_id=self.tokenizer_id)
			self._scanner.set_input(self._input)
		return self._scanner

	# @property
	# def can_consume(self):
	# 	return self._input is not None and self._pointer < self._input_len

	# @property
	# def current_char(self):
	# 	_input = self._input
	# 	_pointer = self._pointer
	# 	return _input[_pointer] if _input and self.can_consume else None

	@property
	def can_consume(self):
		return self.scanner.can_consume

	@property
	def current_char(self):
		# _input = self.scanner._input
		# _pointer = self.scanner._pointer
		# return _input[_pointer] if _input and self.can_consume else None
		return self.scanner.current_char

	@property
	def tokens(self):
		return self._tokens

	@property
	def input(self):
		return self.scanner.input

	def scanner_factory(self, *args, **kwargs):
		return Scanner(*args, **kwargs)

	def set_input(self, input):
		self._input = input
		self.scanner.set_input(input)
		# self._input_len = len(input)

	def reset(self):
		self.scanner.reset()
		_retval = self.flush_tokens()
		self.set_input("")
		return _retval

	def create_token(self, token_type, token_val, token_id=None):
		return self.token_factory(token_type, token_val, token_id=token_id)

	def token_factory(self, *args, **kwargs):
		if not bool(self._token_factory):
			_error_details = f"unable to instantiate a new token as tokenizer's '_token_factory' has not yet been associated with a valid token factory..."
			raise RuntimeError(_error_details)
		return self._token_factory(*args, **kwargs)

	def peek(self, offset=0):
		return self.scanner.peek(offset=offset)

	def peek_range(self, start=0, until=-1, step=1):
		return self.scanner.peek_range(start=start, until=until, step=step)

	def advance(self):
		return self.scanner.advance()

	def consume(self):
		return self.scanner.consume()

	def cond_consume(self, condition):
		return self.scanner.cond_consume(condition)

	def expect(self, value):
		return self.scanner.expect(value)

	def expect_at(self, value, offset=1):
		return self.scanner.expect_at(value, offset=offset)

	def input_at(self, index):
		return self.scanner.input_at(index)

	def input_range(self, *slice_args):
		return self.scanner.input_range(*slice_args)

	def add_token(self, token_type, token_val, token_id=None):
		# TODO: consider adding the 'block=False, timeout=None' params, like how the
		# 		built-in 'Queue' object does it
		_new_token = self.create_token(token_type, token_val, token_id=token_id)
		self.tokens.append(_new_token)

	def pop_token(self, idx=-1):
		if not self.tokens or len(self.tokens) <= 0:
			# TODO: create and raise custom error here
			_error_details = f"unable to 'pop' token from token container, as it's currently empty..."
			raise IndexError(_error_details)
		return self.tokens.pop(idx)

	def token_at(self, index):
		if index >= self._input_len:
			# TODO: create and raise custom error here
			_error_details = f"unable to access token at index: {index} as it exceeds the bounds of tokens container..."
			raise IndexError(_error_details)
		return self._tokens[index]

	def token_range(self, *slice_args):
		_slicer = slice(*slice_args)
		return self.tokens[_slicer]

	def tokenize(self, handler):
		handler.set_tokenizer(self)
		handler.handle()
		return self.tokens

	def flush_tokens(self):
		_retval = []
		while self.tokens:
			_next_token = self.tokens.pop(0)
			_retval.append(_next_token)
		assert len(self.tokens) == 0, "an error occured when attempting to flush token buffer (i.e. the '_tokens' field); please review and try again..."
		return _retval


if __name__ == "__main__":
	from enum import StrEnum, IntEnum, auto

	from pyprofiler import profile_callable, SortBy
	from .lex_handler import LexHandler
	from ...utils import apply_color, underline_text, bold_text


	def setup_tokenizer(tokenizer):
		def tokenize(handler):
			return tokenizer.tokenize(handler)
		return tokenize


	def display_tokens(tokens):
		print()
		print(underline_text(bold_text(apply_color(206, "TOKENS"))))
		print()
		_text = ""
		for idx, token in enumerate(tokens):
			if idx == 0:					
				_text += f"    |\n"
				_text += f"    |\n"
				_text += f"    |\n"
				_text += f"    • ----> ({token.token_type}: {token.token_val})"
			else:
				_text += f"            ({token.token_type}: {token.token_val})"
			print(_text)
			_text = ""
		print()
		print()


	class TestTokenType(IntEnum):

		HOW = auto()
		ARE = auto()
		YOU = auto()
		Q_MARK = auto()


	class TestGrammar4TokenType(StrEnum):

		NUMBER = "NUMBER"
		PLUS_OPERATOR = "PLUS_OPERATOR"
		MULT_OPERATOR = "MULT_OPERATOR"
		WS = "WS"
		LEFT_PAREN = "LEFT_PAREN"
		RIGHT_PAREN = "RIGHT_PAREN"


	class HowAreYouTokenizeHandler(LexHandler):

		def handle(self):
			while self.tokenizer.can_consume:
				_current_char = self.tokenizer.current_char
				_token_type, _token_val = (None, None)
				if _current_char.lower() == "h":
					_token_type, _token_val = (f"<TestTokenType: {TestTokenType.HOW.name}>", self.tokenizer.cond_consume(lambda x, y, tkzr: y.lower() == "how"))
				elif _current_char.lower() == "a":
					_token_type, _token_val = (f"<TestTokenType: {TestTokenType.ARE.name}>", self.tokenizer.cond_consume(lambda x, y, tkzr: y.lower() == "are"))
				elif _current_char.lower() == "y":
					_token_type, _token_val = (f"<TestTokenType: {TestTokenType.YOU.name}>", self.tokenizer.cond_consume(lambda x, y, tkzr: y.lower() == "you"))
				elif _current_char.lower() == "?":
					_token_type, _token_val = (f"<TestTokenType: {TestTokenType.Q_MARK.name}>", self.tokenizer.consume())

				if _token_type and _token_val:
					self.tokenizer.add_token(_token_type, _token_val, token_id=None)
				self.tokenizer.advance()


	class TestGrammar4TokenizeHandler(LexHandler):

		def __init__(self, tokenizer=None):
			super().__init__(tokenizer=tokenizer)
			self._symbol_mapping = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "*", "(", ")", " "]
			self._token_type_idx_mapper = [
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.NUMBER,
				TestGrammar4TokenType.PLUS_OPERATOR,
				TestGrammar4TokenType.MULT_OPERATOR,
				TestGrammar4TokenType.LEFT_PAREN,
				TestGrammar4TokenType.RIGHT_PAREN,
				TestGrammar4TokenType.WS
			]

		def handle(self):
			# NOTE: variables initialized with "_a" suffix are aliases for method calls in
			# 		order to suck out a litte bit more performnace since the additional
			# 		lookup isn't needed
			_add_token_alias = self.tokenizer.add_token
			_tokenizer_advance_a = self.tokenizer.advance
			_symbol_mapping_index_a = self._symbol_mapping.index
			_cond_consume_a = self.tokenizer.cond_consume
			while self.tokenizer.can_consume:
				_current_char = self.tokenizer.current_char
				_token_type, _token_val = (None, None)

				if _current_char == " ":
					self.tokenizer.advance()
					continue

				if _current_char not in self._symbol_mapping:
					_error_details = f"symbol: '{_current_char}' does not exists within this handler's symbol mapping ('_symbol_mapping') property; please verify symbol mapping and try again..."
					raise RuntimeError(_error_details)

				_token_idx = _symbol_mapping_index_a(_current_char)
				_token_type = self._token_type_idx_mapper[_token_idx]
				_token_val = _current_char
				_tokenizer_advance_a()
				if bool(_token_type) and bool(_token_val):
					_add_token_alias(_token_type, _token_val)


	# @profile_callable(sort_by=SortBy.TIME)
	def main():
		_how_are_you_tokenizer = Tokenizer(input="How are you?")
		_how_are_you_tokenizer_handler = HowAreYouTokenizeHandler(tokenizer=_how_are_you_tokenizer)

		_test_grammar_4_tokenizer = Tokenizer(input="1 + 1")
		_test_grammar_4_tokenizer_handler = TestGrammar4TokenizeHandler(tokenizer=_test_grammar_4_tokenizer)

		print()
		print()
		print(bold_text(underline_text(apply_color(208, f"TOKENS\n"))))
		for i in _how_are_you_tokenizer.tokenize(_how_are_you_tokenizer_handler):
			print(i)

		for _ in range(2):
			print()

		_tokenize_1 = setup_tokenizer(_how_are_you_tokenizer)
		_tokenizer_1_tokens = _tokenize_1(_how_are_you_tokenizer_handler)
		display_tokens(_tokenizer_1_tokens)
		print()

		print()

		_tokenize_2 = setup_tokenizer(_test_grammar_4_tokenizer)
		_tokenizer_2_tokens = _tokenize_2(_test_grammar_4_tokenizer_handler)
		display_tokens(_tokenizer_2_tokens)
		print()

		for i in _tokenizer_2_tokens:
			for k, v in i._token_cache.items():
				print(f"{k} ---> {v}")
			break


	main()