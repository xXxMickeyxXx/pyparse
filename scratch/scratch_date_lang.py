import sys
from enum import StrEnum, IntEnum, auto

from pyparse import Tokenizer, LexHandler, Token
from pylog import PyLogger, LogType
from .scratch_cons import (
	LanguageType,
	DateLangVersion
)


_date_lang_logger = PyLogger(logger_id=f"{LanguageType.DATE_LANG}{DateLangVersion.V0_0_1}")
STD_OUT = sys.stdout
STD_FLUSH = sys.stdout.flush


class DateUnit(IntEnum):

	MONTH = auto()
	DAY = auto()
	YEAR = auto()


class DateLangParserInstruction(IntEnum):
	"""
		 _____________________
	    |          			  |
	    •__INSTRUCTION ENUMS__•

			HALT (int: 1)
			INIT (int: 2)
			START (int: 3)
			SHIFT (int: 4)
			REDUCE (int: 5)
			ACCEPT (int: 6)
			ERROR (int: 7)
			PRINT (int: 8)
			CLEANUP (int: 9)
			CALC_STATE (int: 10)
			MAIN_LOOP (int: 11)


	"""

	# @NOTE<Shift/reduce parser instructions>
	HALT = auto()
	INIT = auto()
	START = auto()
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

	# @NOTE<Basic token types>
	INVALID = "INVALID"
	SKIP = ""
	END_SYMBOL = "END_SYMBOL"
	NUMBER = "NUMBER"
	DELIM = "DELIM"

	# @NOTE<'DateLang' token types>


class DateLangTokenHandler(LexHandler):

	def __init__(self, delimiter="-"):
		super.__init__(handler_id=f"{LanguageType.DATE_LANG}{DateLangVersion.V0_0_1}")
		self._delimiter = delimiter

	def handler(self, tokenizer):
		_add_token_alias = tokenizer.add_token
		_tokenizer_advance = tokenizer.advance
		_cond_consume = tokenizer.cond_consume
		_counter = 1

		while tokenizer.can_consume:
			_current_char = tokenizer.current_char
			
			match _current_char:
				case _:
					# _add_token_alias(DateLangTokenType.SKIP, _current_char, token_id=f"SKIP_{_counter}")
					_add_token_alias(DateLangTokenType.INVALID, _current_char, token_id=f"INVALID_{_counter}")
					_tokenizer_advance()

			_counter += 1
		_add_token_alias(SimpleLangTokenType.END_SYMBOL, "#", token_id=f"END_SYMBOL_{_counter}")


class PyParser:

	__slots__ = ("_executor", "_parser_id", "_state", "_args", "_context", "_result", "_result_set", "_quit_flag")

	def __init__(self, init_state=0, executor, parser_id=None):
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

	def peek(self, offset=0, default=):
		return self._context[offset]

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

	def __init__(self, executor=None, invalid_instruction=DateLangParserInstruction.HALT, logger_id=None):
		super.__init__(init_state=(0, ()), (DateLangParserInstruction.START), executor or self.__EXECUTOR__, parser_id=f"{LanguageType.DATE_LANG}{DateLangVersion.V0_0_1}")
		self._handlers = {}
		self._instructions = deque()
		self._curr_instruction = None
		self._args = ((), {})
		self._invalid_instr = invalid_instruction

		self._logger = logger or _date_lang_logger
		self._delim = delim
		self._state = (None, None)
		self._state_stack = []
		self._symbol_stack = []
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
		self.add_instruction(DateLangParserInstruction.START, self.__START__)
		self.add_instruction(DateLangParserInstruction.MAIN_LOOP, self.__MAIN_LOOP__)
		self.add_instruction(DateLangParserInstruction.ERROR, self.__ERROR__)
		self.add_instruction(DateLangParserInstruction.SHIFT, self.__SHIFT__)
		self.add_instruction(DateLangParserInstruction.REDUCE, self.__REDUCE__)
		self.add_instruction(DateLangParserInstruction.CALC_STATE, self.__CALC_STATE__)
		self.add_instruction(DateLangParserInstruction.PRINT, self.__PRINT__)

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
		print()
		print(f"    |" + underline_text(bold_text(apply_color(214, f"CURRENT INSTRUCTION"))) + bold_text(apply_color(168, f" • --- • {SimpleLangParserInstruction.INSTR(int_val=self.curr_instruction)} <iCOUNT: {self.instr_count}>")))
		print()

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
		self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=self.peek(offset=0))
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1
		pass

	def __START__(self):
		pass

	def __MAIN_LOOP__(self):
		pass

	def __ERROR__(self, error=None, error_msg="Critical: a runtime error has occurred; please review and try again..."):
		__error__ = error or RuntimeError
		raise __error__(error_msg)

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
			print(f"\nPOPPING SYMBOL  ---> '{_sym_pop}' FROM SYMBOL STACK")
			print(f"POPPING STATE   ---> '{_state_pop}' FROM STATE STACK\n")
		self._symbol_stack.append(rule_head)
		self._state_stack.append(goto)
		self.add_instruction(SimpleLangParserInstruction.CALC_STATE, symbol=None)
		self.add_instruction(SimpleLangParserInstruction.MAIN_LOOP)
		self._instr_counter += 1

	def __CALC_STATE__(self):
		self.set_state((self._state_stack[-1], self._symbol_stack[-1] if symbol is None else symbol))

	def __PRINT__(self, *args, **kwargs):
		print(*args, **kwargs)
		self._instr_counter += 1


if __name__ == "__main__":
	pass
