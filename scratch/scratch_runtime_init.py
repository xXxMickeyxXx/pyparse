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
from .scratch_runtime_setup import (
	GRAMMAR,
	CoreParser2,
	TestGrammar4ParserEnv,
	ParseContext,
	TestGrammar4Tokenizer,
	TestGrammar4TokenizeHandler,
	parse_and_display,
	user_runtime
)
from .scratch_shell_init import initialize_shell
from .scratch_logging_init import init_logging
# from .source_descriptor import SourceFile, 
from .scratch_cons import PyParseLoggerID
from .utils import display_result


_runtime_logger = PyLogger.get(PyParseLoggerID.RUNTIME)


def runner(env):
	_PARSER_ENVIRONMENT_ID = env.env_id
	_result_logger_msg_mapping = {
		0: f"'pyparse' has completed it's expected runtime without issue...exiting program...",
		1: f"'pyparse' has completed it's runtime with un-expected errors; please review and try again...exiting program..."
	}

	try:
		env.setup()
	except RuntimeError:
		pass

	_runtime_logger.submit_log(
		message=f"'pyparse' environment has completed it's setup...initializing test input and parse context...",
		env_id=f"ENVIRONMENT ID: {_PARSER_ENVIRONMENT_ID}"
	)


	_runtime_logger.submit_log(
		message=f"Test input and parse context for the 'pyparse' package runtime has been initialized...entering parser's mainloop...",
		env_id=f"ENVIRONMENT ID: {_PARSER_ENVIRONMENT_ID}"
	)
	_retval = env.run()

	_runtime_logger.submit_log(
		message=_result_logger_msg_mapping[_retval ^ 0],
		env_id=f"ENVIRONMENT ID: {_PARSER_ENVIRONMENT_ID}",
		function="runner",
		file=str(__file__),
		module=f"scratch_runtime_init"
	)


@profile_callable(sort_by=SortBy.TIME)
def parse_main():

	# Initialize runtime for shell and logging
	_logging_setup_callbacks = initialize_shell()

	DEBUG_MODE = cmd_argument("debug_mode", parser=DEFAULT_CMD_LINE_PARSER)
	ENCODING = "UTF-8"
	USE_LOGGING = cmd_argument("log", parser=DEFAULT_CMD_LINE_PARSER) or DEBUG_MODE
	LOGGING_DIR = cmd_argument("logging_dir", parser=DEFAULT_CMD_LINE_PARSER)
	LOG_FILENAME = cmd_argument("log_filename", parser=DEFAULT_CMD_LINE_PARSER)
	LOGGING_LEVEL = "DEBUG" if DEBUG_MODE else cmd_argument("logging_level", parser=DEFAULT_CMD_LINE_PARSER)

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
	TOKENIZER_ID = 'SCRATCH_TEST_TOKENIZER'
	_tokenizer = TestGrammar4Tokenizer(input="")


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
	if DEBUG_MODE:
		print(f"PARSER IN DEBUG MODE")
	_parser_impl = CoreParser2(init_state=0, grammar=GRAMMAR, parse_table=_parse_table, parser_id=PARSER_ID, debug_mode=DEBUG_MODE)


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


	_test_grammar_4_env.setup()
	_runtime_logger.submit_log(
		message=f"'pyparse' environment has been initialized and has set it's 'grammar', 'tokenizer', 'table', and 'parser' fields; continuing setup...",
		env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}",
		grammar_id=GRAMMAR.grammar_id,
		tokenizer_id=TOKENIZER_ID,
		table_id=PARSE_TABLE_ID,
		parser_id=PARSER_ID
	)


	def user_input_runner():
		_counter = 0
		_user_runtime_generator = user_runtime(_test_grammar_4_env)
		while True:
			try:
				_user_input, _parse_result = next(_user_runtime_generator)
				_counter + 1
			except StopIteration as stop_iter:
				return 0
			else:
				if not _parse_result:
					_package_parse_message = f"'pyparse' package runtime has failed parsing it's associated input; exiting runtime and gracefully shutting down program..."
				else:
					_package_parse_message = f"'pyparse' package runtime has succeeded parsing it's associated input; exiting runtime and gracefully shutting down program..."
				_runtime_logger.submit_log(
					message=_package_parse_message,
					env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}",
					parse_result=_parse_result,
					user_input=_user_input,
					runtime_cycle=_counter
				)
		for _ in range(5):
			print()


	def single_parse_runner(string="0+1*1*0*0+1+1+1+1+1+1+1+1+1+1+1", env=None):
		_env = env if env is not None else _test_grammar_4_env
		_parse_context = ParseContext()
		_parse_context.set_input(string)
		_package_parse_result = _test_grammar_4_env.parse(_parse_context).result()
		display_result(string, _package_parse_result)

		if not _package_parse_result:
			_package_parse_message = f"'pyparse' package runtime has failed parsing it's associated input; exiting runtime and gracefully shutting down program..."
		else:
			_package_parse_message = f"'pyparse' package runtime has succeeded parsing it's associated input; exiting runtime and gracefully shutting down program..."

		_runtime_logger.submit_log(
			message=_package_parse_message,
			env_id=f"ENVIRONMENT ID: {PARSER_ENVIRONMENT_ID}",
			result=_package_parse_result
		)
		for _ in range(5):
			print()


	def parse_and_display_runner(env=None, count=-1):
		_env = env if env is not None else _test_grammar_4_env
		_test_input_lst = []

		for i in ['0 + 1', '1 + 0', '00 + 11', '11 + 00', '1 + 1', '0 + 0', '0 * 1', '1 * 0', '00 * 11', '11 * 00', '1 * 1', '0 * 0', '6 * 51']:
			_tmp_lst = []
			for e in i:
				if e in {" ", "  ", "   "}:
					continue
				_tmp_lst.append(e)
			_test_input_lst.append("".join(_tmp_lst))

		_should_be_valid_results = [True, True, False, False, True, True, True, True, False, False, True, True, False]
		parse_and_display(_env, _test_input_lst, _should_be_valid_results, count=count)


	# Invoke one of several runtimes for scratch sub-package testing
	# user_input_runner()
	# single_parse_runner(string="1*0")
	# parse_and_display_runner(count=-1)


	# Invoke main 'runner' function
	runner(_test_grammar_4_env)


if __name__ == "__main__":
	pass
