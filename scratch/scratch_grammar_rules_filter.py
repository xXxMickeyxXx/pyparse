from abc import abstractmethod


class RuleSelector:

	@abstractmethod
	def select(self, item):
		raise NotImplementedError

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return f"{self.__class__.__name__}()"

	def __and__(self, other):
		return AndRuleSelector(self, other)

	def __or__(self, other):
		return OrRuleSelector(self, other)

	def __invert__(self):
		return NotRuleSelector(self)


class AndRuleSelector(RuleSelector):

	def __init__(self, select_1, select_2):
		self._select_1 = select_1
		self._select_2 = select_2

	def __repr__(self):
		return f"{self.__class__.__name__}(select_1={self._select_1}, select_2={self._select_2})"

	def select(self, item):
		return self._select_1.select(item) and self._select_2.select(item)


class OrRuleSelector(RuleSelector):
	
	def __init__(self, select_1, select_2):
		self._select_1 = select_1
		self._select_2 = select_2

	def __repr__(self):
		return f"{self.__class__.__name__}(select_1={self._select_1}, select_2={self._select_2})"

	def select(self, item):
		return self._select_1.select(item) or self._select_2.select(item)


class NotRuleSelector(RuleSelector):
	
	def __init__(self, select):
		self._select = select

	def __repr__(self):
		return f"{self.__class__.__name__}(select={self._select})"

	def select(self, item):
		return not self._select.select(item)


class RuleIDSelector(RuleSelector):

	def __init__(self, rule_id):
		self._rule_id = rule_id

	def __repr__(self):
		return f"{self.__class__.__name__}(rule_id={self._rule_id})"

	def select(self, rule):
		return rule.rule_id == self._rule_id


class RuleHeadSelector(RuleSelector):

	def __init__(self, rule_head):
		self._rule_head = rule_head

	def __repr__(self):
		return f"{self.__class__.__name__}(rule_head={self._rule_head})"

	def select(self, rule):
		return rule.rule_head == self._rule_head


class RuleBodySelector(RuleSelector):

	def __init__(self, rule_body):
		self._rule_body = rule_body

	# def __call__(self, *args, **kwargs):
	# 	raise NotImplementedError

	def __repr__(self):
		return f"{self.__class__.__name__}(rule_body={self._rule_body})"

	def select(self, rule):
		return rule.rule_body == self._rule_body


class AugItemStatusSelector(RuleSelector):

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

	def select(self, aug_item):
		return self._aug_item.status() == aug_item.status()


if __name__ == "__main__":
	pass
