from abc import abstractmethod


class RuleFilter:

	@abstractmethod
	def filter(self, item):
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

	def filter(self, item):
		return self._filter_1.filter(item) and self._filter_2.filter(item)


class OrRuleFilter(RuleFilter):
	
	def __init__(self, filter_1, filter_2):
		self._filter_1 = filter_1
		self._filter_2 = filter_2

	def __repr__(self):
		return f"{self.__class__.__name__}(filter_1={self._filter_1}, filter_2={self._filter_2})"

	def filter(self, item):
		return self._filter_1.filter(item) or self._filter_2.filter(item)


class NotRuleFilter(RuleFilter):
	
	def __init__(self, filter):
		self._filter = filter

	def __repr__(self):
		return f"{self.__class__.__name__}(filter={self._filter})"

	def filter(self, item):
		return not self._filter.filter(item)


class RuleByID(RuleFilter):

	def __init__(self, rule_id):
		self._rule_id = rule_id

	def __repr__(self):
		return f"{self.__class__.__name__}(rule_id={self._rule_id})"

	def filter(self, rule):
		return rule.rule_id == self._rule_id


class RuleByHead(RuleFilter):

	def __init__(self, rule_head):
		self._rule_head = rule_head

	def __repr__(self):
		return f"{self.__class__.__name__}(rule_head={self._rule_head})"

	def filter(self, rule):
		return rule.rule_head == self._rule_head


class RuleByBody(RuleFilter):

	def __init__(self, rule_body):
		self._rule_body = rule_body

	def __repr__(self):
		return f"{self.__class__.__name__}(rule_body={self._rule_body})"

	def filter(self, rule):
		return rule.rule_body == self._rule_body


class AugItemStatus(RuleFilter):

	def __init__(self, aug_item):
		self._aug_item = aug_item

	@property
	def advance_by(self):
		return self._advance_by

	@property
	def reverse_by(self):
		return self._reverse_by

	def __repr__(self):
		return f"{self.__class__.__name__}(aug_item={self._aug_item.rule_id})"

	def filter(self, aug_item):
		return self._aug_item.status() == aug_item.status()


if __name__ == "__main__":
	pass
