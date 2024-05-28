from ..utils import generate_id


class Grammar:

	# TODO: update this class to be more of a container for grammar, allowing the 
	#       parser to more easily interact with the rules it uses to parse.

	# TODO/NOTE: should separate a callable that acts on the parser, closer to a 'rule'
	#            and then have the grammar be able to add 'action' callables, which can
	#            be used to build a structure, based on whatever is happening during
	#            parsing (such as building a request object for use in application
	#            code/for building some sort of composite/etc.). Should also create
	#            a way to associate an action for with a rule or many rules (i.e. a
	#            one-to-many relationship or a many-many relationship)

	def __init__(self, grammar_id=None):
		self._grammar_id = grammar_id or generate_id()
		self._rules = []

	@property
	def grammar_id(self):
		return self._grammar_id

	def add_rule(self, non_terminal, rule):
		_new_rule = [non_terminal, rule]
		self._rules.append(_new_rule)

	def get_grammar(self):
		return self._rules


if __name__ == "__main__":
	pass
