from abc import abstractmethod


class RuleFilter:

	@abstractmethod
	def match(self, item):
		raise NotImplementedError

	def __str__(self):
		return f"{self.__class__.__name__}"

	def __repr__(self):
		return self.__str__()

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

	def __str__(self):
		return f"{self._filter_1} and {self._filter_2}"

	def __repr__(self):
		return self.__str__()

	def match(self, item):
		return self._filter_1.match(item) and self._filter_2.match(item)


class OrRuleFilter(RuleFilter):
	
	def __init__(self, filter_1, filter_2):
		self._filter_1 = filter_1
		self._filter_2 = filter_2

	def __str__(self):
		return f"{self._filter_1} or {self._filter_2}"

	def __repr__(self):
		return self.__str__()

	def match(self, item):
		return self._filter_1.match(item) or self._filter_2.match(item)


class NotRuleFilter(RuleFilter):
	
	def __init__(self, filter):
		self._filter = filter

	def __str__(self):
		return f"not {self._filter}"

	def __repr__(self):
		return self.__str__()

	def match(self, item):
		return not self._filter.match(item)


class RuleByID(RuleFilter):

	def __init__(self, rule_id):
		return self._rule_id = rule_id

	def match(self, rule):
		return rule.rule_id == self._rule_id


class RuleByHead(RuleFilter):

	def __init__(self, rule_head):
		return self._rule_head = rule_head

	def match(self, rule):
		return rule.rule_head == self._rule_head


class RuleByBody(RuleFilter):

	def __init__(self, rule_body):
		return self._rule_body = rule_body

	def match(self, rule):
		return rule.rule_body == self._rule_body


if __name__ == "__main__":
	pass
