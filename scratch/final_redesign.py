from typing import (
    Protocol,
    Callable,
    Sequence,
    TypeVar,
    Union,
    Any,
    List,
    Dict,
    Tuple,
    LiteralString,
    Type,
    Optional,
    runtime_checkable,
)
from enum import StrEnum, auto
from abc import ABC, abstractmethod

from pyparse import Tokenizer, LexHandler, Token
from pylog import PyLogger, LogType
from pysynchrony import (
	PySynchronyScheduler,
	PySynchronyEventLoop,
	PySynchronyContext,
	PySynchronyCoroutineTask,
	PySynchronyPort,
	PySynchronyEvent,
	PySynchronySysCall,
	PriorityQueueFactory,
	PySynchronyPortError
)
from pyutils import (
    cmd_argument,
    DEFAULT_PARSER as DEFAULT_CMD_LINE_PARSER
)
from .scratch_runtime_setup import (
	TestArithmaticGrammarTokenType,
	TestArithmaticGrammarTokenizeHandler,
	CoreParser2,
	ParserContext,
	ParseContext
)
from .scratch_parse_env import ParserEnvironment
from .scratch_init_grammar import (
		test_grammar_factory,
		init_grammar
	)
from .scratch_evaluator import Evaluator
from .scratch_nodes import Node
from .scratch_grammar_rules_filter import (
	RuleSelector,
	AndRuleSelector,
	OrRuleSelector,
	NotRuleSelector,
	RuleIDSelector,
	RuleHeadSelector,
	RuleBodySelector
)
from .scratch_package_paths import (
	TEST_INPUT_1,
	TEST_INPUT_2
)
from .scratch_shell_init import initialize_shell
from .scratch_logging_init import init_logging
from .scratch_utils import generate_id, read_source
from .utils import display_result, apply_color, bold_text, underline_text, center_text
from .scratch_cons import (
	PyParsePortID,
	PyParseEventID,
	ParserActionState,
	ParserActionType,
	PyParseLoggerID,
	GrammarRuleBy
)


_FINAL_REDESIGN_LOGGER = PyLogger.get(PyParseLoggerID.FINAL_REDESIGN)


class TestDateTimeGrammarTokenType(StrEnum):
	pass


class TestDateTimeGrammarTokenizeHandler(LexHandler):

	def __init__(self):
		super().__init__(tokenizer=None)


class Grammar9TokenType(StrEnum):
	
	# HASHTAG_T = 	 	"#"
	a_SYMBOL_T = "a_SYMBOL_T"
	b_SYMBOL_T = "b_SYMBOL_T"
	EXCLAMATION_T = "EXCLAMATION_T"
	LEFT_PAREN_T = "LEFT_PAREN_T"
	RIGHT_PAREN_T = "RIGHT_PAREN_T"
	# S_SYMBOL_NT = "S_SYMBOL_NT"
	# A_SYMBOL_NT = "A_SYMBOL_NT"
	# B_SYMBOL_NT = "B_SYMBOL_NT"
	# C_SYMBOL_NT = "C_SYMBOL_NT"
	HASHTAG_END = "HASHTAG_END"


class Grammar9TokenizerHandler(LexHandler):

	def __init__(self):
		super().__init__(handler_id=self.__class__.__name__)

	def handle(self, tokenizer):
		_add_token_alias = tokenizer.add_token
		_tokenizer_advance_a = tokenizer.advance
		_cond_consume_a = tokenizer.cond_consume
		while tokenizer.can_consume:
			_current_char = tokenizer.current_char
			if _current_char:
				match _current_char:
					# case "#":
					# 	_add_token_alias(Grammar9TokenType.HASHTAG_T, "#", token_id=None)
					# 	continue
					case "a":
						_add_token_alias(Grammar9TokenType.a_SYMBOL_T, "a", token_id=None)
						_tokenizer_advance_a()
						continue
					case "b":
						_add_token_alias(Grammar9TokenType.b_SYMBOL_T, "b", token_id=None)
						_tokenizer_advance_a()
						continue
					case "!":
						_add_token_alias(Grammar9TokenType.EXCLAMATION_T, "!", token_id=None)
						_tokenizer_advance_a()
						continue
					case "(":
						_add_token_alias(Grammar9TokenType.LEFT_PAREN_T, "(", token_id=None)
						_tokenizer_advance_a()
						continue
					case ")":
						_add_token_alias(Grammar9TokenType.RIGHT_PAREN_T, ")", token_id=None)
						_tokenizer_advance_a()
						continue
					# case "S":
					# 	_add_token_alias(Grammar9TokenType.S_SYMBOL_NT, "S", token_id=None)
					# 	_tokenizer_advance_a()
					# 	continue
					# case "A":
					# 	_add_token_alias(Grammar9TokenType.A_SYMBOL_NT, "A", token_id=None)
					# 	_tokenizer_advance_a()
					# 	continue
					# case "B":
					# 	_add_token_alias(Grammar9TokenType.B_SYMBOL_NT, "B", token_id=None)
					# 	_tokenizer_advance_a()
					# 	continue
					# case "C":
					# 	_add_token_alias(Grammar9TokenType.C_SYMBOL_NT, "C", token_id=None)
					# 	_tokenizer_advance_a()
					# 	continue
					case _:
						_error_details = f"unexpected character: '{_current_char}'; handler is unable to determine how to tokenize character...please review and try again..."
						raise RuntimeError(_error_details)
			else:
				break
		_add_token_alias(Grammar9TokenType.HASHTAG_END, "#", token_id=None)


class DateGrammarTokenType(StrEnum):

	FSLASH_DELIM = "FSLASH_DELIM"
	BSLASH_DELIM = "BSLASH_DELIM"
	HYPHEN_DELIM = "HYPHEN_DELIM"
	PERIOD_DELIM = "PERIOD_DELIM"
	MONTH = "MONTH"
	DAY = "DAY"
	YEAR = "YEAR"
	WS = "WS"
	END_SYMBOL = "END_SYMBOL"


class DateGrammarTokenizerHandler(LexHandler):
	
	"""
  	VALID 'DateGrammarTokenType.FSLASH_DELIM' VALUE:
	  |
	  |
	  |
	  • -----> LiteralString -> '/'


  	VALID 'DateGrammarTokenType.BSLASH_DELIM' VALUE:
	  |
	  |
	  |
	  • -----> LiteralString -> '\\'


  	VALID 'DateGrammarTokenType.HYPHEN_DELIM' VALUE:
	  |
	  |
	  |
	  • -----> LiteralString -> '-'


  	VALID 'DateGrammarTokenType.PERIOD_DELIM' VALUE:
	  |
	  |
	  |
	  • -----> LiteralString -> '.'


	VALID 'DateGrammarTokenType.MONTH' VALUES:
	  |
	  |
	  |
	  • -----> List[int] -> [1-12]
	

  	VALID 'DateGrammarTokenType.DAY' VALUES:
	  |
	  |
	  |
	  • -----> List[int] -> [1-31]
	

  	VALID 'DateGrammarTokenType.YEAR' VALUES:
	  |
	  |
	  |
	  • -----> List[int] -> [00-30] & List[int] -> [2000-2030]


  	VALID 'DateGrammarTokenType.YEAR' VALUES:
	  |
	  |
	  |
	  • -----> LiteralString -> ' ' & '\n' & '\r\n' & '\t'


  	VALID 'DateGrammarTokenType.END_SYMBOL' VALUES:
	  |
	  |
	  |
	  • -----> LiteralString -> '#'
	"""

	def __init__(self, end_symbol="#"):
		super().__init__(handler_id=self.__class__.__name__)
		self._end_symbol = end_symbol
		self._token_mapping = {
			"/": DateGrammarTokenType.FSLASH_DELIM,
			"\\": DateGrammarTokenType.BSLASH_DELIM,
			"-": DateGrammarTokenType.HYPHEN_DELIM,
			".": DateGrammarTokenType.PERIOD_DELIM,
			" ": DateGrammarTokenType.WS,
			"\n": DateGrammarTokenType.WS,
			"\t": DateGrammarTokenType.WS,
			"\r\n": DateGrammarTokenType.WS,
			self._end_symbol: DateGrammarTokenType.END_SYMBOL
		}

	def handle(self, tokenizer):
		_add_token_alias = tokenizer.add_token
		_tokenizer_advance_a = tokenizer.advance
		_cond_consume_a = tokenizer.cond_consume

		_month_lexed = False
		_day_lexed = False
		_year_lexed = False
		while tokenizer.can_consume:
			_current_char = tokenizer.current_char
			
			if _current_char in {" ", "\n", "\t", "\r\n"}:
				self.skip_ws(tokenizer)
				continue

			if _current_char.isdigit():
				if not _month_lexed:
					_token_val = tokenizer.cond_consume(lambda curr_char, lexeme, scanner: not curr_char.isdigit())
					_add_token_alias(DateGrammarTokenType.MONTH, _token_val, token_id=None)
					_month_lexed = True
				elif not _day_lexed:
					_token_val = tokenizer.cond_consume(lambda curr_char, lexeme, scanner: not curr_char.isdigit())
					_add_token_alias(DateGrammarTokenType.DAY, _token_val, token_id=None)
					_day_lexed = True
				elif not _year_lexed:
					_token_val = tokenizer.cond_consume(lambda curr_char, lexeme, scanner: not curr_char.isdigit())
					_add_token_alias(DateGrammarTokenType.YEAR, _token_val, token_id=None)
					_year_lexed = True
				else:
					_error_details = f"error tokenizing number-like symbol; please review and try again..."
					raise RuntimeError(_error_details)
				continue

			match _current_char:
				case ".":
					_add_token_alias(self._token_mapping[_current_char], _current_char, token_id=None)
				case "/":
					_add_token_alias(self._token_mapping[_current_char], _current_char, token_id=None)
				case _:
					_error_details = f"unexpected character: '{_current_char}'; handler is unable to determine how to tokenize character...please review and try again..."
					raise RuntimeError(_error_details)
			_tokenizer_advance_a()

		_add_token_alias(self._token_mapping[self._end_symbol], self._end_symbol, token_id=None)

	def skip_ws(self, tokenizer):
		_result = tokenizer.cond_consume(lambda curr_chr, lexeme, scanner: curr_chr not in {" ", "\n", "\t", "\r\n"})


class TableBuilder(ABC):

	__slots__ = ("_grammar")

	def __init__(self, grammar=None):
		self._grammar = grammar

	@property
	def grammar(self):
		if self._grammar is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access the 'grammar' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._grammar

	def set_grammar(self, grammar):
		self._grammar = grammar

	@abstractmethod
	def build_table(self, table):
		raise NotImplementedError


class Grammar9TableBuilder(TableBuilder):

	# def build_table(self, table):
	# 	INIT_RULE = self.grammar.select(RuleIDSelector("INIT_RULE"))[0]
	# 	S_rule_1 = self.grammar.select(RuleIDSelector("S_rule_1"))[0]
	# 	A_rule_1 = self.grammar.select(RuleIDSelector("A_rule_1"))[0]
	# 	B_rule_1 = self.grammar.select(RuleIDSelector("B_rule_1"))[0]

	# 	# SYMBOLS ---> [a, b, S, A, B]
	# 	# STATE 0:
	# 	# table.add_action((0, "("), (ParserActionType.SHIFT))
	# 	table.add_action((0, "a"), (ParserActionType.SHIFT, 2))
	# 	table.add_goto((0, "S"), (1, INIT_RULE.copy().advance_by(1)))

	# 	# STATE 1:
	# 	table.add_action((1, "#"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))

	# 	# STATE 2:
	# 	table.add_action((2, "b"), (ParserActionType.SHIFT, 3))
	# 	table.add_goto((2, "A"), (4, S_rule_1.copy().advance_by(2)))
	# 	table.add_goto((2, "B"), (5, B_rule_1.copy().advance_by(1)))

	# 	# STATE 3:
	# 	table.add_action((3, "#"), (ParserActionType.REDUCE, B_rule_1.copy().advance_by(1)))

	# 	# STATE 4:
	# 	table.add_action((4, "#"), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(2)))

	# 	# STATE 5:
	# 	table.add_action((5, "#"), (ParserActionType.REDUCE, A_rule_1.copy().advance_by(1)))

	def build_table(self, table):
		INIT_RULE = self.grammar.select(RuleIDSelector("INIT_RULE"))[0]
		S_rule_1 = self.grammar.select(RuleIDSelector("S_rule_1"))[0]
		S_rule_2 = self.grammar.select(RuleIDSelector("S_rule_2"))[0]
		S_rule_3 = self.grammar.select(RuleIDSelector("S_rule_3"))[0]
		A_rule_1 = self.grammar.select(RuleIDSelector("A_rule_1"))[0]
		B_rule_1 = self.grammar.select(RuleIDSelector("B_rule_1"))[0]
		# B_rule_2 = self.grammar.select(RuleIDSelector("B_rule_2"))[0]
		C_rule_1 = self.grammar.select(RuleIDSelector("C_rule_1"))[0]

		# STATE 0:
		# table.add_action((0, "a"), (ParserActionType.SHIFT, 2))
		# table.add_goto((0, "S"), (1, INIT_RULE.copy().advance_by(1)))

		table.add_action((0, "a"), (ParserActionType.SHIFT, 4))
		table.add_action((0, "("), (ParserActionType.SHIFT, 1))
		table.add_goto((0, "S"), (1, INIT_RULE.copy().advance_by(1)))
		table.add_goto((0, "C"), (1, S_rule_3.copy().advance_by(1)))



		# STATE 1:
		# table.add_action((1, "#"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))
		# table.add_action((1, "b"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))
		# table.add_action((1, "!"), (ParserActionType.SHIFT, 3))

		table.add_action((1, "#"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))
		table.add_action((1, "a"), (ParserActionType.SHIFT, 4))
		# table.add_action((1, "b"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))
		table.add_action((1, "!"), (ParserActionType.SHIFT, 3))
		table.add_goto((1, "S"), (5, C_rule_1.copy().advance_by(2)))

		# STATE 2:
		# table.add_action((2, "b"), (ParserActionType.SHIFT, 4))
		# table.add_goto((2, "A"), (8, S_rule_1.copy().advance_by(2)))
		# table.add_goto((2, "B"), (5, B_rule_1.copy().advance_by(1)))
		# # table.add_goto((2, "C"), (6, B_rule_2.copy().advance_by(1)))
		# table.add_action((2, "("), (ParserActionType.SHIFT, 7))
		
		table.add_action((2, "b"), (ParserActionType.SHIFT, 4))
		table.add_goto((2, "A"), (8, S_rule_1.copy().advance_by(2)))
		table.add_goto((2, "B"), (5, B_rule_1.copy().advance_by(1)))
		# table.add_goto((2, "C"), (6, B_rule_2.copy().advance_by(1)))
		table.add_action((2, "("), (ParserActionType.SHIFT, 7))
		
		# STATE 3:
		table.add_action((3, "#"), (ParserActionType.REDUCE, S_rule_2.copy().advance_by(2)))

		# STATE 4:
		# table.add_action((4, "#"), (ParserActionType.REDUCE, B_rule_1.copy().advance_by(1)))
		
		table.add_action((4, "b"), (ParserActionType.SHIFT, 8))

		# STATE 5:
		table.add_action((5, "#"), (ParserActionType.REDUCE, A_rule_1.copy().advance_by(1)))

		table.add_action((5, ")"), (ParserActionType.SHIFT, 10))

		# STATE 6:
		# table.add_action((6, "#"), (ParserActionType.REDUCE, B_rule_2.copy().advance_by(1)))

		# STATE 7:
		table.add_action((7, "a"), (ParserActionType.SHIFT, 2))

		# STATE 8:
		# table.add_action((8, "#"), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(3)))
		
		for _symbol in self.grammar.terminals():
			table.add_action((8, _symbol), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(3)))

		# STATE 9:
		# table.add_action((9, ")"), (ParserActionType.SHIFT, 10))

		table.add_action((9, ")"), (ParserActionType.SHIFT, 10))
		table.add_action((9, "#"), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(2)))


		# STATE 10:
		table.add_action((10, "#"), (ParserActionType.REDUCE, C_rule_1.copy().advance_by(3)))


class DateGrammarTableBuilder(TableBuilder):

	def build_table(self, table):
		pass


class CoreParser3(CoreParser2):

	# def __init__(self, init_state=0, grammar=None, parse_table=None, debug_mode=False, parser_id=None):
	# 	super().__init__(init_state=init_state, grammar=grammar, parse_table=parse_table, debug_mode=debug_mode, parser_id=parser_id)
	# 	self._parser_context = ParserContext(context_id=self.parser_id)

	# @property
	# def parser_context(self):
	# 	return self._parser_context

	def parse(self, parse_context):
		# NOTE: remove below (up unti' series of consecutive '#'s) code as it's for coloring terminal debug output
		_xor_val = 208 ^ 226
		_color_code = 226

		####################
		# self.init_parse()
		# self.init_parse_context(parse_context)
		parse_context.append_state(self.init_state)

		_current_state = parse_context.state()
		_current_symbol = parse_context.current_symbol().token_val
		_action_info = self.parse_table.action((_current_state, _current_symbol), default=(ParserActionType.ERROR, None))
		while not parse_context.done_parsing:
			# if parse_context.done_parsing:
			# 	break

			if self.debug_mode:
				_color_code ^= _xor_val
				_debug_text_mainloop_top = "---------- TOP OF 'parse' MAINLOOP ----------\n"
				_colored_debug_text = bold_text(apply_color(_color_code, _debug_text_mainloop_top))
				print(_colored_debug_text)
				print()
				print()
				print(f"• CURRENT STATE: {_current_state}")
				print(f"• CURRENT SYMBOL: {_current_symbol}")
				print()
				print(f"• CURRENT STATE STACK: {parse_context.stack}")
				print(f"• CURRENT SYMBOL STACK: {parse_context.symbol_stack}")
				print()
				print()
				self.logger.submit_log(
					message=f"TOP OF 'parse' CYCLE",
					current_state=f"PARSE CONTEXT ID: {parse_context.context_id} ---> ({_current_state}/{_current_symbol})",
					log_type=LogType.DEBUG
					)

			_parse_stack = parse_context.stack
			_parse_sym_stack = parse_context.symbol_stack

			if (len(parse_context.symbol_stack) >= 2 and parse_context.symbol_stack[-2] == "a") and (parse_context.symbol_stack[-1] == "b"):
				_action_info = self.parse_table.action((parse_context.state(), parse_context.symbol_stack[-1]), default=(ParserActionType.ERROR, None))


			_action = _action_info[0]

			if self.debug_mode:
				print(f"• ACTION INFO:")
				print(f"\t{_action_info}")

			if _action == ParserActionType.SHIFT:
				if self.debug_mode:
					print(f"IN SHIFT ACTION:")
				parse_context.append_state(_action_info[1])
				parse_context.append_symbol(_current_symbol)
				self.logger.submit_log(
					message=f"Performing SHIFT action",
					new_state=f"PARSE CONTEXT ID: {parse_context.context_id} ---> ({_action_info[1]}/{_current_symbol})",
					log_type=LogType.DEBUG
					)

				# TODO: create a new action, aside from SHIFT/REDUCE/ACCEPT/ERROR, which allows
				# 		for this behaviour to be ran. Should also allow for other actions. NOTE:
				# 		the actual layout for the function will completely change once all of the
				# 		pieces are more glued together and it's more clear how I'm implementing it
				if _current_state == 0 and _current_symbol == "a":
					_next_input_char = parse_context.peek(offset=1)
					if _next_input_char == "b":
						parse_context.append_state(9)
						parse_context.append_symbol("A")
						parse_context.advance()

						self.logger.submit_log(
							message=f"Since the current state of the parser is 0/'a' (CURRENT-STATE/CURRENT-SYMBOL) and since the next input symbol is a 'b', Performing shortcut SHORTCUT SHIFT action",
							new_state=f"PARSE CONTEXT ID: {parse_context.context_id} ---> (9/A)",
							log_type=LogType.DEBUG
							)
				parse_context.advance()
			elif _action == ParserActionType.REDUCE:
				_reduce_item = _action_info[1]
				if self.debug_mode:
					print(f"IN REDUCE ACTION:")
					for _ in range(_reduce_item.rule_size):
						_popped_state = parse_context.pop_state()
						_popped_symbol = parse_context.pop_symbol()
						print(f"POPPED STATE: {_popped_state}")
						print(f"POPPED SYMBOL: {_popped_symbol}")
					print(f"REDUCE ACTION HANDLING COMPLETE; CALCULATING GOTO:")
				else:
					for _ in range(_reduce_item.rule_size):
						parse_context.pop_state()
						parse_context.pop_symbol()

				if self.debug_mode:
					_goto_key = (parse_context.state(), _reduce_item.rule_head)
					print(f"GOTO KEY ---> {_goto_key}")
					_goto_state = self.parse_table.goto(_goto_key)
					_next_state = _goto_state[0]
					parse_context.append_state(_next_state)
					parse_context.append_symbol(_reduce_item.rule_head)
					print(f"PARSE CONTEXT STATE UPDATED ---> {_next_state}")
					print(f"PARSE CONTEXT SYMBOL STACK UPDATED---> {_reduce_item.rule_head}")
				else:
					_goto_key = (parse_context.state(), _reduce_item.rule_head)
					_goto_state = self.parse_table.goto(_goto_key)
					_next_state = _goto_state[0]
					parse_context.append_state(_next_state)
					parse_context.append_symbol(_reduce_item.rule_head)
			elif _action == ParserActionType.ERROR:
				parse_context.set_result(False)
			elif _action == ParserActionType.ACCEPT:
				parse_context.set_result(True)


			_current_state = parse_context.state()
			_current_symbol = parse_context.current_symbol().token_val
			_action_info = self.parse_table.action((_current_state, _current_symbol), default=(ParserActionType.ERROR, None))

			if self.debug_mode:
				_debug_text_mainloop_bottom = "---------- BOTTOM OF 'parse' MAINLOOP ----------\n"
				_colored_debug_text = bold_text(apply_color(_color_code, _debug_text_mainloop_bottom))
				print(_colored_debug_text)

		_parse_retval = parse_context.result()
		self.logger.submit_log(
				message=f"PARSE CONTEXT ID: {parse_context.context_id} IS {'VALID' if _parse_retval else 'INVALID'}",
				log_type=LogType.DEBUG
			)
		return _parse_retval

	def init_parse(self):
		pass


class FinalRedesignEnv(ParserEnvironment):

	def __init__(self, parser=None, grammar=None, tokenizer=None, parse_table=None, table_builder=None):
		super().__init__(parser=parser, grammar=grammar, env_id=str(__class__.__name__))
		self._parse_table = parse_table
		self._tokenizer = tokenizer
		self._table_builder = table_builder
		self._initialized = False

	@property
	def tokenizer(self):
		if self._tokenizer is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access the 'tokenizer' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._tokenizer

	@property
	def parse_table(self):
		if self._parse_table is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access the 'parse_table' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._parse_table

	@property
	def table_builder(self):
		if self._table_builder is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access the 'table_builder' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._table_builder

	@property
	def is_setup(self):
		return bool(self._initialized)

	def set_tokenizer(self, tokenizer):
		self._tokenizer = tokenizer

	def set_table(self, parse_table):
		self._parse_table = parse_table

	def set_builder(self, table_builder):
		self._table_builder = table_builder

	def setup(self):
		if not self._initialized:
			_grammar_version = self.field("grammar_version", default=10)
			init_grammar(self.grammar, _grammar_version)

			_parser_logger = self.field("logger", default=_FINAL_REDESIGN_LOGGER)
			self.parser.set_logger(_parser_logger)
			self.parser.set_table(self.parse_table)

			self.table_builder.build_table(self.parse_table)

			_logging_setup_callbacks = initialize_shell()

			DEBUG_MODE = cmd_argument("debug_mode", parser=DEFAULT_CMD_LINE_PARSER)
			ENCODING = "UTF-8"
			USE_LOGGING = cmd_argument("log", parser=DEFAULT_CMD_LINE_PARSER) or DEBUG_MODE
			LOGGING_DIR = cmd_argument("logging_dir", parser=DEFAULT_CMD_LINE_PARSER)
			LOG_FILENAME = cmd_argument("log_filename", parser=DEFAULT_CMD_LINE_PARSER)
			LOGGING_LEVEL = "DEBUG" if DEBUG_MODE else cmd_argument("logging_level", parser=DEFAULT_CMD_LINE_PARSER)

			init_logging(
				use_logging=USE_LOGGING,
				log_filename=LOG_FILENAME,
				logging_dir=LOGGING_DIR,
				logging_level=LOGGING_LEVEL,
				logging_callbacks=_logging_setup_callbacks,
				encoding=ENCODING
			)

			self._initialized = True

	def execute(self, input, context_id=None):
		if not self.is_setup:
			self.setup()
		_parse_context = self.create_context(input, end_symbol=self.field("end_symbol", default="#"), context_id=context_id)
		return self.parser.parse(_parse_context)

	def create_context(self, *args, **kwargs):
		return self.context_factory(*args, **kwargs)

	def context_factory(self, input, end_symbol="$", context_id=None):
		return ParseContext(input=input, end_symbol=end_symbol, context_id=context_id)

	def tokenize(self, input):
		return self.tokenizer.tokenize(input)


if __name__ == "__main__":
	pass
