# from pyparse import Grammar
from .grammar_rule import GrammarRule


class Grammar:
    # NOTE: this would replace the original implementation of "Grammar"

    __slots__ = ("_grammar_id", "_rules")

    def __init__(self, grammar_id=None):
        self._grammar_id = grammar_id or generate_id()
        self._rules = []
    
    def add_rule(self, rule):
        if rule not in self._rules:
            self._rules.append(rule)

    def remove_rule(self, rule_head=None, rule_body=None):
        # TODO: refine to make it more clear what's happening here
        # TODO: create separate methods to handle different types of removal (i.e.
        #       removing one rule body from a multi-body rule/rule head, remove
        #       entire rule if only one rule body exists for that rule/rule head,
        #       etc.)
        # for i in range(len(self._rules)):
        #     _rule_head = self._rules[i].rule_head
        #     _rule_body = self._rules[i].rule_body
        #     if rule_head is not None and rule_body is not None:
        #         if _rule_head == rule_head and _rule_body == rule_body:
        #             return self._rules.pop(i)
        #     elif rule_head is not None:
        #         if _rule_head == rule_head:
        #             return self._rules.pop(i)
        #     elif rule_body is not None:
        #         if _rule_body == rule_body:
        #             return self._rules.pop(i)
        #     else:
        #         # TODO: create and raise custom error here as nothing is found matching rule
        #         #       head/rule body
        #         _error_details = f"invalid 'rule_head' and/or 'rule_body' args..."
        #         raise RuntimeError(_error_details)
        raise NotImplementedError

    def rules(self, invert=False):
        # TODO: implement the logic for the 'invert' param (do so in the
        #       "_inverted_rules" method below)
        _rules = {}
        for rule in self._rules:
            _rule_head = rule.rule_head
            _rule_body = rule.rule_body
            if _rule_head not in _rules:
                _rules[_rule_head] = []
            if _rule_body not in _rules[_rule_head]:
                _rules[_rule_head].append(_rule_body)
        return _rules

    def terminals(self):
        raise NotImplementedError

    def _inverted_rules(self):
        raise NotImplementedError

    def copy(self, *, deepcopy=False):
        raise NotImplementedError

    @classmethod
    def from_rules(cls, *, grammar_id=None, **rules):
        # TODO: fix this as it's not correctly adding rules to the object

        # _new_cls = cls(grammar_id=grammar_id)
        # for rule_id, rule in rules.items():
        #   _new_cls.add_rule(rule_id, rule)
        # return _new_cls
        raise NotImplementedError


if __name__ == "__main__":
    pass
