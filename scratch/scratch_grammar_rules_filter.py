from abc import abstractmethod


class RuleFilter:

	@abstractmethod
	def matches(self, item):
		raise NotImplementedError

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return f"{self.__class__.__name__}()"

	def __and__(self, other):
		return AndRuleFilter(self, other)

	def __or__(self, other):
		return OrRuleFilter(self, other)

	def __invert__(self):
		return NotRuleFilter(self)


class AndRuleFilter(RuleFilter):

	def __init__(self, filter_1, filter_2):
		self._filter_1 = filter_1
		self._filter_2 = filter_2

	def __repr__(self):
		return f"{self.__class__.__name__}(filter_1={self._filter_1}, filter_2={self._filter_2})"

	def matches(self, item):
		return self._filter_1.matches(item) and self._filter_2.matches(item)


class OrRuleFilter(RuleFilter):
	
	def __init__(self, filter_1, filter_2):
		self._filter_1 = filter_1
		self._filter_2 = filter_2

	def __repr__(self):
		return f"{self.__class__.__name__}(filter_1={self._filter_1}, filter_2={self._filter_2})"

	def matches(self, item):
		return self._filter_1.matches(item) or self._filter_2.matches(item)


class NotRuleFilter(RuleFilter):
	
	def __init__(self, filter):
		self._filter = filter

	def __repr__(self):
		return f"{self.__class__.__name__}(filter={self._filter})"

	def matches(self, item):
		return not self._filter.matches(item)


class RuleByID(RuleFilter):

	def __init__(self, rule_id):
		self._rule_id = rule_id

	def __repr__(self):
		return f"{self.__class__.__name__}(rule_id={self._rule_id})"

	def matches(self, rule):
		return rule.rule_id == self._rule_id


class RuleByHead(RuleFilter):

	def __init__(self, rule_head):
		self._rule_head = rule_head

	def __repr__(self):
		return f"{self.__class__.__name__}(rule_head={self._rule_head})"

	def matches(self, rule):
		return rule.rule_head == self._rule_head


class RuleByBody(RuleFilter):

	def __init__(self, rule_body):
		self._rule_body = rule_body

	def __repr__(self):
		return f"{self.__class__.__name__}(rule_body={self._rule_body})"

	def matches(self, rule):
		return rule.rule_body == self._rule_body


if __name__ == "__main__":
	pass
