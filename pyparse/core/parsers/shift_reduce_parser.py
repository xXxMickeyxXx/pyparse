from ...library import PyChannel
from ...cons import ParserAction
# from ...utils import generate_id


# class ParserStateManager:

# 	def __init__(self, manager_id=None):
# 		self._manager_id = manager_id or generate_id()
# 		self._current_state = None
# 		self._actions = {}

# 	@property
# 	def manager_id(self):
# 		return self._manager_id

# 	def update_state(self, state):
# 		self._current_state = state

# 	def register_action(self, state, input, action):
# 		self._actions[state][input] = action

# 	def select_action(self, state, input):
# 		_retval = None
# 		_state = self._actions.get(state, None)
# 		if _state is not None:
# 			_retval = _state.get(input, None)
# 		return _retval

# 	def update(self, parser):
# 		_state = self._actions.get(self._current_state, None)
# 		if _state is not None:
# 			_action = _state.get(parser.current_input, None)
# 			if _action:
# 				return _action(parser)
# 		return None


class ShiftReduceParser:

	# TODO: create a bridge class which takes a parser implementation as the main
	#       object that a client works with

	# TODO: when implementing this into a separate package, have it be so that state
	#       can be saved for each different parse request; that way you don't have to
	#       create/instantiate multiple parsers, but instead, using something like the
	#       memento pattern, you can save and reference previous state. Will have to keep
	#       in mind the usage of threads (i.e. make it thread-safe or not thread-safe, perhaps
	#       offer a warning). It should, however, be easy to add a thread-safe implementation
	#       into this whole design

	# def __init__(self, grammar=None, state_manager=None, end_match=None):
	def __init__(self, grammar=None, end_match=None):
		self._grammar = grammar
		self.stack = []
		self.end_match = end_match
		self._tokens = None
		self._get_grammar = None
		self._handlers = None
		# self._state_manager = state_manager or ParserStateManager()

	@property
	def grammar(self):
		if self._grammar is None or not self._grammar:
			_error_details = f"'grammar' have not yet been associated with this object; please set them either during object's instantiation ('__init__') or using the 'set_grammar' setter method"
			raise ValueError(_error_details)
		return self._grammar

	@property
	def tokens(self):
		return self._tokens

	@property
	def handlers(self):
		if self._handlers is None:
			self._handlers = self.actions_factory()
		return self._handlers

	def register_handler(self, rule, handler, handler_id=None):
		self.handlers.register(rule, handler, receiver_id=handler_id)

	def remove_handler(self, rule, handler_id=None):
		if handler_id is None:
			_retval = self.handlers.remove(rule)
		else:
			_action_signal = self.handlers.select(rule)
			_retval = _action_signal.remove(handler_id)
		return _retval

	def actions_factory(self):
		return PyChannel()

	def get_grammar(self):
		if self._get_grammar is None:
			self._get_grammar = self.grammar.get_grammar()
		return self._get_grammar

	def reset(self):
		self._tokens = None
		self.stack = []
		self._get_grammar = None

	def set_grammar(self, grammar):
		self._grammar = grammar

	def stack_peek(self, index=-1):
		if self.stack:
			return self.stack[index]
		return None

	def pop_stack(self, index=-1):
		if self.stack:
			return self.stack.pop(index)
		return None

	def token_peek(self, index=-1):
		if self.tokens:
			return self.tokens[index]
		return None

	def pop_token(self, index=-1):
		return self.tokens.pop(index)

	def update(self, token):
		pass

	def shift(self):
		if self.tokens:
			token_type, token_value = self.pop_token(0)
			self.stack.append((token_type, token_value))
			self.handlers.emit(ParserAction.SHIFT, token_type, token_value)
		else:
			self.raise_error()

	def raise_error(self, error=Exception, error_text="Unexpected end of input"):
		raise error(error_text)

	def can_reduce(self):
		for prod_rule, match_cases in self.get_grammar():
			if len(match_cases) <= len(self.stack) and [i[0] for i in self.stack[-len(match_cases):][0:]] == match_cases:
				return prod_rule, match_cases
		return False

	def reduce(self, matched_grammar):
		production_rule, match_cases = matched_grammar
		_matched_tokens = [self.pop_stack() for i in match_cases][::-1]
		self.stack.append((production_rule, match_cases))
		self.handlers.emit(ParserAction.REDUCE, production_rule, _matched_tokens)
		self.handlers.emit(production_rule, _matched_tokens)

	def parse(self, tokens):
		self._tokens = tokens
		while self.tokens:
			potential_prod_rules = self.can_reduce()
			if potential_prod_rules:
				self.reduce(potential_prod_rules)
				continue
			self.shift()

		_potential_prod_rules = self.can_reduce()
		while _potential_prod_rules:
			self.reduce(_potential_prod_rules)
			_potential_prod_rules = self.can_reduce()

		_end_stack_pop = self.pop_stack(index=-1)
		_end_of_stack_pop = _end_stack_pop[0] if _end_stack_pop else None
		if self.end_match == (_end_of_stack_pop if _end_stack_pop else None):
			_retval = True
		else:
			_retval = False
		self.reset()
		return _retval


if __name__ == "__main__":
	pass
