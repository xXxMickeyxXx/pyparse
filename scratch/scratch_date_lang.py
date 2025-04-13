from typing import (
	Union,
	Callable
)
from collections import deque
from abc import ABC, abstractmethod
from enum import StrEnum, IntEnum, auto

from pylog import PyLogger, LogType
from pyutils import (
    cmd_argument,
    DEFAULT_PARSER as DEFAULT_CMD_LINE_PARSER
)
from pyparse import Tokenizer, Scanner, LexHandler, Token

from .scratch_utils import generate_id
from .scratch_cons import (
	LanguageType,
	DateLangVersion
)
from .utils import (
	apply_color,
	bold_text,
	underline_text,
	center_text
)
from .scratch_shell_init import initialize_shell


_date_lang_logger = PyLogger(logger_id=f"{LanguageType.DATE_LANG}{DateLangVersion.V0_0_1}")


class DateFormat(StrEnum):

	YYYY = "YYYY"
	YY = "YY"
	MM = "MM"
	M = "M"
	DD = "DD"
	D = "D"


class DateLangTokenizerMode(IntEnum):

	DEFAULT = auto()


class DateLangParserInstruction(IntEnum):
	"""
		 _____________________
	    |          			  |
	    •__INSTRUCTION ENUMS__•

			HALT (int: 1)
			INIT (int: 2)
			SHIFT (int: 3)
			REDUCE (int: 4)
			ACCEPT (int: 5)
			ERROR (int: 6)
			PRINT (int: 7)
			CLEANUP (int: 8)
			CALC_STATE (int: 9)
			MAIN_LOOP (int: 10)

	"""

	# @NOTE<Shift/reduce parser instructions>
	HALT = auto()
	INIT = auto()
	SHIFT = auto()
	REDUCE = auto()
	ACCEPT = auto()
	ERROR = auto()
	# CONFLICT = auto()  # @NOTE<Potentially add new CONFLICT enumss so it may be good to remove this
					     #       generalized one to give space to the specific ones>

	# @NOTE<MISC parser instructions>
	PRINT = auto()
	CLEANUP = auto()
	CALC_STATE = auto()

	# @NOTE<Parser mainloop instruction>
	MAIN_LOOP = auto()


class DateLangTokenType(StrEnum):

	# @NOTE<'DateLang' token types>
	DELIM = "DELIM"
	YEAR = "YEAR"
	MONTH = "MONTH"
	DAY = "DAY"


	# @NOTE<Basic token types>
	INVALID = "INVALID"
	SKIP = ""
	END_SYMBOL = "END_SYMBOL"


class DateLangToken(Token):

		def __init__(self, token_type, token_val, token_id=None):
			super().__init__(token_type, token_val, token_id=token_id)


class TokenizerContext(ABC):
	
	def __init__(self):
		pass


class TokenizerStateInstance(ABC):
	
	def __init__(self):
		pass


class TokenizerState(ABC):
	
	def __init__(self):
		pass


class Tokenizer(ABC):

	__slots__ = ("_tokenizer_id", "_scanner", "_tokens")

	def __init__(self, tokenizer_id=None):
		self._tokenizer_id = tokenizer_id or generate_id()
		self._scanner = Scanner(scanner_id=self.tokenizer_id)
		self._tokens = []

	@property
	def tokenizer_id(self):
		return self._tokenizer_id

	@property
	def scanner(self):
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
		return self.scanner.input

	def set_input(self, input):
		self.scanner.set_input(input)

	def reset(self):
		self.scanner.reset()
		return self.flush_tokens()

	def peek(self, offset=1):
		return self.scanner.peek(offset=offset)

	def peek_range(self, offset=0, step=1):
		return self.scanner.peek_range(offset=offset, step=step)

	def advance(self):
		return self.scanner.advance()

	def consume(self):
		return self.scanner.consume()

	def cond_consume(self, condition):
		return self.scanner.cond_consume(condition)

	def expect(self, value):
		return self.scanner.expect(value)

	def expect_at(self, value, offset=0):
		return self.scanner.expect_at(value, offset=offset)

	def input_at(self, index):
		return self.scanner.input_at(index)

	def input_range(self, *slice_args):
		return self.scanner.input_range(*slice_args)

	def add_token(self, token):
		self._tokens.append(token)

	def pop_token(self, offset=-1):
		if not self._tokens or len(self._tokens) <= 0:
			# TODO: create and raise custom error here
			_error_details = f"unable to 'pop' token from token container as it's currently empty..."
			raise IndexError(_error_details)
		return self._tokens.pop(idx)

	def token_at(self, offset=0):
		if index >= len(self._tokens):
			# TODO: create and raise custom error here
			_error_details = f"unable to access token at index: {index} as it exceeds token container bounds..."
			raise IndexError(_error_details)
		return self._tokens[index]

	def token_range(self, *slice_args):
		_slicer = slice(*slice_args)
		return self._tokens[_slicer]

	def flush_tokens(self):
		_retval = list(self._tokens)
		self._tokens.clear()
		assert not self._tokens, "an error occured when attempting to flush token buffer; please review and try again..."
		return _retval

	@abstractmethod
	def tokenize(self):
		raise NotImplementedError


class DateLangTokenizer:

	# @NOTE<Abstract out the attributes/properties/methods that define the 'Tokenizer',
	#       makign sure to leave methods specific to this tokenizer type (i.e. it
	# 		being the tokenizer class used for tokenizing a date input)>

	__slots__ = ("_tokenizer_id", "_format", "_input")

	def __init__(self, format=None, tokenizer_id=None):
		self._tokenizer_id = tokenizer_id or generate_id()  # @NOTE<move to 'Tokenizer' interface>
		self._format = format or f"{DateFormat.YYYY}-{DateFormat.MM}-{DateFormat.DD}"
		self._input = None
		self._format_pointer = 0

	@property
	def tokenizer_id(self):
		# @NOTE<Probably needs to ultimately be added to the 'Tokenizer' interface>
		return self._tokenizer_id

	@property
	def input(self):
		# @NOTE<Probably needs to ultimately be added to the 'Tokenizer' interface>
		if not bool(self._input):
		# @NOTE<Create and raise custom error here>
			_error_details = f"unable to access 'input' property as an input has not yet been set for this instance of '{self.__class__.__name__}'..."
			raise RuntimeError(_error_details)
		return self._input

	@property
	def format(self):
		# @NOTE<Probably needs to ultimately be added to the 'Tokenizer' interface>
		return self._format

	def set_input(self, input):
		# @NOTE<Probably needs to ultimately be added to the 'Tokenizer' interface>
		self._input = input

	def set_format(self, format):
		# @NOTE<Probably needs to ultimately be added to the 'Tokenizer' interface>
		self._format = format

	def tokenize(self):
		_format = self.format

		_format_pointer = 0
		_format_len = len(_format)
		while _format_pointer < _format_len:
			_current_format_sym = _format[_format_pointer]

			match _current_format_sym:
				case _:
					_error_details = f"an error has occurred within 'tokenize' method of instance of '{self.__class__.__name__}'...please review and try again..."
					raise RuntimeError(_error_details)

		_END_OF_INPUT = DateLangToken(DateLangTokenType.END_SYMBOL, "#", token_id=DateLangTokenType.END_SYMBOL)

	def _handler_year(self):
		pass


class PyParser:

	__slots__ = ("_executor", "_parser_id", "_state", "_args", "_context", "_result", "_result_set", "_quit_flag")

	def __init__(self, executor, init_state=0, parser_id=None):
		self._parser_id = parser_id or generate_id()
		self._executor = executor
		self._state = init_state
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

	def set_state(self, state):
		self._state = state

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
		# @NOTE<Perhaps add an assertion here to ensure parser has completed according
		#       to the qut flag and hopefully by extension it's set during parser
		#       runtime so something like the muted code below:
		# 
		# 
		# 			_parse_result = self._executor(self)
		# 			assert self._quit_flag, f"WARNING: something may have gone wrong here as the parser exited it's mainloop with a falsey quit flag value (int 0)"
		# 			return _parse_result>
		return self._executor(self)


class DateLangParser(PyParser):

	__slots__ = ("_handlers", "_instructions", "_curr_instruction", "_args", "_invalid_instr", "_state", "_state_stack", "_symbol_stack", "_instr_counter", "_logger")

	def __init__(self, executor=None, invalid_instruction=DateLangParserInstruction.HALT, logger=None):
		super().__init__(executor or self.__EXECUTOR__, init_state=0, parser_id=f"{LanguageType.DATE_LANG.lower()}_{DateLangVersion.V0_0_1}")
		self._handlers = {}
		self._instructions = deque()
		self._curr_instruction = None
		self._args = ((), {})
		self._invalid_instr = invalid_instruction

		self._state_stack = []
		self._symbol_stack = []
		self._instr_counter = 0
		self._logger = logger or _date_lang_logger
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
	def state_stack(self):
		return self._state_stack

	@property
	def symbol_stack(self):
		return self._symbol_stack

	@property
	def logger(self):
		return self._logger

	def peek(self, offset=0, default=None):
		try:
			return self.context[offset]
		except IndexError as _indx_err:
			return default
		finally:
			# @NOTE<Shouldn't reach here but just in case error isn't caught>
			return default

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
		# @NOTE<Setup instruction handlers>
		self.add_handler(DateLangParserInstruction.HALT, self.__HALT__)
		self.add_handler(DateLangParserInstruction.INIT, self.__INIT__)
		self.add_handler(DateLangParserInstruction.SHIFT, self.__SHIFT__)
		self.add_handler(DateLangParserInstruction.REDUCE, self.__REDUCE__)
		self.add_handler(DateLangParserInstruction.ACCEPT, self.__ACCEPT__)
		self.add_handler(DateLangParserInstruction.ERROR, self.__ERROR__)
		self.add_handler(DateLangParserInstruction.PRINT, self.__PRINT__)
		self.add_handler(DateLangParserInstruction.CLEANUP, self.__CLEAN_UP__)
		self.add_handler(DateLangParserInstruction.CALC_STATE, self.__CALC_STATE__)
		self.add_handler(DateLangParserInstruction.MAIN_LOOP, self.__MAIN_LOOP__)


		# @NOTE<Submit initial instruction(s)>
		self.add_instruction(DateLangParserInstruction.INIT)
		# self.add_instruction(DateLangParserInstruction.HALT)

	@staticmethod
	def __EXECUTOR__(parser):
		while parser.instructions and (parser.is_running):
			_instr_type, _args, _kwargs = parser.next_instruction(default=(parser.invalid_instruction, (), {}))  # @NOTE<'default' value of (None, (), {}) in order to allow tuple unpacking syntax, regardless if valid next instruction type (i.e. unsupportd)>
			_handler = parser._handlers.get(_instr_type, None)
			# @NOTE<Determine if should logic should dictate that it exit early, IF the
			# 		'_handler' evaluates to 'None', which would prevent the parser from
			# 		updating and setting the current instruction and args or just allow
			# 		it, even if no '_handler' is found (i.e. '_handler' evaluates to
			# 		'None')>
			if _handler is None:
				# @TODO<Create and raise custom error here>
				_error_details = f"unable to find supported handler for NEXT INSTRUCTION TYPE: '{parser.curr_instruction}'...exiting with runtime-error..."
				raise RuntimeError(_error_details)

			# @NOTE<set currently being executed instruction and set the 'args' and/or
			# 		'kwargs' for the specific handler. Even though this could be
			# 		skipped, setting them in the parser gives the ability to reference
			# 		the data associated with the currently executing instruction and
			# 		it's 'args' and/or 'kwargs'>
			parser.set_instruction(_instr_type)
			parser.send(*_args, **_kwargs)

			# _handler = parser.next_handler(default=None)
			# if _handler is None:
			# 	# @TODO<Create and raise custom error here>
			# 	_error_details = f"unable to find supported handler for NEXT INSTRUCTION TYPE: '{parser.curr_instruction}'...exiting with runtime-error..."
			# 	raise RuntimeError(_error_details)
			_args, _kwargs = parser.curr_args
			_handler(*_args, **_kwargs)
		return parser.result

	def __HALT__(self, condition=None):
		_condition_ = condition if isinstance(condition, Callable) else lambda: False
		self.set_result(_condition_())
		self.halt()
		self._instr_counter +=1

	def __INIT__(self):
		_state_int = self.state
		_type_ = self.context[0].token_type
		# _print_text = f"\t   |\n"
		# _print_text += f"\t   |\n"
		# _print_text += f"\t   |\n"
		# _print_text += f"\t    • ---> "
		# _print_text += apply_color(226, underline_text("ESTABLISHING PARSERS INITAL STATE") + "...\n\n")
		# _print_text += apply_color(226, f"\tSTATE #        •---> {_state_int}\n")
		# _print_text += apply_color(226, f"\tNEXT TOKEN     •---> {_type_}\n")
		# print(_print_text)
		self._state_stack.append(self.state)
		self.add_instruction(DateLangParserInstruction.CALC_STATE, _type_, state_int=_state_int)
		self.add_instruction(DateLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1

	def __SHIFT__(self, state_int, default=None):
		_next_token = self.context.pop(0)
		_next_token_type = _next_token.token_type
		self._state_stack.append(state_int)
		self._symbol_stack.append(_next_token_type)
		if not self.context:
			_token_type = default
		else:
			_token_type = self.context[0].token_type
		self.add_instruction(DateLangParserInstruction.CALC_STATE, _token_type, state_int=self._state_stack[-1])
		self.add_instruction(DateLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1

	def __REDUCE__(self, rule_head, pop_count, goto):
		for _ in range(pop_count):
			_sym_pop = self._symbol_stack.pop(-1)
			_state_pop = self._state_stack.pop(-1)
		self._symbol_stack.append(rule_head)
		self._state_stack.append(goto)
		if not self.context:
			_token_type = self._symbol_stack[-1]
		else:
			_token_type = self.context[0].token_type
		self.add_instruction(DateLangParserInstruction.CALC_STATE, _token_type, state_int=self._state_stack[-1])
		self.add_instruction(DateLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1

	def __ACCEPT__(self):
		self.add_instruction(DateLangParserInstruction.PRINT, f" TEST ACCEPT\n    |\n    • ---> @NOTE<As a test, setting parser state to int -1>")
		self.set_state(-1)
		self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: self.state == -1)

	def __ERROR__(self, error=None, error_msg="Critical: a runtime error has occurred; please review and try again..."):
		__error__ = error or RuntimeError
		raise __error__(error_msg)

	def __PRINT__(self, *args, **kwargs):
		print(*args, **kwargs)
		self._instr_counter += 1

	def __CLEAN_UP__(self):
		raise NotImplementedError

	def __CALC_STATE__(self, symbol, state_int=None):
		_state_int = state_int if state_int is not None else (self._state_stack[-1] if self._state_stack else 0)
		self.set_state((_state_int, symbol))

	def __MAIN_LOOP__(self):
		_state_int = self.state[0]
		_type_ = self.state[1]

		# print()
		# print(f"MAIN_LOOP INSTRUCTION")
		# print(f"    |")
		# print(f"    | ({_state_int}, {_type_.lower()})")
		# print()
		# print()
		# print()
		# print(f"STATE INT STACK: {self._state_stack}")
		# print(f"SYMBOL STACK: {self._symbol_stack}")
		# print()
		# print()


		match _state_int:
			case None:
				# print(f"HALTING on 'case None'")
				self.add_instruction(DateLangParserInstruction.HALT)
			case 0:
				if _type_.lower() == "year":
					# print(f"SHIFTING TO STATE INT 9")
					self.add_instruction(DateLangParserInstruction.SHIFT, 9)
				else:
					# print(f"HALTING on 'case 0'")
					self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: False)
			case 2:
				if _type_ == DateLangTokenType.END_SYMBOL:
					# print(f"REDUCING: {self._symbol_stack} ---> 'date'\nGOTO STATE INT: 3")
					self.add_instruction(DateLangParserInstruction.REDUCE, "year_format", 1, 3)
				else:
					# print(f"HALTING on 'case 2'")
					self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: False)
			case 3:
				if _type_ == DateLangTokenType.END_SYMBOL:
					self.add_instruction(DateLangParserInstruction.ACCEPT)
				else:
					# print(f"HALTING on 'case 3'")
					self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: False)
			case 9:
				if _type_.lower() == "delim":
					# print(f"SHIFTING TO STATE INT: 14")
					self.add_instruction(DateLangParserInstruction.SHIFT, 14)
				else:
					# print(f"HALTING on 'case 9'")
					self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: False)
			case 14:
				if _type_.lower() == "month":
					# print(f"SHIFTING TO STATE INT: 22")
					self.add_instruction(DateLangParserInstruction.SHIFT, 22)
				else:
					# print(f"HALTING on 'case 14'")
					self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: False)
			case 22:
				if _type_.lower() == "delim":
					# print(f"SHIFTING TO STATE INT: 26")
					self.add_instruction(DateLangParserInstruction.SHIFT, 26)
				else:
					# print(f"HALTING on 'case 22'")
					self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: False)
			case 26:
				if _type_.lower() == "day":
					# print(f"SHIFTING TO STATE INT: 31")
					self.add_instruction(DateLangParserInstruction.SHIFT, 31, default=DateLangTokenType.END_SYMBOL)
				else:
					# print(f"HALTING on 'case 26'")
					self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: False)
			case 31:
				if _type_ == DateLangTokenType.END_SYMBOL:
					# print(f"REDUCING: {self._symbol_stack} ---> 'date'\nGOTO STATE INT: 2")
					self.add_instruction(DateLangParserInstruction.REDUCE, "year_format", 5, 2)
				else:
					# print(f"HALTING on 'case 31'")
					self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: False)
			case _:
				# print(f"HALTING on 'case _'")
				self.add_instruction(DateLangParserInstruction.HALT, condition=lambda: False)


if __name__ == "__main__":

	########################################################################################################################
	#                                                                                                                      #
	# • -------------------------------------------------- 'DateLang' -------------------------------------------------- • #
	#                                                                                                                      #
	########################################################################################################################


	from pyprofiler import profile_callable, SortBy
	from pyutils import (
	    cmd_argument,
	    DEFAULT_PARSER as DEFAULT_CMD_LINE_PARSER
	)
	from .scratch_evaluator import Evaluator
	from .scratch_nodes import Node
	from .scratch_init_grammar import (
		test_grammar_factory,
		init_grammar
	)
	from .scratch_logging_init import init_logging
	from .scratch_cons import (
		LanguageType,
		DateLangVersion,
		PyParseFileSystemPath
	)
	from .utils import (
		display_result,
		display_item_states,
		bold_text,
		apply_color,
		underline_text,
		center_text
	)


	_SCRATCH_PARSER_RUNTIME_LOGGER = PyLogger.get("scratch_runtime_init_final_redesign")


	@profile_callable(sort_by=SortBy.CUMULATIVE)
	# @profile_callable(sort_by=SortBy.TIME)
	# @profile_callable(sort_by=SortBy.CALLS)
	def date_lang_main(debug_mode=True):
		# __CURRENT_FILE__ = fr"{__file__}"
		# _date_lang_input_filepath = r"/Users/mickey/Desktop/Python/custom_packages/pyparse/examples/example_datelang_source.dlang"
		# with open(_date_lang_input_filepath, "r", newline="") as _in_file:
		# 	_test_input = _in_file.read()


		__LANG_TYPE__ = LanguageType.DATE_LANG
		__GRAMMAR_VERSION__ = DateLangVersion.V0_0_1
		__LANG_INFO__ = f"{__LANG_TYPE__.lower()}_{__GRAMMAR_VERSION__}"  # @VERSION_NOTE_<'date_lang_v0_0_1' as of 2025/04/10>
		# __GRAMMAR__ = test_grammar_factory()
		# init_grammar(__GRAMMAR__, __LANG_INFO__)


		_logging_setup_callbacks = initialize_shell(logger=_SCRATCH_PARSER_RUNTIME_LOGGER, version=str(__LANG_INFO__))

		ENCODING = cmd_argument("encoding", parser=DEFAULT_CMD_LINE_PARSER)
		USE_LOGGING = cmd_argument("log", parser=DEFAULT_CMD_LINE_PARSER)
		LOGGING_DIR = cmd_argument("logging_dir", parser=DEFAULT_CMD_LINE_PARSER)
		LOG_FILENAME = cmd_argument("log_filename", parser=DEFAULT_CMD_LINE_PARSER)
		LOGGING_LEVEL = cmd_argument("logging_level", parser=DEFAULT_CMD_LINE_PARSER)

		init_logging(
			use_logging=USE_LOGGING,
			log_filename=LOG_FILENAME,
			logging_dir=LOGGING_DIR,
			logging_level=LOGGING_LEVEL,
			logging_callbacks=_logging_setup_callbacks,
			encoding=ENCODING
		)


		# for state, rule in __GRAMMAR__.generate_states().items():
		# 	print(bold_text(apply_color(214, f"STATE: {state}")))
		# 	print()
		# 	for i in rule:
		# 		_id = i.rule_id
		# 		_head = i.rule_head
		# 		_body = i.rule_body
		# 		_status = i.status()
		# 		print(f"\t • -------")
		# 		print(f"\t| RULE-ID:     {_id}")
		# 		print(f"\t| RULE-HEAD:   {_head}")
		# 		print(f"\t| RULE-BODY:   {_body}")
		# 		print(f"\t| AUG-RULE-:   {_status}")
		# 		print(f"\t • -------")
		# 		print()
		# 	print()
		# 	print()



		_test_input = "2023-08-07"
		# _token_context_ = []


		# FORMAT_WIDTHS = {
		#     "%Y": 4,
		#     "%m": 2,
		#     "%d": 2,
		# }

		# def tokenize_format(fmt: str):
		# 	"""Tokenize the format string into a list of format tokens and literals."""
		# 	tokens = []
		# 	i = 0
		# 	while i < len(fmt):
		# 		if fmt[i] == '%':
		# 			token = fmt[i:i+2]
		# 			if token not in FORMAT_WIDTHS:
		# 				raise ValueError(f"Unsupported format token: {token}")
		# 			tokens.append(token)
		# 			i += 2
		# 		else:
		# 			tokens.append(fmt[i])
		# 			i += 1
		# 	return tokens
		# _test_format = f"{DateFormat.YYYY}-{DateFormat.MM}-{DateFormat.DD}"
		# _test_format_deque = deque(_test_format.split())
		# _test_input_deque = deque(_test_input.split())

		# _delim = ""
		# _year = ""
		# _month = ""
		# _day = ""

		# while _test_format_deque or _test_input_deque:

		# 	_format_char = _test_format_deque.popleft()
		# 	_4_year = ""
		# 	for i in range(4):


		# 	if "".join(_test_format[:4]) == DateFormat.YYYY:
		# 		for i in range(4):
		# 			_year_char = _test_input[_pointer]
		# 			_pointer += 1

		# 	elif 

		# 		break
		# 	else:
		# 		break
			
		# 	_pointer += 1
	

		# _token_context_ = tokenize_format("%Y-%m-%d")
		_token_context_ = [DateLangToken(DateLangTokenType.YEAR, "2023", token_id=DateLangTokenType.YEAR), DateLangToken(DateLangTokenType.DELIM, "-", token_id=DateLangTokenType.DELIM), DateLangToken(DateLangTokenType.MONTH, "08", token_id=DateLangTokenType.MONTH), DateLangToken(DateLangTokenType.DELIM, "-", token_id=DateLangTokenType.DELIM), DateLangToken(DateLangTokenType.DAY, "07", token_id=DateLangTokenType.DAY), DateLangToken(DateLangTokenType.END_SYMBOL, "#", token_id=DateLangTokenType.END_SYMBOL)]

		# __TOKENIZER__ = DateLangTokenizer(tokenizer_id=__LANG_INFO__)
		# __TOKENIZER__.set_input(_test_input)
		# _token_context_ = __TOKENIZER__.tokenize()
		# _token_context_ = [i for i in _token_context_ if i.token_type != DateLangTokenType.SKIP]


		print()
		print(bold_text(apply_color(214, f" INPUT:")), end="\n")
		print(f"    |")
		print(f"    |")
		print(f"    |")
		for _idx_, _input_ in enumerate(_test_input.split("\n"), start=1):
			_input_repr_ = repr(_input_)
			if _idx_ == 1:
				print(f"     • ---> {_input_repr_}")
			else:
				print(f"            {_input_repr_}")
		print()
		print()
		print(bold_text(apply_color(204, " TOKEN CONTEXT:")))
		print(f"    |")
		print(f"    |")
		print(f"    |")
		_total_tokens = 0
		for _idx, _token_ in enumerate(_token_context_, start=1):
			if _idx == 1:
				print(f"     • ---> {_token_}")
			else:
				print(f"            {_token_}")
			_total_tokens += 1
		print()
		print()
		print(bold_text(apply_color(214, f" TOTAL TOKENS: {_total_tokens}")))
		for _ in range(2):
			print()


		__PARSER__ = DateLangParser(executor=None, invalid_instruction=DateLangParserInstruction.HALT, logger=_SCRATCH_PARSER_RUNTIME_LOGGER)
		_pretval = __PARSER__.parse(_token_context_)
		print()
		print()
		print(center_text(bold_text(apply_color(214, f"PARSE IS...\n"))))
		print(center_text(bold_text(apply_color(10, f"• --- VALID --- •")) if _pretval else bold_text(apply_color(9, f"• --- INVALID --- •"))))


	date_lang_main(debug_mode=True)
