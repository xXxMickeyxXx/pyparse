from pylog import PyLogger, LogType
from pyprofiler import profile_callable, SortBy
from pyutils import (
    cmd_argument,
    DEFAULT_PARSER as DEFAULT_CMD_LINE_PARSER
)

from .scratch_package_paths import (
    LOGGING_ROOT
)
from .scratch_init_grammar import (
	test_grammar_factory,
	init_grammar
)
from .final_redesign import (
	Grammar9TableBuilder,
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


@profile_callable(sort_by=SortBy.TIME)
def final_main():
	__GRAMMAR__ = test_grammar_factory()

	__TOKENIZER__ = Tokenizer(handler=None)

	__PARSE_TABLE__ = ParseTable(table_id="[ • --- • Grammar9ParseTable • ---• ]")
	__PARSER__ = CoreParser3(init_state=0, grammar=__GRAMMAR__, parse_table=__PARSE_TABLE__, debug_mode=True, parser_id="[ • --- • CoreParser3 • ---• ]")
	_final_redesign_env = FinalRedesignEnv(parser=__PARSER__, grammar=__GRAMMAR__, tokenizer=__TOKENIZER__, parse_table=__PARSE_TABLE__)

	_final_redesign_env.add_field("grammar_version", 9)
	_final_redesign_env.add_field("end_symbol", "#")
	_final_redesign_env.add_field("table_builder", Grammar9TableBuilder(__GRAMMAR__))

	# Init grammar (add grammar rules for defined grammar), etc.
	_final_redesign_env.setup()

	# for state, items in _final_redesign_env.item_states.items():
	# 	print(f"STATE_{state}")
	# 	for _item in items:
	# 		print(_item)
	# 		print()
	# 	print()
	_TEST_INPUT_1_ = "ab"
	_TEST_INPUT_2_ = None
	_TEST_INPUT_3_ = None

	_INPUT_ = _TEST_INPUT_1_
	_parse_result = _final_redesign_env.execute(_INPUT_)
	_result_text_out = bold_text(apply_color(11, f"\t{_INPUT_}")) + "\n\n\t |\n\t |\n\t |\n\t • -----> " + bold_text((apply_color(10, " • --- VALID • --- • ") if _parse_result else apply_color(9, " • --- • INVALID • --- • ")))
	print(_result_text_out)
	print()
	print()


if __name__ == "__main__":
	pass
