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
	END_SYMBOL = "END_SYMBOL"
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

	__slots__ = ("_parser_id", "_handlers", "_instructions", "_ip", "_parse_context", "_result", "_result_set", "_quit_flag")

	def __init__(self, init_state=0, parser_id=None):
		self._parser_id = parser_id or generate_id()
		self._handlers = {}
		self._instructions = []
		self._ip = 0
		self._parse_context = None
		self._result = None
		self._result_set = False
		self._quit_flag = False

	@property
	def parser_id(self):
		return self._parser_id

	@property
	def is_running(self):
		return not self._quit_flag

	@property
	def parse_context(self):
		return self._parse_context

	@property
	def current_instruction(self):
		return self._instructions[self._ip][0]

	@property
	def arg_count(self):
		return self._instructions[self._ip][1]

	def add_instruction(self, instruction_type, count, *args):
		self._instructions.append((instruction_type, count))
		self._instructions.extend(args)

	def update_ip(self, ip):
		self._ip = ip

	def args(self, count=1):
		# @NOTE<'count' should be an integer of 1 or greater. If it is integer 0 then it will be an empty list>
		return self._instructions[self._ip + 1: count + 1]

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

	def add_handler(self, instruction_type, handler):
		self._handlers[instruction_type] = handler
	
	def stop(self):
		self._quit_flag = True

	def parse(self, parse_context):
		self.set_context(deque(parse_context))
		self._quit_flag = False
		while self._ip:
			_instruction_type, _arg_count = self.current_instruction, self.arg_count
			_handler = self._handlers.get(_instruction_type, lambda *args, **kwargs: None)
			_handler(*self.args(_arg_count))
		return self.result()


class SimpleLangParser(PyParser):

	def __init__(self, init_state=0, parser_id=None):
		super().__init__(init_state=init_state, parser_id=parser_id)
		self.init()
		self._bool_ = False
		# self.set_result(False)
		print(f"INSTRUCTIONS ---> {self._instructions}")
		print(f"CURRENT INSTRUCTION ---> {self.current_instruction}")
		print(f"CURRENT ARGS ---> {self.arg_count}")

	@property
	def next_token(self):
		if self._context_ptr < len(self.parse_context):
			return self.parse_context[self._context_ptr]
		raise NotImplementedError("@TODO<Finish implementing 'next_token' property>")

	def init(self):
		self.add_handler("ADD", self._add_tester_)
		self.add_instruction("ADD", 3, 10, 3)
		# self.add_instruction("ADD",3, 13, 2)

	# def _add_tester_(self, parser):
	def _add_tester_(self, x, y):
		_next_inst_idx = len(_args) + 1
		print(f"{x} + {y} = {x + y}")
		self.update_ip(2)
		print()
		print(self._instructions)
		if self._bool_:
			parser.stop()
			self.set_result(False)
		else:
			self._bool_ = True

		# _args = parser.args(2)
		# _next_inst_idx = len(_args)
		# print(f"{_args[0]} + {_args[1]} = {sum(_args)}")
		# self.update_ip(_next_inst_idx)
		# print()
		# print(f)
		# print(self._instructions)
		# if self._bool_:
		# 	parser.stop()
		# else:
		# 	self._bool_ = True

	# def step(self, parser):
	# 	try:
	# 		for _handler in self._signals[self._state]:
	# 			_handler(self)
	# 	except KeyError as key_err:
	# 		parser.update((None, None))

	# def register(self, state, handler):
	# 	_signals = self._signals
	# 	if state not in _signals:
	# 		_signals[state] = []
	# 	_signals[state].append(handler)

	# def __SHIFT__(self):
	# 	self._symbol_stack.append((self.parse_context[self._context_ptr].token_type))
	# 	self._context_ptr += 1

	# def __REDUCE__(self, new_symbol, pop_count, state=(None, None)):
	# 	for _ in range(pop_count):
	# 		self._symbol_stack.pop()
	# 	self._symbol_stack.append(new_symbol)
	# 	self.update(state)

	# @staticmethod
	# def __END__(parser):
	# 	print()
	# 	print(f"STOPPING PARSER...")
	# 	print()
	# 	parser.set_result(True)
	# 	# parser.submit_action(parser.stop)
	# 	parser.stop()

	# @staticmethod
	# def _state_0(parser):
	# 	print(f"I'm in state {parser.state}!!!!")
	# 	print(f"CHANGING TO STATE {1}")
	# 	parser.__SHIFT__()

	# 	parser.update((1, parser._symbol_stack[-1]))

	# @staticmethod
	# def __number_state1(parser):
	# 	_parse_context = parser.parse_context
	# 	print(_parse_context)
	# 	parser.__REDUCE__("B", 1, (4, _parse_context[parser._context_ptr].token_type))
	# 	print(f"SHIT")

	# @staticmethod
	# def __number_state4(parser):
	# 	parser.__REDUCE__("A", 1, (5, parser.parse_context[parser._context_ptr].token_type))

	# @staticmethod
	# def __number_state5(parser):
	# 	parser.__REDUCE__("S", 1, (2, parser.parse_context[parser._context_ptr].token_type))

	# @staticmethod
	# def __invalid_parsse(parser):
	# 	parser.set_result(False)
	# 	parser.stop()


# __simple_lang_actions = {}


# def __ADD_ACTION_HANDLER__(action, handler):
# 	__simple_lang_actions[action] = handler
# 	return True


# def __SIMPLE_LANG_ACTION_HANDLER__(action, default=None):
# 	return __simple_lang_actions.get(action, default)


if __name__ == "__main__":
	pass
