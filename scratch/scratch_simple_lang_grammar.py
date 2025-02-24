from random import randrange
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


class SimpleLangParserInstruction(IntEnum):
	HALT = auto()
	PRINT = auto()
	ADD_OP = auto()
	SUB_OP = auto()
	MULT_OP = auto()
	DIV_OP = auto()
	INIT = auto()
	CLEANUP = auto()

	@classmethod
	def INSTR(cls, *, int_val: int = 0, enum_name: str = ""):
		if int_val is not None:
			for _field in cls:
				_intval = _field.value
				if int_val == _intval:
					return _field.name
		elif enum_name is not None:
			for _field in cls:
				_enumname = _field.name
				if enum_name == _enumname:
					return _field.value
		else:
			# @TODO<Create and raise custom error here>
			_error_details = f"null arguments received; must pass AT LEAST an 'int' value for the 'int_val' kwarg (in order to get the name of the instruction) OR a 'str' value for the 'enum_name' kwarg (in order to get the 'int' value associated with the enum name) - NOTE: if parameters receive a value, 'int_val' takes precedence"
			raise ValueError(_error_details)


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

	__slots__ = ("_parser_id", "_handlers", "_instructions", "_curr_instruction", "_args", "_parse_context", "_result", "_result_set", "_quit_flag", "_invalid_instr")

	def __init__(self, invalid_instruction=SimpleLangParserInstruction.HALT, parser_id=None):
		self._parser_id = parser_id or generate_id()
		self._handlers = {}
		self._instructions = deque()
		self._curr_instruction = None
		self._args = ((), {})
		self._parse_context = None
		self._result = None
		self._result_set = False
		self._quit_flag = False
		self._invalid_instr = invalid_instruction

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
	def curr_instruction(self):
		return self._curr_instruction

	@property
	def curr_args(self):
		return self._args

	@property
	def instructions(self):
		return self._instructions

	@property
	def invalid_instruction(self):
		return self._invalid_instr

	@property
	def result_set(self):
		return self._result_set

	def send(self, *args, **kwargs):
		self._args = (args, kwargs)

	def set_instruction(self, instruction_type):
		self._curr_instruction = instruction_type

	def add_instruction(self, instruction_type, *args, **kwargs):
		self._instructions.append((instruction_type, args, kwargs))

	def next_instruction(self, default=None):
		return self._instructions.popleft() if self._instructions else default

	def next_handler(self, default=None):
		_instr_type, _args, _kwargs = self.next_instruction(default=(self.invalid_instruction, (), {}))  # @NOTE<'default' value of (None, (), {}) in order to allow tuple unpacking syntax, regardless if valid next instruction type (i.e. unsupportd)>
		_handler = self._handlers.get(_instr_type, default)
		self.set_instruction(_instr_type)
		self.send(*_args, **_kwargs)
		return _handler

	def set_result(self, result):
		self._result = result
		self._result_set = True

	def set_context(self, parse_context):
		self._parse_context = parse_context

	def add_handler(self, instruction_type, handler):
		self._handlers[instruction_type] = handler
	
	def halt(self):
		self._quit_flag = True
		self._instructions = deque()

	def parse(self, parse_context):
		self.set_context(deque(parse_context))
		self._quit_flag = False
		while self._instructions and (not self._quit_flag):
			_handler = self.next_handler(default=None)
			if _handler is None:
				# @TODO<Create and raise custom error here>
				_error_details = f"unable to find supported handler for NEXT INSTRUCTION TYPE: '{self.curr_instruction}'...exiting with runtime-error..."
				raise RuntimeError(_error_details)
			_args, _kwargs = self._args
			_handler(*_args, **_kwargs)
		return self._result


class SimpleLangParser(PyParser):

	def __init__(self, invalid_instruction=SimpleLangParserInstruction.HALT, parser_id=None):
		super().__init__(invalid_instruction=invalid_instruction, parser_id=parser_id)
		self._instruction_counter = 1
		self._valid_parse = 0
		self._valid_parse_set = False
		self._random_val = 10
		self._instr_color_map = {
			SimpleLangParserInstruction.HALT: 11,
			SimpleLangParserInstruction.PRINT: 198,
			SimpleLangParserInstruction.ADD_OP: 10,
			SimpleLangParserInstruction.SUB_OP: 5,
			SimpleLangParserInstruction.CLEANUP: 226
		}
		self.init()

	def init(self):
		# @NOTE
			# <Handlers for INSTRUCTION TYPE:
			#	'HALT' (INSTR #: 1),
			#	'PRINT' (INSTR #: 2),
			#	'ADD_OP' (INSTR #: 3),
			#	'SUB_OP' (INSTR #: 4),
			# 	'CLEANUP' (INSTR #: 8>
		self.add_handler(SimpleLangParserInstruction.INSTR(int_val=1), self.__HALT__)
		self.add_handler(SimpleLangParserInstruction.HALT, self.__HALT__)
		self.add_handler(SimpleLangParserInstruction.PRINT, self.__PRINT__)
		self.add_handler(SimpleLangParserInstruction.ADD_OP, self._ADD_)
		self.add_handler(SimpleLangParserInstruction.SUB_OP, self._SUB_)
		self.add_handler(SimpleLangParserInstruction.CLEANUP, self.__CLEANUP__)
		
		# @NOTE<Test instructions to run first, upon calling of 'parse' runner method>
		self.add_instruction(SimpleLangParserInstruction.ADD_OP, randrange(100), randrange(100))
		self.add_instruction(SimpleLangParserInstruction.ADD_OP, randrange(100), randrange(100))
		_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=3)}' INSTRUCTION --- •]"
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.ADD_OP], _msg)), end="\n")
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.ADD_OP], _msg)), end="\n\n")

	def _ADD_(self, x: int, y: int) -> None:
		print(bold_text(apply_color(208, f"START OF INSTRUCTION COUNT ---> {self._instruction_counter}")))
		_instr_msg = f"PERFORMING '{SimpleLangParserInstruction.INSTR(int_val=3)}' INSTRUCTION..."
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.ADD_OP], _instr_msg)), end="\n\n")
		_result = x + y
		print(f"{x} + {y} = {_result}")
		print(f"RESULT ---> {_result}")
		if _result >= 25:
			self.add_instruction(SimpleLangParserInstruction.SUB_OP, randrange(100), randrange(100))
			print()
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=4)}' INSTRUCTION --- •]"
			print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.SUB_OP], _msg)), end="\n\n")
		else:
			self.add_instruction(SimpleLangParserInstruction.SUB_OP, randrange(100), randrange(100))
			print()
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=4)}' INSTRUCTION --- •]"
			print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.SUB_OP], _msg)), end="\n\n")
		print(bold_text(apply_color(208, f"END OF INSTRUCTION COUNT ---> {self._instruction_counter}")), end="\n\n")
		print(apply_color(190, f" ----- ================================================== "))
		print()
		self._instruction_counter += 1

	def _SUB_(self, x: int, y:int) -> None:
		print(bold_text(apply_color(208, f"START OF INSTRUCTION COUNT ---> {self._instruction_counter}")))
		_instr_msg = f"PERFORMING '{SimpleLangParserInstruction.INSTR(int_val=4)}' INSTRUCTION..."
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.SUB_OP], _instr_msg)), end="\n\n")
		_result = x - y
		self.add_instruction(SimpleLangParserInstruction.PRINT, f"{x} - {y} = {_result}")
		if _result < 7:
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=2)}' INSTRUCTION --- •]"
			print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.PRINT], _msg)), end="\n\n")
		else:
			if not self._valid_parse_set:
				print(f"TESTING VALIDITY OF PARSE ---> 10 < [{_result}] <= 18 ---> {10 < _result <=18}")
				if 18 >= _result > 10:
					self._valid_parse = 1
					_msg = f"\nVALID PARSE ---> {self._valid_parse}"
				else:
					self._valid_parse = 0
					_msg = f"\nVALID PARSE ---> {self._valid_parse}"
				self._valid_parse_set = True
				print(bold_text(apply_color(166, _msg)), end="\n\n")

		print(bold_text(apply_color(208, f"END OF INSTRUCTION COUNT ---> {self._instruction_counter}")), end="\n\n")
		print(apply_color(190, f" ----- ================================================== "))
		print()
		self._instruction_counter += 1
		return None

	def __PRINT__(self, *args, **kwargs):
		print(bold_text(apply_color(208, f"START OF INSTRUCTION COUNT ---> {self._instruction_counter}")))
		_instr_msg = f"PERFORMING '{SimpleLangParserInstruction.INSTR(int_val=2)}' INSTRUCTION..."
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.PRINT], _instr_msg)), end="\n\n")
		print(*args, **kwargs)
		print()
		if self._random_val >= 10:
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=3)}' INSTRUCTION --- •]"
			print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.ADD_OP], _msg)), end="\n\n")
			self.add_instruction(SimpleLangParserInstruction.ADD_OP, randrange(1000), randrange(1000))
			self._random_val -= 1
		else:
			_PRINT_CONCAT = underline_text(bold_text(apply_color(randrange(256), "YOU STUPID SON OF A BITCH!")))
			self.add_instruction(SimpleLangParserInstruction.PRINT, _PRINT_CONCAT, end="\n")
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=2)}' INSTRUCTION --- •]"
			print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.PRINT], _msg)), end="\n\n")

			self.add_instruction(SimpleLangParserInstruction.HALT)
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=1)}' INSTRUCTION --- •]"
			print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.HALT], _msg)), end="\n")

		print(bold_text(apply_color(208, f"END OF INSTRUCTION COUNT ---> {self._instruction_counter}")), end="\n\n")
		print(apply_color(190, f" ----- ================================================== "))
		print()
		self._instruction_counter += 1

	def __HALT__(self):
		print(bold_text(apply_color(208, f"START OF INSTRUCTION COUNT ---> {self._instruction_counter}")))
		_instr_msg = f"PERFORMING '{SimpleLangParserInstruction.INSTR(int_val=1)}' INSTRUCTION..."
		print(underline_text(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.HALT], _instr_msg))), end="\n\n")
		self.__CLEANUP__()
		print()
		self.halt()
		print(bold_text(apply_color(160, f"HALTING PARSER...")))
		print()
		print(bold_text(apply_color(208, f"END OF INSTRUCTION COUNT ---> {self._instruction_counter}")), end="\n\n")
		print(apply_color(190, f" ----- ================================================== "))
		self._instruction_counter += 1

	def __CLEANUP__(self):
		print(bold_text(apply_color(208, f"START OF INSTRUCTION COUNT ---> {self._instruction_counter}")))
		_instr_msg = f"CLEANING UP PARSE RUNTIME..."
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.CLEANUP], _instr_msg)), end="\n")
		_setting_res_msg = f"SETTING RESULT..."
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.CLEANUP], _setting_res_msg)), end="\n\n")
		if self._valid_parse >= 1:
			self.set_result(True)
		else:
			self.set_result(False)
		print(apply_color(190, f" ----- ================================================== "))
		print()
		self._instruction_counter += 1


"""
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
"""


if __name__ == "__main__":
	pass
