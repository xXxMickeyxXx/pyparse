from abc import ABC, abstractmethod

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


class Tokenizer:

	# @NOTE<update 'current_char' to 'current_symbol' or 'current_sym'; make sure to update everywhere applicable>

	def __init__(self, input=None, handler=None, token_factory=Token, tokenizer_id=None):
		self._tokenizer_id = tokenizer_id or generate_id()
		self._scanner = None
		self._input = input
		self._tokens = []
		self._token_factory = token_factory
		self._handler = handler
		# if handler:
		# 	self.set_handler(handler)

		# self._handler = handler
		# if self._handler:
		# 	self._handler.set_tokenizer(self)

	@property
	def tokenizer_id(self):
		return self._tokenizer_id

	@property
	def scanner(self):
		if self._scanner is None:
			self._scanner = self.scanner_factory(scanner_id=self.tokenizer_id)
			self._scanner.set_input(self._input)
		return self._scanner

	@property
	def can_consume(self):
		return self.scanner.can_consume

	@property
	def current_char(self):
		return self.scanner.current_char

	@property
	def tokens(self):
		return self._tokens

	@property
	def input(self):
		if self._input is None or not self._input:
			# TODO: create and raise custom error here
			_error_details = f"unable to access 'input' property as one has not yet been associated with instance of '{self.__class__.__name__}'..."
		return self.scanner.input

	@property
	def handler(self):
		if self._handler is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access 'handler' property as one has not yet been associated with instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._handler

	def set_handler(self, handler):
		self._handler = handler
		# handler.set_tokenizer(self)

	def scanner_factory(self, *args, **kwargs):
		return Scanner(*args, **kwargs)

	def set_input(self, input):
		self._input = input
		self.scanner.set_input(input)

	def reset(self):
		self.scanner.reset()
		return self.flush_tokens()

	def create_token(self, token_type, token_val, token_id=None):
		return self.token_factory(token_type, token_val, token_id=token_id)

	def token_factory(self, *args, **kwargs):
		if not bool(self._token_factory):
			_error_details = f"unable to instantiate a new token as tokenizer's '_token_factory' has not yet been associated with a valid token factory..."
			raise RuntimeError(_error_details)
		return self._token_factory(*args, **kwargs)

	def peek(self, offset=1):
		return self.scanner.peek(offset=offset)

	def peek_range(self, offset=1, step=1):
		return self.scanner.peek_range(offset=offset, step=step)

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
		if index >= len(self.tokens):
			# TODO: create and raise custom error here
			_error_details = f"unable to access token at index: {index} as it exceeds the bounds of tokens container..."
			raise IndexError(_error_details)
		return self._tokens[index]

	def token_range(self, *slice_args):
		_slicer = slice(*slice_args)
		return self.tokens[_slicer]

	def tokenize(self, input):
		self.set_input(input)
		self.handler.handle(self)
		return self.reset()

	def flush_tokens(self):
		_retval = [i for i in self.tokens]
		self._tokens.clear()
		assert len(self.tokens) == 0, "an error occured when attempting to flush token buffer; please review and try again..."
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
		SUB_OPERATOR = "SUB_OPERATOR"
		MULT_OPERATOR = "MULT_OPERATOR"
		DIV_OPERATOR = "DIV_OPERATOR"
		FLOOR_DIV_OPERATOR = "FLOOR_DIV_OPERATOR"
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
			self._symbol_mapping = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "*", "-", "/", "//", "(", ")", " "]
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
				TestGrammar4TokenType.SUB_OPERATOR,
				TestGrammar4TokenType.DIV_OPERATOR,
				TestGrammar4TokenType.FLOOR_DIV_OPERATOR,
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
				_token_idx = _symbol_mapping_index_a(_current_char)

				# if _current_char == " ":
				# 	self.tokenizer.advance()
				# 	continue

				if _current_char == "/":
					_next_char = self.tokenizer.peek()
					if _next_char == "/":
						_token_idx += 1
						print(f"TOKEN INDEX @ FLOOR_DIV_OPERATOR")
						print(f"\t• {_token_idx}")
						print(f"\t• {self._token_type_idx_mapper[_token_idx]}")
						_token_type = self._token_type_idx_mapper[_token_idx]
						_token_val = "//"
						_add_token_alias(_token_type, _token_val, token_id=None)
						for _ in range(2):
							self.tokenizer.advance()
						continue

				if _current_char not in self._symbol_mapping:
					_error_details = f"symbol: '{_current_char}' does not exists within this handler's symbol mapping ('_symbol_mapping') property; please verify symbol mapping and try again..."
					raise RuntimeError(_error_details)

				_token_type = self._token_type_idx_mapper[_token_idx]
				_token_val = _current_char
				_tokenizer_advance_a()
				if bool(_token_type) and bool(_token_val):
					_add_token_alias(_token_type, _token_val)


	# @profile_callable(sort_by=SortBy.TIME)
	def main():
		_how_are_you_tokenizer = Tokenizer(input="How are you?")
		_how_are_you_tokenizer_handler = HowAreYouTokenizeHandler(tokenizer=_how_are_you_tokenizer)

		_test_grammar_4_tokenizer = Tokenizer(input="1  1")
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