from collections import deque

from .utils import apply_color, bold_text, underline_text  # TODO: remove this once I solve an issue in this module (item states aren't being created correctly if two items have the same 'rule_head' and have the their 'look_behinds' and 'look_aheads' method calls match)
# from pyparse import Grammar
from .grammar_rule import GrammarRule
from .scratch_marker_symbol import MarkerSymbol
from .scratch_cons import GrammarRuleBy
from pyparse import GrammarRuleError
from .scratch_utils import generate_id


class Grammar:

    # NOTE: this will replace the original 'Grammar' implementation

    __slots__ = ("_grammar_id", "_rule_factory", "_rules", "_item_states_cache", "_terminals_cache", "_non_terminals_cache")

    def __init__(self, grammar_id=None, rule_factory=GrammarRule):
        self._grammar_id = grammar_id or generate_id()
        self._rule_factory = rule_factory
        self._rules = []
        self._item_states_cache = None
        self._terminals_cache = None
        self._non_terminals_cache = None

    @property
    def grammar_id(self):
        return self._grammar_id

    @property
    def init_symbol(self):
        if self._rules:
            return self._rules[0].rule_head
        return ""

    @property
    def init_item(self):
        if self._rules:
            return self._rules[0]
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

    # NOTE: currently saved/committed implementation (as of 2024-07-24)
    # def generate_states(self):
    #     if self._item_states_cache is None:
    #         _terminals = self.terminals()
    #         _non_terminals = self.non_terminals()
    #         _rules = self.rules()
    #         _augmented_item = _rules[0]

    #         _current_state = 0
    #         _init_item_set = self.closure(_augmented_item, _current_state)
    #         _item_sets = [_init_item_set]

    #         # _goto_mapping = {}
    #         _rule_queue = deque([_init_item_set])
    #         while _rule_queue:
    #             _next_item_set = _rule_queue.popleft()
    #             _current_state = len(_item_sets)
    #             for _item in _next_item_set:
    #                 _item = _item.copy()
    #                 # if _item.can_reduce:
    #                 #     continue
    #                 _item.advance()
    #                 if _item.next_symbol() in _non_terminals:
    #                     _next_group = self.closure(_item, _current_state)
    #                     if _next_group not in _item_sets:
    #                         _item_sets.append(_next_group)
    #                         _rule_queue.append(_next_group)

    #                 else:
    #                     _next_group = [_item]
    #                     if _next_group not in _item_sets:
    #                         _item_sets.append(_next_group)
    #                         _rule_queue.append(_next_group)

    #         _retval = {}
    #         for idx, i in enumerate(_item_sets):
    #             _retval[idx] = []
    #             for k in i:
    #                 _retval[idx].append(k)
    #         self._item_states_cache = _retval
    #     else:
    #         _retval = self._item_states_cache
    #     return _retval

    # NOTE: newest implementation (as of 2024-07-24)
    # def generate_states(self):
    #     if self._item_states_cache is None:
    #         _terminals = self.terminals()
    #         _non_terminals = self.non_terminals()
    #         _rules = self.rules()
    #         _augmented_item = self.rule("$", search_by=GrammarRuleBy.HEAD)[0]

    #         # Initialize the item set with the closure of the augmented item
    #         _init_item_set = self.closure(_augmented_item)
    #         _item_sets = [_init_item_set]

    #         _goto_mapping = {}
    #         _rule_queue = deque([_init_item_set])
    #         while _rule_queue:
    #             _current_item_set = _rule_queue.popleft()
    #             for symbol in _terminals + _non_terminals:
    #                 _next_item_set = set()
    #                 for item in _current_item_set:
    #                     if item.next_symbol() == symbol:
    #                         next_item = item.copy()
    #                         next_item.advance()
    #                         _next_item_set.add(next_item)
    #                 if _next_item_set:
    #                     # Apply the closure to the new item set
    #                     for _next_item in _next_item_set:
    #                         _next_item_set = self.closure(_next_item)
    #                     # _next_item_set = self.closure(_next_item_set)
    #                         if _next_item_set not in _item_sets:
    #                             _item_sets.append(_next_item_set)
    #                             _rule_queue.append(_next_item_set)

    #         _retval = {}
    #         for idx, item_set in enumerate(_item_sets):
    #             # _retval[idx] = sorted(item_set, key=lambda x: (x.rule_id, x.marker_pos))
    #             _retval[idx] = item_set
    #         self._item_states_cache = _retval
    #     else:
    #         _retval = self._item_states_cache
    #     return _retval

    # NOTE: current working/updated implementation (as of 2024-07-24)
    def generate_states(self):
        if self._item_states_cache is None:

            _retval = {}
            _item_sets = []
            _current_state = 0
            _item_set_buffer = [self.closure(self.init_item)]
            _item_set_queue = deque(_item_set_buffer)
            while _item_set_buffer and _item_set_buffer:
                print(f"ITEM SET BUFFER @ TOP ---> {_item_set_buffer}\n")
                _retval.update({_current_state: _item_set_buffer})
                _item_sets.append(_item_set_buffer)
                _item_set_buffer.clear()

                _next_item_sets = {}
                _dequeued_item_set = _item_set_queue.popleft()
                _possible_transitions = [(_item.next_symbol(default=None), _item.copy(deepcopy=True)) for _item in _dequeued_item_set if not _item.can_reduce]
                _temp_buffer = deque(_possible_transitions)
                while _temp_buffer:
                    _items_next_sym, _item = _temp_buffer.popleft()
                    print(f"NEXT SYMBOL FOR RULE ID: '{_item.rule_id}' ---> {_items_next_sym}")
                    print(f"ITEM STATUS: {_item}\n")
                    _next_set = []
                    if _items_next_sym not in _next_item_sets:
                        _next_item_sets[_items_next_sym] = _next_set
                    else:
                        _next_set = _next_item_sets[_items_next_sym]

                    if _item not in _next_set:
                        _next_set.append(_item)
                        _item.advance()
                print(f"NEXT ITEM SETS:")
                for k, v in _next_item_sets.items():
                    print(f"{k}")
                    for i in v:
                        print(f"\t• {i}")
                        print(f"\t• {i.rule_head} ---> {i.rule_body}")
                        print(f"\t• {i.status()}")
                        print()
                break









            self._item_states_cache = _retval
        else:
            _retval = self._item_states_cache
        return _retval

    def closure(self, rule):
        _non_terminals = self.non_terminals()
        _closure_group = [rule]
        _rule_queue = deque(_closure_group)

        while _rule_queue:
            _next_rule = _rule_queue.popleft()
            _next_symbol = _next_rule.next_symbol(default=None)
            if _next_symbol in _non_terminals:
                _found_rules = self.rule(_next_symbol, search_by=GrammarRuleBy.HEAD)
                _closure_group_rule_ids = [i.rule_id for i in _closure_group]
                for _check_rule in _found_rules:
                    if _check_rule in _closure_group:
                        continue
                    _closure_group.append(_check_rule)
                    _rule_queue.append(_check_rule)
        return tuple([i.copy(deepcopy=True) for i in _closure_group])
        # return tuple(sorted(_closure_group, key=lambda x: (x.rule_id, x.marker_pos)))

    def create_rule(self, *args, **kwargs):
        _new_rule = self.rule_factory(*args, **kwargs)
        if _new_rule in self._rules:
            # TODO: create and raise custom error here
            _error_details = f"invalid rule; grammar rule already exists within instance ({_new_rule.rule_head} ---> {_new_rule.rule_body})..."
            raise RuntimeError(_error_details)
        self.add_rule(_new_rule)
        return _new_rule

    def rule_factory(self, rule_head, rule_body, marker_symbol=MarkerSymbol("•"), rule_id=None):
        return self._rule_factory(rule_head, rule_body, marker_symbol=marker_symbol, rule_id=rule_id)
    
    def add_rule(self, rule):
        if rule in self._rules:
            # TODO: create and raise custom error here
            _error_details = f"invalid argument; rule object with head: {rule.rule_head} and body: {rule.rule_body} already exists within {self.__class__.__name__} ID: {self.grammar_id}..."
            raise RuntimeError(_error_details)
        self._rules.append(rule)
        self._terminals_cache = None
        self._non_terminals_cache = None
        self._item_states_cache = None

    def remove_rule(self, rule_input, *, remove_by=GrammarRuleBy.HEAD):
        raise NotImplementedError()

    @staticmethod
    def _remove_rule_by_head(rule_input, grammar):
        _remove_rule_queue = deque([idx for idx, rule in enumerate(grammar._rules) if rule.rule_head == rule_input])
        return [grammar._rules.pop(_remove_rule_queue.popleft()) for _ in range(len(_remove_rule_queue))]

    def symbols(self):
        _symbols = self.terminals()
        _symbols.extend(self.non_terminals)
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
        if self._non_terminals_cache is None or not self._non_terminals_cache:
            _rules = self.rules()
            _non_terminals = []
            for _rule in _rules:
                _rule_head = _rule.rule_head
                _non_terminals.append(_rule_head)
            self._non_terminals_cache = _non_terminals
        else:
            _non_terminals = self._non_terminals_cache
        return _non_terminals

    def terminals(self):
        if self._terminals_cache is None or not self._terminals_cache:
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
        else:
            _terminals = self._terminals_cache
            # print(f"USING CACHED TERMINALS")
        return _terminals

    def _inverted_rules(self):
        raise NotImplementedError

    def copy(self, *, deepcopy=False):
        _new_cls = type(self)(grammar_id=self.grammar_id)
        _new_cls._rules = [i.copy(deepcopy=deepcopy) for i in self.rules()]
        return _new_cls

    # @classmethod
    # def from_rules(cls, *, grammar_id=None, **rules):
    #     # TODO: fix this as it's not correctly adding rules to the object

    #     # _new_cls = cls(grammar_id=grammar_id)
    #     # for rule_id, rule in rules.items():
    #     #   _new_cls.add_rule(rule_id, rule)
    #     # return _new_cls
    #     raise NotImplementedError


if __name__ == "__main__":
    _test_grammar = Grammar(grammar_id="[ • -- TEST_GRAMMR -- • ]")
    _test_grammar.create_rule("$", ["S"], rule_id="INIT_RULE")
    _test_grammar.create_rule("S", ["a", "A"], rule_id="S_rule_1")
    _test_grammar.create_rule("A", ["b"], rule_id="A_rule_1")

    _item_states = _test_grammar.generate_states()
    for k, v in _item_states.items():
        print(f"STATE: {k}")
        for i in v:
            print(f"\tRULE: {i.rule_head}")
            print(f"\t{i.status()}")
        print()

    _item_states_2 = _test_grammar.generate_states()
    for k, v in _item_states_2.items():
        print(f"STATE: {k}")
        for i in v:
            print(f"\tRULE: {i.rule_head}")
            print(f"\t{i.status()}")
        print()

