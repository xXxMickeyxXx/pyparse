from pyprofiler import profile_callable, SortBy

from .scratch_parse_table import ParseTable
import scratch.scratch_runtime_setup as runtime_setup


GRAMMAR = runtime_setup.GRAMMAR
CoreParser2 = runtime_setup.CoreParser2
TestGrammar4ParserEnv = runtime_setup.TestGrammar4ParserEnv


@profile_callable(sort_by=SortBy.TIME)
def parse_main():
	# Initialized parser environment ID
	PARSER_ENVIRONMENT_ID = "SCRATCH_TEST_PARSER_ENV"


	# TODO: impolement tokenizer for 'init_grammar_4'
	# Generate tokens to feed the parser
	_tokenizer = None


	# Create parse table, used to guide the LR(0) automaton that makes
	# up the design for the shift/reduce parser
	_parse_table = ParseTable(table_id="[ • -- TEST_PARSE_TABLE -- • ]")


	# Instantiate parser back-end (actual parsing implementation)
	_parser_impl = CoreParser2(init_state=0, grammar=GRAMMAR, parse_table=_parse_table)


	# Instantiate parser environment
	_test_grammar_4_env = TestGrammar4ParserEnv(env_id=PARSER_ENVIRONMENT_ID)

	# Set parer env's 'parser', 'grammar', 'tokenizer' and 'parse_table' fields
	_test_grammar_4_env.set_grammar(GRAMMAR)
	_test_grammar_4_env.set_tokenizer(_tokenizer)
	_test_grammar_4_env.set_table(_parse_table)
	_test_grammar_4_env.set_parser(_parser_impl)


	# Setup environment (as defined within the 'setup' method of the environment implementation)
	_test_grammar_4_env.setup()


	# TODO: remove call to build parse table as it's just for **TESTING** (at least
	# 		the call here is for testing)
	_test_grammar_4_env.__build_table__()

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
