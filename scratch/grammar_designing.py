# from pyparse import Grammar
from .grammar_rule import GrammarRule
from .scratch_cons import GrammarRuleBy
from pyparse import GrammarRuleError
from .scratch_utils import generate_id


class Grammar:
    # NOTE: this would replace the original implementation of "Grammar"

    __slots__ = ("_grammar_id", "_rules")

    def __init__(self, grammar_id=None):
        self._grammar_id = grammar_id or generate_id()
        self._rules = []

    @property
    def grammar_id(self):
        return self._grammar_id

    @property
    def rule_count(self):
        return len(self._rules)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(grammar_id={self.grammar_id})"

    def __eq__(self, other):
        return (self._rules == other._rules) and (self.grammar_id == other.grammar_id)

    def __hash__(self):
        return hash((self.grammar_id, tuple(self._rules)))

    def __len__(self):
        return len(self._rules)
    
    def add_rule(self, rule):
        if rule not in self._rules:
            self._rules.append(rule)

    def remove_rule(self, rule_head=None, rule_body=None):
        raise NotImplementedError

    def rules(self):
        return self._rules

    def rule(self, rule_input, *, search_by=GrammarRuleBy.HEAD):
        if search_by == GrammarRuleBy.HEAD:
            _by = self._get_rule_by_head
        elif by == GrammarRuleBy.BODY:
            _by = self._get_rule_by_body
        else:
            if not callable(search_by):
                _error_details = f"invalid 'search_by' argument value; must be either a callable, or a member of the 'GrammarRuleBy' enumeration, i.e. 'HEAD' or 'BODY',  (NOTE: neither of the 'GrammarRuleBy' members are of a callable type, however, they represent the association that is used to indicate a default implementation, provided by this class, as two static methods, '_get_rule_by_head' and '_get_rule_by_body')"
                raise GrammarRuleError(details=_error_details)
            _by = by
        return _by(rule_input, self)

    @staticmethod
    def _get_rule_by_head(rule_input, grammar):
        _rules = []
        for _rule in grammar._rules:
            if rule_input == _rule.rule_head:
                _rules.append(_rule)
        return _rules

    @staticmethod
    def _get_rule_by_body(grammar):
        raise NotImplementedError

    def non_terminals(self):
        _rules = self.rules()
        _non_terminals = []
        for _rule in _rules:
            _rule_head = _rule.rule_head
            _non_terminals.append(_rule_head)
        return _non_terminals

    def terminals(self):
        _rules = self._rules
        _non_terminals = self.non_terminals()
        _terminals = []
        for _rule in _rules:
            for _rule_body in _rule.rule_body:
                for _rule in _rule_body:
                    if _rule_body in _non_terminals or (_rule_body in _terminals):
                        continue
                    _terminals.append(_rule_body)
        return _terminals

    def _inverted_rules(self):
        raise NotImplementedError

    def copy(self, *, deepcopy=False):
        _new_cls = type(self)(grammar_id=self.grammar_id)
        _new_cls._rules = [i.copy(deepcopy=deepcopy) for i in self.rules()]
        return _new_cls

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
