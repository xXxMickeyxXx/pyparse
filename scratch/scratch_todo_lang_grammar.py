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


class ToDoLangTokenType(StrEnum):

	AT_SYM = "@"
	TODO = "TODO"
	NOTE = "NOTE"
	TEXT = "TEXT"
	L_ANGLE = "<"
	R_ANGLE = ">"
	DOUBLE_QUOTE = "\""
	SINGLE_QUOTE = "'"
	COMMENT_ENTRY = "#"
	SKIP = ""
	END_SYMBOL = "$"


class ToDoLangTokenizerHandler(LexHandler):
	
	def handle(self, tokenizer):
		_add_token_alias = tokenizer.add_token
		_tokenizer_advance = tokenizer.advance
		_cond_consume = tokenizer.cond_consume
		_counter = 1

		_NOTE_OR_TODO_DECLARED = False
		while tokenizer.can_consume:
			_current_char = tokenizer.current_char
			print(f"CURRENT CHAR ---> {_current_char}")
			if _current_char.isalpha() and not _NOTE_OR_TODO_DECLARED:
				_test_peek_range = tokenizer.peek_range(offset=4)
				match _test_peek_range.upper():
					case "TODO":
						_add_token_alias(ToDoLangTokenType.TODO, "TODO", token_id=f"TODO_{_counter}")
						for _ in range(4):
							_tokenizer_advance()
						_NOTE_OR_TODO_DECLARED = True
					case "NOTE":
						_add_token_alias(ToDoLangTokenType.NOTE, "NOTE", token_id=f"NOTE_{_counter}")
						for _ in range(4):
							_tokenizer_advance()
						_NOTE_OR_TODO_DECLARED = True
			else:
				_peek_range = tokenizer.peek_range(3)
				if _peek_range in {"'''", "\"\"\""}:
					_add_token_alias(ToDoLangTokenType.COMMENT_ENTRY, "#", token_id=f"COMMENT_ENTRY_{_counter}")
					for _ in range(3):
						_tokenizer_advance()
				elif _current_char == "#":
					_add_token_alias(ToDoLangTokenType.COMMENT_ENTRY, "#", token_id=f"COMMENT_ENTRY_{_counter}")
					_tokenizer_advance()
				else:
					if _current_char in {" ", "\n", "\t", "\r\n", "'", "\""}:
						_add_token_alias(ToDoLangTokenType.SKIP, _current_char, token_id=f"SKIP_{_counter}")
						_tokenizer_advance()
					else:
						match _current_char:
							case "<":
								_add_token_alias(ToDoLangTokenType.L_ANGLE, "<", token_id=f"L_ANGLE_{_counter}")
								_tokenizer_advance()
							case ">":
								_add_token_alias(ToDoLangTokenType.R_ANGLE, ">", token_id=f"R_ANGLE_{_counter}")
								_tokenizer_advance()
							case "@":
								_add_token_alias(ToDoLangTokenType.AT_SYM, "@", token_id=f"AT_SYM_{_counter}")
								_tokenizer_advance()
							case _:
								_add_token_alias(ToDoLangTokenType.SKIP, _current_char, token_id=f"SKIP_{_counter}_INVALID_SYMBOL")
								_tokenizer_advance()
			_counter += 1
		_add_token_alias(ToDoLangTokenType.END_SYMBOL, "$", token_id="END_SYMBOL")


class ToDoLangTableBuilder(TableBuilder):

	def build_table(self, table):
		pass


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

			# @TODO<maybe state handler(s) and their invocation cause actions to be
			# buffered, which get executed after state handler(s) take care of business>
		return parse_context


class ToDoLangParser(PyParser):
	pass


if __name__ == "__main__":
	pas
