from collections import deque

from .utils import apply_color, bold_text, underline_text  # TODO: remove this once I solve an issue in this module (item states aren't being created correctly if two items have the same 'rule_head' and have the their 'look_behinds' and 'look_aheads' method calls match)
# from pyparse import Grammar
from .grammar_rule import GrammarRule
from .scratch_marker_symbol import MarkerSymbol
from .scratch_cons import GrammarRuleBy
from pyparse import GrammarRuleError
from .scratch_utils import generate_id

from . import item_details


class Grammar:

    # NOTE: this will replace the original 'Grammar' implementation

    __slots__ = ("_grammar_id", "_rule_factory", "_rules", "_symbols_cache", "_item_states_cache", "_terminals_cache", "_non_terminals_cache")

    def __init__(self, grammar_id="", rule_factory: GrammarRule = GrammarRule):
        self._grammar_id = grammar_id or generate_id()
        self._rule_factory = rule_factory
        self._rules = []
        self._symbols_cache = None
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

    # NOTE: current working/updated implementation (as of 2024-07-24)
    def generate_states(self):
        if self._item_states_cache is None:
            _augmented_item_closure = self.closure(self.init_item)

            # _check_queue = deque(_augmented_item_closure)
            # _item_set_queue = deque([_augmented_item_closure])

            _item_sets = [_augmented_item_closure]
            # _next_item_sets = {}
            _item_set_added = True

            _color_id = 208

            _current_set_idx = 0
            _item_set_added = True
            _counter = 1
            while _item_set_added:
                # Toggling between colors associated with 208 (hexadecimal '0xd0') and 220 (hexadecimal '0xdc') using bitwise XOR 12 on the current '_color_id' variable
                _color_id ^= 50
                print()
                print(underline_text(bold_text(apply_color(_color_id, f"** TOP OF WHILE-LOOP **"))))
                print(apply_color(_color_id, f" |"))
                print(apply_color(_color_id, f" |"))
                print(apply_color(_color_id, f" • --- "), end="")
                _underlined_txt = underline_text(f"COUNT {_counter}")
                _text = apply_color(_color_id, f"[{_underlined_txt}") + apply_color(_color_id, "]")
                _text += "\n"
                print(_text)
                _item_set_added = False




                # if _current_set_idx < len(_item_sets):
                #     _item_set = _item_sets

                _next_sets = []
                _item_sets_len = len(_item_sets)
                for i in range(_item_sets_len):
                    _item_set = _item_sets[i]
                    print()
                    print(apply_color(_color_id, f"\t\t[STATE {i}]\n"))
                    print(apply_color(_color_id, f"\t\t\t[ITEM]"))
                    # _temp_mapping = {}
                    for _item in _item_set:
                        _item_copy = _item.copy(deepcopy=True)
                        if _item_copy.can_reduce:
                            _next_sets.append([_item_copy])
                            continue
                        _item_copy.advance()
                        print(item_details(_item_copy, _color_id), end="\n\n")  # TODO: **REMOVE ONCE FINISHED IMPLEMENTING**
                        _temp_mapping = {}
                        _next_symbol = _item_copy.next_symbol()
                        if _next_symbol not in _temp_mapping:
                            _temp_mapping[_next_symbol] = []
                        _temp_mapping[_next_symbol].append(_item_copy)
                        if _next_symbol in self.non_terminals():
                            for _item_from_closure in self.closure(_item_copy):
                                if _item_from_closure not in _temp_mapping[_next_symbol]:
                                    _temp_mapping[_next_symbol].append(_item_from_closure)    

                        _next_sets.extend(list(_temp_mapping.values()))
                for _new_item_set in _next_sets:
                    if _new_item_set not in _item_sets:
                        _item_sets.append(_new_item_set)
                        _item_set_added = True

                print()
                print()
                print(underline_text(bold_text(apply_color(_color_id, f"** BOTTOM OF WHILE-LOOP **\n"))))
                print()
                _counter += 1
            print()
            print(underline_text(bold_text(apply_color(15, f"** EXITED WHILE-LOOP **\n"))))
            print()
            _retval = {idx: i for idx, i in enumerate(_item_sets)}
            self._item_states_cache = _retval
        else:
            _retval = self._item_states_cache
        return _retval

    def closure(self, rule):
        # print()
        # print(f"CLOSING RULE")
        # print(f"\t• {rule.rule_head} ---> {rule.rule_body}")
        # print(f"\t• {rule.status()}")
        # print()
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
        _retval = tuple([i.copy(deepcopy=True) for i in _closure_group])
        # print()
        # print(f"CLOSURE RESULT:")
        # print()
        # for i in _retval:
        #     print(f"\t• {i}")
        # print()
        return _retval

    def create_rule(self, *args, **kwargs):
        _new_rule = self.rule_factory(*args, **kwargs)
        if _new_rule in self._rules:
            # TODO: create and raise custom error here
            _error_details = f"invalid rule; grammar rule already exists within instance |  {_new_rule.rule_head} ---> {_new_rule.rule_body}  |..."
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
        self._symbols_cache = None
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
        _symbols.extend(self.non_terminals())
        if self._symbols_cache is None:
            self._symbols_cache = _symbols
        return self._symbols_cache

    def rules(self):
        return self._rules

    def rule(self, rule_input, search_by=GrammarRuleBy.HEAD, all=True):
        # TODO: need to change this to make it more fluent and make sense; like maybe
        #       I create a 'rule_by_id' method and then a 'rule_by_head' method, and
        #       so on (though I don't like those method names and length)
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

    # NOTE: this method may replace the above 'rule' method, though I'll need to
    #       update it everywhere it's currently used
    def select(self, rule_id, copy=False, deepcopy=True):
        _retval = None
        for _rule in self.rules():
            if _rule.rule_id == rule_id:
                return _rule.copy(deepcopy=deepcopy) if copy else _rule

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

    @classmethod
    def from_rules(cls, rules: list | tuple, grammar_id: str = "", grammar_rule: GrammarRule = GrammarRule):
        _new_cls = cls(grammar_id=grammar_id, rule_factory=grammar_rule)
        for rule in rules:
            _new_cls.add_rule(rule)
        return _new_cls


if __name__ == "__main__":
    # _rule_lst = [
    #     GrammarRule("$", ("E",), rule_id="INIT_RULE").bind_state(0, "E", 1),
    #     GrammarRule("E", ("E", "*", "B"), rule_id="E_rule_1").bind_state(0, "E", 1),
    #     GrammarRule("E", ("E", "+", "B"), rule_id="E_rule_2").bind_state(0, "E", 1),
    #     GrammarRule("E", ("B",), rule_id="E_rule_3").bind_state(0, "E", 1),
    #     GrammarRule("B", ("0",), rule_id="B_rule_1").bind_state(0, "0", 3),
    #     GrammarRule("B", ("1",), rule_id="B_rule_2").bind_state(0, "1", 4)
    # ]

    # _test_grammar = Grammar.from_rules(_rule_lst)

    _test_grammar = Grammar(grammar_id="[ • -- TEST_GRAMMR -- • ]")
    
    init_rule = _test_grammar.create_rule("$", ("E",), rule_id="INIT_RULE")
    init_rule.bind_state(0, "E", 1)

    E_rule_1 = _test_grammar.create_rule("E", ("E", "*", "B"), rule_id="E_rule_1")
    E_rule_1.bind_state(0, "E", 1)

    E_rule_2 = _test_grammar.create_rule("E", ("E", "+", "B"), rule_id="E_rule_2")
    E_rule_2.bind_state(0, "E", 1)

    E_rule_3 = _test_grammar.create_rule("E", ("B",), rule_id="E_rule_3")
    E_rule_3.bind_state(0, "B", 1)

    B_rule_1 = _test_grammar.create_rule("B", ("0",), rule_id="B_rule_1")
    B_rule_1.bind_state(0, "0", 3)

    B_rule_2 = _test_grammar.create_rule("B", ("1",), rule_id="B_rule_2")
    B_rule_2.bind_state(0, "1", 4)


    _states = _test_grammar.generate_states()


    _state_color_id = 170
    _color_id = 208
    print(f"ITEM STATES:\n")
    for idx, i in enumerate(_states.values()):
        _state_color_id ^= 8
        print(apply_color(_state_color_id, f"\tSTATE: {idx}"))
        for _item in i:
            _color_id ^= 12
            print(apply_color(_color_id, f"\t\t\t{repr(_item)}\n"))
            print(apply_color(_color_id, f"\t\t\t\tSTATUS: {_item.status()}"))
            print()
            print()
        print()
    print()
    print()
    print(apply_color(10, f"There are {len(_states)} unique item sets/states!"))
    print()

    # init_rule = _test_grammar.select("INIT_RULE")
    # print(f"RULE ID: '{init_rule.rule_id}':  {init_rule.rule_head} ---> {init_rule.rule_body}")

    # init_rule.set_state(0)
    # _next_symbol = "E"
    # _next_state = init_rule.get_state(_next_symbol)
    # print(f"WHEN PARSER IS IN STATE: {init_rule.state} ON RULE ID: {init_rule.rule_id} TRANSITION TO STATE: {_next_state}")
