import string

from ..core import Parser, Parse, ShiftReduceParser, ParseContextManager, Tokenizer, Grammar
from ..cons import ParserAction
from ..utils import apply_color, underline_text, bold_text, center_text


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

		while self.can_consume:

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

	def _consume_words(self, _):
		_peek = self.peek()
		# if _peek and _peek in self._words:
			# if 
		if self.can_consume:
			return _peek in self._words or _peek in ".,!@#$%^&*()_;:-"
		return False


def dict_grammar_factory():
	_dict_grammar = Grammar(grammar_id="DICT_GRAMMAR")
	_dict_grammar.add_rule("dict", ["dict", "CLOSING_BRACE"])
	_dict_grammar.add_rule("dict", ["OPENING_BRACE", "dict_objects", "CLOSING_BRACE"])
	_dict_grammar.add_rule("dict", ["dict_objects"])
	_dict_grammar.add_rule("dict_objects", ["dict_objects", "dict_object"])
	_dict_grammar.add_rule("dict_objects", ["dict_object", "COMMA", "dict_object"])
	_dict_grammar.add_rule("dict_objects", ["dict_object"])
	_dict_grammar.add_rule("dict_object", ["key_pair"])
	_dict_grammar.add_rule("key_pair", ["key_part", "COLON", "key_part"])
	# _dict_grammar.add_rule("key", ["quotation", "WORD", "quotation"])
	_dict_grammar.add_rule("key_part", ["quotation", "WORD", "quotation"])
	# _dict_grammar.add_rule("value", ["dict"])
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
	# _current_key_part
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
	_shift_reduce_parser = ShiftReduceParser(grammar=_dict_grammar, end_match="dict")
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
	TEST_INPUT_2 = "{'hel-lo_123': 'moto_;:45,6', 'shitklasd;jfl;kasdjf': 'fuck'}"
	# TEST_INPUT_4 = input(">>: ")
	print()
	parse_dict(TEST_INPUT_1)
	print()
	print(bold_text(f"--------------------------------------------------"))
	print()
	parse_dict(TEST_INPUT_2)
	print()
	print(bold_text(f"--------------------------------------------------"))
	print()
	# parse_dict(TEST_INPUT_3)
	# print()


def _dict_tokenizer_testing():
	TEST_INPUT = "{'hello_123':'moto_456', \"fuck\": \"you\"}"
	_dict_tokenizer = DictTokenizer(input=None)
	_dict_tokenizer.set_input(TEST_INPUT)
	for i in _dict_tokenizer.tokenize():
		print(i)


if __name__ == "__main__":
	pass
