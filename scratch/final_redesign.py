from collections import deque
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
from pyevent import PyChannel
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
from pyprofiler import profile_callable, SortBy
	
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


class CustomParserActionType(StrEnum):

	__CUSTOM_ACTION_1__ = "__CUSTOM_ACTION_1__"
	__SHORTCUT_1__ = "__SHORTCUT_1__"
	__SHORTCUT_2__ = "__SHORTCUT_2__"
	__ALT__REDUCE__ = "__ALT__REDUCE__"
	__ALT__SHIFT__ = "__ALT__SHIFT__"
	__ALT__SHIFT_2__ = "__ALT__SHIFT_2__"


class Grammar8TokenType(StrEnum):

	NUMBER = "NUMBER"
	PLUS_OP = "+"
	SUB_OP = "-"
	MULT_OP = "*"
	DIV_OP = "/"
	LEFT_PAREN = "("
	RIGHT_PAREN = ")"
	SKIP = ""
	END_SYMBOL = "$"
	OPERATOR = "OPERATOR"


class Grammar8TokenizerHandler(LexHandler):

	def handle(self, tokenizer):
		_add_token_alias = tokenizer.add_token
		_tokenizer_advance_a = tokenizer.advance
		_cond_consume = tokenizer.cond_consume
		_counter = 0
		while tokenizer.can_consume:
			_current_char = tokenizer.current_char

			if _current_char.isdigit():
				_token_val = tokenizer.cond_consume(lambda x, y, z: not x.isdigit())
				_add_token_alias(Grammar8TokenType.NUMBER, _token_val, token_id=f"NUMBER_{_counter}")
				continue

			if _current_char in {" ", "\t", "\n", "\r\n"}:
				_add_token_alias(Grammar8TokenType.SKIP, _current_char, token_id=f"SKIP_{_counter}")
				_tokenizer_advance_a()
				continue

			if _current_char in {"+", "-", "*", "/"}:
				_add_token_alias(Grammar8TokenType.OPERATOR, _current_char, token_id=f"OPERATOR_{_counter}")
				_tokenizer_advance_a()
				continue

			if _current_char:
				match _current_char:
					# case "+":
					# 	_add_token_alias(Grammar8TokenType.PLUS_OP, "+", token_id=f"PLUS_OP_{_counter}")
					# 	_tokenizer_advance_a()
					# 	continue
					# case "-":
					# 	_add_token_alias(Grammar8TokenType.SUB_OP, "-", token_id=f"SUB_OP_{_counter}")
					# 	_tokenizer_advance_a()
					# 	continue
					# case "*":
					# 	_add_token_alias(Grammar8TokenType.MULT_OP, "*", token_id=f"MULT_OP_{_counter}")
					# 	_tokenizer_advance_a()
					# 	continue
					# case "/":
					# 	_add_token_alias(Grammar8TokenType.DIV_OP, "/", token_id=f"DIV_OP_{_counter}")
					# 	_tokenizer_advance_a()
					# 	continue
					case "(":
						_add_token_alias(Grammar8TokenType.LEFT_PAREN, "(", token_id=f"LEFT_PAREN_{_counter}")
						_tokenizer_advance_a()
						continue
					case ")":
						_add_token_alias(Grammar8TokenType.RIGHT_PAREN, ")", token_id=f"RIGHT_PAREN_{_counter}")
						_tokenizer_advance_a()
						continue
					case _:
						_add_token_alias(Grammar8TokenType.SKIP, _current_char, token_id=f"SKIP_{_counter}_non_character")
						_tokenizer_advance_a()
						# _error_details = f"unexpected character: '{_current_char}'; handler ID: '{self.handler_id}' is unable to determine how to tokenize character...please review and try again..."
						# raise RuntimeError(_error_details)
			else:
				break
		_add_token_alias(Grammar8TokenType.END_SYMBOL, "$", token_id="END_SYMBOL")
		_counter += 1


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
	INVALID = "INVALID"
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
						_add_token_alias(Grammar9TokenType.INVALID, _current_char, token_id=None)
						_tokenizer_advance_a()
						# _error_details = f"unexpected character: '{_current_char}'; handler is unable to determine how to tokenize character...please review and try again..."
						# raise RuntimeError(_error_details)
			else:
				break
		_add_token_alias(Grammar9TokenType.HASHTAG_END, "#", token_id=None)


class DateGrammarTokenType(StrEnum):

	FSLASH_DELIM = "slash_delim"
	HYPHEN_DELIM = "hyphen_delim"
	PERIOD_DELIM = "dot_delim"
	MONTH = "month"
	DAY = "day"
	YEAR = "year"
	WS = "WS"
	SKIP = "SKIP"
	END_SYMBOL = "HASHTAG_END"


class DateGrammarTokenizerHandler(LexHandler):
	
	"""
  	VALID 'DateGrammarTokenType.FSLASH_DELIM' VALUE:
	  |
	  |
	  |
	  • -----> LiteralString -> '/'


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
	  • -----> List[int] -> [2000-2030]


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
		_counter = 0
		while tokenizer.can_consume:
			_current_char = tokenizer.current_char
			_curr_count = _counter
			_counter += 1
			
			if _current_char in {" ", "\n", "\t", "\r\n"}:
				tokenizer.cond_consume(lambda curr_chr, lexeme, scanner: curr_chr not in {" ", "\n", "\t", "\r\n"})
				continue

			if _current_char.isdigit():
				if not _month_lexed:
					_month_token_val = tokenizer.cond_consume(lambda curr_char, lexeme, scanner: not curr_char.isdigit())
					_add_token_alias(DateGrammarTokenType.MONTH, _month_token_val, token_id=None)
					_month_lexed = True
				elif not _day_lexed:
					_day_token_val = tokenizer.cond_consume(lambda curr_char, lexeme, scanner: not curr_char.isdigit())
					_add_token_alias(DateGrammarTokenType.DAY, _day_token_val, token_id=None)
					_day_lexed = True
				elif not _year_lexed:
					_year_token_val = tokenizer.cond_consume(lambda curr_char, lexeme, scanner: not curr_char.isdigit())
					_add_token_alias(DateGrammarTokenType.YEAR, _year_token_val, token_id=None)
					_year_lexed = True
				else:
					_error_details = f"error tokenizing number-like symbol; please review and try again..."
					raise RuntimeError(_error_details)
				continue

			if _current_char.isalpha():
				_add_token_alias(DateGrammarTokenType.SKIP, _current_char, token_id=f"SKIP_{_curr_count}")
				_tokenizer_advance_a()

			match _current_char:
				case ".":
					_add_token_alias(self._token_mapping[_current_char], _current_char, token_id=None)
				case "/":
					_add_token_alias(self._token_mapping[_current_char], _current_char, token_id=None)
				case _:
					_add_token_alias(DateGrammarTokenType.SKIP, _current_char, token_id=f"SKIP_{_curr_count}")
					_tokenizer_advance_a()
			_tokenizer_advance_a()


		_add_token_alias(self._token_mapping[self._end_symbol], self._end_symbol, token_id=None)


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


class Grammar8TableBuilder(TableBuilder):

	def build_table(self, table):
		INIT_RULE = self.grammar.select(RuleIDSelector("INIT_RULE"))[0]
		E_1 = self.grammar.select(RuleIDSelector("E_1"))[0]
		E_2 = self.grammar.select(RuleIDSelector("E_2"))[0]
		B_1 = self.grammar.select(RuleIDSelector("B_1"))[0]
		B_2 = self.grammar.select(RuleIDSelector("B_2"))[0]
		C_1 = self.grammar.select(RuleIDSelector("C_1"))[0]
		number = self.grammar.select(RuleIDSelector("number"))[0]
		operator_1 = self.grammar.select(RuleIDSelector("operator_1"))[0]
		operator_2 = self.grammar.select(RuleIDSelector("operator_2"))[0]
		operator_3 = self.grammar.select(RuleIDSelector("operator_3"))[0]
		operator_4 = self.grammar.select(RuleIDSelector("operator_4"))[0]

		_init_rule_head = INIT_RULE.rule_head


		# STATE 0:
		table.add_action((0, "("), (ParserActionType.SHIFT, 4))
		table.add_action((0, "NUMBER"), (ParserActionType.SHIFT, 5))
		table.add_goto((0, "number"), (1, B_2))
		table.add_goto((0, "C"), (3, B_1))
		table.add_goto((0, "B"), (6, E_2))
		table.add_goto((0, "E"), (2, E_2))

		# STATE 1:
		# table.add_action((1, "number"), (ParserActionType.REDUCE, B_2))
		table.add_action((1, "+"), (ParserActionType.REDUCE, B_2))
		table.add_action((1, "-"), (ParserActionType.REDUCE, B_2))
		table.add_action((1, "*"), (ParserActionType.REDUCE, B_2))
		table.add_action((1, "/"), (ParserActionType.REDUCE, B_2))
		table.add_action((1, ")"), (ParserActionType.REDUCE, B_2))

		# STATE 2:
		table.add_action((2, _init_rule_head), (ParserActionType.ACCEPT, None))
		# table.add_action((2, "+"), (ParserActionType.SHIFT, 7))
		table.add_action((2, "+"), (CustomParserActionType.__ALT__SHIFT__, 7))
		table.add_action((2, "-"), (ParserActionType.SHIFT, 7))
		table.add_action((2, ")"), (CustomParserActionType.__ALT__SHIFT__, 14))
		# table.add_action((2, ")"), (ParserActionType.REDUCE, E_1))
		# table.add_action((2, "*"), (ParserActionType.SHIFT, 7))
		table.add_action((2, "*"), (CustomParserActionType.__ALT__SHIFT__, 7))
		table.add_action((2, "/"), (ParserActionType.SHIFT, 7))
		table.add_goto((2, "E"), (7, E_1))
		table.add_goto((2, "B"), (10, E_1))


		# STATE 3:
		table.add_action((3, _init_rule_head), (ParserActionType.REDUCE, B_1))
		# table.add_action((3, "+"), (ParserActionType.REDUCE, B_1))
		table.add_action((3, "+"), (ParserActionType.REDUCE, E_2))
		table.add_action((3, "-"), (ParserActionType.REDUCE, B_1))
		table.add_action((3, "/"), (ParserActionType.REDUCE, B_1))
		table.add_action((3, ")"), (ParserActionType.REDUCE, B_2))


		# STATE 4:
		table.add_action((4, "*"), (ParserActionType.REDUCE, C_1))
		table.add_action((4, "("), (ParserActionType.SHIFT, 12))
		table.add_action((4, ")"), (ParserActionType.REDUCE, C_1))
		# table.add_action((4, "+"), (ParserActionType.REDUCE, C_1))
		table.add_action((4, "+"), (ParserActionType.REDUCE, E_2))
		# table.add_action((4, "/"), (ParserActionType.REDUCE, C_1))
		# table.add_action((4, "/"), (ParserActionType.REDUCE, C_1))
		table.add_action((4, "/"), (ParserActionType.REDUCE, B_1))
		table.add_action((4, "NUMBER"), (ParserActionType.SHIFT, 5))
		# table.add_action((4, "NUMBER"), (CustomParserActionType.__SHORTCUT_2__, 2))
		table.add_goto((4, "number"), (12, E_1))
		table.add_goto((4, "E"), (2, E_1))
		# table.add_goto((4, "E"), (7, E_1))
		table.add_goto((4, "B"), (6, E_1))
		table.add_goto((4, "C"), (14, E_1))

		# STATE 5:
		table.add_action((5, "*"), (ParserActionType.REDUCE, number))
		table.add_action((5, "/"), (ParserActionType.REDUCE, number))
		table.add_action((5, "+"), (ParserActionType.REDUCE, number))
		table.add_action((5, "-"), (ParserActionType.REDUCE, number))
		table.add_action((5, ")"), (ParserActionType.REDUCE, number))
		table.add_action((5, _init_rule_head), (ParserActionType.REDUCE, number))
		table.add_action((5, "NUMBER"), (ParserActionType.REDUCE, number))
		table.add_action((5, Grammar8TokenType.OPERATOR), (CustomParserActionType.__ALT__REDUCE__, number))

		# STATE 6:
		table.add_action((6, "+"), (ParserActionType.REDUCE, E_2))
		# table.add_action((6, "+"), (ParserActionType.REDUCE, C_1))
		table.add_action((6, "-"), (ParserActionType.REDUCE, E_2))
		table.add_action((6, "*"), (ParserActionType.REDUCE, E_2))
		table.add_action((6, "/"), (ParserActionType.REDUCE, E_2))
		table.add_action((6, _init_rule_head), (ParserActionType.REDUCE, E_2))
		# table.add_action((6, ")"), (ParserActionType.REDUCE, E_1))
		table.add_action((6, ")"), (ParserActionType.REDUCE, E_2))

		# STATE 7:
		table.add_action((7, "*"), (ParserActionType.SHIFT, 7))
		table.add_action((7, "/"), (ParserActionType.SHIFT, 4))
		table.add_action((7, "+"), (ParserActionType.SHIFT, 4))
		table.add_action((7, "("), (ParserActionType.SHIFT, 4))
		table.add_action((7, ")"), (ParserActionType.REDUCE, E_1))
		table.add_action((7, "NUMBER"), (ParserActionType.SHIFT, 5))
		table.add_action((7, "number"), (ParserActionType.SHIFT, 1))
		table.add_goto((7, "number"), (14, E_2))
		table.add_goto((7, "B"), (13,))
		table.add_goto((7, "E"), (13,))
		table.add_goto((7, "C"), (12,))
		table.add_goto((7, _init_rule_head), (ParserActionType.ERROR, None))

		# STATE 8:

		# STATE 9:

		# STATE 10:
		# table.add_action((10, "NUMBER"), (ParserActionType.SHIFT, 5))
		# table.add_goto((10, "number"), (6, E_2.copy().advance_by(1)))
		# table.add_goto((10, "E"), (6, E_2.copy().advance_by(1)))

		# STATE 11:

		# STATE 12:
		table.add_action((12, "NUMBER"), (ParserActionType.SHIFT, 5))
		table.add_action((12, "+"), (ParserActionType.REDUCE, E_2))
		table.add_action((12, "-"), (ParserActionType.REDUCE, B_2))
		table.add_action((12, "*"), (ParserActionType.REDUCE, B_2))
		# table.add_action((12, "*"), (ParserActionType.REDUCE, E_1))  # Switched from B_2 -> E_1
		table.add_action((12, "/"), (ParserActionType.REDUCE, B_2))
		table.add_action((12, ")"), (ParserActionType.REDUCE, B_1))
		table.add_action((12, _init_rule_head), (ParserActionType.REDUCE, B_1))
		table.add_action((12, "("), (ParserActionType.SHIFT, 4))
		table.add_goto((12, "number"), (1, number))
		table.add_goto((12, "B"), (6, E_2))
		table.add_goto((12, "E"), (7, C_1))

		# STATE 13:
		table.add_action((13, _init_rule_head), (ParserActionType.REDUCE, C_1))
		table.add_action((13, "+"), (ParserActionType.REDUCE, C_1))
		table.add_action((13, "-"), (ParserActionType.REDUCE, C_1))
		table.add_action((13, "NUMBER"), (ParserActionType.REDUCE, E_2))
		table.add_action((13, ")"), (ParserActionType.REDUCE, E_1))
		# table.add_action((13, ")"), (ParserActionType.REDUCE, E_2))
		# table.add_action((13, ")"), (ParserActionType.REDUCE, C_1))
		table.add_action((13, "*"), (ParserActionType.REDUCE, E_2))
		table.add_action((13, "/"), (ParserActionType.REDUCE, C_1))
		
		# STATE 14:
		# table.add_action((14, "*"), (ParserActionType.REDUCE, B_2))
		table.add_action((14, "*"), (ParserActionType.SHIFT, 5))
		table.add_action((14, "-"), (ParserActionType.REDUCE, C_1))
		# table.add_action((14, "+"), (ParserActionType.REDUCE, C_1))
		table.add_action((14, "+"), (CustomParserActionType.__ALT__SHIFT_2__, 4, B_2))
		# table.add_action((14, "/"), (ParserActionType.REDUCE, C_1))
		table.add_action((14, "/"), (CustomParserActionType.__ALT__SHIFT_2__, 4, B_1))
		# table.add_action((14, "NUMBER"), (ParserActionType.REDUCE, B_2))
		table.add_action((14, "NUMBER"), (ParserActionType.SHIFT, 5))
		table.add_action((14, ")"), (CustomParserActionType.__ALT__SHIFT_2__, 6, E_2))
		table.add_action((14, _init_rule_head), (ParserActionType.REDUCE, C_1))
		table.add_goto((14, "number"), (3, B_2))
		table.add_goto((14, "B"), (6, B_2))
		table.add_goto((14, "E"), (7,))


class Grammar9TableBuilder(TableBuilder):

	def build_table(self, table):
		"""
		# INIT_RULE = self.grammar.select(RuleIDSelector("INIT_RULE"))[0]
		# S_rule_1 = self.grammar.select(RuleIDSelector("S_rule_1"))[0]
		# S_rule_2 = self.grammar.select(RuleIDSelector("S_rule_2"))[0]
		# S_rule_3 = self.grammar.select(RuleIDSelector("S_rule_3"))[0]
		# A_rule_1 = self.grammar.select(RuleIDSelector("A_rule_1"))[0]
		# B_rule_1 = self.grammar.select(RuleIDSelector("B_rule_1"))[0]
		# # B_rule_2 = self.grammar.select(RuleIDSelector("B_rule_2"))[0]
		# C_rule_1 = self.grammar.select(RuleIDSelector("C_rule_1"))[0]

		# # STATE 0:
		# # table.add_action((0, "a"), (ParserActionType.SHIFT, 2))
		# # table.add_goto((0, "S"), (1, INIT_RULE.copy().advance_by(1)))

		# table.add_action((0, "a"), (ParserActionType.SHIFT, 4))
		# table.add_action((0, "("), (ParserActionType.SHIFT, 1))
		# table.add_goto((0, "S"), (1, INIT_RULE.copy().advance_by(1)))
		# table.add_goto((0, "C"), (1, S_rule_3.copy().advance_by(1)))



		# # STATE 1:
		# # table.add_action((1, "#"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))
		# # table.add_action((1, "b"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))
		# # table.add_action((1, "!"), (ParserActionType.SHIFT, 3))

		# table.add_action((1, "#"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))
		# table.add_action((1, "a"), (ParserActionType.SHIFT, 4))
		# # table.add_action((1, "b"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))
		# table.add_action((1, "!"), (ParserActionType.SHIFT, 3))
		# table.add_goto((1, "S"), (5, C_rule_1.copy().advance_by(2)))

		# # STATE 2:
		# # table.add_action((2, "b"), (ParserActionType.SHIFT, 4))
		# # table.add_goto((2, "A"), (8, S_rule_1.copy().advance_by(2)))
		# # table.add_goto((2, "B"), (5, B_rule_1.copy().advance_by(1)))
		# # # table.add_goto((2, "C"), (6, B_rule_2.copy().advance_by(1)))
		# # table.add_action((2, "("), (ParserActionType.SHIFT, 7))
		
		# table.add_action((2, "b"), (ParserActionType.SHIFT, 4))
		# table.add_goto((2, "A"), (8, S_rule_1.copy().advance_by(2)))
		# table.add_goto((2, "B"), (5, B_rule_1.copy().advance_by(1)))
		# # table.add_goto((2, "C"), (6, B_rule_2.copy().advance_by(1)))
		# table.add_action((2, "("), (ParserActionType.SHIFT, 7))
		
		# # STATE 3:
		# table.add_action((3, "#"), (ParserActionType.REDUCE, S_rule_2.copy().advance_by(2)))

		# # STATE 4:
		# # table.add_action((4, "#"), (ParserActionType.REDUCE, B_rule_1.copy().advance_by(1)))
		
		# table.add_action((4, "b"), (ParserActionType.SHIFT, 8))

		# # STATE 5:
		# table.add_action((5, "#"), (ParserActionType.REDUCE, A_rule_1.copy().advance_by(1)))

		# table.add_action((5, ")"), (ParserActionType.SHIFT, 10))
		# table.add_action((5, "!"), (ParserActionType.SHIFT, 6))

		# # STATE 6:
		# # table.add_action((6, "#"), (ParserActionType.REDUCE, B_rule_2.copy().advance_by(1)))

		# table.add_action((6, ")"), (ParserActionType.REDUCE, S_rule_2.copy().advance_by(2)))

		# # STATE 7:
		# table.add_action((7, "a"), (ParserActionType.SHIFT, 2))

		# # STATE 8:
		# table.add_action((8, "#"), (ParserActionType.REDUCE, B_rule_1.copy().advance_by(1)))
		# table.add_action((8, "b"), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(3)))
		# # table.add_action((8, "!"), (ParserActionType.REDUCE, B_rule_1.copy().advance_by(1)))

		# # STATE 9:
		# # table.add_action((9, ")"), (ParserActionType.SHIFT, 10))

		# table.add_action((9, ")"), (ParserActionType.SHIFT, 10))
		# table.add_action((9, "#"), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(2)))


		# # STATE 10:
		# table.add_action((10, "#"), (ParserActionType.REDUCE, C_rule_1.copy().advance_by(3)))
		"""


		INIT_RULE = self.grammar.select(RuleIDSelector("INIT_RULE"))[0]
		S_rule_1 = self.grammar.select(RuleIDSelector("S_rule_1"))[0]
		S_rule_2 = self.grammar.select(RuleIDSelector("S_rule_2"))[0]
		S_rule_3 = self.grammar.select(RuleIDSelector("S_rule_3"))[0]
		A_rule_1 = self.grammar.select(RuleIDSelector("A_rule_1"))[0]
		B_rule_1 = self.grammar.select(RuleIDSelector("B_rule_1"))[0]
		C_rule_1 = self.grammar.select(RuleIDSelector("C_rule_1"))[0]

		# STATE 0:
		table.add_action((0, "a"), (ParserActionType.SHIFT, 4))
		table.add_action((0, "("), (ParserActionType.SHIFT, 1))
		table.add_goto((0, "S"), (1, INIT_RULE.copy().advance_by(1)))
		table.add_goto((0, "C"), (1, S_rule_3.copy().advance_by(1)))

		# STATE 1:
		table.add_action((1, "#"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))
		table.add_action((1, "a"), (ParserActionType.SHIFT, 4))
		table.add_action((1, "!"), (ParserActionType.SHIFT, 3))
		table.add_goto((1, "S"), (5, C_rule_1.copy().advance_by(2)))

		# STATE 2:
		table.add_action((2, "b"), (ParserActionType.SHIFT, 4))
		table.add_goto((2, "A"), (8, S_rule_1.copy().advance_by(2)))
		table.add_goto((2, "B"), (5, B_rule_1.copy().advance_by(1)))
		table.add_action((2, "("), (ParserActionType.SHIFT, 7))
		
		# STATE 3:
		table.add_action((3, "#"), (ParserActionType.REDUCE, S_rule_2.copy().advance_by(2)))
		table.add_action((3, "!"), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(2)))
		table.add_action((3, ")"), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(2)))

		# STATE 4:
		table.add_action((4, "b"), (ParserActionType.SHIFT, 8))
		table.add_goto((4, "B"), (3, S_rule_2.copy().advance_by(1)))

		# STATE 5:
		table.add_action((5, "#"), (ParserActionType.REDUCE, A_rule_1.copy().advance_by(1)))
		table.add_action((5, ")"), (ParserActionType.SHIFT, 10))
		table.add_action((5, "!"), (ParserActionType.SHIFT, 6))

		# STATE 6:
		table.add_action((6, ")"), (ParserActionType.REDUCE, S_rule_2.copy().advance_by(2)))

		# STATE 7:
		table.add_action((7, "a"), (ParserActionType.SHIFT, 2))

		# STATE 8:
		table.add_action((8, "#"), (ParserActionType.REDUCE, B_rule_1.copy().advance_by(1)))
		table.add_action((8, "!"), (ParserActionType.REDUCE, B_rule_1.copy().advance_by(1)))
		table.add_action((8, ")"), (ParserActionType.REDUCE, B_rule_1.copy().advance_by(1)))

		# STATE 9:
		table.add_action((9, ")"), (ParserActionType.SHIFT, 10))
		table.add_action((9, "#"), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(2)))

		# STATE 10:
		table.add_action((10, "#"), (ParserActionType.REDUCE, C_rule_1.copy().advance_by(3)))


class DateGrammarTableBuilder(TableBuilder):

	def build_table(self, table):
		INIT_RULE = self.grammar.select(RuleIDSelector("INIT_RULE"))[0]
		_date_rule = self.grammar.select(RuleIDSelector("date"))[0]
		_slash_delim = self.grammar.select(RuleIDSelector("slash_delim"))[0]
		_hyphen_delim = self.grammar.select(RuleIDSelector("hyphen_delim"))[0]
		_dot_delim = self.grammar.select(RuleIDSelector("dot_delim"))[0]

		# table.add_action((), ())
		# table.add_goto((), ())

		# STATE 0:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "month"), (ParserActionType.SHIFT, 2))

		# STATE 1:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))

		# STATE 2:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "month"), (ParserActionType.SHIFT, 2))

		# STATE 3:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "month"), (ParserActionType.SHIFT, 2))

		# STATE 4:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "month"), (ParserActionType.SHIFT, 2))

		# STATE 5:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "month"), (ParserActionType.SHIFT, 2))

		# STATE 6:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "month"), (ParserActionType.SHIFT, 2))

		# STATE 7:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "month"), (ParserActionType.SHIFT, 2))

		# STATE 8:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "month"), (ParserActionType.SHIFT, 2))

		# STATE 9:
		table.add_action((0, "date"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "month"), (ParserActionType.SHIFT, 2))


"""
class CoreParser3(CoreParser2):

	def __init__(self, init_state=0, grammar=None, parse_table=None, debug_mode=False, parser_id=None):
		super().__init__(init_state=init_state, grammar=grammar, parse_table=parse_table, debug_mode=debug_mode, parser_id=parser_id)
	# 	self._channel = PyChannel(channel_id=parser_id)

	# def register(self, action, receiver=None, receiver_id=None):
	# 	self._channel.register(action, receiver=receiver, receiver_id=receiver_id)

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
		_parse_stack = parse_context.stack
		_parse_sym_stack = parse_context.symbol_stack
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


			if (len(_parse_sym_stack) >= 2 and _parse_sym_stack[-2] == "a") and (_parse_sym_stack[-1] == "b"):
				_action_info = self.parse_table.action((parse_context.state(), _parse_sym_stack[-1]), default=(ParserActionType.ERROR, None))


			_action = _action_info[0]

			# self._channel.emit(_action, self, parse_context, _action_info)

			if self.debug_mode:
				print(f"• ACTION INFO:")
				print(f"\t{_action_info}\n")

			# NOTE: possibly use match/case syntax here
			if _action == ParserActionType.ERROR:
				parse_context.set_result(False)
			elif _action == ParserActionType.SHIFT:
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
				# if _current_state == 0 and _current_symbol == "a":
				# 	_next_input_char = parse_context.peek(offset=1)
				# 	if _next_input_char == "b":
				# 		parse_context.append_state(9)
				# 		parse_context.append_symbol("A")
				# 		parse_context.advance()

				# 		self.logger.submit_log(
				# 			message=f"Since the current state of the parser is 0/'a' (CURRENT-STATE/CURRENT-SYMBOL) and since the next input symbol is a 'b', Performing shortcut SHORTCUT SHIFT action",
				# 			new_state=f"PARSE CONTEXT ID: {parse_context.context_id} ---> (9/A)",
				# 			log_type=LogType.DEBUG
				# 			)
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
"""


class CoreParser3(CoreParser2):

	def __init__(self, init_state=0, grammar=None, parse_table=None, debug_mode=False, parser_id=None):
		super().__init__(init_state=init_state, grammar=grammar, parse_table=parse_table, debug_mode=debug_mode, parser_id=parser_id)
		self._channel = PyChannel(channel_id=parser_id)
		self.init_parser()

	def init_parser(self):
		# Standard LR Parser Actions (SHIFT/REDUCE/ACCEPT/ERROR)
		self.register(ParserActionType.SHIFT, self.__SHIFT__)
		self.register(ParserActionType.ACCEPT, self.__ACCEPT__)
		self.register(ParserActionType.ERROR, self.__ERROR__)
		self.register(ParserActionType.REDUCE, self.__REDUCE__)
		
		# Custom LR Parser Actions
		# self.register(CustomParserActionType.__REDUCE_2__, self.__REDUCE_2__)

	def register(self, action_type, receiver=None, receiver_id=None):
		self._channel.register(action_type, receiver=receiver, receiver_id=receiver_id)

	def parse(self, parse_context):
		# NOTE: remove below (up unti' series of consecutive '#'s) code as it's for coloring terminal debug output		
		parse_context.set_parser(self)
		parse_context.append_state(self.init_state)
		_action_type, _action_info = self.next_action(parse_context)
		while True:
			self._channel.emit(_action_type, *parse_context.action_info())
			_action_type, _action_info = self.next_action(parse_context)
			if parse_context.done_parsing:
				break
		return parse_context

	def next_action(self, parse_context):
		_current_state = parse_context.state()
		_current_symbol = parse_context.current_symbol().token_type
		_action_info = self.parse_table.action((_current_state, _current_symbol), default=(ParserActionType.ERROR, None))
		parse_context.set_action(_action_info)
		return _action_info

	def __REDUCE__(self, parse_context, action_info):
		_reduce_item = action_info[1]
		for _ in range(_reduce_item.rule_size):
			parse_context.pop_state()
			parse_context.pop_symbol()
		_goto_key = (parse_context.state(), _reduce_item.rule_head)
		_goto_state = parse_context.parser.parse_table.goto(_goto_key)
		_next_state = _goto_state[0]
		parse_context.append_state(_next_state)
		parse_context.append_symbol(_reduce_item.rule_head)

	def __SHIFT__(self, parse_context, action_info):
		parse_context.append_state(action_info[1])
		parse_context.append_symbol(parse_context.current_symbol().token_val)
		parse_context.advance()

	def __ACCEPT__(self, parse_context, action_info):
		parse_context.set_result(True)

	def __REDUCE_2__(self, parse_context, action_info):
		pass

	def __ERROR__(self, parse_context, action_info):
		parse_context.set_result(False)


class CoreParser4(CoreParser2):

	__slots__ = ("_channel")

	def __init__(self, init_state=0, grammar=None, parse_table=None, debug_mode=False, parser_id=None):
		super().__init__(init_state=init_state, grammar=grammar, parse_table=parse_table, debug_mode=debug_mode, parser_id=parser_id)
		self._channel = PyChannel(channel_id=parser_id)

	def register(self, action_type, receiver=None, receiver_id=None):
		self._channel.register(action_type, receiver=receiver, receiver_id=receiver_id)


class Grammar8Parser(CoreParser4):

	def __init__(self, init_state=0, grammar=None, parse_table=None, debug_mode=False, parser_id=None):
		super().__init__(init_state=init_state, grammar=grammar, parse_table=parse_table, debug_mode=debug_mode, parser_id=parser_id)
		self.precedence = {
			"+": 0,
			"-": 0,
			"*": 1,
			"/": 1
		}
		self.init_parser()

	def init_parser(self):
		# Standard LR Parser Actions (SHIFT/REDUCE/ACCEPT/ERROR)
		self.register(ParserActionType.SHIFT, self.__SHIFT__)
		self.register(ParserActionType.ACCEPT, self.__ACCEPT__)
		self.register(ParserActionType.ERROR, self.__ERROR__)
		self.register(ParserActionType.REDUCE, self.__REDUCE__)
		
		# Custom LR Parser Actions
		self.register(CustomParserActionType.__CUSTOM_ACTION_1__, self.__CUSTOM_ACTION_1__)
		self.register(CustomParserActionType.__SHORTCUT_1__, self.__SHORTCUT_1__)
		self.register(CustomParserActionType.__SHORTCUT_2__, self.__SHORTCUT_2__)
		self.register(CustomParserActionType.__ALT__REDUCE__, self.__ALT__REDUCE__)
		self.register(CustomParserActionType.__ALT__SHIFT__, self.__ALT__SHIFT__)
		self.register(CustomParserActionType.__ALT__SHIFT_2__, self.__ALT__SHIFT_2__)

		# Token type Parser Actions (Syntactical/Semantical)
		self.register(Grammar8TokenType.PLUS_OP, self.test_plus_op)
		self.register(Grammar8TokenType.RIGHT_PAREN, self.test_right_paren)
		self.register(Grammar8TokenType.END_SYMBOL, self.test_end_symbol)

	def __REDUCE__(self, parse_context, action_info):
		_reduce_item = action_info[0]
		for _ in range(_reduce_item.rule_size):
			_state = parse_context.pop_state()
			_symbol = parse_context.pop_symbol()
			print(f"POP STATE ---> {_state}")
			print(f"POP SYMBOL ---> {_symbol}")
		# print(parse_context.stack)
		# print(parse_context.symbol_stack)
		_goto_key = (parse_context.state(), _reduce_item.rule_head)
		print(f"GOTO KEY ---> {underline_text(bold_text(_goto_key))}")
		print()
		_goto_state = parse_context.parser.parse_table.goto(_goto_key)
		_next_state = _goto_state[0]
		parse_context.append_state(_next_state)
		parse_context.append_symbol(_reduce_item.rule_head)

	def __SHIFT__(self, parse_context, action_info):
		parse_context.append_state(action_info[0])
		parse_context.append_symbol(str(parse_context.current_symbol().token_type))
		parse_context.advance()

	def __ACCEPT__(self, parse_context, action_info):
		parse_context.set_result(True)

	def __ERROR__(self, parse_context, action_info):
		parse_context.set_result(False)

	def __CUSTOM_ACTION_1__(self, parse_context, action_info):
		print(f"SHIFTING!")
		self.__SHIFT__(parse_context, action_info)

	def __SHORTCUT_1__(self, parse_context, action_info):
		_peeked_token = parse_context.peek()
		# print(apply_color(208, f"PEEKING:"))
		# print(apply_color(208, f"\tTOKEN TYPE ---> {_peeked_token.token_type}"))
		# print(apply_color(208, f"\tTOKEN VALUE ---> {_peeked_token.token_val}"))
		print(f"PERFORMING REDUCE FOR TEST SHORTCUT ACTION 1")
		print()
		self.__REDUCE__(parse_context, action_info)

	def __SHORTCUT_2__(self, parse_context, action_info):
		_peeked_token = parse_context.peek()
		# print(apply_color(208, f"PEEKING:"))
		# print(apply_color(208, f"\tTOKEN TYPE ---> {_peeked_token.token_type}"))
		# print(apply_color(208, f"\tTOKEN VALUE ---> {_peeked_token.token_val}"))
		# print(apply_color(208, f"\tACTION INFO ---> {action_info}"))
		print(f"PERFORMING REDUCE FOR TEST SHORTCUT ACTION 2")
		print()
		self.__SHIFT__(parse_context, (action_info[0], action_info[1]))
		parse_context.pop_symbol()
		parse_context.append_symbol("E")

	def __ALT__REDUCE__(self, parse_context, action_info):
		_peeked_token = parse_context.peek(offset=0)
		# if _peeked_token == ")":
		# 	parse_context
		print(apply_color(208, f"PEEKING SHIT:"))
		print(apply_color(208, f"\tTOKEN TYPE ---> {_peeked_token.token_type}"))
		print(apply_color(208, f"\tTOKEN VALUE ---> {_peeked_token.token_val}"))
		# print(apply_color(208, f"\tACTION INFO ---> {action_info}"))
		print()
		print(f"PERFORMING ALT REDUCE TEST ACTION 1")
		print(f"ACTION INFO: {action_info}")
		self.__REDUCE__(parse_context, action_info)
		parse_context.pop_symbol()
		parse_context.append_symbol("E")

	def __ALT__SHIFT__(self, parse_context, action_info):
		_peeked_token = parse_context.peek(offset=0)
		# print(apply_color(208, f"\tTOKEN TYPE ---> {_peeked_token.token_type}"))
		# print(apply_color(208, f"\tTOKEN VALUE ---> {_peeked_token.token_val}"))
		# print(apply_color(208, f"\tACTION INFO ---> {action_info}"))
		# print()
		if parse_context.state() == 2 and len(parse_context.symbol_stack) >= 3 and [parse_context.symbol_stack[-3], parse_context.symbol_stack[-2], parse_context.symbol_stack[-1]] in [["E", "+", "E"], ["E", "-", "E"], ["E", "*", "E"], ["E", "/", "E"]]:
			print(apply_color(208, f"PERFORMING ALT SHIFT TEST ACTION 1"))
			for _ in range(3):
				parse_context.pop_symbol()
				parse_context.pop_state()
			parse_context.append_state(action_info[0])
			parse_context.append_symbol("E")
		else:
			self.__SHIFT__(parse_context, action_info)
		# self.__SHIFT__(parse_context, action_info)
		# print(f"STATE STACK AFTER ALT SHIFT TEST ACTION 1")

	def __ALT__SHIFT_2__(self, parse_context, action_info):
		_peeked_token = parse_context.peek(offset=0)
		# print(apply_color(208, f"\tTOKEN TYPE ---> {_peeked_token.token_type}"))
		# print(apply_color(208, f"\tTOKEN VALUE ---> {_peeked_token.token_val}"))
		# print(apply_color(208, f"\tACTION INFO ---> {action_info}"))
		# print()

		if parse_context.state() == 14 and len(parse_context.symbol_stack) >= 1 and parse_context.symbol_stack[-1] in ("number", "C"):
			print(apply_color(208, f"PERFORMING ALT SHIFT TEST ACTION 2.1"))
			print(apply_color(208, f"ACTION INFO IN 2.1 ---> {action_info}"))
			print()
			for _ in range(1):
				parse_context.pop_symbol()
				parse_context.pop_state()
			parse_context.append_state(action_info[0])
			parse_context.append_symbol(action_info[1].rule_head)
		elif parse_context.state() == 14 and len(parse_context.symbol_stack) >= 3 and [parse_context.symbol_stack[-3], parse_context.symbol_stack[-2], parse_context.symbol_stack[-1]] == ["(", "E", ")"]:
			print(apply_color(208, f"PERFORMING ALT SHIFT TEST ACTION 2.2"))
			print(apply_color(208, f"ACTION INFO IN 2.2 ---> {action_info}"))
			print()
			for _ in range(3):
				parse_context.pop_symbol()
				parse_context.pop_state()
			parse_context.append_state(action_info[0])
			parse_context.append_symbol("C")
		elif parse_context.state() == 14 and len(parse_context.symbol_stack) >= 3 and [parse_context.symbol_stack[-3], parse_context.symbol_stack[-2], parse_context.symbol_stack[-1]] == ["(", "C", ")"]:
			print(apply_color(208, f"PERFORMING ALT SHIFT TEST ACTION 2.3"))
			print(apply_color(208, f"ACTION INFO IN 2.3 ---> {action_info}"))
			print()
			for _ in range(3):
				parse_context.pop_symbol()
				parse_context.pop_state()
			parse_context.append_state(action_info[0])
			parse_context.append_symbol("C")
		elif parse_context.state() == 14 and len(parse_context.symbol_stack) >= 3 and (parse_context.symbol_stack[-3] == "C"):
			print(apply_color(208, f"PERFORMING ALT SHIFT TEST ACTION 2.4"))
			print(apply_color(208, f"ACTION INFO IN 2.4 ---> {action_info}"))
			print()
			parse_context.pop_symbol()
			parse_context.pop_state()
			parse_context.append_state(6)
			parse_context.append_symbol("B")
		else:
			self.__SHIFT__(parse_context, action_info)
		# self.__SHIFT__(parse_context, action_info)
		# print(f"STATE STACK AFTER ALT SHIFT TEST ACTION 1")

	def test_plus_op(self, parser, parse_context):
		print(f"HELLO MOTO!!!")
		print(f"CURRENT SYMBOL ---> {parse_context.current_symbol().token_type}")

	def test_right_paren(self, parser, parse_context):
		print(f"GOODBYE MOTO!!!")
		print(f"CURRENT SYMBOL ---> {parse_context.current_symbol().token_type}")
		if parse_context.state() == 2:
			print(apply_color(9, f"SKIPPING CLOSING RIGHT PAREN IN STATE ---> 2"))
			print(parse_context.action_info())
			parse_context.advance()
			if parse_context.current_symbol().token_type == Grammar8TokenType.END_SYMBOL:
				parse_context.set_result(True)

	def test_end_symbol(self, parser, parse_context):
		print(f"SHITTTTT")

	def parse(self, parse_context):
		# NOTE: remove below (up unti' series of consecutive '#'s) code as it's for coloring terminal debug output		
		parse_context.set_parser(self)
		parse_context.append_state(self.init_state)
		_action_type = self.next_action(parse_context)
		while not parse_context.done_parsing:
			_token_type = parse_context.current_symbol().token_type
			print(f"STATE: {parse_context.state()}")
			print(f"\tcurrent_symbol: {parse_context.current_symbol().token_type}")
			print(f"\tACTION TYPE: {_action_type}")
			print(f"\t\tSTACK ---> {parse_context.stack}")
			print(f"\t\tSYMBOL STACK ---> {parse_context.symbol_stack}")
			print()
			# self._channel.emit(_token_type, self, parse_context)
			self._channel.emit(_action_type, *parse_context.action_info())
			_action_type = self.next_action(parse_context)
		return parse_context

	def next_action(self, parse_context):
		_current_state = parse_context.state()
		_current_symbol = parse_context.current_symbol().token_type
		# _current_symbol = parse_context.current_symbol().token_val
		_action_info = self.parse_table.action((_current_state, _current_symbol), default=(ParserActionType.ERROR, None))
		parse_context.set_action(_action_info[1:])
		return _action_info[0]


class Grammar8Parser2_0(CoreParser2):

	__slots__ = ("_handlers", "_stop_flag")
	def __init__(self, init_state=0, grammar=None, parse_table=None, debug_mode=False, parser_id=None):
		super().__init__(init_state=init_state, grammar=grammar, parse_table=parse_table, debug_mode=debug_mode, parser_id=parser_id)
		self._handlers = {}
		self._stop_flag = False

	def add_handler(self, handler, handler_id=None, overwrite=False):
		_handler_id = handler.__name__ if handler_id is None else handler_id
		if _handler_id not in self._handlers or overwrite:
			self._handlers[_handler_id] = handler

	def remove_handler(self, handler_id):
		self._handlers.pop(handler_id)

	def stop(self):
		self._stop_flag = True

	def parse(self, parse_context):
		self._stop_flag = False
		while not self._stop_flag:
			for _, _handler in self._handlers.items():
				_handler(self, parse_context)
		return parse_context


class Grammar8Parser2_1(Grammar8Parser2_0):

	_test_buffer = []
	_channel = PyChannel()

	@classmethod
	def _test_handler_1(cls, parser):
		_test_buffer_len = len(cls._test_buffer)
		if _test_buffer_len >= 9:
			parser.stop()
		else:
			print(f"RUNNING HANDLER STEP: {_test_buffer_len}")
			cls._test_buffer.append("")

	@classmethod
	def _test_handler_2(cls, parser):
		parse_context = parser.parse_context()
		if parse_context.done_parsing:
			parser.stop()
		_current_state = parse_context.state()
		_current_symbol = parse_context.current_symbol().token_val
		_action_info = parser.parse_table.action((_current_state, _current_symbol), default=(ParserActionType.ERROR, None))

		_action = _action_info[0]
		print(f"{_action}")

		if _action == ParserActionType.ERROR:
			parse_context.set_result(False)
			parser.stop()
		elif _action == ParserActionType.SHIFT:
			if parser.debug_mode:
				print(f"IN SHIFT ACTION:")
			parse_context.append_state(_action_info[1])
			parse_context.append_symbol(_current_symbol)
			parser.logger.submit_log(
				message=f"Performing SHIFT action",
				new_state=f"PARSE CONTEXT ID: {parse_context.context_id} ---> ({_action_info[1]}/{_current_symbol})",
				log_type=LogType.DEBUG
				)

			# TODO: create a new action, aside from SHIFT/REDUCE/ACCEPT/ERROR, which allows
			# 		for this behaviour to be ran. Should also allow for other actions. NOTE:
			# 		the actual layout for the function will completely change once all of the
			# 		pieces are more glued together and it's more clear how I'm implementing it
			# if _current_state == 0 and _current_symbol == "a":
			# 	_next_input_char = parse_context.peek(offset=1)
			# 	if _next_input_char == "b":
			# 		parse_context.append_state(9)
			# 		parse_context.append_symbol("A")
			# 		parse_context.advance()

			# 		self.logger.submit_log(
			# 			message=f"Since the current state of the parser is 0/'a' (CURRENT-STATE/CURRENT-SYMBOL) and since the next input symbol is a 'b', Performing shortcut SHORTCUT SHIFT action",
			# 			new_state=f"PARSE CONTEXT ID: {parse_context.context_id} ---> (9/A)",
			# 			log_type=LogType.DEBUG
			# 			)
			parse_context.advance()
		elif _action == ParserActionType.REDUCE:
			_reduce_item = _action_info[1]
			if parser.debug_mode:
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

			if parser.debug_mode:
				_goto_key = (parse_context.state(), _reduce_item.rule_head)
				print(f"GOTO KEY ---> {_goto_key}")
				_goto_state = parser.parse_table.goto(_goto_key)
				_next_state = _goto_state[0]
				parse_context.append_state(_next_state)
				parse_context.append_symbol(_reduce_item.rule_head)
				print(f"PARSE CONTEXT STATE UPDATED ---> {_next_state}")
				print(f"PARSE CONTEXT SYMBOL STACK UPDATED---> {_reduce_item.rule_head}")
			else:
				_goto_key = (parse_context.state(), _reduce_item.rule_head)
				_goto_state = parser.parse_table.goto(_goto_key)
				_next_state = _goto_state[0]
				parse_context.append_state(_next_state)
				parse_context.append_symbol(_reduce_item.rule_head)
		elif _action == ParserActionType.ACCEPT:
			parse_context.set_result(True)

	def parse(self, parse_context):
		# self.add_handler(self._test_handler_1)
		self.add_handler(self._test_handler_2)
		parse_context.set_parser(self)
		parse_context.append_state(self.init_state)
		return super().parse(parse_context)


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

	@classmethod
	def logging_set(cls):
		cls.LOGGING_SET = True

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
		_parse_context = self.create_context(input, end_symbol=self.field("end_symbol", default="$"), context_id=context_id)
		return self.parser.parse(_parse_context)

	def create_context(self, *args, **kwargs):
		return self.context_factory(*args, **kwargs)

	def context_factory(self, input, end_symbol="$", context_id=None):
		return ParseContext(input=input, end_symbol=end_symbol, context_id=context_id)

	def tokenize(self, input):
		return self.tokenizer.tokenize(input)


if __name__ == "__main__":
	pass
