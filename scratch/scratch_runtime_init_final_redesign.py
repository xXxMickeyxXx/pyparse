from pylog import PyLogger, LogType
from pyprofiler import profile_callable, SortBy
from pyutils import (
    cmd_argument,
    DEFAULT_PARSER as DEFAULT_CMD_LINE_PARSER
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
from .final_redesign import (
	Grammar9TokenType,
	Grammar9TokenizerHandler,
	Grammar9TableBuilder,
	DateGrammarTokenType,
	DateGrammarTokenizerHandler,
	DateGrammarTableBuilder,
	CoreParser3,
	FinalRedesignEnv
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
# from .source_descriptor import SourceFile, 
from .scratch_cons import PyParseLoggerID
from .utils import (
	display_result,
	display_item_states,
	bold_text,
	apply_color,
	underline_text,
	center_text
)


def display_tokens(tokens, input):
	_tokens_str = bold_text(apply_color(214, "** TOKENS **"))
	_all_except_last_token = tokens[:-1:]
	_last_token = tokens[-1]
	print()
	_input_txt = f"{'INPUT'} --->  {apply_color(208, input)}"
	print(f"  +---------------------+---------------------+")
	print(f"                                               ")
	print(f"  |              {apply_color(226, _input_txt)}               |")
	print(f"                                               ")
	print(f"  +---------------------+---------------------+")
	print(f"                                               ")
	print(f"  |        {bold_text(apply_color(11, 'TYPE'))}         |        {bold_text(apply_color(11, 'VALUE'))}        |")
	print(f"                                               ")
	for _token in _all_except_last_token:
		print(f"  +---------------------+---------------------+")
		print(f"  |                     |                     |")
		if _token.token_val in {"!", "(", ")"}:
			print(f"  +  {_token.token_type}\t          {_token.token_val}           +")
		else:
			print(f"  +  {_token.token_type}\t\t          {_token.token_val}           +")
		print(f"  |                     |                     |")
	print(f"  +---------------------+---------------------+")
	print(f"  |                     |                     |")
	print(f"  +  {_last_token.token_type}\t\t  {_last_token.token_val}           +")
	print(f"  |                     |                     |")
	print(f"  +---------------------+---------------------+")
	print()


def display_tokens(tokens, input):
	_tokens_str = bold_text(apply_color(214, "    ** TOKENS **"))
	print(_tokens_str)
	print()
	for _token in tokens:
		print(f"\tTOKEN TYPE:  {apply_color(208, _token.token_type)}")
		print(f"\tTOKEN VALUE: {apply_color(208, _token.token_val)}")
		print()


def G9_environment_factory():

	__GRAMMAR__ = test_grammar_factory()

	_G9_tokenizer_handler = Grammar9TokenizerHandler()
	__TOKENIZER__ = Tokenizer(handler=_G9_tokenizer_handler)

	__PARSE_TABLE__ = ParseTable(table_id="[ • --- • Grammar9ParseTable • ---• ]")
	__TABLE_BUILDER__ = Grammar9TableBuilder(grammar=__GRAMMAR__)
	# __TABLE_BUILDER__ = ManualGrammar4TableBuilder(grammar=__GRAMMAR__)

	_PARSER_ID_ = "CoreParser3"
	__PARSER__ = CoreParser3(init_state=0, grammar=__GRAMMAR__, parse_table=__PARSE_TABLE__, debug_mode=False, parser_id=_PARSER_ID_)
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


def G10_environment_factory():
	# Environment factory for test grammar 10, i.e. a simple 'date' grammar

	__GRAMMAR__ = test_grammar_factory()

	_G10_tokenizer_handler = DateGrammarTokenizerHandler()
	__TOKENIZER__ = Tokenizer(handler=_G10_tokenizer_handler)

	__PARSE_TABLE__ = ParseTable(table_id="[ • --- • Grammar9ParseTable • ---• ]")
	__TABLE_BUILDER__ = DateGrammarTableBuilder(grammar=__GRAMMAR__)

	_PARSER_ID_ = "CoreParser3"
	__PARSER__ = CoreParser3(init_state=0, grammar=__GRAMMAR__, parse_table=__PARSE_TABLE__, debug_mode=True, parser_id=_PARSER_ID_)
	_final_redesign_env = FinalRedesignEnv(parser=__PARSER__, grammar=__GRAMMAR__, tokenizer=__TOKENIZER__, table_builder=__TABLE_BUILDER__, parse_table=__PARSE_TABLE__)

	_final_redesign_env.add_field("tokenize", True)
	_final_redesign_env.add_field("grammar_version", 10)
	_final_redesign_env.add_field("end_symbol", "#")
	_final_redesign_env.add_field("logger", PyLogger.get(_PARSER_ID_))

	# Init grammar (add grammar rules for defined grammar), etc.
	_final_redesign_env.setup()


	# Display parse table setup
	# __PARSE_TABLE__.print()

	# Display item sets
	# display_item_states(__GRAMMAR__.generate_states())

	return _final_redesign_env


def run_testing(test_inputs, environment):
	print()
	for idx, (_INPUT_, _is_valid) in enumerate(test_inputs, start=1):
		_TOKENIZED_INPUT = environment.tokenize(_INPUT_)
		_parse_result = environment.execute(_TOKENIZED_INPUT, context_id=f"TEST-INPUT-{idx}")
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
	print()
	print()


# @profile_callable(sort_by=SortBy.TIME)
def final_main():
	# _TEST_INPUTS_1_ = [
	# 	("ab", True),
	# 	# ("ab!", False),
	# 	# ("a!b", False),
	# 	# ("ba!", False),
	# 	# ("b!a", False),
	# 	# ("!ab", False),
	# 	# ("!ba", False),
	# 	("(ab)", True),
	# 	("(ab!)", False),
	# 	# ("(a!b)", False),
	# 	# ("(ba!)", False),
	# 	# ("(b!a)", False),
	# 	# ("(!ab)", False),
	# 	# ("(!ba)", False)
	# ]

	# _test_grammar_9_env = G9_environment_factory()	
	# run_testing(_TEST_INPUTS_1_, _test_grammar_9_env)


	_TEST_INPUTS_1_ = [
		("  /12/2024", False),
		("12/22/1990", True),
		("12.22 .2004", True),
		("11/29/2025", True),
		("12/22/1990", False)
	]


	_G10_environment_factory = G10_environment_factory()	
	run_testing(_TEST_INPUTS_1_, _G10_environment_factory)


if __name__ == "__main__":
	pass
