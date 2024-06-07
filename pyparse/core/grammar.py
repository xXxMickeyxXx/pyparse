from ..utils import generate_id


class GrammarRule:

	__slots__ = ("_rule_id", "_rule")

	def __init__(self, rule_id, rule):
		self._rule_id = rule_id
		self._rule = rule

	@property
	def rule_id(self):
		return self._rule_id

	@property
	def rule(self):
		return self._rule

	def __eq__(self, other):
		pass


class Grammar:

	# TODO: potentially create some sort of tree structure (perhaps under the hood
	# 		utilize 'c' but that's absolutely not a requirement); that way the
	# 		the 'grammar' instance that will automatically create the item sets
	# 		and/or states, notifies on potential conflicts, for dynamically
	# 		adding/registering a grammar rule, even if only temporarily


	# TODO: update this class to be more of a container for grammar, allowing the 
	#       parser to more easily interact with the rules it uses to parse.

	__slots__ = ("_grammar_id", "_rules")

	def __init__(self, grammar_id=None):
		self._grammar_id = grammar_id or generate_id()
		self._rules = {}

	@property
	def grammar_id(self):
		return self._grammar_id

	def add_rule(self, rule_id, rule):
		_retval = False
		_rule_list = []
		if rule_id not in self._rules:
			self._rules[rule_id] = _rule_list
		else:
			_rule_list = self._rules[rule_id]
		_rule_list.append(rule)

	def remove_rule(self, rule_id, *rules):
		if len(rules) > 0:
			_rule_list = self._rules[rule_id]
			for _rule in rules:
				_rule_list.pop()

	def rules(self):
		return self._rules

	def inverted_rules(self):
		_inverted_rules = {}
		for head, body_options in self._rules.items():
			for body in body_options:
				_inverted_rules[tuple(body)] = head
		return _inverted_rules

	# def copy(self):
	# 	_new_rules = {}
	# 	for rule_id, rule_symbols in self._rules.items():
	# 		_new_rules_lst = []
	# 		if rule_id not in _new_rules:
	# 			_new_rules[rule_id] = []
	# 		else:
	# 			_new_rules_lst = _new_rules[rule_id]
	# 		_new_rules

	# 		print(rule_id)
	# 		print(rule_symbols)

	@classmethod
	def from_rules(cls, *, grammar_id=None, **rules):
		# TODO: fix this as it's not correctly adding rules to the object

		# _new_cls = cls(grammar_id=grammar_id)
		# for rule_id, rule in rules.items():
		# 	_new_cls.add_rule(rule_id, rule)
		# return _new_cls
		raise NotImplementedError


if __name__ == "__main__":
	pass
