from abc import ABC, abstractmethod
import inspect
from collections import deque, defaultdict
from pathlib import Path
import time
from enum import IntEnum, StrEnum, auto

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

from pyparse import Tokenizer, LexHandler, Token
from .scratch_parse_table import ParseTable
from .scratch_parse_env import ParserEnvironment
from .scratch_init_grammar import (
	test_grammar_factory,
	init_grammar_1,
	init_grammar_2,
	init_grammar_3,
	init_grammar_4,
	init_grammar_5,
	init_grammar_6,
	init_grammar_7
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
from .scratch_handlers import Chain, Handler
from .scratch_parser_action import countdown, sleeper, close_at_finish
from .source_descriptor import SourceFile
from .scratch_package_paths import (
	TEST_INPUT_1,
	TEST_INPUT_2
)
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


		###################################################################################################################################
		#                                                                                                                   			  #
		# • -------------------------------------------------- SCRATCH RUNTIME SETUP -------------------------------------------------- • #
		#                                                                                                                   			  #
		###################################################################################################################################


_SCRATCH_PARSER_RUNTIME_LOGGER = PyLogger.get(PyParseLoggerID.PARSER)
GRAMMAR = test_grammar_factory()
GRAMMAR_RULES = GRAMMAR.rules()
NON_TERMINALS = GRAMMAR.non_terminals()
TERMINALS = GRAMMAR.terminals()
SYMBOLS = NON_TERMINALS + TERMINALS


ITEM_STATES_TEXT = apply_color(200, """
#########################################################################################################################
#                                                                                                                       #
# • -------------------------------------------------- ITEM STATES -------------------------------------------------- • #
#                                                                                                                       #
#########################################################################################################################
""")


TEST_PARSING_TEXT = apply_color(200, """
##########################################################################################################################
#                                                                                                                        #
# • -------------------------------------------------- TEST PARSING -------------------------------------------------- • #
#                                                                                                                        #
##########################################################################################################################
""")


class TestArithmaticGrammarTokenType(StrEnum):

	NUMBER = "NUMBER"
	PLUS_OPERATOR = "PLUS_OPERATOR"
	SUB_OPERATOR = "SUB_OPERATOR"
	MULT_OPERATOR = "MULT_OPERATOR"
	DIV_OPERATOR = "DIV_OPERATOR"
	FLOOR_DIV_OPERATOR = "FLOOR_DIV_OPERATOR"
	WS = "WS"
	LEFT_PAREN = "LEFT_PAREN"
	RIGHT_PAREN = "RIGHT_PAREN"
	END_SYMBOL = "END_SYMBOL"


class TestArithmaticGrammarTokenizeHandler(LexHandler):

	def __init__(self):
		super().__init__(handler_id=self.__class__.__name__)
		# self._symbol_mapping = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "*", "-", "/", "//", "(", ")", " "]
		self._token_type_idx_mapper = [
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.NUMBER,
			TestArithmaticGrammarTokenType.PLUS_OPERATOR,
			TestArithmaticGrammarTokenType.MULT_OPERATOR,
			TestArithmaticGrammarTokenType.SUB_OPERATOR,
			TestArithmaticGrammarTokenType.DIV_OPERATOR,
			TestArithmaticGrammarTokenType.FLOOR_DIV_OPERATOR,
			TestArithmaticGrammarTokenType.LEFT_PAREN,
			TestArithmaticGrammarTokenType.RIGHT_PAREN,
			TestArithmaticGrammarTokenType.WS
		]

	def handle(self, tokenizer):
		# NOTE: variables initialized with "_a" suffix are aliases for method calls in
		# 		order to suck out a litte bit more performnace since the additional
		# 		lookup isn't needed
		_add_token_alias = tokenizer.add_token
		_tokenizer_advance_a = tokenizer.advance
		_cond_consume_a = tokenizer.cond_consume
		while tokenizer.can_consume:
			_current_char = tokenizer.current_char
			_next_char_peek = tokenizer.peek()

			if _current_char.isdigit():
				_token_val = tokenizer.cond_consume(lambda x, y, z: not x.isdigit())
				_add_token_alias(TestArithmaticGrammarTokenType.NUMBER, _token_val, token_id=None)
				continue


			match _current_char:
				case " ":
					_add_token_alias(TestArithmaticGrammarTokenType.WS, " ", token_id=None)
					_tokenizer_advance_a()
					continue
				case "/":
					_next_char = tokenizer.peek()
					if _next_char != "/":
						_add_token_alias(TestArithmaticGrammarTokenType.DIV_OPERATOR, "/", token_id=None)
						_tokenizer_advance_a()
						continue
					else:
						_add_token_alias(TestArithmaticGrammarTokenType.FLOOR_DIV_OPERATOR, "//")
						_tokenizer_advance_a()
						_tokenizer_advance_a()
						continue
				case "+":
					_add_token_alias(TestArithmaticGrammarTokenType.PLUS_OPERATOR, "+", token_id=None)
					_tokenizer_advance_a()
					continue
				case "-":
					_add_token_alias(TestArithmaticGrammarTokenType.SUB_OPERATOR, "-", token_id=None)
					_tokenizer_advance_a()
					continue
				case "*":
					_add_token_alias(TestArithmaticGrammarTokenType.MULT_OPERATOR, "*", token_id=None)
					_tokenizer_advance_a()
					continue
				case "(":
					_add_token_alias(TestArithmaticGrammarTokenType.LEFT_PAREN, "(", token_id=None)
					_tokenizer_advance_a()
					continue
				case ")":
					_add_token_alias(TestArithmaticGrammarTokenType.RIGHT_PAREN, ")", token_id=None)
					_tokenizer_advance_a()
					continue

			_error_details = f"unexpected character: '{_current_char}'; handler is unable to determine how to tokenize character...please review and try again..."
			raise RuntimeError(_error_details)
		_add_token_alias(TestArithmaticGrammarTokenType.END_SYMBOL, "$", token_id=None)


class ParserSettings:

	def __init__(self, parser=None):
		self._parser = parser
		self._settings = {}

	@property
	def parser(self):
		if not bool(self._parser):
			# TODO: create and raise custom error here
			_error_details = f"unable to access 'parser' as one has not yet been associated with instance of {self.__class__.__name__}..."
			raise AttributeError(_error_details)
		return self._parser

	def set_parser(self, parser):
		self._parser = parser

	def contains(self, setting_key):
		return setting_key in self._settings

	def add_setting(self, setting_key, setting_value, overwrite=False):
		if setting_key not in self._settings or overwrite:
			self._settings[setting_key] = setting_value
			return True
		return False

	def remove_setting(self, setting_key):
		return self._settings.pop(setting_key) if setting_key in self._settings else None

	def get_setting(self, setting_key, default=None):
		return self._settings.get(setting_key, default)


class ParserAction:

	def __init__(self, target, action_type, state=ParserActionState.CREATED, action_id=None):
		self._target = target
		self._action_id = action_id or generate_id()
		if action_type not in [i for i in ParserActionType]:
			_error_details = f"unable to initialize instance of '{self.__class__.__name__}', parser action ID: {self._action_id} as an invalid 'action_type' was submitted: {action_type}..."
			raise RuntimeError(_error_details)
		self._action_type = action_type
		self._state = state
		self._send_value = None
		self._send_value_used = False
		self._result = None
		self._context = None
		self._task_finished = False
		self._channel = None
		self._task_finished = False

		self._initialize()
		self.logger.submit_log(
			function=f"{self.__class__.__name__}.__init__",
			action_id=f"{self._action_id}"
		)

	@property
	def target(self):
		return self._target

	@property
	def action_type(self):
		return self._action_type

	@property
	def action_id(self):
		return self._action_id

	@property
	def state(self):
		return self._state

	@property
	def task_finished(self):
		return self._task_finished

	@property
	def context(self):
		return self._context

	@property
	def logger(self):
		return _task_logger

	def _initialize(self):
		self.initialize()

	def initialize(self):
		self.state.set_task(self)

	def set_finished(self, finished_bool):
		self._task_finished = finished_bool

	def send(self, value):
		old_val = self._send_value
		self._send_value = value
		self._send_value_used = False
		return old_val

	def result_factory(self):
		return PySynchronyResult(result_id=self.action_id)

	def set_context(self, context):
		self._context = context

	def get_status(self):
		return self.state.status

	def result(self):
		# TODO: update so that it call's the result method for getting the result from the result obj
		return self._result

	def set_result(self, result):
		self._result = result

	def update_state(self, state, *args, **kwargs):
		self._state = state

	def update_status(self, status):
		self._state.update_status(status)

	def quit(self):
		self.target.close()

	def throw(self, error, *args):
		return self.target.throw(error, *args)

	def execute(self):
		if not self._send_value_used:
			_send_value = self._send_value
			self._send_value_used = True
		else:
			_send_value = None
		result_val = self.target.send(_send_value)
		self.set_result(result_val)
		_action_id = self.action_id
		self.logger.submit_log(
			message=f"Performing call on target associated with task ID: {_action_id}",
			function=f"{self.__class__.__name__}.execute",
			action_id=f"{_action_id}"
		)
		self.set_result(result_val)
		return result_val


class ParserSysCall(PySynchronySysCall):
	pass


class ParserEvent(PySynchronyEvent):
	pass


class InputStream:
	"""NOTE: will be responsible for actually containing/managing a given input/input
	stream. Each instance of 'ParseContext' will contain an instance of this class."""
	pass


class CoreParser2:

	# TODO: definitely need to split this class up into separate components; verify all of the additional overhead is needed as well

	# __slots__ = ("_scheduler", "_parser_id", "_grammar", "_parse_table", "_parser_settings", "_init_state", "_state", "_channel", "_logger", "_ports")
	__slots__ = ("_parser_id", "_grammar", "_parse_table", "_parser_settings", "_init_state", "_state", "_channel", "_logger", "_ports", "_debug_mode")

	# def __init__(self, scheduler, init_state=0, grammar=None, parse_table=None, parser_id=None):
	def __init__(self, init_state=0, grammar=None, parse_table=None, debug_mode=False, parser_id=None):
		self._parser_id = parser_id or generate_id()
		self._grammar = grammar
		self._parse_table = parse_table
		self._debug_mode = debug_mode
		self._parser_settings = ParserSettings(self)
		self._init_state = init_state
		self._state = None
		self._logger = None
		self._ports = {}

	@property
	def parser_id(self):
		return self._parser_id

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
	
	@property
	def init_state(self):
		return self._init_state

	@property
	def logger(self):
		if self._logger is None:
			self._logger = _SCRATCH_PARSER_RUNTIME_LOGGER
		return self._logger

	def __str__(self):
		return f"{self.__class__.__name__}"

	def setting(self, setting_key, default=None):
		return self._parser_settings.get_setting(setting_key, default=default)

	def config(self, setting_key, setting_value, overwrite=False):
		return self._parser_settings.add_setting(setting_key, setting_value, overwrite=overwrite)

	def set_grammar(self, grammar):
		# TODO: perhaps create and raise custom error here if '_grammar' has already been set
		self._grammar = grammar

	def set_table(self, parse_table):
		# TODO: perhaps create and raise custom error here if '_grammar' has already been set
		self._parse_table = parse_table

	def set_logger(self, logger):
		# TODO: perhaps create and raise custom error here if '_grammar' has already been set
		self._logger = logger

	# # TODO: interface should include this as an 'abstractmethod' 
	def parse(self, parse_context):
		self.init_parse_context(parse_context)

		# NOTE: remove below (up unti' series of consecutive '#'s) code as it's for coloring terminal debug output
		_xor_val = 208 ^ 226
		_color_code = 226

		####################
		# if hasattr(_current_symbol, "token_type"):
		# 	_current_symbol = _current_symbol.token_type
		while not parse_context.done_parsing:
			
			if self.debug_mode:
				_color_code ^= _xor_val
				_debug_text_mainloop_top = "---------- TOP OF 'parse' MAINLOOP ----------\n"
				_colored_debug_text = bold_text(apply_color(_color_code, _debug_text_mainloop_top))
				print(_colored_debug_text)
				print()


			_current_state = parse_context.state()
			_current_symbol = parse_context.current_symbol()
			_current_action = self.parse_table.action((_current_state, _current_symbol), default=(ParserActionType.ERROR, None))

			if self.debug_mode:
				_debug_text = f"• CURRRENT STATE: {_current_state}\n• CURRENT SYMBOL: {_current_symbol}\n• CURRENT ACTION: {_current_action}\n"
				print(bold_text(apply_color(_color_code, _debug_text)))

			_action = _current_action[0]

			if self.debug_mode:
				print()
				print(f"• CURRENT STATE: {_current_state}")
				print(f"• CURRENT STATE STACK: {parse_context.stack}")
				print()
				print(f"• CURRENT SYMBOL: {_current_symbol}")
				print(f"• CURRENT SYMBOL STACK: {parse_context.symbol_stack}")
				print()
				print()

			_parse_stack = parse_context.stack
			_parse_sym_stack = parse_context.symbol_stack

			if _action == ParserActionType.SHIFT:
				if self.debug_mode:
					print(f"IN SHIFT ACTION:")
				parse_context.append_state(_current_action[1])
				parse_context.append_symbol(_current_symbol)
				parse_context.advance()
			elif _action == ParserActionType.REDUCE:
				_reduce_item = _current_action[1]
				if self.debug_mode:
					print(f"IN REDUCE ACTION:")
				for _ in range(_reduce_item.rule_size):
					_popped_state = parse_context.pop_state()
					_popped_symbol = parse_context.pop_symbol()
					if self.debug_mode:
						print(f"POPPED STATE: {_popped_state}")
						print(f"POPPED SYMBOL: {_popped_symbol}")
				_goto_state = self.parse_table.goto((parse_context.state(), _reduce_item.rule_head))
				_next_state = _goto_state[0]
				parse_context.append_state(_next_state)
				parse_context.append_symbol(_reduce_item.rule_head)
				if self.debug_mode:
					print(f"UPDATED PARSE CONTEXT STATE TO ---> {_next_state}")
					print(f"UPDATED SYMBOL STACK WITH SYMBOL ---> {_reduce_item.rule_head}")
			elif _action == ParserActionType.ERROR:
				parse_context.set_result(False)
			elif _action == ParserActionType.ACCEPT:
				parse_context.set_result(True)

			if self.debug_mode:
				_debug_text_mainloop_bottom = "---------- BOTTOM OF 'parse' MAINLOOP ----------\n"
				_colored_debug_text = bold_text(apply_color(_color_code, _debug_text_mainloop_bottom))
				print(_colored_debug_text)

		return parse_context

	def init_parse_context(self, parse_context):
		parse_context.append_state(self.init_state)
		# self._debug_mode = True  # WARNING: overrides whatever has been passed into as command line arg

	def event_factory(self, event_id, **data):
		return PySynchronyEvent(event_id, **data)

	def mainloop(self):
		print(f"(PARSER ID: {self.parser_id} SAYS): Hello from 'mainloop'!!!")


class ParserContext(PySynchronyScheduler):

	def __init__(self, context_id):
		super().__init__(event_loop=PySynchronyEventLoop(), context_id=context_id)
		self._action_map = {}

	def register_event(self, signal_id, receiver=None, receiver_id=None):
		_channel = self.channel()
		_channel.register(signal_id, receiver=receiver, receiver_id=receiver_id)

	# def submit(self, action, *args, action_id=None, **kwargs):
	# 	inspect.

	def schedule_task(self, task):
		self.send(task, PyParsePortID.READY)

	def schedule_sleep(self, deadline, task):
		self.send((deadline, task), PyParsePortID.SLEEP)

	# def schedule_action(self, action):
	# 	self.send(action, PyParsePortID.ACTIONS)

	def _push_event(self, event):
		_port = self.port(PyParsePortID.EVENTS)
		return _port.send(event)

	# def _events_handler_port(self, port):
	# 	while port.pending():
	# 		_next_event = port.receive()
	# 		if _next_event:
	# 			self.emit(PyParseEventID.ON_EVENT, _next_event)

	# def _actions_handler_for_port_imp(self, port):
	# 	if port.peek():
	# 		_next_action = port.receive()
	# 		_action_context = self._action_map[_next_action.action_id]
	# 		return _action_context(_next_action, self)

	def _sleep_handler_for_port_imp_2(self, port):
		while True:
			try:
				_peeked_port_data = port.peek()
			except PySynchronyPortError:
				return
			else:
				if _peeked_port_data:
					_delta = _peeked_port_data[0] - time.time()
					if _delta > 0:
						return
					_, _sleep_task = port.receive()
					self.schedule_task(_sleep_task)
				return

	def _ready_handler_for_port_imp_2(self, port):
		if port.peek():
			current_task = port.receive()
			# _execution_context = self._task_execution_context[current_task.action_id]  # NOTE: use this once 'ParserAction' has been implemented
			_execution_context = self._task_execution_context[current_task.task_id]
			return _execution_context(current_task, self)

	def run_cycle(self):
		# _port_alias = self.port
		# _schedule_task_alias = self.schedule_task

		# _actions_port = _port_alias(PyParsePortID.ACTIONS)
		

		# _sleep_port = _port_alias(PyParsePortID.SLEEP)
		# if _sleep_port.pending():
		# 	while True:
		# 		try:
		# 			_peeked_port_data = _sleep_port.peek()
		# 		except PySynchronyPortError:
		# 			break
		# 		else:
		# 			if _peeked_port_data:
		# 				_delta = _peeked_port_data[0] - time.time()
		# 				if _delta > 0:
		# 					return
		# 				_, _sleep_task = _sleep_port.receive()
		# 				_schedule_task_alias(_sleep_task)
		# 				continue
		# 			break

		# _ready_port = _port_alias(PyParsePortID.READY)
		# if _ready_port.pending():
		# 	current_task _ready_port.receive()
		# 	self._task_execution_context[current_task.task_id](current_task, self)

		self.handle_port(PyParsePortID.SLEEP)
		self.handle_port(PyParsePortID.READY)

	def setup(self):
		self.add_port(PySynchronyPort(port_id=PyParsePortID.SLEEP, queue_factory=PriorityQueueFactory()))
		self.add_port(PySynchronyPort(port_id=PyParsePortID.READY))
		self.add_port(PySynchronyPort(port_id=PyParsePortID.EVENTS, queue_factory=PriorityQueueFactory()))
		self.add_port(PySynchronyPort(port_id=PyParsePortID.ACTIONS))
		self.add_port(PySynchronyPort(port_id=PyParsePortID.COMMANDS))
		# self.add_port(PySynchronyPort(port_id=PyParsePortID.ACTIONS))
		# self.add_port(PySynchronyPort(port_id=PyParsePortID.EVENTS))
		# self.event_loop.on_loop(self.run_cycle)

	def run(self, environment):
		"""Main runner, called to initialize and execute runtime, according to the registration seen below, which I'll describe a little bit more, below.
		

			• 'on_loop()' - is the defactor runtime of the entire program. It's the top most call
							in the event loops lifetime cycle. The value passed to it, a callable
							of some sort, takes an arbitrary number of arguments upon invocation of
							the associated logic until the 'stop()' is called on the 'event_loop'
							object or if an error of some kind occurs and isn't handled.

			• 'PyParsePortID.PUSH_EVENT' - 'PyParsePortID.EVENTS' port, allow calling from client code using the channel
										   to 'emit' a signal, or get the signal from the channel and 'emit'
										   the signal directly. Goes to the 'PyParsePortID.EVENTS' port, normally executed
										   once per the event loops cycle when it's handler checks and pulls out an event to
										   resolve.

			• 'PyParsePortID.PUSH_ACTION' - 'PyParsePortID.EVENTS' port, allowing calling from client code using the chanel
											to 'emit' a signal or get the signal from the channel and 'emit'
											the signal directly. Goes to the 'PyParsePortID.EVENTS' port, normally executed
											once per the event loop cycle when it's handler checks and pulls out an action to
											resolve.


		"""
		# self.event_loop.on_loop(environment.run)
		self.event_loop.on_loop(self.run_cycle)
		
		self.register_event(PyParseEventID.ON_EVENT, receiver=self._push_event)
		self.register_event(PyParseEventID.ON_QUIT, receiver=self.quit)
		self.register_event(PyParseEventID.ON_FORCE_QUIT, receiver=self.force_quit)
				
		self.register_handler(PyParsePortID.SLEEP, self._sleep_handler_for_port_imp_2)
		self.register_handler(PyParsePortID.READY, self._ready_handler_for_port_imp_2)

		# # self.register_handler(PyParsePortID.EVENTS, self._events_handler_port)
		# # self.register_handler(PyParsePortID.ACTIONS, self._actions_handler_for_port_imp)
		return self.event_loop.run()


class ParseContext:

	def __init__(self, input=None, end_symbol="$", context_id=None):
		self._context_id = context_id or generate_id()
		self._input = None
		self._input_len = 0
		self._end_symbol = end_symbol
		self._result = None
		self._result_set = False
		self._pointer = 0
		self._state = None
		self._symbol_state = None
		self._stack = None
		self._symbol_stack = None
		self._action_info = None
		self._parser = None
		if input is not None:
			self.set_input(input)

	@property
	def context_id(self):
		return self._context_id

	@property
	def input(self):
		if not bool(self._input):
			_error_details = f"input has not yet been set for instance of '{self.__class__.__name__}'..."
			raise RuntimeError(_error_details)
		return self._input

	@property
	def stack(self):
		if self._stack is None:
			self._stack = self.stack_factory()
		return self._stack

	@property
	def symbol_stack(self):
		if self._symbol_stack is None:
			self._symbol_stack = self.stack_factory()
		return self._symbol_stack

	@property
	def can_advance(self):
		return self._pointer < self._input_len

	@property
	def at_end(self):
		return not self.can_advance

	@property
	def done_parsing(self):
		return self._result_set and self._result is not None

	@property
	def end_symbol(self):
		return self._end_symbol

	@property
	def parser(self):
		if self._parser is None:
			# TODO: create and raise custom error here
			_error_details = f"parser has not yet been associated for instance of '{self.__class__.__name__}'..."
			raise RuntimeError(_error_details)
		return self._parser

	def action_info(self):
		return self, *self._action_info

	def set_parser(self, parser):
		self._parser = parser

	def set_action(self, *action_info):
		self._action_info = action_info

	def peek(self, offset=0):
		_peek_idx = self._pointer + offset
		if _peek_idx < self._input_len:
			return self.input[_peek_idx]
		return self.end_symbol

	def state(self):
		return self._state

	def symbol_state(self):
		return self._symbol_state

	def reset(self):
		self._input = None
		self._input_len = 0
		self._result = None
		self._result_set = False
		self._pointer = 0
		self._state = None
		self._stack = None
		self._symbol_stack = None

	def result(self):
		return self._result

	def set_result(self, result):
		if not self._result_set and self._result is None:
			self._result = result
			self._result_set = True

	def append_state(self, element):
		self.stack.append(element)
		self.update(element)

	def pop_state(self):
		_retval = self.stack.pop()
		self.update(self.stack[-1] if self.stack else None)
		return _retval

	def append_symbol(self, element):
		self.symbol_stack.append(element)
		self.update_symbol(element)

	def pop_symbol(self):
		element = self.symbol_stack.pop()
		self.update_symbol(element)
		return element

	def update(self, state):
		self._state = state

	def update_symbol(self, symbol):
		self._symbol_state = symbol

	def stack_factory(self):
		return deque()

	def set_input(self, input):
		if not bool(self._input):
			self._input = input
			self._input_len = len(self._input)

	def current_symbol(self):
		return self.peek(offset=0)
		# if self._pointer < self._input_len:
		# 	return self.input[self._pointer]
		# return self.end_symbol

	def advance(self):
		if not self.can_advance:
			_error_details = f"unable to consume any further symbols as the end of input has been reached..."
			raise RuntimeError(_error_details)
		self._pointer += 1

	def consume(self):
		if not self.can_advance:
			_error_details = f"unable to consume any further symbols as the end of input has been reached..."
			raise RuntimeError(_error_details)
		_retval = self.current_symbol()
		self.advance()
		return _retval


class AutomaticGrammar4TableBuilder:

	def __init__(self, grammar):
		self._grammar = grammar

	@property
	def grammar(self):
		return self._grammar

	@property
	def item_states(self):
		# if self._item_states:
		# 	self._item_states = self.grammar.generate_states()
		return self.grammar.generate_states()

	def build_table(self, table):
		_rules = self._grammar.rules()
		item_states = self._grammar.generate_states()
		_init_rule = _rules[0]
		_init_rule_head = _init_rule.rule_head
		_terminals = self._grammar.terminals()
		for state, items in item_states.items():
			for item in items:
				next_symbol = item.next_symbol()
				if item.can_reduce:
					_aug_start_rule_head = _init_rule.rule_head
					if item.rule_head == _aug_start_rule_head:
						table.add_action(state, _aug_start_rule_head, (ParserActionType.ACCEPT, item))
					else:
						for terminal in _terminals:
							table.add_action(state, terminal, (ParserActionType.REDUCE, item))
						table.add_action(state, _init_rule_head, (ParserActionType.REDUCE, item))
				elif next_symbol in _terminals:
					next_state = self._find_next_state(item_states, item)
					table.add_action(state, next_symbol, (ParserActionType.SHIFT, next_state, item))
				else:
					next_state = self._find_next_state(item_states, item)
					table.add_goto(state, next_symbol, (next_state, item))

	def _find_next_state(self, item_states, item):
		_item_copy = item.copy()
		_item_copy.advance()
		for state, items in item_states.items():
			if _item_copy in items:
				return state
		return None


class ManualGrammar4TableBuilder:

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

	@property
	def item_states(self):
		# if self._item_states:
		# 	self._item_states = self.grammar.generate_states()
		return self.grammar.generate_states()

	def set_grammar(self, grammar):
		self._grammar = grammar

	def build_table(self, table):
		INIT_RULE = self.grammar.select(RuleIDSelector("INIT_RULE"))[0]
		E_times_B = self.grammar.select(RuleIDSelector("E_rule_1"))[0]
		E_plus_B = self.grammar.select(RuleIDSelector("E_rule_2"))[0]
		E_is_B = self.grammar.select(RuleIDSelector("E_rule_3"))[0]
		B_is_0 = self.grammar.select(RuleIDSelector("B_rule_1"))[0]
		B_is_1 = self.grammar.select(RuleIDSelector("B_rule_2"))[0]

		# STATE 0 PARSE TABLE TRANSITION DECLARATIONS:
		E_times_B_copy_1 = E_times_B.copy()
		E_plus_B_copy_1 = E_plus_B.copy()
		E_is_B_copy_1 = E_is_B.copy()
		table.add_action((0, "0"), (ParserActionType.SHIFT, 3))
		table.add_action((0, "1"), (ParserActionType.SHIFT, 4))
		table.add_action((0, "E"), (ParserActionType.SHIFT, 1))
		table.add_action((0, "B"), (ParserActionType.SHIFT, 2))
		table.add_action((0, "*"), (ParserActionType.ERROR, None))
		table.add_action((0, "+"), (ParserActionType.ERROR, None))
		table.add_action((0, "$"), (ParserActionType.ERROR, None))	
		table.add_goto((0, "E"), (1, E_times_B_copy_1.advance_by(1)))
		table.add_goto((0, "E"), (1, E_plus_B_copy_1.advance_by(1)))
		table.add_goto((0, "B"), (2, E_is_B_copy_1.advance_by(1)))

		# STATE 1 PARSE TABLE TRANSITION DECLARATIONS:
		INIT_RULE_copy = INIT_RULE.copy()
		table.add_action((1, "*"), (ParserActionType.SHIFT, 5))
		table.add_action((1, "+"), (ParserActionType.SHIFT, 6))
		table.add_action((1, "E"), (ParserActionType.ERROR, None))
		table.add_action((1, "B"), (ParserActionType.ERROR, None))
		table.add_action((1, "$"), (ParserActionType.ACCEPT, INIT_RULE_copy.advance_by(1)))
		table.add_action((1, "0"), (ParserActionType.ERROR, None))
		table.add_action((1, "1"), (ParserActionType.ERROR, None))
		table.add_goto((1, "E"), None)
		table.add_goto((1, "B"), None)

		# STATE 2 PARSE TABLE TRANSITION DECLARATIONS:
		E_is_B_copy_2 = E_is_B.copy()
		table.add_action((2, "*"), (ParserActionType.REDUCE, E_is_B_copy_2.advance_by(1)))
		table.add_action((2, "+"), (ParserActionType.REDUCE, E_is_B_copy_2.advance_by(1)))
		table.add_action((2, "$"), (ParserActionType.REDUCE, E_is_B_copy_2.advance_by(1)))
		table.add_action((2, "0"), (ParserActionType.ERROR, None))
		table.add_action((2, "1"), (ParserActionType.ERROR, None))
		table.add_goto((2, "E"), None)
		table.add_goto((2, "B"), None)

		# STATE 3 PARSE TABLE TRANSITION DECLARATIONS:
		B_is_0_copy = B_is_0.copy()
		table.add_action((3, "*"), (ParserActionType.REDUCE, B_is_0_copy.advance_by(1)))
		table.add_action((3, "+"), (ParserActionType.REDUCE, B_is_0_copy.advance_by(1)))
		table.add_action((3, "$"), (ParserActionType.REDUCE, B_is_0_copy.advance_by(1)))
		table.add_action((3, "0"), (ParserActionType.ERROR, None))
		table.add_action((3, "1"), (ParserActionType.ERROR, None))
		table.add_goto((3, "E"), None)
		table.add_goto((3, "B"), None)

		# STATE 4 PARSE TABLE TRANSITION DECLARATIONS:
		B_is_1_copy = B_is_1.copy()
		table.add_action((4, "*"), (ParserActionType.REDUCE, B_is_1_copy.advance_by(1)))
		table.add_action((4, "+"), (ParserActionType.REDUCE, B_is_1_copy.advance_by(1)))
		table.add_action((4, "$"), (ParserActionType.REDUCE, B_is_1_copy.advance_by(1)))
		table.add_action((4, "0"), (ParserActionType.ERROR, None))
		table.add_action((4, "1"), (ParserActionType.ERROR, None))
		table.add_goto((4, "E"), None)
		table.add_goto((4, "B"), None)

		# STATE 5 PARSE TABLE TRANSITION DECLARATIONS:
		E_times_B_copy_2 = E_times_B.copy()
		table.add_action((5, "0"), (ParserActionType.SHIFT, 3))
		table.add_action((5, "1"), (ParserActionType.SHIFT, 4))
		table.add_action((5, "*"), (ParserActionType.ERROR, None))
		table.add_action((5, "+"), (ParserActionType.ERROR, None))
		table.add_action((5, "$"), (ParserActionType.ERROR, None))
		table.add_goto((5, "E"), None)
		table.add_goto((5, "B"), (7, E_times_B_copy_2.advance_by(2)))

		# STATE 6 PARSE TABLE TRANSITION DECLARATIONS:
		E_plus_B_copy_2 = E_plus_B.copy()
		table.add_action((6, "0"), (ParserActionType.SHIFT, 3))
		table.add_action((6, "1"), (ParserActionType.SHIFT, 4))
		table.add_action((6, "*"), (ParserActionType.ERROR, None))
		table.add_action((6, "+"), (ParserActionType.ERROR, None))
		table.add_action((6, "$"), (ParserActionType.ERROR, None))
		table.add_goto((6, "E"), None)
		table.add_goto((6, "B"), (8, E_plus_B_copy_2.advance_by(2)))

		# STATE 7 PARSE TABLE TRANSITION DECLARATIONS:
		E_times_B_copy_3 = E_times_B.copy()
		table.add_action((7, "*"), (ParserActionType.REDUCE, E_times_B_copy_3.advance_by(3)))
		table.add_action((7, "+"), (ParserActionType.REDUCE, E_times_B_copy_3.advance_by(3)))
		table.add_action((7, "$"), (ParserActionType.REDUCE, E_times_B_copy_3.advance_by(3)))
		table.add_action((7, "0"), (ParserActionType.ERROR, None))
		table.add_action((7, "1"), (ParserActionType.ERROR, None))
		table.add_goto((7, "E"), None)
		table.add_goto((7, "B"), None)

		# STATE 8 PARSE TABLE TRANSITION DECLARATIONS:
		E_plus_B_copy_3 = E_plus_B.copy()
		table.add_action((8, "*"), (ParserActionType.REDUCE, E_plus_B_copy_3.advance_by(3)))
		table.add_action((8, "+"), (ParserActionType.REDUCE, E_plus_B_copy_3.advance_by(3)))
		table.add_action((8, "$"), (ParserActionType.REDUCE, E_plus_B_copy_3.advance_by(3)))
		table.add_action((8, "0"), (ParserActionType.ERROR, None))
		table.add_action((8, "1"), (ParserActionType.ERROR, None))
		table.add_goto((8, "E"), None)
		table.add_goto((8, "B"), None)


class ManualGrammar7TableBuilder(ManualGrammar4TableBuilder):
	
	def build_table(self, table):
		super().build_table(table)
		# # STATE 0 PARSE TABLE TRANSITION DECLARATIONS:
		# E_times_B_copy_1 = E_times_B.copy()
		# E_plus_B_copy_1 = E_plus_B.copy()
		# E_is_B_copy_1 = E_is_B.copy()
		# table.add_action((0, "0"), (ParserActionType.SHIFT, 3))
		# table.add_action((0, "1"), (ParserActionType.SHIFT, 4))
		# table.add_action((0, "E"), (ParserActionType.SHIFT, 1))
		# table.add_action((0, "B"), (ParserActionType.SHIFT, 2))
		# table.add_action((0, "*"), (ParserActionType.ERROR, None))
		# table.add_action((0, "+"), (ParserActionType.ERROR, None))
		# table.add_action((0, "$"), (ParserActionType.ERROR, None))	
		# table.add_goto((0, "E"), (1, E_times_B_copy_1.advance_by(1)))
		# table.add_goto((0, "E"), (1, E_plus_B_copy_1.advance_by(1)))
		# table.add_goto((0, "B"), (2, E_is_B_copy_1.advance_by(1)))

		# # STATE 1 PARSE TABLE TRANSITION DECLARATIONS:
		# INIT_RULE_copy = INIT_RULE.copy()
		# table.add_action((1, "*"), (ParserActionType.SHIFT, 5))
		# table.add_action((1, "+"), (ParserActionType.SHIFT, 6))
		# table.add_action((1, "E"), (ParserActionType.ERROR, None))
		# table.add_action((1, "B"), (ParserActionType.ERROR, None))
		# table.add_action((1, "$"), (ParserActionType.ACCEPT, INIT_RULE_copy.advance_by(1)))
		# table.add_action((1, "0"), (ParserActionType.ERROR, None))
		# table.add_action((1, "1"), (ParserActionType.ERROR, None))
		# table.add_goto((1, "E"), None)
		# table.add_goto((1, "B"), None)

		# # STATE 2 PARSE TABLE TRANSITION DECLARATIONS:
		# E_is_B_copy_2 = E_is_B.copy()
		# table.add_action((2, "*"), (ParserActionType.REDUCE, E_is_B_copy_2.advance_by(1)))
		# table.add_action((2, "+"), (ParserActionType.REDUCE, E_is_B_copy_2.advance_by(1)))
		# table.add_action((2, "$"), (ParserActionType.REDUCE, E_is_B_copy_2.advance_by(1)))
		# table.add_action((2, "0"), (ParserActionType.ERROR, None))
		# table.add_action((2, "1"), (ParserActionType.ERROR, None))
		# table.add_goto((2, "E"), None)
		# table.add_goto((2, "B"), None)


class AutomaticGrammar7TableBuilder(AutomaticGrammar4TableBuilder):
	
	def build_table(self, table):
		_init_item = self.grammar.init_item
		_init_rule_head = self.grammar.init_symbol
		_terminals = self.grammar.terminals()
		
		print(f"BUILDING PARSE TABLE FOR TEST GRAMMAR # 7:")
		print()
		for state, item_sets in self.item_states.items():
			for _item in item_sets:
				_next_symbol = _item.next_symbol(default=None)
				if _item.at_end:
					raise NotImplementedError("HANDLE BUILDING TABLE WHEN AN ITEM IS REDUCABLE...")
				elif _next_symbol in _terminals:
					_next_state = self._find_next_state(_item)
					table.add_action(state, _next_symbol, (ParserActionType.SHIFT, _next_state, _item))


	def _find_next_state(self, item):
		_item_copy = item.copy()
		_item_copy.advance()
		for state, items in self.item_states.items():
			if _item_copy in items:
				return state
		return None


class TestGrammarParserEnv(ParserEnvironment):

	def __init__(self, parser=None, grammar=None, tokenizer=None, parse_table=None, env_id=None):
		super().__init__(parser=parser, grammar=grammar, env_id=env_id)
		self._tokenizer = tokenizer
		self._parse_table = parse_table
		self._parser_context = ParserContext(context_id=env_id)
		self._test_data = None
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
	def test_data(self):
		if self._test_data is None:
			# TODO: create and raise custom error here
			_error_details = f" unable to access 'test_data' field as test data has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._test_data

	@property
	def is_setup(self):
		return bool(self._initialized)

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return f"{self.__class__.__name__}(parser={self._parser}, grammar={self._grammar}, tokenizer={self._tokenizer}, parse_table={self._parse_table}, env_id={self.env_id})"

	def setup(self):
		if not self._initialized:
			self._parser_context.setup()
			# self._init_grammar_4(self.grammar)
			# self._init_grammar_7(self.grammar)
			# self._init_test_data_(self, TEST_INPUT_1)
			# self._init_mainloop_(self._parser_context)
			# self._init_test_task_(self._parser_context)
			self._initialized = True
		else:
			# TODO: create and raise custom error here
			_error_details = f"parser environment ID: {self.env_id} cannot be re-initialized as parser environment initialization can only happen once per runtime..."
			raise RuntimeError(_error_details)

	def _read_source(self, source_file):
		_filepath = source_file.get()
		if not isinstance(_filepath, Path):
			_filepath = Path(_filepath)
		_file_data = ""
		with open(_filepath, "r") as in_file:
			_file_data = in_file.read()

		if not bool(_file_data):
			# TODO: create and raise custom error here
			_error_details = f"Error Reading Source File Contents -- unable to read data contained within file @: {filepath}"
			raise RuntimeError
		return [i for i in _file_data.split("\n") if i]

	def set_tokenizer(self, tokenizer):
		self._tokenizer = tokenizer

	def set_table(self, parse_table):
		self._parse_table = parse_table

	def set_test_data(self, test_data):
		# NOTE: this won't be in the final implementation; currently included in
		# 		design to allow removing it from the 'paser_main' function
		if self._test_data is not None:
			# TODO: create and raise custom error here
			_error_details = f"unable to re-assign new data to the 'test_data' field as it can only be set once..."
			raise ValueError(_error_details)
		self._test_data = test_data

	def run(self):
		if not self.is_setup:
			self.setup()
		return self._parser_context.run(self)

	def _init_grammar_4(self, grammar):
		init_grammar_4(self.grammar)

	def _init_grammar_7(self, grammar):
		init_grammar_7(self.grammar)

	@staticmethod
	def _init_test_data_(parser_env, path_input):
		_source_file = SourceFile(path=path_input)
		_source_file_data = read_source(_source_file)
		parser_env.set_test_data(_source_file_data)

	def _init_mainloop_(self, parser_context):
		parser_context.submit(self.parser.mainloop)

	@staticmethod
	def _init_test_task_(parser_context):
		_TEST_TASK_ID = "TEST_COUNTDOWN_TASK"
		parser_context.submit(close_at_finish, rate=.10)
		# parser_context.submit(countdown, length=10, rate=1, step=1, action_id=_TEST_TASK_ID)
		parser_context.submit(countdown, length=3, rate=1, step=1, task_id=_TEST_TASK_ID)

	def __build_table_4__(self):
		_tbl_builder = ManualGrammar4TableBuilder(self.grammar)
		# _tbl_builder = AutomaticGrammar4TableBuilder(self.grammar)
		self.parse_table.build(_tbl_builder)

	def __build_table_7__(self):
		_tbl_builder = ManualGrammar7TableBuilder(self.grammar)
		self.parse_table.build(_tbl_builder)

	def tokenize(self, input):
		# Tokens with white-space removed
		return [i for i in self.tokenizer.tokenize(input) if i != TestArithmaticGrammarTokenType.WS]

	def execute(self, input):
		# self._init_grammar_4(GRAMMAR)
		# self.__build_table_4__()

		self._init_grammar_7(GRAMMAR)
		self.__build_table_7__()

		# Generate tokens from input
		_tokens = self.tokenize(input)

		# Display tokens
		for token in _tokens:
			print(f"TOKEN ---> {token}")
		print()
		print()

		# Instantiate the parse context object with tokens. (NOTE: generated specifically for test grammar 7)
		# _parse_context = ParseContext(input=input)  # NOTE: for parsing test grammar # 4
		_parse_context = ParseContext(input=_tokens)  # NOTE: for parsing test grammar # 7
		return self.parser.parse(_parse_context)


def parse_and_display(evn, test_data, actual_results, count=-1):
	_test_data_len, _actual_result_len = len(test_data), len(actual_results)
	assert _test_data_len == _actual_result_len, f"Actual results must contain the same amount of data as the data used for testing, as the algorithm depends on index mapping; {_test_data_len} != {_actual_result_len}..."
	print(TEST_PARSING_TEXT)
	print()
	_test_data_queue = deque(test_data)
	_counter = 0
	while _test_data_queue and (_counter < count if (isinstance(count, int) and count > 0) else True):
		_next_test_data_piece = _test_data_queue.popleft()
		_parse_context = ParseContext(input=_next_test_data_piece)
		_parse_result = evn.execute(_parse_context).result()
		_compare_results = _parse_result == actual_results[_counter]
		_passing_message = apply_color(10, f"TEST-CASE PASSED") if _compare_results else apply_color(9, f"TEST-CASE FAILED")
		display_result(_next_test_data_piece, _parse_result, _passing_message)
		print()
		_counter += 1
	print()


def user_runtime(env):
	_input_start_symbol = ">>: "
	_exit_runtime_vals = {"exit", "quit", "stop"}
	_user_input = input(_input_start_symbol)
	while _user_input.lower() not in _exit_runtime_vals:
		_parse_context = ParseContext(input=_user_input)
		_parse_result = env.execute(_parse_context).result()
		display_result(_user_input, _parse_result)
		print()
		_user_input = input(_input_start_symbol)
		yield _user_input, _parse_result
	yield _user_input, _parse_result


if __name__ == "__main__":
	init_grammar_4(GRAMMAR)
	# init_grammar_7(GRAMMAR)
	_TEST_INPUT_1_ = "1 / 1"
	_TEST_INPUT_2_ = "1 + 1 // 503 * 1"
	_TEST_INPUT_3_ = "1 * 0 + 1 / 1"
	_TEST_INPUT_4_ = "8675309 + 18001314321"
	_TEST_INPUT_5_ = "0 + 1 * 0 + 0 * 1 + 1"
	
	_TEST_INPUT_STREAM = [
		_TEST_INPUT_1_,
		_TEST_INPUT_2_,
		_TEST_INPUT_3_,
		_TEST_INPUT_4_,
		_TEST_INPUT_5_
	]

	TEST_TOKENIZER_ID = f"[TEST_TOKENIZER]"
	_test_tokenizer_handler = TestArithmaticGrammarTokenizeHandler()
	_test_tokenizer = Tokenizer(tokenizer_id=TEST_TOKENIZER_ID, handler=_test_tokenizer_handler)  # NOTE: should make 'add_handler' instead and use the 'tokenizer.tokenize()' method call with 'input' instead (encapsulating the 'handling' logic within the implementation, ideally an interface rather))


	# print()
	# for _input_ in _TEST_INPUT_STREAM:
	# 	_test_tokenizer.set_input(_input_)
	# 	_token_results = _test_tokenizer.tokenize(_test_tokenizer_handler)
	# 	print(f"INPUT TO TOKENIZE ---> {_input_}\n")
	# 	print()
	# 	for _token in _token_results:
	# 		if _token == Token(TestArithmaticGrammarTokenType.WS, " "):
	# 			continue
	# 		print(f"\t• TYPE:  ---> {_token.token_type}")
	# 		print(f"\t• VALUE: ---> {_token.token_value}")
	# 		print()
	# 	print()
	# 	print()


	_parse_table = ParseTable(table_id="TEST_RUNTIME_SETUP_PARSE_TABLE")
	# _manual_grammar_4_builder = ManualGrammar4TableBuilder(GRAMMAR)
	# _automatic_grammar_4_builder = AutomaticGrammar4TableBuilder(GRAMMAR)
	_manual_grammar_7_builder = ManualGrammar7TableBuilder(GRAMMAR)
	print()
	print()
	print()
	# Build parse table out using manual builder
	# _manual_grammar_4_builder.build_table(_parse_table)
	# _automatic_grammar_4_builder.build_table(_parse_table)
	_manual_grammar_7_builder.build_table(_parse_table)
	_test_parse_context = ParseContext()
	print()
	print()
	_parse_table.print()
	print()
	print(f"ITEM STATES")
	print()
	for state, items in _manual_grammar_7_builder.item_states.items():
		print(bold_text(apply_color(226, f"S{state} ------------------------------")))
		for item in items:
			print(f"{item}")
			print()
		print()
		print()
	print()
	for _input in _TEST_INPUT_STREAM:
		# TODO: call 'reset' within the 'set_input' method of both parse_context and tokenizer (though check if that doesn't undo previously executed logic, affecting state or otherwise)
		_tokens = [i for i in _test_tokenizer.tokenize(_input) if i.token_type != TestArithmaticGrammarTokenType.WS]
		# _tokens = [i for i in _tokens if i.token_type != TestArithmaticGrammarTokenType.WS]
		_test_parse_context.reset()
		_test_parse_context.set_input(_tokens)
		_parser = CoreParser2(init_state=0, grammar=GRAMMAR, parse_table=_parse_table, debug_mode=False, parser_id="TEST_SCRATCH_RUNTIME_SETUP_PARSER")
		_results = _parser.parse(_test_parse_context).result()
		_results = _results is True or bool(_results)
		print(f"PARSE PASSED ---> {_results}")
		for _i in _tokens:
			print(_i)
		print()
		print()
	# _test_parse_context = ParseContext()
	# _test_parse_context.set_input(_TEST_INPUT_1_)
	# _tokens = _test_par
