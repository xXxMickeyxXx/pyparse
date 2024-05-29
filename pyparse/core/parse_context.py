from abc import abstractmethod


class ParseContextManager:

	def __init__(self, parse, manager_id=None):
		self._manager_id = manager_id or generate_id()
		self._current_state = None
		self._input = ""
		self._stack = []
		self._tokens
		# self._actions = {}
		# self._gotos = {}

	@property
	def manager_id(self):
		return self._manager_id

	def update_state(self, state):
		self._current_state = state

	# def register_action(self, state, input, action):
	# 	self._actions[state][input] = action

	# def register_gotos(self, state, input, goto):
	# 	self._gotos[state][input] = goto

	# def select_action(self, state, input):
	# 	_retval = None
	# 	_state = self._actions.get(state, None)
	# 	if _state is not None:
	# 		_retval = _state.get(input, None)
	# 	return _retval

	# def select_goto(self, state, input):
	# 	_retval = None
	# 	_state = self._gotos.get(state, None)
	# 	if _state is not None:
	# 		_retval = _gotos.get(input, None)
	# 	return _retval

	def update(self, parser):
		# _action_retval = None
		# _goto_retval = None

		# _action_state = self._actions.get(self._current_state, None)
		# _goto_state = self._gotos.get(self, _current_state, None)

		# if _action_state is not None:
		# 	_action = _action_state.get(parser.current_input, None)
		# 	if _action:
		# 		_action_retval = _action(parser)
		
		# if _goto_state is not None:
		# 	_goto = _goto_state.get(parser.current_input, None)			
		# 	if _goto:
		# 		_goto_retval = _goto(parser)
		# return None
		pass


class Parse:
	"""Encapsulates both the state and parse result object for a given input.
	The motive is as follows:
		
		1. Provides a sort of 'future' object, in the event that concurrency
		is added to this model
		
		2. Allows the parser implementation to switch parse contexts for different
		parses, at different times for whatever reason, making it so that you don't
		have to create and use multiple parser instances to achieve the desired
		result, which ideally reduces the memory footprint of this parsing system

		3. Gives the parsing implementation(s) the freedom to perform it's work in
		any way that it see's fit without being tied to object(s) that the client
		interacts with.

	The parser will always 

	"""

	__slots__ = ("_parse_id", "_input_counter", "_input")

	def __init__(self, parse_id=None):
		self._parse_id = parse_id
		self._input_counter = 0
		self._output = None
		self._parse_context = ParseContextManager(self, manager_id=parse_id)

	@property
	def parse_id(self):
		return self._parse_id

	@parse_id.setter
	def parse_id(self, val):
		# TODO: create and raise custom error here
		_error_details = f"unable to update 'parse_id' attribute; once the '{self.__class__.__name__}' instance is created and assigned the ID (via the value passed to the 'parse_id' parameter, upon instantiation), it remains as such for the duration of it's lifetime..."
		raise AttributeError(_error_details)

	@property
	def parse_context(self):
		return self._parse_context

	def feed(self, input):
		self._parse_context.update(input)

	def get(self):
		# NOTE: should get the resulting output produced by the parser, either part of
		# 		or the whole, depending on parser implementation (need to ensure this
		# 		is consistent across different implementation boundries)
		return self._output


if __name__ == "__main__":
	pass
