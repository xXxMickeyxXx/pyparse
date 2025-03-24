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
	# Shift/reduce parser instructions
	HALT = auto()
	INIT = auto()
	SHIFT = auto()
	REDUCE = auto()
	ACCEPT = auto()
	ERROR = auto()

	# Test instructions
	PRINT = auto()
	ADD_OP = auto()
	SUB_OP = auto()
	CLEANUP = auto()
	CALC_STATE = auto()

	# Test mainloop instruction
	MAIN_LOOP = auto()

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
	# S = "S"
	# A = "A"
	# C = "C"
	# B = "B"
	# a = "a"
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


"""class PyParser:

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
		return self._result"""


class PyParser:

	__slots__ = ("_executor", "_parser_id", "_args", "_context", "_result", "_result_set", "_quit_flag")

	def __init__(self, executor, parser_id=None):
		self._parser_id = parser_id or generate_id()
		self._executor = executor
		self._context = None
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
	def context(self):
		return self._context

	@property
	def state(self):
		return self._state

	@property
	def result_set(self):
		return self._result_set

	@property
	def result(self):
		if not self._result_set:
			_error_details = f"unable to access parse 'result' as one has not yet been set..."
			raise RuntimeError(_error_details)
		return self._result

	def set_result(self, result):
		self._result = result
		self._result_set = True

	def set_context(self, context):
		self._context = context

	def add_handler(self, instruction_type, handler):
		self._handlers[instruction_type] = handler
	
	def halt(self):
		self._quit_flag = True

	# def parse(self, context):
	# 	self.set_context(context)
	# 	self._quit_flag = False
	# 	while self._instructions and (not self._quit_flag):
	# 		_handler = self.next_handler(default=None)
	# 		if _handler is None:
	# 			# @TODO<Create and raise custom error here>
	# 			_error_details = f"unable to find supported handler for NEXT INSTRUCTION TYPE: '{self.curr_instruction}'...exiting with runtime-error..."
	# 			raise RuntimeError(_error_details)
	# 		_args, _kwargs = self._args
	# 		_handler(*_args, **_kwargs)
	# 	return self._result

	def parse(self, context):
		self._quit_flag = False
		self.set_context(context)
		return self._executor(self)


class SimpleLangParser(PyParser):

	def __init__(self, executor=None, delim="\n", init_state=0, invalid_instruction=SimpleLangParserInstruction.HALT, parser_id=None):
		super().__init__(executor or self.__EXECUTOR__, parser_id=parser_id)
		self._init_state = init_state
		self._handlers = {}
		self._instructions = deque()
		self._curr_instruction = None
		self._args = ((), {})
		self._invalid_instr = invalid_instruction

		self._delim = delim
		self._state = (None, None)
		self._state_stack = []
		self._symbol_stack = []
		self._instr_counter = 1
		self.init()

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
	def state(self):
		return self._state

	@staticmethod
	def __EXECUTOR__(parser):
		while parser.instructions and (parser.is_running):
			_handler = parser.next_handler(default=None)
			if _handler is None:
				# @TODO<Create and raise custom error here>
				_error_details = f"unable to find supported handler for NEXT INSTRUCTION TYPE: '{parser.curr_instruction}'...exiting with runtime-error..."
				raise RuntimeError(_error_details)
			_args, _kwargs = parser.curr_args
			_handler(*_args, **_kwargs)
		return parser.result

	def set_state(self, state):
		self._state = state

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

	def init(self):
		self.init_parse_table()

		# Add instruction handler(s)
		self.add_handler(SimpleLangParserInstruction.HALT, self.__HALT__)
		self.add_handler(SimpleLangParserInstruction.INIT, self.__INIT__)
		self.add_handler(SimpleLangParserInstruction.MAIN_LOOP, self.__MAIN_LOOP__)
		self.add_handler(SimpleLangParserInstruction.SHIFT, self.__SHIFT__)
		self.add_handler(SimpleLangParserInstruction.REDUCE, self.__REDUCE__)
		self.add_handler(SimpleLangParserInstruction.CALC_STATE, self.calculate_state)


		# Add initial instruction(s)
		self.add_instruction(SimpleLangParserInstruction.INIT)

		_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.INIT)}' INSTRUCTION --- •]"
		print(bold_text(apply_color(211, _msg)), end="\n")

	def init_parse_table(self):
		pass

	def calculate_state(self, symbol=None):
		self._state = (self._state_stack[-1], self._symbol_stack[-1] if symbol is None else symbol)

	def peek(self, offset=0):
		return self.context[offset]

	def __INIT__(self):
		# self.add_instruction(SimpleLangParserInstruction.HALT)  # @NOTE<Submit SimpleLangParserInstruction.HALT instruction to quickly halt the
		# 																  parser -- for use halting parser after it runs testing instructions, such
		# 																  as parser initialization via the SimpleLangParserInstruction.INIT>
		print()
		print(f"    |" + underline_text(bold_text(apply_color(214, f"CURRENT INSTRUCTION"))) + bold_text(apply_color(168, f" • --- • {SimpleLangParserInstruction.INSTR(int_val=self.curr_instruction)} <iCOUNT: {self._instr_counter}>")))
		print()

		_state_int = self._init_state
		_type_ = self.context[0].token_type
		_print_text = f"\t   |\n"
		_print_text += f"\t   |\n"
		_print_text += f"\t   |\n"
		_print_text += f"\t    • ---> "
		_print_text += apply_color(226, underline_text("ESTABLISHING PARSERS INITAL STATE") + "...\n\n")
		_print_text += apply_color(226, f"\tSTATE #        •---> {_state_int}\n")
		_print_text += apply_color(226, f"\tNEXT TOKEN     •---> {_type_}\n")
		print(_print_text)
		self._state_stack.append(self._init_state)
		self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=self.peek(offset=0))
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1

	def __SHIFT__(self, state_int):
		_next_token = self.context.pop(0)
		_next_token_type = _next_token.token_type
		self._state_stack.append(state_int)
		self._symbol_stack.append(_next_token_type)
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)

	def __REDUCE__(self, rule_head, pop_count, goto):
		for _ in range(pop_count):
			_sym_pop = self._symbol_stack.pop(-1)
			_state_pop = self._state_stack.pop(-1)
		self._symbol_stack.append(rule_head)
		self._state_stack.append(goto)
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)

	def __MAIN_LOOP__(self):
		print()
		print(f"    |" + underline_text(bold_text(apply_color(214, f"CURRENT INSTRUCTION"))) + bold_text(apply_color(168, f" • --- • {SimpleLangParserInstruction.INSTR(int_val=self.curr_instruction)} <iCOUNT: {self._instr_counter}>")))
		print()
		_state_int = self.state[0]
		_type_ = self.peek(0).token_type
		# _print_text = apply_color(226, f"\tSTATE #        •---> {_state_int}\n")
		# _print_text += apply_color(226, f"\tNEXT TOKEN     •---> {_type_}\n")

		print()
		print(f"\t• STATE STACK  ---> {self._state_stack}")
		print(f"\t• SYMBOL STACK ---> {self._symbol_stack}")
		print(f"\t• NEXT:\n             |\n             • {self.peek(offset=0)}\n             |\n             • {_type_}")
		print()

		match _state_int:
			case None:
				self.__SHIFT__(self._init_state)
			case 0:
				match _type_:
					case SimpleLangTokenType.NUMBER:
						self.add_instruction(SimpleLangParserInstruction.SHIFT, 6)
						self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
					case _:
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
			case 4:
				match _type_:
					case "C":
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
						# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.HALT)}' INSTRUCTION --- •]"
						# print(bold_text(apply_color(211, _msg)), end="\n")
					case _:
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
						# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.HALT)}' INSTRUCTION --- •]"
						# print(bold_text(apply_color(211, _msg)), end="\n")
			case 6:
				if len(self._symbol_stack) == 3 and self._symbol_stack[-1] == SimpleLangTokenType.NUMBER:
					self.add_instruction(SimpleLangParserInstruction.REDUCE, "C", 1, 10)
					# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.REDUCE)}' INSTRUCTION --- •]"
					# print(bold_text(apply_color(211, _msg)), end="\n")

					self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
					# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.CALC_STATE)}' INSTRUCTION --- •]"
					# print(bold_text(apply_color(211, _msg)), end="\n")
				else:
					match _type_:
						case SimpleLangTokenType.DELIM:
							self.add_instruction(SimpleLangParserInstruction.REDUCE, "C", 1, 8)
							# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.REDUCE)}' INSTRUCTION --- •]"
							# print(bold_text(apply_color(211, _msg)), end="\n")

							self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
							# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.CALC_STATE)}' INSTRUCTION --- •]"
							# print(bold_text(apply_color(211, _msg)), end="\n")
						case _:
							self.set_result(False)
							self.add_instruction(SimpleLangParserInstruction.HALT)
							# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.HALT)}' INSTRUCTION --- •]"
							# print(bold_text(apply_color(211, _msg)), end="\n")
			case 7:
				match _type_:
					case SimpleLangTokenType.NUMBER:
						self.add_instruction(SimpleLangParserInstruction.SHIFT, 6)
						# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.SHIFT)}' INSTRUCTION --- •]"
						# print(bold_text(apply_color(211, _msg)), end="\n")

						self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
						# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.CALC_STATE)}' INSTRUCTION --- •]"
						# print(bold_text(apply_color(211, _msg)), end="\n")
					case _:
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
						# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.HALT)}' INSTRUCTION --- •]"
						# print(bold_text(apply_color(211, _msg)), end="\n")
			case 8:
				match _type_:
					case SimpleLangTokenType.DELIM:
						self.add_instruction(SimpleLangParserInstruction.SHIFT, 7)
						# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.SHIFT)}' INSTRUCTION --- •]"
						# print(bold_text(apply_color(211, _msg)), end="\n")

						self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
						# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.CALC_STATE)}' INSTRUCTION --- •]"
						# print(bold_text(apply_color(211, _msg)), end="\n")
					case _:						
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
						# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.HALT)}' INSTRUCTION --- •]"
						# print(bold_text(apply_color(211, _msg)), end="\n")
			case 10:
				if ("C", SimpleLangTokenType.DELIM, "C") == tuple(self._symbol_stack):
					self.add_instruction(SimpleLangParserInstruction.REDUCE, "B", 3, 3)
					# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.REDUCE)}' INSTRUCTION --- •]"
					# print(bold_text(apply_color(211, _msg)), end="\n")

					self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
					# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.CALC_STATE)}' INSTRUCTION --- •]"
					# print(bold_text(apply_color(211, _msg)), end="\n")

					print(bold_text(apply_color(9, f"HEEEY MUST BE THE MONAYYY!")))
					# self.set_result(False)
					# self.add_instruction(SimpleLangParserInstruction.HALT)
			case _:
				self.set_result(False)
				self.add_instruction(SimpleLangParserInstruction.HALT)
				# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.HALT)}' INSTRUCTION --- •]"
				# print(bold_text(apply_color(211, _msg)), end="\n")
		self._instr_counter += 1

	def __HALT__(self):
		# print(f"STATE ---> {self.state}")
		if self.state == (0, SimpleLangTokenType.NUMBER):
			self.set_result(True)
		self.halt()


"""class SimpleLangParser(PyParser):

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
			#	'PRINT' (INSTR #: 7),
			#	'ADD_OP' (INSTR #: 8),
			#	'SUB_OP' (INSTR #: 9),
			# 	'CLEANUP' (INSTR #: 10>
		self.add_handler(SimpleLangParserInstruction.INSTR(int_val=1), self.__HALT__)
		self.add_handler(SimpleLangParserInstruction.HALT, self.__HALT__)
		self.add_handler(SimpleLangParserInstruction.PRINT, self.__PRINT__)
		self.add_handler(SimpleLangParserInstruction.ADD_OP, self._ADD_)
		self.add_handler(SimpleLangParserInstruction.SUB_OP, self._SUB_)
		self.add_handler(SimpleLangParserInstruction.CLEANUP, self.__CLEANUP__)
		
		# @NOTE<Test instructions to run first, upon calling of 'parse' runner method>
		self.add_instruction(SimpleLangParserInstruction.ADD_OP, randrange(100), randrange(100))
		self.add_instruction(SimpleLangParserInstruction.ADD_OP, randrange(100), randrange(100))
		_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=8)}' INSTRUCTION --- •]"
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.ADD_OP], _msg)), end="\n")
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.ADD_OP], _msg)), end="\n\n")

	def _ADD_(self, x: int, y: int) -> None:
		print(bold_text(apply_color(208, f"START OF INSTRUCTION COUNT ---> {self._instruction_counter}")))
		_instr_msg = f"PERFORMING '{SimpleLangParserInstruction.INSTR(int_val=8)}' INSTRUCTION..."
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.ADD_OP], _instr_msg)), end="\n\n")
		_result = x + y
		print(f"{x} + {y} = {_result}")
		print(f"RESULT ---> {_result}")
		if _result >= 25:
			self.add_instruction(SimpleLangParserInstruction.SUB_OP, randrange(100), randrange(100))
			print()
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=9)}' INSTRUCTION --- •]"
			print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.SUB_OP], _msg)), end="\n\n")
		else:
			self.add_instruction(SimpleLangParserInstruction.SUB_OP, randrange(100), randrange(100))
			print()
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=9)}' INSTRUCTION --- •]"
			print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.SUB_OP], _msg)), end="\n\n")
		print(bold_text(apply_color(208, f"END OF INSTRUCTION COUNT ---> {self._instruction_counter}")), end="\n\n")
		print(apply_color(190, f" ----- ================================================== "))
		print()
		self._instruction_counter += 1

	def _SUB_(self, x: int, y:int) -> None:
		print(bold_text(apply_color(208, f"START OF INSTRUCTION COUNT ---> {self._instruction_counter}")))
		_instr_msg = f"PERFORMING '{SimpleLangParserInstruction.INSTR(int_val=9)}' INSTRUCTION..."
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.SUB_OP], _instr_msg)), end="\n\n")
		_result = x - y
		self.add_instruction(SimpleLangParserInstruction.PRINT, f"{x} - {y} = {_result}")
		if _result < 7:
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=7)}' INSTRUCTION --- •]"
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
		_instr_msg = f"PERFORMING '{SimpleLangParserInstruction.INSTR(int_val=7)}' INSTRUCTION..."
		print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.PRINT], _instr_msg)), end="\n\n")
		print(*args, **kwargs)
		print()
		if self._random_val >= 10:
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=8)}' INSTRUCTION --- •]"
			print(bold_text(apply_color(self._instr_color_map[SimpleLangParserInstruction.ADD_OP], _msg)), end="\n\n")
			self.add_instruction(SimpleLangParserInstruction.ADD_OP, randrange(1000), randrange(1000))
			self._random_val -= 1
		else:
			_PRINT_CONCAT = underline_text(bold_text(apply_color(randrange(256), "YOU STUPID SON OF A BITCH!")))
			self.add_instruction(SimpleLangParserInstruction.PRINT, _PRINT_CONCAT, end="\n")
			_msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=7)}' INSTRUCTION --- •]"
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
		self._instruction_counter += 1"""


if __name__ == "__main__":
	pass
