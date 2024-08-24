from pylog import PyLogger, LogType
from pyprofiler import profile_callable, SortBy
from pyutils import (
    cmd_argument,
    DEFAULT_PARSER as DEFAULT_CMD_LINE_PARSER
)

from .scratch_package_paths import (
    LOGGING_ROOT
)
from .scratch_parse_table import ParseTable
import scratch.scratch_runtime_setup as runtime_setup
from .scratch_shell_init import initialize_shell
from .scratch_logging_init import init_logging
from .scratch_cons import PyParseLoggerID
from .utils import display_result


GRAMMAR = runtime_setup.GRAMMAR
CoreParser2 = runtime_setup.CoreParser2
TestGrammar4ParserEnv = runtime_setup.TestGrammar4ParserEnv
ParseContext = runtime_setup.ParseContext


_runtime_logger = PyLogger.get(PyParseLoggerID.RUNTIME)


# @profile_callable(sort_by=SortBy.TIME)
def parse_main():

	# Initialize runtime for shell and logging
	_logging_setup_callbacks = initialize_shell()

	ENCODING = "UTF-8"
	USE_LOGGING = cmd_argument("log", parser=DEFAULT_CMD_LINE_PARSER)
	LOGGING_DIR = cmd_argument("logging_dir", parser=DEFAULT_CMD_LINE_PARSER)
	LOG_FILENAME = cmd_argument("log_filename", parser=DEFAULT_CMD_LINE_PARSER)
	LOGGING_LEVEL = cmd_argument("logging_level", parser=DEFAULT_CMD_LINE_PARSER)

	init_logging(
		use_logging=USE_LOGGING,
		log_filename=LOG_FILENAME,
		logging_dir=LOGGING_DIR,
		logging_level=LOGGING_LEVEL,
		logging_callbacks=_logging_setup_callbacks,
		encoding=ENCODING
	)


	# Instantiate parser environment
	PARSER_ENVIRONMENT_ID = "SCRATCH_TEST_PARSER_ENV"
	_test_grammar_4_env = TestGrammar4ParserEnv(env_id=PARSER_ENVIRONMENT_ID)


	_runtime_logger.submit_log(
		message=f"Initializing 'pyparse' runtime environment ('pyparse', running as a package)",
		env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}"
	)
	# TODO: impolement tokenizer for 'init_grammar_4'
	# Generate tokens to feed the parser
	TOKENIZER_ID = None
	_tokenizer = None


	_runtime_logger.submit_log(
		message=f"Tokenizer has been initialized",
		env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}",
		tokenizer_id=f"TOKENIZER ID: {TOKENIZER_ID} (TOKENIZER IS CURRENTLY DISABLED)"
	)


	# Create parse table, used to guide the LR(0) automaton that makes
	# up the design for the shift/reduce parser
	PARSE_TABLE_ID = "[ • -- TEST_PARSE_TABLE -- • ]"
	_parse_table = ParseTable(table_id=PARSE_TABLE_ID)


	_runtime_logger.submit_log(
		message=f"Parse table has been initialized",
		env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}",
		table_id=f"PARSE TABLE ID: {PARSE_TABLE_ID}"
	)


	# Instantiate parser back-end (actual parsing implementation)
	PARSER_ID = "[ • -- TEST SHIFT/REDUCE PARSER (LR(0)) -- • ]"
	_parser_impl = CoreParser2(init_state=0, grammar=GRAMMAR, parse_table=_parse_table, parser_id=PARSER_ID)


	_runtime_logger.submit_log(
		message=f"'pyparse' has been initialized",
		env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}",
		parser_id=f"PARSE TABLE ID: {PARSER_ID}"
	)



	# Set parer env's 'parser', 'grammar', 'tokenizer' and 'parse_table' fields
	_test_grammar_4_env.set_grammar(GRAMMAR)
	_test_grammar_4_env.set_tokenizer(_tokenizer)
	_test_grammar_4_env.set_table(_parse_table)
	_test_grammar_4_env.set_parser(_parser_impl)


	_runtime_logger.submit_log(
		message=f"'pyparse' environment has been initialized and has set it's 'grammar', 'tokenizer', 'table', and 'parser' fields; continuing setup...",
		env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}",
		grammar_id=GRAMMAR.grammar_id,
		tokenizer_id=TOKENIZER_ID,
		table_id=PARSE_TABLE_ID,
		parser_id=PARSER_ID
	)


	# Setup environment (as defined within the 'setup' method of the environment implementation)
	_test_grammar_4_env.setup()


	_runtime_logger.submit_log(
		message=f"'pyparse' environment has completed it's setup...Initializing test input and parse context...",
		env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}"
	)


	TEST_INPUT = "1+0"
	_parse_context = ParseContext(input=TEST_INPUT)


	_runtime_logger.submit_log(
		message=f"Test input and parse context for the 'pyparse' package runtime has been initialized; entering parser's mainloop...",
		env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}"
	)


	_package_parse_result = _test_grammar_4_env.parse(_parse_context).result()
	display_result(TEST_INPUT, _package_parse_result)


	if not _package_parse_result:
		_package_parse_message = f"'pyparse' package runtime has failed parsing it's associated input; exiting runtime and gracefully shutting down program..."
	else:
		_package_parse_message = f"'pyparse' package runtime has succeeded parsing it's associated input; exiting runtime and gracefully shutting down program..."

	_runtime_logger.submit_log(
		message=_package_parse_message,
		env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}",
		result=_package_parse_result
	)


	# Run parser environment (**TESTING (call to it's 'run' method will bemoved, and possibly renamed all together, that is, the 'run' method may be changed**)
	# _test_grammar_4_env.run()


	# Initialize parser environment, as it's been all setup otherwise
	# parse_and_display(_test_grammar_4_env, count=1)

	# Add white space below final text that displays in order to better separate the text
	# displayed from running this function and the profiler results displaying
	for _ in range(5):
		print()


if __name__ == "__main__":
	pass
