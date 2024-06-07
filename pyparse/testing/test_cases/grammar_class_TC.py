import importlib
from unittest import TestCase, skip, skipIf, skipUnless

from unittest_utils import register_test


_pyparse_core = importlib.import_module(".core", package="pyparse")


@register_test("grammar_TC")
class GrammarClassTestCase(TestCase):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._grammar_id = "grammar_TC"
		self._grammar = _pyparse_core.Grammar(grammar_id=self._grammar_id)
		
		self._test_grammars = {
			"grammar_TC": [["$", ["S"]], ["S", ["a", "A"]], ["A", ["b"]]]
		}

	def _get_next_test_grammar(self):
		for prod_head, prod_rule in self._test_grammar_1:
			self._grammar.add_rule(prod_head, prod_rule)

	def setUp(self):


	def tearDown(self):
		pass


if __name__ == "__main__":
	pass
