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
from .scratch_parse_table import ParseTable
from .scratch_utils import generate_id
from .utils import (
	bold_text,
	apply_color,
	underline_text,
	center_text
)
from .scratch_cons import (
	LanguageType,
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
	CONFLICT = auto()

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
						_add_token_alias(SimpleLangTokenType.SKIP, "", token_id=f"NEWLINE_DLIM_{_counter}")
						_tokenizer_advance()
					case "\t":
						_add_token_alias(SimpleLangTokenType.SKIP, "", token_id=f"TAB_DLIM_	{_counter}")
						_tokenizer_advance()
					case ",":
						_add_token_alias(SimpleLangTokenType.DELIM, ",", token_id=f"COMMA_DLIM_{_counter}")
						_tokenizer_advance()
					case _:
						_add_token_alias(SimpleLangTokenType.SKIP, _current_char, token_id=f"SKIP_{_counter}")
						_tokenizer_advance()
			_counter += 1
		_add_token_alias(SimpleLangTokenType.END_SYMBOL, "#", token_id="END_SYMBOL")


class SimpleLangTableBuilder(TableBuilder):

	def build_table(self, table):
		pass


class SimpleLangParseTable(ParseTable):

	def __init__(self):
		super().__init__(table_id=LanguageType.SIMPLE_LANG)
		self.add_action((0, SimpleLangTokenType.NUMBER), (SimpleLangParserInstruction.SHIFT, 5))
		self.add_action((0, SimpleLangTokenType.DELIM), (SimpleLangParserInstruction.ERROR, None))
		

		self.add_action((1, SimpleLangTokenType.END_SYMBOL), (SimpleLangParserInstruction.REDUCE, "A", 1, 3))
		

		self.add_action((2, SimpleLangTokenType.DELIM), (SimpleLangParserInstruction.CONFLICT, (7, ("C", 3, 2))))
		self.add_action((2, SimpleLangTokenType.END_SYMBOL), (SimpleLangParserInstruction.REDUCE, "B", 3, 1))


		self.add_action((3, SimpleLangTokenType.END_SYMBOL), (SimpleLangParserInstruction.REDUCE, "S", 1, 4))
		

		self.add_action((4, SimpleLangTokenType.END_SYMBOL), (SimpleLangParserInstruction.ACCEPT, None))


		self.add_action((5, SimpleLangTokenType.DELIM), (SimpleLangParserInstruction.REDUCE, "C", 1, 2))
		self.add_action((5, SimpleLangTokenType.NUMBER), (SimpleLangParserInstruction.REDUCE, "C", 1, 2))
		self.add_action((5, SimpleLangTokenType.END_SYMBOL), (SimpleLangParserInstruction.REDUCE, "C", 1, 2))
		

		self.add_action((6, SimpleLangTokenType.NUMBER), (SimpleLangParserInstruction.REDUCE, "B", 2, 8))


		self.add_action((7, SimpleLangTokenType.NUMBER), (SimpleLangParserInstruction.SHIFT, 5))
		

		self.add_action((8, SimpleLangTokenType.DELIM), (SimpleLangParserInstruction.SHIFT, 6))


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

	def parse(self, context):
		self._quit_flag = False
		self.set_context(context)
		return self._executor(self)


class SimpleLangParser(PyParser):

	def __init__(self, executor=None, delim=",", init_state=0, invalid_instruction=SimpleLangParserInstruction.HALT, parser_id=None):
		super().__init__(executor or self.__EXECUTOR__, parser_id=parser_id)
		self._init_state = init_state
		self._handlers = {}
		self._instructions = deque()
		self._curr_instruction = None
		self._args = ((), {})
		self._invalid_instr = invalid_instruction

		self._parse_table = SimpleLangParseTable()
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
	def instr_count(self):
		return self._instr_counter

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

	@property
	def parse_table(self):
		return self._parse_table

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
		self.add_handler(SimpleLangParserInstruction.ERROR, self.__ERROR__)
		self.add_handler(SimpleLangParserInstruction.SHIFT, self.__SHIFT__)
		self.add_handler(SimpleLangParserInstruction.REDUCE, self.__REDUCE__)
		self.add_handler(SimpleLangParserInstruction.CALC_STATE, self.calculate_state)
		self.add_handler(SimpleLangParserInstruction.PRINT, self.__PRINT__)
		self.add_handler(SimpleLangParserInstruction.CONFLICT, self.__CONFLICT__)

		# Add initial instruction(s)
		self.add_instruction(SimpleLangParserInstruction.INIT)

		# _msg = f"\t[• --- NEW '{SimpleLangParserInstruction.INSTR(int_val=SimpleLangParserInstruction.INIT)}' INSTRUCTION --- •]"
		# print(bold_text(apply_color(211, _msg)), end="\n")

	def init_parse_table(self):
		pass

	def calculate_state(self, symbol=None):
		self._state = (self._state_stack[-1], self._symbol_stack[-1] if symbol is None else symbol)

	def peek(self, offset=0):
		return self.context[offset]

	def __ERROR__(self, *args, **kwargs):
		raise RuntimeError(*args, **kwargs)

	def __PRINT__(self, *args, **kwargs):
		print(*args, **kwargs)
		self._instr_counter += 1

	def __INIT__(self):
		# print()
		# print(f"    |" + underline_text(bold_text(apply_color(214, f"CURRENT INSTRUCTION"))) + bold_text(apply_color(168, f" • --- • {SimpleLangParserInstruction.INSTR(int_val=self.curr_instruction)} <iCOUNT: {self.instr_count}>")))
		# print()

		_state_int = self._init_state
		_type_ = self.context[0].token_type
		# _print_text = f"\t   |\n"
		# _print_text += f"\t   |\n"
		# _print_text += f"\t   |\n"
		# _print_text += f"\t    • ---> "
		# _print_text += apply_color(226, underline_text("ESTABLISHING PARSERS INITAL STATE") + "...\n\n")
		# _print_text += apply_color(226, f"\tSTATE #        •---> {_state_int}\n")
		# _print_text += apply_color(226, f"\tNEXT TOKEN     •---> {_type_}\n")
		# print(_print_text)
		self._state_stack.append(self._init_state)
		self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=self.peek(offset=0))
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1

	def __CONFLICT__(self, logic):
		# print(f"SHIFT LOGIC   ---> {logic[0]}")
		# print(f"REDUCE LOGIC  ---> {logic[1]}")
		if len(self._symbol_stack) <= 1 and self._symbol_stack[-1] == "C":
			self.add_instruction(SimpleLangParserInstruction.SHIFT, logic[0])
		elif len(self._symbol_stack) >= 3:
			self.add_instruction(SimpleLangParserInstruction.REDUCE, *logic[1])
		
	def __SHIFT__(self, state_int):
		_next_token = self.context.pop(0)
		_next_token_type = _next_token.token_type
		self._state_stack.append(state_int)
		self._symbol_stack.append(_next_token_type)
		self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1

	def __REDUCE__(self, rule_head, pop_count, goto):
		for _ in range(pop_count):
			_sym_pop = self._symbol_stack.pop(-1)
			_state_pop = self._state_stack.pop(-1)
			# print(f"\nPOPPING SYMBOL  ---> '{_sym_pop}' FROM SYMBOL STACK")
			# print(f"POPPING STATE   ---> '{_state_pop}' FROM STATE STACK\n")
		self._symbol_stack.append(rule_head)
		self._state_stack.append(goto)
		self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1

	def __MAIN_LOOP__(self):
		# print()
		# print(f"    |" + underline_text(bold_text(apply_color(214, f"CURRENT INSTRUCTION"))) + bold_text(apply_color(168, f" • --- • {SimpleLangParserInstruction.INSTR(int_val=self.curr_instruction)} <iCOUNT: {self.instr_count}>")))
		# print()
		_state_int = self.state[0]
		_type_ = self.peek(0).token_type

		# print()
		# print(f"\t• STATE STACK  ---> {self._state_stack}")
		# print(f"\t• SYMBOL STACK ---> {self._symbol_stack}")
		# print(f"\t• NEXT:\n             |\n             • {self.peek(offset=0)}\n             |\n             • {_type_}")

		# _action, *args = self.parse_table.action((_state_int, _type_), default=(SimpleLangParserInstruction.ERROR, None))
		# print()
		# print(f"\t• ACTION ---> {SimpleLangParserInstruction.INSTR(int_val=_action)}")
		# print(f"\t• ARGS   ---> {args}")
		# print()

		# match _action:
		# 	case SimpleLangParserInstruction.SHIFT:
		# 		self.add_instruction(SimpleLangParserInstruction.SHIFT, *args)
		# 	case SimpleLangParserInstruction.REDUCE:
		# 		self.add_instruction(SimpleLangParserInstruction.REDUCE, *args)
		# 	case SimpleLangParserInstruction.CONFLICT:
		# 		self.add_instruction(SimpleLangParserInstruction.CONFLICT, *args)
		# 	case SimpleLangParserInstruction.ERROR:
		# 		self.set_result(False)
		# 		self.add_instruction(SimpleLangParserInstruction.HALT)
		# 	case SimpleLangParserInstruction.ACCEPT:
		# 		self.set_result(True)
		# 		self.add_instruction(SimpleLangParserInstruction.HALT)
		# 	case _:
		# 		self.set_result(False)
		# 		self.add_instruction(SimpleLangParserInstruction.HALT)

		match _state_int:
			case None:
				self.__SHIFT__(self._init_state)
			case 0:
				match _type_:
					case SimpleLangTokenType.NUMBER:
						self.add_instruction(SimpleLangParserInstruction.SHIFT, 2)
					case _:
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
			case 1:
				match _type_:
					case SimpleLangTokenType.END_SYMBOL:
						self.set_result(True)
						self.add_instruction(SimpleLangParserInstruction.HALT)
			case 2:					
				match _type_:
					case SimpleLangTokenType.DELIM:
						self.add_instruction(SimpleLangParserInstruction.REDUCE, "C", 1, 3)
					case SimpleLangTokenType.END_SYMBOL:
						self.add_instruction(SimpleLangParserInstruction.REDUCE, "C", 1, 3)
					case _:
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
			case 3:
				match _type_:
					case SimpleLangTokenType.DELIM:
						if tuple(self._symbol_stack) == ("C", SimpleLangTokenType.DELIM, "C"):
							self.add_instruction(SimpleLangParserInstruction.REDUCE, "C", 3, 3)
						else:
							self.add_instruction(SimpleLangParserInstruction.SHIFT, 5)
					case SimpleLangTokenType.END_SYMBOL:
						self.add_instruction(SimpleLangParserInstruction.REDUCE, "B", 3, 4)
					case _:
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
			case 4:
				match _type_:
					case SimpleLangTokenType.END_SYMBOL:
						if self._symbol_stack[-1] and self._symbol_stack[-1] == "B":
							self.add_instruction(SimpleLangParserInstruction.REDUCE, "S", 1, 1)
						else:
							self.set_result(False)
							self.add_instruction(SimpleLangParserInstruction.HALT)
					case _:
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
			case 5:
				match _type_:
					case SimpleLangTokenType.NUMBER:
						self.add_instruction(SimpleLangParserInstruction.SHIFT, 2)
					case SimpleLangTokenType.END_SYMBOL:
						self.add_instruction(SimpleLangParserInstruction.REDUCE, "S", 2, 1)
					case _:
						self.set_result(False)
						self.add_instruction(SimpleLangParserInstruction.HALT)
			case _:
				self.set_result(False)
				self.add_instruction(SimpleLangParserInstruction.HALT)
		self._instr_counter += 1

	def __HALT__(self):
		if self.state == (0, SimpleLangTokenType.NUMBER):
			self.set_result(True)
		self.halt()
		self._instr_counter += 1


if __name__ == "__main__":
	from pyevent import PyChannel


	class MaybeParserImp:
		
		__slots__ = ("_parser_id", "_channel", "_state", "_quit_flag")

		def __init__(self, init_state=0, parser_id=None):
			self._parser_id = parser_id or generate_id()
			self._channel = PyChannel(channel_id=self._parser_id)
			self._state = init_state
			self._quit_flag = True

		@property
		def parser_id(self):
			return self._parser_id

		@property
		def state(self):
			return self._state

		@property
		def is_running(self):
			return not self._quit_flag

		def __str__(self):
			return self.__repr__()

		def __repr__(self):
			return f"{self.__class__.__name__}(parser_id='{self.parser_id}')"

		def set_state(self, state):
			self._state = state

		def halt(self):
			self._quit_flag =True

		def signal(self, signal_id=None):
			return self._channel.signal(signal_id=signal_id)

		def register(self, signal_id, receiver=None, receiver_id=None):
			self._channel.register(signal_id, receiver=receiver, receiver_id=receiver_id)

		def parse(self, context):
			self._quit_flag = False
			while not self._quit_flag:
				self._channel.emit(self.state, self)
			assert self._quit_flag, f"ERROR HAS OCCURRED ASSERTING '_quit_flag'; please verify logic in 'parse' method within instance of '{self.__class_.__name__}'..."


	class TestParserImp(MaybeParserImp):
		
		def __init__(self):
			super().__init__(init_state=0, parser_id="HOPEFULLY_THIS_PARSER_DESIGN_STICKS")


	def test_parser_runner(input):
		return test_parser.parse(input)

	def test_parser_state_registration(test_parser):
		test_parser.register(0, receiver=lambda _parser_: _parser_.set_state(1), receiver_id=1)
		test_parser.register(1, receiver=lambda _parser_: print(f"\n{_parser_}"), receiver_id=2)
		test_parser.register(1, receiver=lambda _parser_: _parser_.set_state(2), receiver_id=3)
		test_parser.register(2, receiver=lambda _parser_: _parser_.set_state((3, "A")), receiver_id=4)
		test_parser.register(2, receiver=lambda _parser_: print(f"I'M DONE FOR RIGHT NOW (as of 5:27pm, Sunday, March 30th, 2025...until next time...)"), receiver_id=5)
		test_parser.register((3, "A"), receiver=lambda _parser_: _parser_.halt(), receiver_id=5)
		test_parser.register((3, "A"), receiver=lambda _parser_: print(f"WELL HOW BOUT THAT NOW..."), receiver_id=6)


	def test_parser_factory(*args, **kwargs):
		return TestParserImp(*args, **kwargs)


	def test_parser_main():
		# @NOTE<Initialize test parser implementation>
		_test_parser_imp = test_parser_factory()

		# @NOTE<Register implementation's state handling>
		test_parser_state_registration(_test_parser_imp)

		# @NOTE<Run test parser implementation with '__TEST_INPUT__'>
		__TEST_INPUT__ = ["HELLO", "MOTO"]
		_valid_parse = _test_parser_imp.parse(__TEST_INPUT__)
