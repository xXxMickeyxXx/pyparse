from abc import ABC, abstractmethod

from pyparse import Tokenizer, LexHandler, Token
from pylog import PyLogger, LogType
from pysynchrony import (
	PySynchronyScheduler,
	PySynchronyEventLoop,
	PySynchronyContext,
	PySynchronyCoroutineTask,
	PySynchronyPort,
	PySynchronyEvent,
	PySynchronySysCall,
	PriorityQueueFactory,
	PySynchronyPortError
)

from .scratch_runtime_setup import (
	TestArithmaticGrammarTokenType,
	TestArithmaticGrammarTokenizeHandler,
	CoreParser2,
	ParserContext,
	ParseContext
)
from .scratch_parse_env import ParserEnvironment
from .scratch_init_grammar import (
		test_grammar_factory,
		init_grammar
	)
from .scratch_grammar_rules_filter import (
	RuleSelector,
	AndRuleSelector,
	OrRuleSelector,
	NotRuleSelector,
	RuleIDSelector,
	RuleHeadSelector,
	RuleBodySelector
)
from .scratch_package_paths import (
	TEST_INPUT_1,
	TEST_INPUT_2
)
from .scratch_utils import generate_id, read_source
from .utils import display_result, apply_color, bold_text, underline_text, center_text
from .scratch_cons import (
	PyParsePortID,
	PyParseEventID,
	ParserActionState,
	ParserActionType,
	PyParseLoggerID,
	GrammarRuleBy
)


FINAL_REDESIGN_LOGGER = PyLogger.get(PyParseLoggerID.FINAL_REDESIGN)


class TableBuilder(ABC):

	__slots__ = ("_grammar")

	def __init__(self, grammar):
		self._grammar = grammar

	@property
	def grammar(self):
		return self._grammar

	@abstractmethod
	def build_table(self, table):
		raise NotImplementedError


class Grammar9TableBuilder(TableBuilder):

	def build_table(self, table):
		INIT_RULE = self.grammar.select(RuleIDSelector("INIT_RULE"))[0]
		S_rule_1 = self.grammar.select(RuleIDSelector("S_rule_1"))[0]
		A_rule_1 = self.grammar.select(RuleIDSelector("A_rule_1"))[0]
		B_rule_1 = self.grammar.select(RuleIDSelector("B_rule_1"))[0]

		# SYMBOLS ---> [a, b, S, A, B]
		# STATE 0:
		table.add_action((0, "("), (ParserActionType.SHIFT))
		table.add_action((0, "a"), (ParserActionType.SHIFT, 2))
		table.add_goto((0, "S"), (1, INIT_RULE.copy().advance_by(1)))

		# STATE 1:
		table.add_action((1, "#"), (ParserActionType.ACCEPT, S_rule_1.copy().advance_by(1)))

		# STATE 2:
		table.add_action((2, "b"), (ParserActionType.SHIFT, 3))
		table.add_goto((2, "A"), (4, S_rule_1.copy().advance_by(2)))
		table.add_goto((2, "B"), (5, B_rule_1.copy().advance_by(1)))

		# STATE 3:
		table.add_action((3, "#"), (ParserActionType.REDUCE, B_rule_1.copy().advance_by(1)))

		# STATE 4:
		table.add_action((4, "#"), (ParserActionType.REDUCE, S_rule_1.copy().advance_by(2)))

		# STATE 5:
		table.add_action((5, "#"), (ParserActionType.REDUCE, A_rule_1.copy().advance_by(1)))


class Grammar9TokenizerHandler(LexHandler):
	pass


class CoreParser3(CoreParser2):
	pass


class FinalRedesignEnv(ParserEnvironment):

	def __init__(self, parser=None, grammar=None, tokenizer=None, parse_table=None):
		super().__init__(parser=parser, grammar=grammar, env_id=str(__class__.__name__))
		self._parse_table = parse_table		
		self._tokenizer = tokenizer
		self._initialized = False

	@property
	def tokenizer(self):
		if self._tokenizer is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access the 'tokenizer' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._tokenizer

	@property
	def parse_table(self):
		if self._parse_table is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access the 'parse_table' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._parse_table

	@property
	def is_setup(self):
		return bool(self._initialized)

	@property
	def item_states(self):
		return self.grammar.generate_states()

	def set_tokenizer(self, tokenizer):
		self._tokenizer = tokenizer

	def set_table(self, parse_table):
		self._parse_table = parse_table

	def setup(self):
		if not self._initialized:
			_grammar_version = self.field("grammar_version", default=9)
			init_grammar(self.grammar, _grammar_version)
			self.parser.set_table(self.parse_table)
			_tbl_builder = Grammar9TableBuilder(self.grammar)
			_tbl_builder.build_table(self.parse_table)
			self._initialized = True

	def execute(self, input):
		if not self.is_setup:
			self.setup()
		# _tokens = self.tokenize(input)
		_parse_context = self.create_context(input, end_symbol=self.field("end_symbol", default="$"))
		return self.parser.parse(_parse_context).result()

	def create_context(self, *args, **kwargs):
		return self.context_factory(*args, **kwargs)

	def context_factory(self, input, end_symbol="$"):
		return ParseContext(input=input, end_symbol=end_symbol)

	def tokenize(self, input):
		return [i for i in self.tokenizer.tokenize(input) if i != TestArithmaticGrammarTokenType.WS]


if __name__ == "__main__":
	pass
