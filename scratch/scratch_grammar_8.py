from enum import StrEnum, IntEnum, auto
from collections import deque

from pyevent import PyChannel
from pyparse import Tokenizer, LexHandler, Token
from pylog import PyLogger, LogType
from .final_redesign import (
	TableBuilder
)
from .scratch_utils import generate_id
# from .scratch_runtime_setup import (
# 	CoreParser2
# )
from .scratch_grammar_rules_filter import (
	RuleSelector,
	AndRuleSelector,
	OrRuleSelector,
	NotRuleSelector,
	RuleIDSelector,
	RuleHeadSelector,
	RuleBodySelector
)
from .utils import (
	bold_text,
	apply_color,
	underline_text,
	center_text
)
from .scratch_cons import (
	ParserActionType
)


class ParserStateType(IntEnum):
	STOP = auto()
	SHIFT = auto()
	REDUCE = auto()
	ACCEPT = auto()
	ERROR = auto()


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

			# if _current_char in {"+", "-", "*", "/"}:
			# 	_add_token_alias(Grammar8TokenType.OPERATOR, _current_char, token_id=f"OPERATOR_{_counter}")
			# 	_tokenizer_advance_a()
			# 	continue

			if _current_char:
				match _current_char:
					case "+":
						_add_token_alias(Grammar8TokenType.PLUS_OP, "+", token_id=f"PLUS_OP_{_counter}")
						_tokenizer_advance_a()
						continue
					case "-":
						_add_token_alias(Grammar8TokenType.SUB_OP, "-", token_id=f"SUB_OP_{_counter}")
						_tokenizer_advance_a()
						continue
					case "*":
						_add_token_alias(Grammar8TokenType.MULT_OP, "*", token_id=f"MULT_OP_{_counter}")
						_tokenizer_advance_a()
						continue
					case "/":
						_add_token_alias(Grammar8TokenType.DIV_OP, "/", token_id=f"DIV_OP_{_counter}")
						_tokenizer_advance_a()
						continue
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


class Grammar8TableBuilder(TableBuilder):

	def build_table(self, table):
		number = self.grammar.select(RuleIDSelector("num"))[0]

		table.add_action((0, "NUMBER"), (ParserActionType.SHIFT, 6))
		table.add_goto((0, "number"), (3, number))


		table.add_action((6, "+"), (ParserActionType.REDUCE, number))


class PyParser:

	__slots__ = ("_parser_id", "_state", "_state_handlers", "_action_buffer", "_stop_flag")

	def __init__(self, init_state=0, parser_id=None):
		self._parser_id = parser_id or generate_id()
		self._state = init_state or 0
		self._state_handlers = {}
		self._action_buffer = deque()
		self._stop_flag = False

	@property
	def parser_id(self):
		return self._parser_id

	@property
	def state(self):
		return self._state

	def register_state(self, state, handler):
		_state_handlers = self._state_handlers
		if state not in _state_handlers:
			_state_handlers[state] = []
		_state_handlers[state].append(handler)

	def remove_state(self, state):
		return self._state_handlers.remove(state)

	def update(self, state):
		self._state = state

	def state_handlers(self, default=None):
		return self._state_handlers.get(self.state, default)

	def submit_action(self, action, *args, **kwargs):
		self._action_buffer.append((action, args, kwargs))

	def next_action(self, default=None):
		if not self._action_buffer:
			return default
		_action, _action_args, _action_kwargs = self._action_buffer.popleft()
		return lambda: _action(*_action_args, **_action_kwargs)

	def stop(self):
		self._stop_flag = True

	def parse(self, parse_context):
		_state_handlers = self.state_handlers(default=[])
		while (len(_state_handlers) >= 1) and (not self._stop_flag):
			for _state_handler in _state_handlers:
				_state_handler(self, parse_context)
			_state_handlers = self.state_handlers(default=[])
		return parse_context


class Grammar8Parser(PyParser):

	def __init__(self, init_state=0, grammar=None, parse_table=None, debug_mode=False, parser_id=None):
		super().__init__(init_state=init_state, parser_id=parser_id)
		self._grammar = grammar
		self._parse_table = parse_table
		self._debug_mode = debug_mode
		self.init_parser()

	@property
	def grammar(self):
		if not bool(self._grammar):
			# TODO: create and raise custom error here
			_error_details = f"unable to access 'grammar' as one has not yet been associated with instance of {self.__class__.__name__}..."
			raise RuntimeError(_error_details)
		return self._grammar

	@property
	def parse_table(self):
		if self._parse_table is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access 'parse_table' as one has not yet been associated with instance of {self.__class__.__name__}..."
			raise RuntimeError(_error_details)
		return self._parse_table
	
	@property
	def debug_mode(self):
		return self._debug_mode
	
	def init_parser(self):
		# self.add_handler(self.__STOP__, handler_id="STOP")
		self.add_handler(self.__BASIC__, handler_id="BASIC")

	def __BASIC__(self, parser, context):
		_action_type = self.next_action(context)

		_action_info = context.action_info()

		print()
		print(f"CONTEXT AT TOP OF '__BASIC__' ---> {context}")
		print(f"\tACTION TYPE ---> {_action_type}")
		print(f"\tACTION INFO ---> {_action_info[1]}")
		print(f"\t\tSTATE: {context.state()}")
		print(f"\t\tCURRENT SYMBOL: {context.current_symbol().token_type}")
		print(f"\t\tSTACK ---> {context.stack}")
		print(f"\t\tSYMBOL STACK ---> {context.symbol_stack}")

		if _action_type == ParserActionType.ERROR:
			context.set_result(False)
			parser.stop()
		elif _action_type == ParserActionType.SHIFT:
			if self.debug_mode:
				print()
				print(f"IN SHIFT ACTION:")
			context.append_state(_action_info[1][0])
			context.append_symbol(str(context.current_symbol().token_type))
			self.logger.submit_log(
				message=f"Performing SHIFT action",
				new_state=f"PARSE CONTEXT ID: {context.context_id} ---> ({_action_info[1][0]}/{context.current_symbol().token_type})",
				log_type=LogType.DEBUG
				)
			context.advance()
		elif _action_type == ParserActionType.REDUCE:
			_reduce_item = _action_info[1][0]
			if self.debug_mode:
				print()
				print(f"IN REDUCE ACTION:")
				for _ in range(_reduce_item.rule_size):
					_popped_state = context.pop_state()
					_popped_symbol = context.pop_symbol()
					print(f"POPPED STATE: {_popped_state}")
					print(f"POPPED SYMBOL: {_popped_symbol}")
				print(f"REDUCE ACTION HANDLING COMPLETE; CALCULATING GOTO:")
			else:
				for _ in range(_reduce_item.rule_size):
					context.pop_state()
					context.pop_symbol()

			if self.debug_mode:
				_goto_key = (context.state(), _reduce_item.rule_head)
				print()
				print(f"GOTO KEY ---> {_goto_key}")
				_goto_state = self.parse_table.goto(_goto_key)
				_next_state = _goto_state[0]
				context.append_state(_next_state)
				context.append_symbol(_reduce_item.rule_head)
				print(f"PARSE CONTEXT STATE UPDATED ---> {_next_state}")
				print(f"PARSE CONTEXT SYMBOL STACK UPDATED---> {_reduce_item.rule_head}")
			else:
				_goto_key = (context.state(), _reduce_item.rule_head)
				_goto_state = self.parse_table.goto(_goto_key)
				_next_state = _goto_state[0]
				context.append_state(_next_state)
				context.append_symbol(_reduce_item.rule_head)
		elif _action_type == ParserActionType.ACCEPT:
			context.set_result(True)

	def __STOP__(self, parser, context):
		# parser.stop()
		pass

	def next_action(self, context):
		_current_state = context.state()
		_current_symbol = context.current_symbol().token_type
		# _current_symbol = context.current_symbol().token_val
		_action_info = self.parse_table.action((_current_state, _current_symbol), default=(ParserActionType.ERROR, None))
		context.set_action(_action_info[1:])
		return _action_info[0]


if __name__ == "__main__":

	def __main__(input, parser):
		return parser.parse(input)


	_test_list = []
	_test_parser = PyParser(init_state="SUCK_IT", parser_id="PARSER_DESIGN_TESTING")


	def _test_handler_1(parser, context):
		print()
		print(f"SHITTTT!!!!!!!!")
		print(f"IN TEST HANDLER 1")
		print(f"PARSER STATE:")
		print(f"\t{parser.state}")
		print()


	def _stop(parser, context):
		print(f"STOPPING!")
		print(f"PARSER STATE ---> {parser.state}")


	def _suck_it(parser, context):
		_context_len = len(context)
		_current_state = parser.state
		print()
		print(underline_text(bold_text(apply_color(172, f"ITERATION: {_context_len}"))))
		print(f"  |")
		print(f"  •--• ", end="")
		print(apply_color(220, f"CURRENT STATE: {_current_state}"))
		if _context_len <= 3:
			context.append(None)
			print()
			print(f"SUCK IT YO!!!!")
			print(f"UPDATING TO 'SUCK_IT4'")
			parser.update("SUCK_IT4")
		else:
			print()
			print(f"STOPPING PARSER...")
			parser.stop()
			print(f"PARSER STOPPED...")
			print()


	def _suck_it_4(parser, context):
		_context_len = len(context)
		_context_len_is_even = (_context_len % 2) == 0
		_current_state = parser.state
		if _context_len_is_even and _context_len > 4:
			parser.update((2, "*"))
		else:
			print()
			_context_len = len(context)
			print()
			print(underline_text(bold_text(apply_color(172, f"ITERATION: {_context_len}"))))
			print(f"  |")
			print(f"  •--• ", end="")
			print(apply_color(220, f"CURRENT STATE: {_current_state}"))
			if _context_len_is_even + 3 == 3:
				print()
				print(f"STATE OF PARSER ID: '{parser.parser_id}' ---> '{_current_state}'...")
				print(f"UPDATING TO STATE 'SUCK_IT''")
				parser.update("SUCK_IT")
			else:
				_next_state = (2, "*")
				print()
				print(f"UPDATING TO ---> {_next_state}...")
				print(apply_color(92, f"---------------"))
				parser.update((2, "*"))


	def _2_and_multiply(parser, context):
		# print(bold_text(apply_color(9, f" •----------• STOPPING PARSE EARLY •----------• ")))
		_context_len = len(context)
		_current_state = parser.state
		print()
		print()
		print(underline_text(bold_text(apply_color(172, f"ITERATION: {_context_len}"))))
		print(f"  |")
		print(f"  •--• ", end="")
		print(apply_color(220, f"CURRENT STATE: {_current_state}"))
		_next_state = (2, "+")
		print()
		print(f"UPDATING TO ---> {_next_state}...")
		print()
		parser.update(_next_state)


	def _2_and_plus(parser, context):
		print()
		print(f"UPDATING TO 'SUCK_IT'...")
		print()
		parser.update("SUCK_IT")


	_test_parser.register_state("SUCK_IT", _suck_it)
	_test_parser.register_state("SUCK_IT4", _suck_it_4)
	_test_parser.register_state((2, "*"), _2_and_multiply)
	_test_parser.register_state((2, "+"), _2_and_plus)
	_test_parser.register_state(ParserStateType.STOP, lambda parser, parse_context: parser.stop())


	__main__(_test_list, _test_parser)
