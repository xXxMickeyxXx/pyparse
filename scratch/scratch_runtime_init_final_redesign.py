from collections import deque
from enum import IntEnum, StrEnum, auto

from pylog import PyLogger, LogType
from pyprofiler import profile_callable, SortBy
from pyutils import (
    cmd_argument,
    DEFAULT_PARSER as DEFAULT_CMD_LINE_PARSER
)
from pyparse import Token

from .scratch_todo_lang_grammar import (
	ToDoLangTokenType,
	ToDoLangTokenizerHandler,
	ToDoLangTableBuilder,
	ToDoLangParser
	)
from .scratch_grammar_8 import (
	Grammar8TokenType,
	Grammar8TokenizerHandler,
	Grammar8TableBuilder,
	Grammar8Parser
	)
from .final_redesign import (
	# Grammar8TokenType,
	# Grammar8TokenizerHandler,
	# Grammar8TableBuilder,
	Grammar9TokenType,
	Grammar9TokenizerHandler,
	Grammar9TableBuilder,
	DateGrammarTokenType,
	DateGrammarTokenizerHandler,
	DateGrammarTableBuilder,
	CoreParser3,
	# Grammar8Parser,
	# Grammar8Parser2_0,
	# Grammar8Parser2_1,
	FinalRedesignEnv
)
from .scratch_package_paths import (
    LOGGING_ROOT
)
from .scratch_evaluator import Evaluator
from .scratch_nodes import Node
from .scratch_init_grammar import (
	test_grammar_factory,
	init_grammar
)
from .scratch_parse_table import ParseTable
from .scratch_runtime_setup import (
	GRAMMAR,
	CoreParser2,
	TestGrammarParserEnv,
	ParseContext,
	Tokenizer,
	TestArithmaticGrammarTokenizeHandler,
	TestArithmaticGrammarTokenType,
	ManualGrammar4TableBuilder,
	parse_and_display,
	user_runtime
)
from .scratch_shell_init import initialize_shell
from .scratch_logging_init import init_logging
from .scratch_cons import PyParseLoggerID, ParserActionType
from .utils import (
	display_result,
	display_item_states,
	bold_text,
	apply_color,
	underline_text,
	center_text
)


class ParserStateType(IntEnum):
	STOP = auto()
	SHIFT = auto()
	REDUCE = auto()
	ACCEPT = auto()
	ERROR = auto()


def display_tokens(tokens, input):
	_tokens_str = bold_text(apply_color(214, "    ** TOKENS **"))
	print(_tokens_str)
	print()
	for _token in tokens:
		print(f"\tTOKEN TYPE:  {apply_color(208, _token.token_type)}")
		print(f"\tTOKEN VALUE: {apply_color(208, _token.token_val)}")
		print()


def G8_environment_factory_newest(debug_mode=False):
	__GRAMMAR__ = test_grammar_factory()

	_G8_tokenizer_handler = Grammar8TokenizerHandler()
	__TOKENIZER__ = Tokenizer(handler=_G8_tokenizer_handler)

	__PARSE_TABLE__ = ParseTable(table_id="[ • --- • Grammar8ParseTable • ---• ]")
	__TABLE_BUILDER__ = Grammar8TableBuilder(grammar=__GRAMMAR__)

	_PARSER_ID_ = "Grammar8Parser(PyParser)"
	__PARSER__ = Grammar8Parser(init_state=0, grammar=__GRAMMAR__, parse_table=__PARSE_TABLE__, debug_mode=debug_mode, parser_id=_PARSER_ID_)
	_final_redesign_env = FinalRedesignEnv(parser=__PARSER__, grammar=__GRAMMAR__, tokenizer=__TOKENIZER__, table_builder=__TABLE_BUILDER__, parse_table=__PARSE_TABLE__)

	_final_redesign_env.add_field("tokenize", True)
	_final_redesign_env.add_field("grammar_version", 8)
	_final_redesign_env.add_field("end_symbol", Token(Grammar8TokenType.END_SYMBOL, "$"))
	_final_redesign_env.add_field("logger", PyLogger.get(_PARSER_ID_))


	# Init grammar (add grammar rules for defined grammar), etc.
	_final_redesign_env.setup()


	# Display item sets
	# display_item_states(__GRAMMAR__.generate_states())
	return _final_redesign_env


def G8_environment_factory(debug_mode=False):
	__GRAMMAR__ = test_grammar_factory()

	_G8_tokenizer_handler = Grammar8TokenizerHandler()
	__TOKENIZER__ = Tokenizer(handler=_G8_tokenizer_handler)

	__PARSE_TABLE__ = ParseTable(table_id="[ • --- • Grammar8ParseTable • ---• ]")
	__TABLE_BUILDER__ = Grammar8TableBuilder(grammar=__GRAMMAR__)

	_PARSER_ID_ = "Grammar8Parser"
	__PARSER__ = Grammar8Parser(init_state=0, grammar=__GRAMMAR__, parse_table=__PARSE_TABLE__, debug_mode=debug_mode, parser_id=_PARSER_ID_)
	_final_redesign_env = FinalRedesignEnv(parser=__PARSER__, grammar=__GRAMMAR__, tokenizer=__TOKENIZER__, table_builder=__TABLE_BUILDER__, parse_table=__PARSE_TABLE__)

	_final_redesign_env.add_field("tokenize", True)
	_final_redesign_env.add_field("grammar_version", 8)
	_final_redesign_env.add_field("end_symbol", Token(Grammar8TokenType.END_SYMBOL, "$"))
	_final_redesign_env.add_field("logger", PyLogger.get(_PARSER_ID_))


	# Init grammar (add grammar rules for defined grammar), etc.
	_final_redesign_env.setup()


	# Display item sets
	# display_item_states(__GRAMMAR__.generate_states())
	return _final_redesign_env


def G9_environment_factory(debug_mode=False):

	__GRAMMAR__ = test_grammar_factory()

	_G9_tokenizer_handler = Grammar9TokenizerHandler()
	__TOKENIZER__ = Tokenizer(handler=_G9_tokenizer_handler)

	__PARSE_TABLE__ = ParseTable(table_id="[ • --- • Grammar9ParseTable • ---• ]")
	__TABLE_BUILDER__ = Grammar9TableBuilder(grammar=__GRAMMAR__)

	_PARSER_ID_ = "CoreParser3"
	__PARSER__ = CoreParser3(init_state=0, grammar=__GRAMMAR__, parse_table=__PARSE_TABLE__, debug_mode=debug_mode, parser_id=_PARSER_ID_)
	_final_redesign_env = FinalRedesignEnv(parser=__PARSER__, grammar=__GRAMMAR__, tokenizer=__TOKENIZER__, table_builder=__TABLE_BUILDER__, parse_table=__PARSE_TABLE__)

	_final_redesign_env.add_field("tokenize", True)
	_final_redesign_env.add_field("grammar_version", 9)
	_final_redesign_env.add_field("end_symbol", "#")
	_final_redesign_env.add_field("logger", PyLogger.get(_PARSER_ID_))

	# Init grammar (add grammar rules for defined grammar), etc.
	_final_redesign_env.setup()


	# Display parse table setup
	# __PARSE_TABLE__.print()

	# Display item sets
	# display_item_states(__GRAMMAR__.generate_states())

	return _final_redesign_env


def dateLang_environment_factory_v0_0_1(debug_mode=False):
	# Environment factory for test grammar 10, i.e. a simple 'date' grammar

	__GRAMMAR__ = test_grammar_factory()

	_G10_tokenizer_handler = DateGrammarTokenizerHandler()
	__TOKENIZER__ = Tokenizer(handler=_G10_tokenizer_handler)

	__PARSE_TABLE__ = ParseTable(table_id="[ • --- • Grammar9ParseTable • ---• ]")
	__TABLE_BUILDER__ = DateGrammarTableBuilder(grammar=__GRAMMAR__)

	_PARSER_ID_ = "CoreParser3"
	__PARSER__ = CoreParser3(init_state=0, grammar=__GRAMMAR__, parse_table=__PARSE_TABLE__, debug_mode=debug_mode, parser_id=_PARSER_ID_)
	_final_redesign_env = FinalRedesignEnv(parser=__PARSER__, grammar=__GRAMMAR__, tokenizer=__TOKENIZER__, table_builder=__TABLE_BUILDER__, parse_table=__PARSE_TABLE__)

	_final_redesign_env.add_field("tokenize", True)
	_final_redesign_env.add_field("grammar_version", "dateLang_v0_0_1")
	_final_redesign_env.add_field("end_symbol", "#")
	_final_redesign_env.add_field("logger", PyLogger.get(_PARSER_ID_))

	# Init grammar (add grammar rules for defined grammar), etc.
	_final_redesign_env.setup()


	# Display parse table setup
	# __PARSE_TABLE__.print()

	# Display item sets
	display_item_states(__GRAMMAR__.generate_states())

	return _final_redesign_env


def simplang_environment_factory(debug_mode=False):
	pass


def todo_lang_parser_factory(debug_mode=False):
	__GRAMMAR__ = test_grammar_factory()
	_grammar_version = "todo_lang_v0_0_1"

	_todo_lang_tokenizer_handler = ToDoLangTokenizerHandler()
	__TOKENIZER__ = Tokenizer(handler=_todo_lang_tokenizer_handler)

	__PARSE_TABLE__ = ParseTable(table_id="[ • --- • ToDoLangParseTable • ---• ]")
	__TABLE_BUILDER__ = ToDoLangTableBuilder(grammar=__GRAMMAR__)

	_PARSER_ID_ = "ToDoLang"
	__PARSER__ = ToDoLangParser(init_state=0, parser_id=_PARSER_ID_)

	# Init grammar directly, without an abstracted environment
	# containing all components
	init_grammar(__GRAMMAR__, _grammar_version)

	# Display item sets
	# display_item_states(__GRAMMAR__.generate_states())
	return __PARSER__


def run_testing(test_inputs, environment):
	print()
	print()
	for idx, (_INPUT_, _is_valid) in enumerate(test_inputs, start=1):
		_TOKENIZED_INPUT = environment.tokenize(_INPUT_)
		_TOKENIZED_INPUT = [i for i in _TOKENIZED_INPUT if i.token_type != Grammar8TokenType.SKIP]
		_parse_context = environment.execute(_TOKENIZED_INPUT, context_id=f"TEST-INPUT-{idx}")
		_parse_result = _parse_context.result() or False
		_test_passed = _parse_result == _is_valid
		_result_text_out = bold_text(apply_color(11, f"\tTEST-INPUT-{idx}")) + f"  \n\t  |\n  \t  |\n" + f"\t  • " + bold_text(apply_color(208, f"{_INPUT_}")) + "\n\t  |\n\t  |\n\t  |\n\t  • -----> " + bold_text((apply_color(10, " • --- VALID • --- • ") if _parse_result else apply_color(9, " • --- • INVALID • --- • ")))
		_test_passed_disp_text = f"  " + (bold_text(apply_color(10, "**PASS**")) if _test_passed else bold_text(apply_color(9, "**FAIL**")))
		print()
		print(f"{_test_passed_disp_text}\n")
		display_tokens(_TOKENIZED_INPUT, _INPUT_)
		print()
		print(_result_text_out)
		print()
		print()
		print()


@profile_callable(sort_by=SortBy.TIME)
def final_main(debug_mode=True):
	_todo_lang_input = None
	_todo_lang_input_filepath = r"/Users/mickey/Desktop/Python/custom_packages/pyparse/examples/example_ToDoLang_input.py"
	with open(_todo_lang_input_filepath, "r", newline="") as _in_file:
		_todo_lang_input = _in_file.read()

	_counter = 0
	_idx = 0
	_len_input = len(_todo_lang_input)
	while _counter < _len_input:
		_idx = _counter
		_counter += 1
		_char = repr(_todo_lang_input[_idx])


	_symbol_stack = deque()
	_state_stack = deque()
	_test_list = []
	_test_input = "@TODO<This is the body of a todo or note>"

	_todo_lang_tokenizer_handler = ToDoLangTokenizerHandler()
	__TOKENIZER__ = Tokenizer(handler=_todo_lang_tokenizer_handler)
	_token_context = __TOKENIZER__.tokenize(_test_input)
	print(f"TOKEN CONTEXT:")
	for i in _token_context:
		print(f"\t{i}")
	print()
	__PARSER__ = todo_lang_parser_factory(debug_mode=debug_mode)


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
		print(underline_text(bold_text(apply_color(172, f"STATE: {_current_state}\nITERATION: {_context_len}"))))
		print(f"  |")
		print(f"  •--• ", end="")
		print(apply_color(220, f"CURRENT STATE: {_current_state}"))
		if _context_len < 3:
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
			print(underline_text(bold_text(apply_color(172, f"STATE: {_current_state}\nITERATION: {_context_len}"))))
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
	

	def _init_state(parser, context):
		_current_state = parser.state


		parser.update("SUCK_IT")




	__PARSER__.register_state(0, _init_state)
	__PARSER__.register_state("SUCK_IT", _suck_it)
	__PARSER__.register_state("SUCK_IT4", _suck_it_4)
	__PARSER__.register_state((2, "*"), _2_and_multiply)
	__PARSER__.register_state((2, "+"), _2_and_plus)
	__PARSER__.register_state(ParserStateType.STOP, lambda parser, parse_context: parser.stop())


	# Updating state to ensure parser's initial state prior to parse is
	# "SUCK_IT"; parser defaults to a kwarg argument value of
	# integer 0 (zero)
	_result = __PARSER__.parse(_test_list)
	print()
	print(f"RESULT")
	print(f"   |")
	print(f"   |")
	print(f"   • --- ", end="")
	print(_result)
	print()


	# _example_grammar_8_src = None
	# with open(r"/Users/mickey/Desktop/Python/custom_packages/pyparse/examples/example_grammar_8_v0_0_1.eight", 'r', newline="") as _in_file:
	# 	_example_grammar_8_src = [i for i in _in_file.readlines() if i]


	# for i in _example_grammar_8_src:
	# 	print(f"•---> {i}")


	# _TEST_INPUTS_1_ = [
	# 	("10 + 10", True),
	# 	("10 + 10 10", False),
	# 	("10 + 10\n", True),
	# 	("10 +", False),
	# 	("10 + -", False),
	# 	("(3 * 2 + 2) / 2", True),
	# 	("(3 * 2 + 2) - (12 + 2 * 10)", True)
	# ]

	# _EXAMPLE_GRAMMAR_8_SOURCE_INPUT_ASSERTIONS = (True, False, True, False, False, True, True)
	# _EXAMPLE_GRAMMAR_8_SOURCE_INPUT = [(_input_, _assert_) for _input_, _assert_ in zip(_example_grammar_8_src, _EXAMPLE_GRAMMAR_8_SOURCE_INPUT_ASSERTIONS)]


	# # _test_grammar_8_env = G8_environment_factory(debug_mode=debug_mode)
	# _test_grammar_8_env = G8_environment_factory_newest(debug_mode=debug_mode)
	# run_testing(_TEST_INPUTS_1_, _test_grammar_8_env)



	# _TEST_INPUTS_1_ = [
	# 	("ab", True),
	# 	("ab!", True),
	# 	("a!b", False),
	# 	("ba!", False),
	# 	("b!a", False),
	# 	("!ab", False),
	# 	("!ba", False),
	# 	("(ab)", True),
	# 	("(a!b)", False),
	# 	("(ba!)", False),
	# 	("(ab!)", True),
	# 	("(b!a)", False),
	# 	("(!ab)", False),
	# 	("(!ba)", False),
	# 	("aaaaaaaaaaaaaaaaaaabbbbbbbbbbbbb!!!!!!!!abbb!)", False)
	# ]

	# _test_grammar_9_env = G9_environment_factory(debug_mode=debug_mode)	
	# run_testing(_TEST_INPUTS_1_, _test_grammar_9_env)



	# _example_datelang_source = None
	# with open(r"/Users/mickey/Desktop/Python/custom_packages/pyparse/examples/example_datelang_source.dlang", "r", newline="") as _datelang_in_file:
	# 	_example_datelang_source = [i for i in _datelang_in_file.readlines() if i]


	# _EXAMPLE_DATELANG_SOURCE_INPUT_IS_VALID = (False, True, True, True, True, False, False, False, True, True, False, True)
	# _EXAMPLE_DATELANG_SOURCE_INPUT = [(str(_input_).strip(), _is_valid) for _input_, _is_valid in zip(_example_datelang_source, _EXAMPLE_DATELANG_SOURCE_INPUT_IS_VALID)]


	# _dateLang_environment_factory_v0_0_1 = dateLang_environment_factory_v0_0_1(debug_mode=debug_mode)
	# return run_testing(_EXAMPLE_DATELANG_SOURCE_INPUT, _dateLang_environment_factory_v0_0_1)


if __name__ == "__main__":
	pass
