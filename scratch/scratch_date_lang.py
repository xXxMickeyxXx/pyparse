from abc import ABC, abstractmethod
from enum import StrEnum, IntEnum, auto

from pyparse import Tokenizer, Scanner, LexHandler, Token
from pylog import PyLogger, LogType
from .scratch_utils import generate_id
from .scratch_cons import (
	LanguageType,
	DateLangVersion
)


_date_lang_logger = PyLogger(logger_id=f"{LanguageType.DATE_LANG}{DateLangVersion.V0_0_1}")


class DateFormat(StrEnum):

	YYYY = "YYYY"
	YY = "YY"
	MM = "MM"
	M = "M"
	DD = "DD"
	D = "D"


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

	# @NOTE<Parser instructions>
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

	def __init__(self, tokenizer_id=None):
		self._tokenizer_id = tokenizer_id or generate_id()
	
	def tokenize(self):
		_END_OF_INPUT = DateLangToken(DateLangTokenType.END_SYMBOL, "#", token_id=DateLangTokenType.END_SYMBOL)
		self.add_token(_END_OF_INPUT)
		return self.reset()


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

	__slots__ = ("_handlers", "_instructions", "_curr_instruction", "_args", "_invalid_instr", "_state", "_state_stack", "_symbol_stack", "_logger")

	def __init__(self, executor=None, invalid_instruction=DateLangParserInstruction.HALT, logger_id=None):
		super.__init__(executor or self.__EXECUTOR__, init_state=0, parser_id=f"{LanguageType.DATE_LANG.lower()}_{DateLangVersion.V0_0_1}")
		self._handlers = {}
		self._instructions = deque()
		self._curr_instruction = None
		self._args = ((), {})
		self._invalid_instr = invalid_instruction

		self._state = (None, None)
		self._state_stack = []
		self._symbol_stack = []
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

	def send(self, *args, **kwargs):
		self._args = (args, kwargs)

	def set_instruction(self, instruction_type):
		self._curr_instruction = instruction_type

	def add_instruction(self, instruction_type, *args, **kwargs):
		self._instructions.append((instruction_type, args, kwargs))

	def next_instruction(self, default=None):
		return self._instructions.popleft() if self._instructions else default

	def init(self):
		self.add_instruction(DateLangParserInstruction.HALT, self.__HALT__)
		self.add_instruction(DateLangParserInstruction.INIT, self.__INIT__)
		self.add_instruction(DateLangParserInstruction.SHIFT, self.__SHIFT__)
		self.add_instruction(DateLangParserInstruction.REDUCE, self.__REDUCE__)
		self.add_instruction(DateLangParserInstruction.ACCEPT, self.__ACCEPT__)
		self.add_instruction(DateLangParserInstruction.ERROR, self.__ERROR__)
		self.add_instruction(DateLangParserInstruction.PRINT, self.__PRINT__)
		self.add_instruction(DateLangParserInstruction.CLEANUP, self.__CLEAN_UP__)
		self.add_instruction(DateLangParserInstruction.CALC_STATE, self.__CALC_STATE__)
		self.add_instruction(DateLangParserInstruction.MAIN_LOOP, self.__MAIN_LOOP__)

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

	def __HALT__(self):
		pass

	def __INIT__(self):
		_state_int = self.state
		_type_ = self.context[0].token_type
		_print_text = f"\t   |\n"
		_print_text += f"\t   |\n"
		_print_text += f"\t   |\n"
		_print_text += f"\t    • ---> "
		_print_text += apply_color(226, underline_text("ESTABLISHING PARSERS INITAL STATE") + "...\n\n")
		_print_text += apply_color(226, f"\tSTATE #        •---> {_state_int}\n")
		_print_text += apply_color(226, f"\tNEXT TOKEN     •---> {_type_}\n")
		print(_print_text)
		self._state_stack.append(self.state)
		self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=_type_)
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1
		pass

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
		self._symbol_stack.append(rule_head)
		self._state_stack.append(goto)
		self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1

	def __ACCEPT__(self):
		raise NotImplementedError

	def __ERROR__(self, error=None, error_msg="Critical: a runtime error has occurred; please review and try again..."):
		__error__ = error or RuntimeError
		raise __error__(error_msg)

	def __PRINT__(self, *args, **kwargs):
		print(*args, **kwargs)
		self._instr_counter += 1

	def __CLEAN_UP__(self):
		raise NotImplementedError

	def __CALC_STATE__(self):
		self.set_state((self._state_stack[-1], self._symbol_stack[-1] if symbol is None else symbol))

	def __MAIN_LOOP__(self):
		raise NotImplementedError


if __name__ == "__main__":
	pass
