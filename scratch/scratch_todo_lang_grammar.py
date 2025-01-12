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
	SKIP = ""
	END_SYMBOL = "#"


class ToDoLangTokenizerHandler(LexHandler):
	
	def handle(self, tokenizer):
		pass


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
		return parse_context


class ToDoLangParser(PyParser):
	pass


if __name__ == "__main__":
	pas
