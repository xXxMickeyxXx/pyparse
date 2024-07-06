from collections import deque

# from pyparse import Grammar
from .grammar_rule import GrammarRule
from .scratch_marker_symbol import MarkerSymbol
from .scratch_cons import GrammarRuleBy
from pyparse import GrammarRuleError
from .scratch_utils import generate_id


class Grammar:

    # NOTE: this will replace the original 'Grammar' implementation

    __slots__ = ("_grammar_id", "_rule_factory", "_rules", "_terminals_cache", "_terminals_cache_invalid", "_non_terminals_cache", "_non_terminals_cache_invalid", "_augmented_item_added", "_init_symbol")

    def __init__(self, grammar_id=None, rule_factory=GrammarRule):
        self._grammar_id = grammar_id or generate_id()
        self._rule_factory = rule_factory
        self._rules = []
        self._terminals_cache = None
        self._terminals_cache_invalid = True
        self._non_terminals_cache = None
        self._non_terminals_cache_invalid = True
        self._augmented_item_added = False

    @property
    def grammar_id(self):
        return self._grammar_id

    @property
    def init_symbol(self):
        if self._rules:
            return self._rules[0].rule_head
        return None

    @property
    def rule_count(self):
        return len(self._rules)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(grammar_id={self.grammar_id})"

    def __eq__(self, other):
        return (self.grammar_id == other.grammar_id) and (self._rules == other._rules)

    def __hash__(self):
        return hash((self.grammar_id, tuple(self._rules)))

    def __len__(self):
        return len(self._rules)

    def __contains__(self, item):
        return isinstance(item, GrammarRule) and item in self._rules

    def generate_states(self):
        raise NotImplementedError

    def create_rule(self, *args, **kwargs):
        _new_rule = self.rule_factory(*args, **kwargs)
        if _new_rule in self._rules:
            # TODO: create and raise custom error here
            _error_details = f"invalid rule; grammar rule already exists within instance..."
            raise RuntimeError(_error_details)
        self.add_rule(_new_rule)
        return _new_rule

    # def _create_augmented_item(self, start_symbol):
    #     if not self._augmented_item_added:
    #         _rules = self.rules()
    #         _first_rule = _rules[0] if _rules else None
    #         if _first_rule is None:
    #             # TODO: create and raise custom error here
    #             _error_details = f"unable to create augmented rule as instance of {self.__class__.__name__} has not yet added any rules..."
    #             raise RuntimeError(_error_details)
    #         _starting_rule = self.create_rule(start_symbol, [_first_rule.rule_head], rule_id=f"{self.grammar_id}")
    #         self._augmented_item_added = True

    def rule_factory(self, rule_head, rule_body, marker_symbol=MarkerSymbol("•"), rule_id=None):
        return self._rule_factory(rule_head, rule_body, marker_symbol=marker_symbol, rule_id=rule_id)
    
    def add_rule(self, rule):
        if rule in self._rules:
            # TODO: create and raise custom error here
            _error_details = f"invalid argument; rule object with head: {rule.rule_head} and body: {rule.rule_body} already exists within {self.__class__.__name__} ID: {self.grammar_id}..."
            raise RuntimeError(_error_details)
        self._rules.append(rule)
        self._terminals_cache_invalid = True
        self._non_terminals_cache_invalid = True


    # def _add_starting_rule(self):
    #     if not self._rules:
    #         _rule_head = rule.rule_head
    #         _aug_rule_head = f"[{_rule_head}]"
    #         self.create_rule(_aug_rule_head, _rule_head, marker_symbol=rule.marker_symbol, rule_id=self.grammar_id)

    def remove_rule(self, rule_input, *, remove_by=GrammarRuleBy.HEAD):
        # TODO: fix this method as it doesn't work as intended
        # TODO: determine how this method should actually work
        # if remove_by == GrammarRuleBy.HEAD:
        #     _remove_by = self._remove_rule_by_head
        # else:
        #     _remove_by = remove_by
        # return _remove_by(rule_input, self)
        raise NotImplementedError()

    @staticmethod
    def _remove_rule_by_head(rule_input, grammar):
        _remove_rule_queue = deque([idx for idx, rule in enumerate(grammar._rules) if rule.rule_head == rule_input])
        return [grammar._rules.pop(_remove_rule_queue.popleft()) for _ in range(len(_remove_rule_queue))]

    def symbols(self):
        _symbols = self.non_terminals()
        _symbols.extend(self.terminals())
        return _symbols

    def rules(self):
        return self._rules

    def rule(self, rule_input, search_by=GrammarRuleBy.HEAD, all=True):
        # TODO: perhaps design this method to run differently
        # TODO: perhaps change "_rules" attribute to a dict instead of a list
        if search_by == GrammarRuleBy.HEAD:
            _by = self._get_rule_by_head
        elif search_by == GrammarRuleBy.BODY:
            _by = self._get_rule_by_body
        elif search_by == GrammarRuleBy.ID:
            _by = self._get_rule_by_id
        else:
            if not callable(search_by):
                _error_details = f"invalid 'search_by' argument value; must be either a callable, or a member of the 'GrammarRuleBy' enumeration, i.e. 'HEAD' or 'BODY',  (NOTE: neither of the 'GrammarRuleBy' members are of a callable type, however, they represent the association that is used to indicate a default implementation, provided by this class, as two static methods, '_get_rule_by_head' and '_get_rule_by_body')"
                raise GrammarRuleError(details=_error_details)
            _by = search_by
        return _by(rule_input, self, all=all)

    @staticmethod
    def _get_rule_by_id(rule_input, grammar, all=True):
        _rules = []
        for _rule in grammar.rules():
            if _rule.rule_id == rule_input:
                if not all:
                    return _rule
                _rules.append(_rule)
        return _rules

    @staticmethod
    def _get_rule_by_head(rule_input, grammar, all=True):
        _rules = []
        for _rule in grammar.rules():
            if rule_input == _rule.rule_head:
                if not all:
                    return _rule
                _rules.append(_rule)
        return _rules

    @staticmethod
    def _get_rule_by_body(grammar):
        raise NotImplementedError

    def non_terminals(self):
        if self._non_terminals_cache_invalid:
            _rules = self.rules()
            _non_terminals = []
            for _rule in _rules:
                _rule_head = _rule.rule_head
                _non_terminals.append(_rule_head)
            self._non_terminals_cache = _non_terminals
            self._non_terminals_cache_invalid = False
        else:
            _non_terminals = self._non_terminals_cache
            print(f"USING CACHED NON-TERMINALS")
        return _non_terminals

    def terminals(self):
        if self._terminals_cache_invalid:
            _rules = self._rules
            _non_terminals = self.non_terminals()
            _terminals = []
            for _rule in _rules:
                for _rule_body in _rule.rule_body:
                    for _rule in _rule_body:
                        if _rule_body in _non_terminals or (_rule_body in _terminals):
                            continue
                        _terminals.append(_rule_body)
            self._terminals_cache = _terminals
            self._terminals_cache_invalid = False
        else:
            _terminals = self._terminals_cache
            print(f"USING CACHED TERMINALS")
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
