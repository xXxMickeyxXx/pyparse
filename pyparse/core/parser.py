import time
from abc import abstractmethod
from collections import deque
import string
from enum import StrEnum, IntEnum, auto

from ..library import PyChannel
from ..utils import (
	generate_id,
	apply_color,
	underline_text,
	bold_text,
	center_text
	)
from ..errors import TimeOutError


# TODO: recreate some of the 'quick-n-diry' implementations contained in this
#       module so that they are more object oriented


# Token Types
METHOD = 'METHOD'
PATH = 'PATH'
HTTP_VERSION = 'HTTP_VERSION'
HEADER_NAME = 'HEADER_NAME'
HEADER_VALUE = 'HEADER_VALUE'
CRLF = 'CRLF'
BODY = 'BODY'


class Node:

	def __init__(self, node_id, nodes=None):
		self._node_id = node_id

	@property
	def node_id(self):
		return sef._node_id


class Nodes(Node):

	def __init__(self, node_id, nodes=None):
		super().__init__(node_id)
		self._nodes = nodes or []

	def add(self, node):
		self._nodes.append(node)

	def remove(self, node_id):
		_nodes_len = len(self._nodes)
		_counter = 0
		while _counter < _nodes_len:
			_current_node = self._nodes[_counter]
			if _current_node.node_id == node_id:
				return self._nodes.pop(_counter)
			_counter += 1
		_error_details = f"invalid 'node_id'; a node associated with ID: {node_id};"


class ParserStateManager:

	def __init__(self, manager_id=None):
		self._manager_id = manager_id or generate_id()
		self._current_state = None
		self._actions = {}

	@property
	def manager_id(self):
		return self._manager_id

	def update_state(self, state):
		self._current_state = state

	def register_action(self, state, input, action):
		self._actions[state][input] = action

	def select_action(self, state, input):
		_retval = None
		_state = self._actions.get(state, None)
		if _state is not None:
			_retval = _state.get(input, None)
		return _retval

	def update(self, parser):
		_state = self._actions.get(self._current_state, None)
		if _state is not None:
			_action = _state.get(parser.current_input, None)
			if _action:
				return _action(parser)
		return None


class ParserAction(IntEnum):

	SHIFT = auto()
	REDUCE = auto()
	ACCEPT = auto()
	FAIL = auto()


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

	def __init__(self, grammar=None, state_manager=None, end_match=None):
		self._grammar = grammar
		self.stack = []
		self.end_match = end_match
		self._tokens = None
		self._get_grammar = None
		self._handlers = None
		self._state_manager = state_manager or ParserStateManager()

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


class Parser:

	# TODO: determine the usage and/or inlusion of a static parsing table; the option
	#       to use one should at the very least be there. Perhaps in one of the 
	#       implementations, that become the input into the 'Parser' constructor (or
	#       the abstract class related to the bridge pattern)

	def __init__(self, parser_imp=None):
		self._parser_imp = parser_imp

	def set_parser(self, parser_imp):
		self._parser_imp = parser_imp

	def parse(self, input):
		return self._parser_imp.parse(input)


# Tokenizer Function (Assuming a simple tokenizer for demonstration)
def http_request_tokenize(input_string):
	tokens = []
	lines = input_string.splitlines()
	_headers_done = False
	_body_done = False

	for line in lines:
		if line.startswith('GET'):
			tokens.append(('METHOD', 'GET'))
			tokens.append(('PATH', line.split()[1]))
			tokens.append(('HTTP_VERSION', line.split()[-1]))
		elif line.startswith("POST"):
			tokens.append(('METHOD', 'POST'))
			tokens.append(('PATH', line.split()[1]))
			tokens.append(('HTTP_VERSION', line.split()[-1]))
		elif ": " in line and not _headers_done:
			_split_line = line.split(": ")
			tokens.append(("HEADER_NAME", _split_line[0]))
			tokens.append(("HEADER_VALUE", _split_line[1]))
		elif ":" in line and not _headers_done:
			_split_line = line.split(":")
			tokens.append(("HEADER_NAME", _split_line[0]))
			tokens.append(("HEADER_VALUE", _split_line[1]))
		elif line == "":
			if not _headers_done:
				tokens.append(('CRLF', ''))
				_headers_done = True
		else:
			if _headers_done:
				tokens.append(('BODY', line))
	return tokens


class Grammar:

	# TODO: update this class to be more of a container for grammar, allowing the 
	#       parser to more easily interact with the rules it uses to parse.

	# TODO/NOTE: should separate a callable that acts on the parser, closer to a 'rule'
	#            and then have the grammar be able to add 'action' callables, which can
	#            be used to build a structure, based on whatever is happening during
	#            parsing (such as building a request object for use in application
	#            code/for building some sort of composite/etc.). Should also create
	#            a way to associate an action for with a rule or many rules (i.e. a
	#            one-to-many relationship or a many-many relationship)

	def __init__(self, grammar_id=None):
		self._grammar_id = grammar_id or generate_id()
		self._rules = []

	@property
	def grammar_id(self):
		return self._grammar_id

	def add_rule(self, non_terminal, rule):
		_new_rule = [non_terminal, rule]
		self._rules.append(_new_rule)

	def get_grammar(self):
		return self._rules


class Tokenizer:

	def __init__(self, input=None):
		self._input = input
		self._pointer = 0
		self._tokens = []
		self._input_len = len(self._input) if self._input is not None else 0


	@property
	def can_consume(self):
		return self._pointer < self._input_len

	@property
	def tokens(self):
		return self._tokens

	@property
	def current_char(self):
		_input = self._input
		_pointer = self._pointer
		return _input[_pointer] if _input and self.can_consume else None

	def set_input(self, input):
		self._input = input
		self._input_len = len(input)

	def reset(self):
		self._pointer = 0
		self._tokens = []
		self._input = None
		self._input_len = 0

	def peek(self):
		if self.can_consume:
			_tmp_pointer = self._pointer + 1
			if (_tmp_pointer) < self._input_len:
				return self._input[_tmp_pointer]
		return None

	def advance(self):
		if self.can_consume:
			self._pointer += 1

	def consume(self):
		_current_char = self.current_char
		self.advance()
		return _current_char

	def consume_until(self, condition_callable, timeout=None):
		_is_expired = False
		_start_time = None
		_elapsed_time = None
		_tmp_word = ""
		while True:
			if timeout is not None:
				if _start_time is None:
					_start_time = time.time() if timeout is not None else None
				_elapsed_time = time.time() - _start_time
				if timeout - _elapsed_time <= 0:
					# TODO: create and raise custom error here
					_error_details = f"call to 'consume_until' has timed out..."
					raise TimeOutError(details=_error_details)
			if not condition_callable(self):
				_consume = self.consume()
				if _consume is None:
					break
				_tmp_word += _consume
				break
			_tmp_word += self.consume()
		if len(_tmp_word) > 0:
			return _tmp_word

	def expect(self, value, *, consume=False):
		_peek_val = self.peek()
		if _peek_val is not None and _peek_val == value:
			if consume:
				return self.consume()
			return True
		return False

	def add_token(self, token):
		self._tokens.append(token)

	def tokenize(self):
		raise NotImplementedError


class DictTokenizer(Tokenizer):

	_words = {"_", *set(string.ascii_lowercase + string.ascii_uppercase), *{str(i) for i in range (10)}}

	def test_input(self, input=None):
		return True if input is None else self.expect(input, consume=True)

	def consume_ws(self):
		if self.current_char is not None:
			while self.peek() != None and self._current_char.isspace():
				yield self.consume()

	def tokenize(self):
		if self._input is None:
			# TODO: create and raise custom error here
			raise RuntimeError("unable to tokenize as an input has not yet been specified")

		while True:
			if self.peek() is None:
				break

			char = self.consume()

			if char == " ":
				# _next_token = ("WS", char)
				continue
			elif char == "{":
				_next_token = ("OPENING_BRACE", char)
			elif char == "}":
				_next_token = ("CLOSING_BRACE", char)
			elif char == "'":
				_next_token = ("SINGLE_QUOTE", char)
			elif char == "\"":
				_next_token = ("DOUBLE_QUOTE", char)
			elif char == ":":
				_next_token = ("COLON", char)
			elif char == ",":
				_next_token = ("COMMA", char)
			elif char in self._words:
				_tmp = char
				_tmp += self.consume_until(self._consume_words)
				_next_token = ("WORD", _tmp)

			self.add_token(_next_token)
		return self.tokens

	@staticmethod
	def _consume_words(tokenizer):
		if tokenizer.can_consume:
			return tokenizer.peek() in tokenizer._words
		return False


class Lexer:
	"""Utilize the state pattern and some sort of handler registry, then build
	an automaton to handle creating tokens for the parser to consume. Ideally,
	the parser can pull tokens from the lexer (tokenizer) one by one, lazily.
	(NOTE: this would also be ideal for making it easier to make parsing part
	of the task as opposed to be used inside of a thread - thread operation
	would only then require actually performing the operation and not any
	additional logic)
	"""

	# TODO: pass tokenizer object (type: 'DictTokenizer[Tokenizer]')

	def __init__(self, tokenizer=None):
		self._tokenizer = tokenizer
		self._consumed = False

	def set_tokenizer(self, tokenizer):
		self._tokenizer = tokenizer
		self._consumed = False

	def generate(self, input):
		self._tokenizer.set_input(input)
		if self._tokenizer is None or not self._tokenizer:
			return iter([])
		_retval = [i for i in self._tokenizer.tokenize()]
		self._consumed = True
		return _retval

	def stream(self, input):
		self._tokenizer.set_input(input)
		_tokenizer = self._tokenizer.tokenize()
		for _token in _tokenizer:
			yield _token
		self._consumed = True


def dict_grammar_factory():
	_dict_grammar = Grammar(grammar_id="DICT_GRAMMAR")  # TODO: create a 'HTTP_GRAMMAR' enum
	_dict_grammar.add_rule("dict", ["OPENING_BRACE", "dict_objects", "CLOSING_BRACE"])
	_dict_grammar.add_rule("dict_objects", ["dict_objects", "dict_object"])
	_dict_grammar.add_rule("dict_objects", ["dict_object", "COMMA", "dict_object"])
	_dict_grammar.add_rule("dict_object", ["key_pair"])
	_dict_grammar.add_rule("key_pair", ["key", "COLON", "value"])
	_dict_grammar.add_rule("key", ["quotation", "WORD", "quotation"])
	_dict_grammar.add_rule("value", ["quotation", "WORD", "quotation"])
	_dict_grammar.add_rule("value", ["dict"])
	_dict_grammar.add_rule("quotation", ["SINGLE_QUOTE"])
	_dict_grammar.add_rule("quotation", ["DOUBLE_QUOTE"])
	return _dict_grammar


class DictObject:

	def __init__(self, parser):
		self._dict_obj = {}

	def contains(self, key):
		return key in self._dict_object

	def add(self, key, value, overwrite=False):
		if key not in self._dict_obj or overwrite:
			self._dict_obj.register(key, value, overwrite=overwrite)
			return True
		return False

	def remove(self, key):
		if key not in self._dict_obj:
			return None
		return self._dict_obj.remove(key)

	def get(self, key, default=None):
		if not self.contains(key):
			return default
		return self._dict_obj.select(key)


def _reduce_handler(rule, matched_tokens):
	print()
	print(f"--------------------------------------------------")
	print(underline_text(bold_text(apply_color(214, f"REDUCING BY RULE"))), end="")
	print(bold_text(apply_color(15, " ---> ")), end="")
	print(bold_text(apply_color(214, f"{rule}")))
	print()
	for i in matched_tokens:
		print(f"\t• {i}")
	print()
	print(f"--------------------------------------------------")
	print()


def _shift_handler(token_type, token_value):
	print()
	print(f"--------------------------------------------------")
	print(underline_text(bold_text(apply_color(214, f"SHIFTING ON:"))))
	print(f"\t• {token_type}: {token_value}")
	print(f"--------------------------------------------------")
	print()


def _key_action(matched_tokens):
	print()
	print(underline_text(bold_text(apply_color(214, f"MATCHED TOKENS:"))))
	print()
	for ttype, token in matched_tokens:
		print(f"\t• {ttype}: {token}")
	print()
	print()


def get_input(filepath, mode="r", dtype=str):
	_dtype_default = {str: "", int: 0}
	_retval = None
	with open(filepath, mode) as in_file:
		_retval = in_file.read()
	return _retval if _retval and isinstance(_retval, dtype) is not None else _dtype_default[dtype]


def register_dict_actions(parser):
	parser.register_handler("dict", _key_action)
	parser.register_handler(ParserAction.REDUCE, _reduce_handler)
	parser.register_handler(ParserAction.SHIFT, _shift_handler)


def generate_tokens(input, tokenizer):
	_lexer = Lexer(tokenizer)
	return _lexer.generate(input)


def stream_tokens(input, tokenizer):
	_lexer = Lexer(tokenizer)
	yield from _lexer.stream(input)


def parse_dict(dict_input):
	print()
	print(bold_text(apply_color(5, f"PARSING INPUT:")))
	print(f"    |")
	print(f"    |")
	print(f"    • ----> {dict_input}")
	print()
	print()
	_dict_grammar = dict_grammar_factory()
	_dict_tokenizer = DictTokenizer(input=dict_input)
	_parse_tokens = [i for i in _dict_tokenizer.tokenize() if i != "WS"]
	print(f"TOKENS:")
	print()
	for i in _parse_tokens:
		print(f"• \t{i}")
	print()
	_shift_reduce_parser = ShiftReduceParser(grammar=_dict_grammar, end_match="dict_object")
	register_dict_actions(_shift_reduce_parser)
	_parser = Parser(parser_imp=_shift_reduce_parser)    
	_dict_object = _parser.parse(_parse_tokens)
	if _dict_object:
		_text = "TEST INPUT IS VALID!!!"
		_border_text = f"-" * len(_text)
		_color = 10
		_result = bold_text(apply_color(_color, _text))
	else:
		_text = "TEST INPUT IS INVALID!!!"
		_border_text = f"-" * len(_text)
		_color = 9
		_result = bold_text(apply_color(_color, _text))
	print(apply_color(_color, _border_text))
	print(_result)
	print(apply_color(_color, _border_text))
	print()


def _dict_json_parsing_main():
	TEST_INPUT_1 = "{'hello': 'moto', \"goodbye\": \"you\"}"
	TEST_INPUT_2 = "{'hello_123': 'moto_456'}"
	print()
	parse_dict(TEST_INPUT_1)
	print()
	print(bold_text(f"--------------------------------------------------"))
	print()
	parse_dict(TEST_INPUT_1)
	print()


def _dict_tokenizer_testing():
	TEST_INPUT = "{'hello_123':'moto_456', \"fuck\": \"you\"}"
	_dict_tokenizer = DictTokenizer(input=None)
	_dict_tokenizer.set_input(TEST_INPUT)
	for i in _dict_tokenizer.tokenize():
		print(i)


def main():
	print()
	_dict_json_parsing_main()
	# _dict_tokenizer_testing()
	print()


if __name__ == "__main__":
	main()
