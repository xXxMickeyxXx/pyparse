from collections import deque
from enum import IntEnum, StrEnum, auto

from pylog import PyLogger, LogType
from pyprofiler import profile_callable, SortBy
from pyutils import (
    cmd_argument,
    DEFAULT_PARSER as DEFAULT_CMD_LINE_PARSER
)
from pyparse import Token

from .scratch_simple_lang_grammar import (
	SimpleLangTokenType,
	SimpleLangTokenizerHandler,
	SimpleLangTableBuilder,
	SimpleLangParser
	# __ADD_ACTION_HANDLER__,
	# __SIMPLE_LANG_ACTION_HANDLER__
	)
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


def register_states(parser):
	# parser.register_state(0, lambda _par_, _par_context_: print(f"HOLA!"))
	# parser.register_state(1, lambda _par_, _par_context_: _par_.stop())
	parser.register_state((1, "$"), lambda _par_, _par_context_: _par_.submit_action(lambda x: print("HEY YOU --->", x), "BILLY!"))
	parser.register_state(0, lambda _par_, _par_context_: print(f"HOLA!"))
	parser.register_state(0, lambda _par_, _par_context_: _par_.update(3))
	parser.register_state(0, lambda _par_, _par_context_: print("IN STATE --->", 0, "TO STATE --->", 3))
	parser.register_state(0, lambda _par_, _par_context_: _par_.submit_action(lambda x, y: print(f"Hell, yeah", x, y), "MICKEY", "and PIZZA!"))
	parser.register_state(3, lambda _par_, _par_context_: _par_.update((1, "$")))
	parser.register_state(3, lambda _par_, _par_context_: _par_.submit_action(lambda x: print(f"Hell yeah {x}!"), "TIMMY"))
	parser.register_state(3, lambda _par_, _par_context_: print("\tIN STATE --->", _par_.state, "\n\tTO STATE --->", "(1, '$')"))
	parser.register_state((1, "$"), lambda _par_, _par_context_: _par_.update(SimpleLangTokenType.END_SYMBOL))
	parser.register_state((1, "$"), lambda _par_, _par_context_: print(f"IN STATE: (1, $) TO STATE: 1"))
	parser.register_state(SimpleLangTokenType.END_SYMBOL, lambda _par_, _par_context_: print("STOPPING PARSER"))
	parser.register_state(SimpleLangTokenType.END_SYMBOL, lambda _par_, _par_context_: _par_.stop())


@profile_callable(sort_by=SortBy.TIME)
def final_main(debug_mode=True):
	_simple_lang_input_filepath = r"/Users/mickey/Desktop/Python/custom_packages/pyparse/examples/example_simplang_input.sim"
	with open(_simple_lang_input_filepath, "r", newline="") as _in_file:
		_test_input = _in_file.read()

	__GRAMMAR__ = test_grammar_factory()
	_GRAMMAR_VERSION_ = "simple_lang_v0_0_1"
	init_grammar(__GRAMMAR__, _GRAMMAR_VERSION_)

	# for state, rule in __GRAMMAR__.generate_states().items():
	# 	print(bold_text(apply_color(214, f"STATE: {state}")))
	# 	print()
	# 	for i in rule:
	# 		_id = i.rule_id
	# 		_head = i.rule_head
	# 		_body = i.rule_body
	# 		_status = i.status()
	# 		print(f"\t • -------")
	# 		print(f"\t| RULE-ID:     {_id}")
	# 		print(f"\t| RULE-HEAD:   {_head}")
	# 		print(f"\t| RULE-BODY:   {_body}")
	# 		print(f"\t| AUG-RULE-:   {_status}")
	# 		print(f"\t • -------")
	# 		print()
	# 	print()
	# 	print()

	_simple_lang_tokenizer_handler = SimpleLangTokenizerHandler()
	__TOKENIZER__ = Tokenizer(handler=_simple_lang_tokenizer_handler)
	_token_context_ = __TOKENIZER__.tokenize(_test_input)
	# _token_context_ = [i for i in _token_context_ if i.token_type != SimpleLangTokenType.SKIP]
	print()
	print(bold_text(apply_color(214, f" INPUT:")), end="\n")
	print(f"    |")
	print(f"    |")
	print(f"    |")
	for _idx_, _input_ in enumerate(_test_input.split("\n"), start=1):
		_input_repr_ = repr(_input_)
		if _idx_ == 1:
			print(f"     • ---> {_input_repr_}")
		else:
			print(f"            {_input_repr_}")
	print()
	print(bold_text(apply_color(204, " TOKEN CONTEXT:")))
	print(f"    |")
	print(f"    |")
	print(f"    |")
	for _idx, _token_ in enumerate(_token_context_, start=1):
		if _idx == 1:
			print(f"     • ---> {_token_}")
		else:
			print(f"            {_token_}")	
	for _ in range(2):
		print()


	_INIT_STATE_ = 0
	_PARSER_ID_ = "SimpleLang_v0_0_1"
	__PARSER__ = SimpleLangParser(init_state=_INIT_STATE_, parser_id=_PARSER_ID_)
	# register_states(__PARSER__)

	_pretval = __PARSER__.parse(_token_context_)
	print()
	print(bold_text(apply_color(214, f"\tPARSE IS...")))
	print(bold_text(apply_color(10, f"\t\t• --- VALID --- •")) if _pretval else bold_text(apply_color(9, f"\t\t• --- INVALID --- •")))
	print()
	# print()
	# for i in _pretval:
	# 	print(i)


	# _symbol_stack = deque()
	# _state_stack = deque()

	# _symbol_stack.append(_token_context_[0])
	# _state_stack.append(_INIT_STATE_)

	# parser.register_state(0, lambda _par_, _par_context_: _par_.submit_action)




	# _test_list = []
	# _test_input = "@TODO<This is the body of a todo or note>"
	# _token_context = __TOKENIZER__.tokenize(_test_input)
	# print(f"TOKEN CONTEXT:")
	# for i in _token_context:
	# 	print(f"\t{i}")
	# print()
	# __PARSER__ = todo_lang_parser_factory(debug_mode=debug_mode)



if __name__ == "__main__":
	pass
