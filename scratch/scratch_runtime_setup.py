"""

__________SCRATCH GRAMMAR SPEC__________

	S ::= aA
	A ::= a | b


__________LR(0) AUTOMATON__________


	I.) TEST GRAMMAR:
			
			S ::= aA
			A ::= a | b


	II.) SYMBOLS:

			A.) NON-TERMINALS:
				
				$
				S
				A

			B.) TERMINALS:
				
				a
				b


	III.) Generate Item Sets:

		A.)  Augment grammar

			1.) Create new, starting prodction rule, and ensure it's at the beginning/top of the rule container
				
				$ ---> S

			2.) Create initial item set

				a.) Start with initial, augmented item

					$ ---> .S

				b.) Close initial, augmented item

					$ ---> .S
					S ---> .aA

				c.) Complete initial item set/state 'I0'

					I0:

						$ ---> .S
						S ---> .aA

				d.) Calculate GOTO for each symbol (if able to) for item set/state 'I0'

						GOTO(0, S) = I1

					(NOTE: the above 'GOTO' function can be read as, "On seeing the symbol 'S', while in state 0, ")

			3.) Perform transitions and calculate GOTO's, using items from initial item sets (and on), until no new item sets/states can be generated

				a.) Perform transition on first item of item set 'I0' (the starting item)

					I1:

						$ ---> S.

				b.) Next, do the transition for the 2nd item of item set 'I0' to create 'I2'

					S ---> a.A

				c.) Close item to create set/state 'I2'

					S ---> a.A
					A ---> b
					A ---> c

				d.) Complete item set/state 'I2'

					I2:

						S ---> a.A
						A ---> .b
						A ---> .c

				e.) Transition on first item of item set/state 'I2' to begin item set/state 'I3'

					I3:

						S ---> aA.

				f.) Transition on 2nd item of item set/state 'I2'

					I4:

						A ---> b.

				g.) Transition on 3rd item of item set/state 'I2'
				
					I5:

						A ---> c.


				

				$ ---> .S 
				S ---> .aA


				A ---> .b



	AUGMENTED TEST GRAMMAR:
		$ ---> .S  
		S ---> .aA
		A ---> .b


		I0:
			S ---> .S
			S ---> .aA
			A ---> .b

		I1:
			$ ---> S.

		I2:
			S ---> a.A
			A ---> .b

		I3:
			A ---> b.


		EXAMPLE INPUT ---> ab

				INITIALIZE:
					[(0, $)]
				
				STEP:
					[(0, $), (2, a)]

				STEP:
					[(0, $), (2, a), (3, b)]

				STEP:
					[(0, $), (2, a), (4, A)]

				STEP:
					[(0, $), (1, S)]


		EXAMPLE INPUT 2 ---> abbA

				INITIALIZE:
					[(0, $)]
				
				STEP:
					[(0, $), (2, a)]

				STEP:
					[(0, $), (2, a), (3, b)]

				STEP:
					[(0, $), (2, a), (4, A)]

				STEP:
					[(0, $), (2, a), (3, A)]

				STEP:
					[(0, $), (2, a)]

				STEP:
					[(0, $), (2, a), (4, A)]

				STEP:
					[(0, $), (1, S)]


__________LR(0) AUTOMATON__________


	TEST GRAMMAR:
		E ---> E * B
		E ---> E + B
		E ---> B
		B ---> 0
		B ---> 1
		B ---> (E)


	TEST AUGMENTED GRAMMAR:
		S ---> .E
		E ---> .E * B
		E ---> .E + B
		E ---> .B
		B ---> .0
		B ---> .1
		B ---> .(E)


		I0:
			KERNEL
				S ---> .E
			CLOSURE
				E ---> .E * B
				E ---> .E + B
				E ---> .B
				B ---> .0
				B ---> .1
				B ---> .(E)
			TRANSITIONS
				GOTO(0, E) = 1
				GOTO(0, B) = 4


		I1:
			KERNEL
				S ---> E.
			CLOSURE
				NONE
			TRANSITIONS
				NONE
			ACTION(S)
				REDUCE(I1, S) = ACCEPT

		I2:
			KERNEL
				E ---> E .* B
			CLOSURE
				NONE
			TRANSITIONS
				NONE
			ACTION(S)

		I3:
			KERNEL
				E ---> E .+ B
			CLOSURE
				NONE
			TRANSITIONS
				NONE
			ACTION(S)


		I4:
			KERNEL:
				E ---> B.
			CLOSURE
				NONE
			TRANSITIONS
				NONE
			ACTION(S)
				REDUCE(4, E)

		I5:
			KERNEL
				B ---> 0.
			CLOSURE
				NONE
			TRANSITIONS
				NONE
			ACTION(S)


		I6:
			KERNEL
				B ---> 1.
			CLOSURE
				NONE
			TRANSITIONS
				NONE
			ACTION(S)

		I7:
			KERNEL
				B ---> (.E)
			CLOSURE
				E ---> .E * B
				E ---> .E + B
				E ---> .B
			TRANSITIONS
				NONE
			ACTION(S)

		I8:
			KERNEL
				E ---> E * .B
			CLOSURE
				B ---> .0
				B ---> .1
			TRANSITIONS
				GOTO(7, B) = 9
			ACTION(S)


		I9:
			KERNEL
				E ---> E + .B
			CLOSURE
				B ---> .0
				B ---> .1
			TRANSITIONS
				GOTO(8, B) = 10
			ACTION(S)


		I10:
			KERNEL
				E ---> E * B.
			CLOSURE
				NONE
			TRANSITIONS
				NONE
			ACTION(S)


		I11:
			KERNEL
				E ---> E + B.
			CLOSURE
				NONE
			TRANSITIONS
				NONE
			ACTION(S)



	INIT:

		• Parser initializes, adding initial state/accept symbol to the stack

	PARSE

		• Parser 



__________LR(0) AUTOMATON__________


	TEST GRAMMAR:
		E ---> E * B
		E ---> E + B
		E ---> B
		B ---> number
		B ---> (E)


	TEST AUGMENTED GRAMMAR:
		E ---> .E
		E ---> .E * B
		E ---> .E + B
		E ---> .B
		B ---> .NUMBER
		B ---> .(E)


		 I0:
			E ---> .E (augmented grammar start symbol)
			E ---> .E * B
			E ---> .E + B
			E ---> .B
			B ---> .NUMBER
			B ---> .(E)

				TRANSITIONS (from I0)
					GOTO(0, E) = 1
					GOTO(0, B) = 4
					GOTO(0, NUMBER) = 


		I1:
			E ---> E.
				
				ACTION: ACCEPT


		I2:
			E ---> E .* B

"""

from abc import ABC, abstractmethod
import inspect
from collections import deque, defaultdict
from pathlib import Path
import time

from pylog import PyLogger, LogType
from pyprofiler import profile_callable, SortBy
from pyevent import PyChannels, PyChannel, PySignal

from pyparse import Parser, Tokenizer
from pysynchrony import (
	PySynchronyScheduler,
	PySynchronyEventLoop,
	PySynchronyContext,
	PySynchronyCoroutineTask,
	PySynchronyPort,
	PySynchronyEvent,
	PySynchronySysCall,
	PriorityQueueFactory,
	PySynchronyPortError,  # NOTE: for testing
	RemainingTasks,  # NOTE: for testing
	AwaitTask,  # NOTE: for testing
	GetTaskID,  # NOTE: for testing
	Sleep,  # NOTE: for testing
	CreateTask,  # NOTE: for testing
	EmitEvent,  # NOTE: for testing
	PySynchronyForceQuit  # NOTE: for testing
)
from .scratch_parse_table import ParseTable
from .scratch_parse_env import ParserEnvironment
# from .test_automaton_design import Automaton
from .scratch_init_grammar import test_grammar_factory, init_grammar_1, init_grammar_2, init_grammar_3, init_grammar_4, init_grammar_5, init_grammar_6
from .source_descriptor import SourceFile
from .scratch_utils import generate_id, CircularBuffer, copy_items, copy_item
from .utils import apply_color, bold_text, underline_text, center_text
from .scratch_cons import (
	PyParsePortID,
	PyParseEventID,
	ParserActionState,
	ParserActionType,
	PyParseLoggerID,
	GrammarRuleBy,
	TEST_INPUT_1,
	TEST_INPUT_2
)


"""
		
		###########################################################################################################################
		#                                                                                                                         #
		# • -------------------------------------------------- PYPARSE TO-DO -------------------------------------------------- • #
		#                                                                                                                         #
		###########################################################################################################################


		I.)





		###################################################################################################################
		#                                                                                                                 #
		# • -------------------------------------------------- NOTES -------------------------------------------------- • #
		#                                                                                                                 #
		###################################################################################################################


		1.) Use the event loop and context designs from the 'pysynchrony' for implementing and designing components of this library/package


"""

		#####################################################################################################################
		#                                                                                                                   #
		# • -------------------------------------------------- TESTING -------------------------------------------------- • #
		#                                                                                                                   #
		#####################################################################################################################


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


class TestGrammar6Tokenizer(Tokenizer):

	# TODO/NOTE: use some sort of chain which has handlers to work with input stream

	def __init__(self, input=None):
		super().__init__(input=input)
		self.on_loop(self._tokenize)
		self._valid_symbols = SYMBOLS

	def _tokenize(self):
		if not self.can_consume:
			self.quit()
			return

		_next_token = None
		_next_char = self.consume()
		if _next_char in {" ", "\r\n", "\r", "\n", "\t"}:
			return
		elif _next_char == "i":
			_expected_d = self.consume()
			if _expected_d:
				_next_char += _expected_d
				_next_token = ("id", _next_char)
				self.push_token(_next_token)
			else:
				print(f"ACTUAL VALUE OF EXPECTED VALUE @ RUNTIME ERROR ---> {_expected_d}")
				_error_details = f"unable to tokenize; expected 'd' after encountering an 'i'..."
				raise RuntimeError(_error_details)

		elif _next_char == "+":
			_next_token = ("PLUS", _next_char)
			self.push_token(_next_token)
		elif _next_char == "*":
			_next_token = ("MULTIPLY", _next_char)
			self.push_token(_next_token)
		elif _next_char == "-":
			_next_token = ("MINUS", _next_char)
			self.push_token(_next_token)
		else:
			_error_details = f"error tokenizing input on character: '{_next_char}'..."
			raise RuntimeError(_error_details)


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


class CoreParser2:

	# TODO: definitely need to split this class up into separate components; verify all of the additional overhead is needed as well

	# __slots__ = ("_scheduler", "_parser_id", "_grammar", "_parse_table", "_parser_settings", "_init_state", "_state", "_channel", "_logger", "_ports")
	__slots__ = ("_parser_id", "_grammar", "_parse_table", "_parser_settings", "_init_state", "_state", "_channel", "_logger", "_ports")

	# def __init__(self, scheduler, init_state=0, grammar=None, parse_table=None, parser_id=None):
	def __init__(self, init_state=0, grammar=None, parse_table=None, parser_id=None):
		self._parser_id = parser_id or generate_id()
		self._grammar = grammar
		self._parse_table = parse_table
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

	@staticmethod
	def create_event(event_id, **data):
		return PySynchronyEvent(event_id, **data)

	# TODO: interface should include this as an 'abstractmethod' 
	# def parse(self, parse_context):
	#     # NOTE: passing 'None' argument to the 'event_id' until a consistent one is specified for this implementation/system

	#     _parse_context = parse_context
	#     parse_context.append_state(self.init_state)

	#     _action_search = None
	#     _previous_action = None
	#     _action = None
	#     _previous_symbol = None
	#     _current_symbol = parse_context.current_symbol()
	#     _current_state = parse_context.state
	#     while not parse_context.done_parsing:
	#         _current_symbol = parse_context.current_symbol()
	#         _current_state = parse_context.state            

	#         _action_search = self.action(_current_state, _current_symbol, default=(ParserActionType.ERROR, None, None))
	#         _action = _action_search[0]
	#         print()
	#         print(f"STATE STACK: {parse_context.stack}")
	#         print(f"SYMBOL STACK: {parse_context.symbol_stack}")
	#         print(f"CURRENT STATE: {_current_state}")
	#         print(f"CURRENT SYMBOL: {_current_symbol}")
	#         print(f"PREVIOUS SYMBOL: {_previous_symbol}")
	#         print(f"ACTION SEARCH: {_action_search}")
	#         print(f"ACTION: {_action}")
	#         if _action == ParserActionType.SHIFT:
	#             _next_state_ = _action_search[1]
	#             _item = _action_search[2]
	#             parse_context.append_state(_next_state_)
	#             _previous_symbol = _current_symbol
	#             parse_context.append_symbol(_current_symbol)
	#             parse_context.advance()
	#             print(f"STATE AFTER SHIFT: {parse_context.state}")
	#         elif _action == ParserActionType.REDUCE:
	#             _item = _action_search[1]
	#             for _ in range(_item.rule_size):
	#                 _popped_state = parse_context.pop_state()
	#                 _popped_symbol = parse_context.pop_symbol()
	#             _goto_state = self.goto(parse_context.state, _item.rule_head)
	#             _next_state = _goto_state[0]
	#             parse_context.append_state(_next_state)
	#             parse_context.append_symbol(_item.rule_head)
	#             print(f"ON GOTO IN REDUCE ({parse_context.state}, {_item.rule_head}): {_goto_state}")
	#         elif _action == ParserActionType.ERROR:
	#             parse_context.set_result(False)
	#         elif _action == ParserActionType.ACCEPT:
	#             parse_context.set_result(True)
	#     return _parse_context

	def parse(self, parse_context):
		raise NotImplementedError

	def event_factory(self, event_id, **data):
		return PySynchronyEvent(event_id, **data)

	def mainloop(self):
		print(f"(PARSER ID: {self.parser_id} SAYS): Hello from 'mainloop'!!!")


class ParseContext:

	def __init__(self, input=None, start_symbol="$"):
		self._input = input
		self._input_len = len(input)
		self._start_symbol = start_symbol
		self._result = None
		self._result_set = False
		self._pointer = 0
		self._state = None
		self._stack = None
		self._symbol_stack = None

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
	def state(self):
		return self.stack[-1] if self.stack else None

	@property
	def done_parsing(self):
		return self._result_set and self._result is not None

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

	def pop_symbol(self):
		return self.symbol_stack.pop()

	def update(self, state):
		self._state = state

	def stack_factory(self):
		return deque()

	def set_input(self, input):
		if not bool(self._input):
			self._input = input

	def current_symbol(self):
		if self._pointer < self._input_len:
			return self.input[self._pointer]
		return self._start_symbol

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


class ParserContext(PySynchronyScheduler):

	def __init__(self, context_id):
		super().__init__(event_loop=PySynchronyEventLoop(), context_id=context_id)
		self._action_map = {}

	def register_event(self, signal_id, receiver=None, receiver_id=None):
		_channel = self.channel()
		_channel.register(signal_id, receiver=receiver, receiver_id=receiver_id)

	# def submit(self, action, action_type, *args, action_id=None, **kwargs):
	# 	inspect.

	def schedule_task(self, task):
		self.send(task, PyParsePortID.READY)

	def schedule_sleep(self, deadline, task):
		self.send((deadline, task), PyParsePortID.SLEEP)

	# def schedule_parse(self, parse_context):
	# 	self.send(parse_context, PyParsePortID.PARSE_REQUEST)

	# def schedule_action(self, action):
	# 	self.send(action, PyParsePortID.ACTIONS)

	# def _push_event(self, event):
	# 	_port = self.port(PyParsePortID.EVENTS)
	# 	return _port.send(event)

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

	# def _parse_request_handler_for_port_imp(self, port):
	# 	raise NotImplementedError

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
		self.step()

	def step(self):
		self.handle_port(PyParsePortID.SLEEP)
		self.handle_port(PyParsePortID.READY)
		self.handle_port(PyParsePortID.SLEEP)
		self.handle_port(PyParsePortID.READY)
		self.handle_port(PyParsePortID.SLEEP)
		self.handle_port(PyParsePortID.READY)

	def setup(self):
		self.add_port(PySynchronyPort(port_id=PyParsePortID.SLEEP, queue_factory=PriorityQueueFactory()))
		self.add_port(PySynchronyPort(port_id=PyParsePortID.READY))
		# self.add_port(PySynchronyPort(port_id=PyParsePortID.ACTIONS))
		# self.add_port(PySynchronyPort(port_id=PyParsePortID.EVENTS))
		# self.add_port(PySynchronyPort(port_id=PyParsePortID.PARSE_REQUEST))
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
		
		# self.register_event(PyParseEventID.ON_EVENT, receiver=self._push_event)
		self.register_event(PyParseEventID.ON_QUIT, receiver=self.quit)
		self.register_event(PyParseEventID.ON_FORCE_QUIT, receiver=self.force_quit)
				
		self.register_handler(PyParsePortID.SLEEP, self._sleep_handler_for_port_imp_2)
		self.register_handler(PyParsePortID.READY, self._ready_handler_for_port_imp_2)

		# self.register_handler(PyParsePortID.EVENTS, self._events_handler_port)
		# self.register_handler(PyParsePortID.ACTIONS, self._actions_handler_for_port_imp)
		# self.register_handler(PyParsePortID.PARSE_REQUEST, self._parse_request_handler_for_port_imp)
		return self.event_loop.run()


def display_grammar(grammar):
	print()
	print(grammar)
	print()


def display_terminals(grammar=None):
	_grammar = GRAMMAR if grammar is None else grammar
	_terminals = TERMINALS if grammar is None else _grammar.terminals()
	print()
	print(f"TERMINALS:")
	for terminal in _terminals:
		print(terminal)
	print()


def display_non_terminals(grammar=None):
	_grammar = GRAMMAR if grammar is None else grammar
	_non_terminals = NON_TERMINALS if grammar is None else _grammar.non_terminals()
	print()
	print(f"NON-TERMINALS:")
	for _non_terminal in _non_terminals:
		print(_non_terminal)
	print()


def display_grammar_info(grammar=None):
	_grammar = GRAMMAR if grammar is None else grammar
	print(f"_______________ORIGINAL GRAMMAR_______________")
	display_grammar(_grammar)
	print()
	display_terminals(_grammar)
	print()
	display_non_terminals(_grammar)
	print()
	_grammar_2 = copy_items(_grammar, deepcopy=True)
	print(f"_______________COPIED GRAMMAR_______________")
	display_grammar(_grammar_2)
	print()
	display_terminals(_grammar_2)
	print()
	display_non_terminals(_grammar_2)
	print()


def display_rule(rule_input, search_by=GrammarRuleBy.HEAD, grammar=None):
	_grammar = GRAMMAR if grammar is None else grammar
	_g_rule = _grammar.rule(rule_input, search_by=search_by)
	if _g_rule:
		print(f"GETTING GRAMMAR RULE")
		for _test_rule in _g_rule:
			print(f"\t{rule_input}: {_test_rule.rule_body}")
	else:
		print(f"INVALID GRAMMAR RULE INPUT ---> {rule_input}")
	print()


def display_rules(grammar=None):
	_grammar = GRAMMAR if grammar is None else grammar
	_grammar_rules = GRAMMAR_RULES if grammar is None else _grammar.rules()
	print()
	print(f"GRAMMAR RULES:")
	for rule in _grammar_rules:
		print(rule)
	print()


def display_table(parse_table):
	parse_table.print()


def display_items(items, set_id):
	print()
	_text = underline_text(bold_text(apply_color(11, f"{set_id} ITEMS:")))
	_text += "\n"
	print(_text)
	for _item in items:
		print(f"\t{_item.rule_head}")
		print(f"\t{_item.rule_body}")
		print(f"\t{_item.status()}")
		print()
	print()


def display_test_data(test_data):
	print()
	print(f"TEST INPUT DATA")
	for i in test_data:
		print(i)
	print()


def display_item_states(item_sets):
	print(ITEM_STATES_TEXT)
	print()
	print(f"ITEM SETS:")
	print()
	print()
	for item_state, _items in item_sets.items():
		print(f"STATE: {item_state}")
		for _item in _items:
			print(f"\t{_item.rule_head} ---> {_item.status()}")
		print()
	print()


def display_goto_mapping(goto_mapping):
	print()
	for i in goto_mapping:
		print(f"{i}: {goto_mapping[i]}")

	print()


def display_result(input, parser_result):
	if parser_result:
		_color = 10
		_text = underline_text(bold_text(apply_color(_color, f"INPUT IS VALID!!!")))
		_text += f"\n    |"
		_text += f"\n    |"
		_text += f"\n    • ----> {bold_text(apply_color(11, input))}"
		_border_text = f"-" * int(len(_text)/2)
		_result = bold_text(apply_color(_color, _text))
	else:
		_color = 9
		_text = underline_text(bold_text(apply_color(_color, f"INPUT IS INVALID!!!")))
		_text += f"\n    |"
		_text += f"\n    |"
		_text += f"\n    • ----> {bold_text(apply_color(11, input))}"
		_border_text = f"-" * int(len(_text)/2)
		_result = _text
	print(apply_color(_color, _border_text))
	print(_result)
	print(apply_color(_color, _border_text))
	print()


def read_source(source_file):
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


def tokenize(input, tokenizer):
	tokenizer.set_input(input)
	_tokens = tokenizer.tokenize()
	tokenizer.reset()
	return _tokens


def parse_data(parse_context, parser):
	_parse_context = parser.parse(parse_context)
	print()
	print(f"SYMBOL STACK:")
	print(_parse_context.symbol_stack)
	return _parse_context.result()


"""
def parse_and_display(test_data, tokenizer, parser, count=-1):
    _test_data_queue = deque(test_data)
    _counter = 0
    while _test_data_queue and (_counter < count if (isinstance(count, int) and count > 0) else True):
        _next_test_data_piece = _test_data_queue.popleft()
        # _request_input_tokens = tokenize(_next_test_data_piece, tokenizer)
        _text = bold_text(apply_color(14, f"NEXT TEST DATA PIECE")) + bold_text(" ---> ") + bold_text(apply_color(14, f"{_next_test_data_piece}"))
        # _text += bold_text(apply_color(48, f"\nTOKENS"))
        print()
        print(_text)
        # for _token in _request_input_tokens:
        #     print(f"• {_token}")
        print()
        _parse_context = ParseContext(input=_next_test_data_piece, start_symbol="$")
        _parse_result = parse_data(_parse_context, parser)
        # _parse_result = parse_data(_request_input_tokens, parser)
        display_result(_next_test_data_piece, _parse_result)
        for _ in range(2):
            print()
        _counter += 1
    print()
"""


def parse_and_display(parser_env, count=-1):
	parser_env.run()
	# _test_data_queue = deque(parser_env.test_data)
	# _counter = 0
	# while _test_data_queue and (_counter < count if (isinstance(count, int) and count > 0) else True):
	# 	_next_test_data_piece = _test_data_queue.popleft()
	# 	# _request_input_tokens = tokenize(_next_test_data_piece, tokenizer)
	# 	_text = bold_text(apply_color(14, f"NEXT TEST DATA PIECE")) + bold_text(" ---> ") + bold_text(apply_color(14, f"{_next_test_data_piece}"))
	# 	# _text += bold_text(apply_color(48, f"\nTOKENS"))
	# 	print()
	# 	print(_text)
	# 	# for _token in _request_input_tokens:
	# 	#     print(f"• {_token}")
	# 	print()
	# 	_parse_context = ParseContext(input=_next_test_data_piece, start_symbol="$")
	# 	_parse_result = parse_data(_parse_context, parser)
	# 	# _parse_result = parse_data(_request_input_tokens, parser)
	# 	display_result(_next_test_data_piece, _parse_result)
	# 	for _ in range(2):
	# 		print()
	# 	_counter += 1
	# print()


def parse_and_display_custom_input(tokenizer, parser, count=-1):
	_tokenizer = TestGrammar6Tokenizer()
	print(TEST_PARSING_TEXT)
	while True:
		_input = input(">>> ")
		if not _input:
			break
		parse_and_display([_input], tokenizer, parser, count=count)


_EXIT_OK_ = set()


def sleeper(count):
	yield Sleep(count)


def countdown(length=5, rate=1, step=1):
	_EXIT_OK_.add(True)

	print(f"PROGRAM WILL EXIT IN...")
	for i in range(1, length+1)[::-1]:
		_time_unit = "SECOND...." if i == 1 else "SECONDS..."
		print(f"{i} {_time_unit}")
		yield Sleep(rate)
	print(f"EXITING PROGRAM...")
	_new_task = yield CreateTask(lambda name: print(f"HELLO {name}!!!"), "MICKEY MOUSE")
	yield AwaitTask(_new_task)
	yield EmitEvent(PyParseEventID.ON_QUIT)
	return 10


def close_at_finish(rate=.5):
	_task_id = yield GetTaskID()
	yield Sleep(rate)
	_remaining_tasks = yield RemainingTasks()
	if (_task_id in _remaining_tasks and len(_task_id) <= 1) and len(_EXIT_OK_) >= 1:
		yield EmitEvent(PyParseEventID.ON_QUIT)
		return
	yield CreateTask(close_at_finish, rate=rate)


class TestGrammar4ParserEnv(ParserEnvironment):

	def __init__(self, parser=None, grammar=None, tokenizer=None, parse_table=None, env_id=None):
		super().__init__(parser=parser, env_id=env_id)
		self._grammar = grammar
		self._tokenizer = tokenizer
		self._parse_table = parse_table
		self._parser_context = ParserContext(context_id=env_id)
		self._test_data = None
		self._initialized = False

	@property
	def grammar(self):
		if self._grammar is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access the 'grammar' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._grammar

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
			self._init_grammar_(self.grammar)
			self._init_test_data_(self, read_source(SourceFile(path=TEST_INPUT_1)))	
			# self._init_mainloop_(self._parser_context)
			self._init_test_task_(self._parser_context)
			self._initialized = True
		else:
			# TODO: create and raise custom error here
			_error_details = f"parser environment ID: {self.env_id} cannot be re-initialized as parser environment initialization can only happen once per runtime..."
			raise RuntimeError(_error_details)

	def set_grammar(self, grammar):
		self._grammar = grammar

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

	@staticmethod
	def _init_grammar_(grammar):
		init_grammar_4(grammar)

	@staticmethod
	def _init_test_data_(parser_env, source_data):
		_source_file = SourceFile(path=TEST_INPUT_1)
		_source_file_data = read_source(_source_file)
		parser_env.set_test_data(_source_file_data)

	@staticmethod
	def _init_mainloop_(parser_context):
		# _parse_request
		parser_context.submit(self.parser.mainloop)

	@staticmethod
	def _init_test_task_(parser_context):
		_TEST_TASK_ID = "TEST_COUNTDOWN_TASK"
		parser_context.submit(close_at_finish, rate=.10)
		parser_context.submit(sleeper, 2)
		parser_context.submit(sleeper, 8)
		# parser_context.submit(countdown, length=10, rate=1, step=1, action_id=_TEST_TASK_ID)
		parser_context.submit(countdown, length=10, rate=1, step=1, task_id=_TEST_TASK_ID)

	# TODO: remove this once done testing with it
	def __build_table__(self):
		print(f"BUILDING PARSE TABLE:")
		self.parse_table.build(self.grammar)
		self.parse_table.print()


@profile_callable(sort_by=SortBy.TIME)
def parse_main():
	# Initialized parser environment ID
	PARSER_ENVIRONMENT_ID = "SCRATCH_TEST_PARSER_ENV"

	# Generate tokens to feed the parser
	_tokenizer = TestGrammar6Tokenizer()


	# Create parse table, used to guide the LR(0) automaton that makes
	# up the design for the shift/reduce parser
	_parse_table = ParseTable(grammar=GRAMMAR, table_id="[ • -- TEST_PARSE_TABLE -- • ]", start_symbol="$")

	# Display parse table
	display_table(_parse_table)


	# Instantiate parser back-end (actual parsing implementation)
	# _parser_impl = CoreParser(init_state=0, grammar=GRAMMAR, parse_table=_parse_table)
	_parser_impl = CoreParser2(init_state=0, grammar=GRAMMAR, parse_table=_parse_table)


	# Instantiate parser environment
	_test_grammar_4_env = TestGrammar4ParserEnv(env_id=PARSER_ENVIRONMENT_ID)

	# Set parer env's 'parser', 'grammar', 'tokenizer' and 'parse_table' fields
	_test_grammar_4_env.set_grammar(GRAMMAR)
	_test_grammar_4_env.set_tokenizer(_tokenizer)
	_test_grammar_4_env.set_table(_parse_table)
	_test_grammar_4_env.set_parser(_parser_impl)

	# Run parser environment (**TESTING (call to it's 'run' method will bemoved, and possibly renamed all together, that is, the 'run' method may be changed**)
	_test_grammar_4_env.run()


	# Initialize parser environment, as it's been all setup otherwise
	# parse_and_display(_test_grammar_4_env, count=1)

	# Add white space below final text that displays in order to better separate the text
	# displayed from running this function and the profiler results displaying
	for _ in range(5):
		print()


if __name__ == "__main__":
	pass
