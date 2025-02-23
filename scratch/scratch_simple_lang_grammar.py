from enum import StrEnum, IntEnum, auto
from collections import deque

from pyparse import Tokenizer, LexHandler, Token
from pylog import PyLogger, LogType

from .final_redesign import (
	TableBuilder
)
from .scratch_grammar_rules_filter import (
	RuleSelector,
	AndRuleSelector,
	OrRuleSelector,
	NotRuleSelector,
	RuleIDSelector,
	RuleHeadSelector,
	RuleBodySelector
)
from .scratch_utils import generate_id
from .utils import (
	bold_text,
	apply_color,
	underline_text,
	center_text
)
from .scratch_cons import (
	ParserActionType
)


class SimpleLangHandlerID(IntEnum):

	STEP_ONE = auto()
	STEP_TWO = auto()


class SimpleLangTokenType(StrEnum):
	INVALID = "INVALID"
	SKIP = ""
	END_SYMBOL = "#"
	S = "S"
	A = "A"
	C = "C"
	B = "B"
	a = "a"
	NUMBER = "NUMBER"
	DELIM = "DELIM"


class SimpleLangTokenizerHandler(LexHandler):

	def __init__(self, handler_id=None):
		super().__init__(handler_id=handler_id or self.__class__.__name__)
	
	def handle(self, tokenizer):
		_add_token_alias = tokenizer.add_token
		_tokenizer_advance = tokenizer.advance
		_cond_consume = tokenizer.cond_consume
		_counter = 1

		while tokenizer.can_consume:
			_current_char = tokenizer.current_char
			if _current_char.isdigit():
				_number = _cond_consume(lambda x, y, z: not x.isdigit())
				_add_token_alias(SimpleLangTokenType.NUMBER, _number, token_id=f"NUMBER_{_counter}")
			else:
				match _current_char:
					case "\n":
						_add_token_alias(SimpleLangTokenType.DELIM, r"\n", token_id=f"NEWLINE_DLIM_{_counter}")
						_tokenizer_advance()
					case "\t":
						_add_token_alias(SimpleLangTokenType.DELIM, r"\t", token_id=f"TAB_DLIM_{_counter}")
						_tokenizer_advance()
					case ",":
						_add_token_alias(SimpleLangTokenType.DELIM, ",", token_id=f"COMMA_DLIM_{_counter}")
						_tokenizer_advance()
					# case "S":
					# 	_add_token_alias(SimpleLangTokenType.S, "S", token_id=f"S_{_counter}")
					# 	_tokenizer_advance()
					# case "A":
					# 	_add_token_alias(SimpleLangTokenType.A, "A", token_id=f"A_{_counter}")
					# 	_tokenizer_advance()
					# case "C":
					# 	_add_token_alias(SimpleLangTokenType.C, "C", token_id=f"C_{_counter}")
					# 	_tokenizer_advance()
					# case "B":
					# 	_add_token_alias(SimpleLangTokenType.B, "B", token_id=f"B_{_counter}")
					# 	_tokenizer_advance()
					# case "a":
					# 	_add_token_alias(SimpleLangTokenType.a, "a", token_id=f"a_{_counter}")
					# 	_tokenizer_advance()
					case _:
						# _add_token_alias(SimpleLangTokenType.SKIP, _current_char, token_id=f"SKIP_{_counter}")
						_add_token_alias(SimpleLangTokenType.INVALID, _current_char, token_id=f"INVALID ---> {_counter}")
						_tokenizer_advance()
			_counter += 1
		_add_token_alias(SimpleLangTokenType.END_SYMBOL, "$", token_id="END_SYMBOL")


class SimpleLangTableBuilder(TableBuilder):

	def build_table(self, table):
		pass


class PyParser:

	__slots__ = ("_parser_id", "_state", "_handlers", "_state_handlers", "_action_handlers", "_action_buffer", "_parse_context", "_result", "_result_set", "_quit_flag")

	def __init__(self, init_state=0, parser_id=None):
		self._parser_id = parser_id or generate_id()
		self._state = init_state or 0
		self._handlers = []
		self._action_buffer = deque()
		self._parse_context = None
		self._result = None
		self._result_set = False
		self._quit_flag = False

	@property
	def parser_id(self):
		return self._parser_id

	@property
	def state(self):
		return self._state

	@property
	def is_running(self):
		return not self._quit_flag

	@property
	def parse_context(self):
		return self._parse_context

	def result(self):
		if not self._result_set:
			# TODO: create and raise custom error here
			_error_details = f"result has not yet been set...please set result via the 'set_result' method and then call this method..."
			raise Exception(_error_details)
		return self._result

	def set_result(self, result):
		self._result = result
		self._result_set = True

	def set_context(self, parse_context):
		self._parse_context = parse_context

	def add_handler(self, handler):
		self._handlers.append(handler)

	def register(self, state, handler):
		_signals = self._signals
		if state not in _signals:
			_signals[state] = []
		_signals[state].append(handler)

	def submit_action(self, action, *args, **kwargs):
		self._action_buffer.append((action, args, kwargs))

	def update(self, state):
		self._state = state

	def stop(self):
		self._quit_flag = True

	def parse(self, parse_context):
		self.set_context(deque(parse_context))
		self._quit_flag = False
		while not self._quit_flag:
			for _handler in self._handlers:
				_handler(self)
		return self.result()


class SimpleLangParser(PyParser):

	def __init__(self, init_state=0, parser_id=None):
		super().__init__(init_state=init_state, parser_id=parser_id)
		self._state_stack = deque()
		self._symbol_stack = deque()
		self._signals = {}
		self._context_ptr = 0
		self.init()


		self._test_val = 0
		self._target_stop = 10000

	@property
	def next_token(self):
		if self._context_ptr < len(self.parse_context):
			return self.parse_context[self._context_ptr]
		raise NotImplementedError("@TODO<Finish implementing 'next_token' property>")

	def init(self):
		self.add_handler(self.step)
		# self.register(None, self.__END__)
		self.register((None, None), self.__invalid_parsse)
		self.register(0, self._state_0)
		self.register((1, "NUMBER"), self.__number_state1)
		self.register((1, "END_SYMBOL"), self.__invalid_parsse)
		self.register((4, "END_SYMBOL"), self.__number_state4)
		self.register((5, "END_SYMBOL"), self.__number_state5)
		self.register((2, "END_SYMBOL"), self.__END__)
		self.register((7, SimpleLangTokenType.NUMBER), self.__number_state7)

	def step(self, parser):
		try:
			for _handler in self._signals[self._state]:
				_handler(self)
		except KeyError as key_err:
			parser.update((None, None))

	def register(self, state, handler):
		_signals = self._signals
		if state not in _signals:
			_signals[state] = []
		_signals[state].append(handler)

	def __SHIFT__(self):
		self._symbol_stack.append((self.parse_context[self._context_ptr].token_type))
		self._context_ptr += 1

	def __REDUCE__(self, new_symbol, pop_count, state=(None, None)):
		for _ in range(pop_count):
			self._symbol_stack.pop()
		self._symbol_stack.append(new_symbol)
		self.update(state)

	@staticmethod
	def __END__(parser):
		print()
		print(f"STOPPING PARSER...")
		print()
		parser.set_result(True)
		# parser.submit_action(parser.stop)
		parser.stop()

	@staticmethod
	def _state_0(parser):
		_next_token_type = parser.parse_context.popleft()
		_next_token_type = _next_token_type.token_type
		print(f"NEXT TOKEN TYPE: {_next_token_type}")
		match _next_token_type:
			case SimpleLangTokenType.NUMBER:
				parser.update((7, SimpleLangTokenType.NUMBER))

		print(f"I'm in state {parser.state}!!!!")
		print(f"CHANGING TO STATE {1}")
		parser.__SHIFT__()

		parser.update((1, parser._symbol_stack[-1]))

	@staticmethod
	def __number_state1(parser):
		_parse_context = parser.parse_context
		print(_parse_context)
		parser.__REDUCE__("B", 1, (4, _parse_context[parser._context_ptr].token_type))
		print(f"SHIT")

	@staticmethod
	def __number_state4(parser):
		parser.__REDUCE__("A", 1, (5, parser.parse_context[parser._context_ptr].token_type))

	@staticmethod
	def __number_state5(parser):
		parser.__REDUCE__("S", 1, (2, parser.parse_context[parser._context_ptr].token_type))

	@staticmethod
	def __number_state7(parser):
		print(f"PARSER STATE 7")
		parser.set_result(False)
		parser.stop()
		parser.__REDUCE__(SimpleLangTokenType.C, 1, (8, parser.parse_context[parser._context_ptr].token_type))

	@staticmethod
	def __invalid_parsse(parser):
		# if parser._test_val < parser._target_stop:
		# 	print(f"NOT ENOUGH")
		# 	parser._test_val += 1
		# 	return
		print()
		print(f"STOPPING PARSER...")
		print()
		parser.set_result(False)
		# parser.submit_action(parser.stop)
		parser.stop()


# __simple_lang_actions = {}


# def __ADD_ACTION_HANDLER__(action, handler):
# 	__simple_lang_actions[action] = handler
# 	return True


# def __SIMPLE_LANG_ACTION_HANDLER__(action, default=None):
# 	return __simple_lang_actions.get(action, default)


if __name__ == "__main__":
	pass
