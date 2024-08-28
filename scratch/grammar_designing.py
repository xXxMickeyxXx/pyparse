from collections import deque

from pyparse import GrammarRuleError
from .utils import apply_color, bold_text, underline_text  # TODO: remove this once I solve an issue in this module (item states aren't being created correctly if two items have the same 'rule_head' and have the their 'look_behinds' and 'look_aheads' method calls match)
from .grammar_rule import GrammarRule
from .scratch_marker_symbol import MarkerSymbol
from .scratch_cons import GrammarRuleBy, ParserActionType
from .scratch_utils import generate_id
from .scratch_grammar_rules_filter import (
    RuleSelector,
    AndRuleSelector,
    OrRuleSelector,
    NotRuleSelector,
    RuleIDSelector,
    RuleHeadSelector,
    RuleBodySelector
)

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
            _symbols = self.symbols()
            # _item_set_pointer = 0
            _closed_init_set = self.closure(self.init_item)
            _item_sets = [_closed_init_set]
            _item_set_queue = deque(_item_sets)
            _item_set_added = True
            while _item_set_queue:
            # while _item_set_added:
            # while _item_set_pointer < len(_item_sets):
                # _item_set_added = False

                # _next_item_set = _item_sets[_item_set_pointer]
                # _item_set_pointer += 1
                # if not _item_set_queue:
                #     break

                _next_item_set = _item_set_queue.popleft()

                # _possible_item_trans = set()
                # for item in _next_item_set:
                #     _item = item.copy(deepcopy=True)
                #     _next_symbol = _item.next_symbol(default=None)
                #     _possible_item_trans.add(_next_symbol)
                #     _item.advance()

                # for i in _possible_item_trans:
                #     print(i)
                # print()

                _possible_trans = {}
                for item in _next_item_set:
                    _item = item.copy(deepcopy=True)
                    _next_symbol = _item.next_symbol(default=None)
                    if _next_symbol is None:
                        continue
                    if _next_symbol not in _possible_trans:
                        _possible_trans[_next_symbol] = []
                    _item.advance()
                    _possible_trans[_next_symbol].append(_item)


                # for i in _possible_trans.values():
                #     if i not in _item_sets:
                #         _item_sets.append(i)
                #         _item_set_added = True

                # print(f"POSSIBLE SYMBOL TRANSITIONS:")
                # for i in _possible_trans:
                #     print(i)
                # print()
                for _item_set_ in _possible_trans.values():
                    _temp_lst = []
                    for _rule in _item_set_:
                        _temp_lst.append(_rule)
                        if _rule.next_symbol(default=None) in self.non_terminals():
                            for _closed_item in self.closure(_rule.copy(deepcopy=True)):
                                if _closed_item not in _temp_lst:
                                    _temp_lst.append(_closed_item)

                    if _temp_lst not in _item_sets:
                        _item_set_queue.append(_temp_lst)

                if _next_item_set not in _item_sets:
                    # for i in range(len(_next_item_set)):
                    #     _next_item = _next_item_set[i]
                    #     if _next_item.next_symbol() in self.non_terminals():
                    #         for _closed_i in self.closure(_next_item):
                    #             _next_item_set.append(_closed_i)
                    _item_sets.append(_next_item_set)



            _retval = {idx: i for idx, i in enumerate(_item_sets)}
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
                _found_rules = self.select(RuleHeadSelector(_next_symbol), copy=False)
                _closure_group_rule_ids = [i.rule_id for i in _closure_group]
                for _check_rule in _found_rules:
                    if _check_rule in _closure_group:
                        continue
                    _closure_group.append(_check_rule)
                    _rule_queue.append(_check_rule)
        _retval = tuple([i.copy(deepcopy=True) for i in _closure_group])
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
    
    def add_rule(self, *rules):
        _rule_exist = []
        for _rule in rules:
            if _rule in self._rules:
                _rule_exist.append(_rule)
                continue
            self._rules.append(_rule)
        if _rule_exist:
            # TODO: create and raise custom error here            
            _last_rule = _rule_exist.pop(-1)
            _error_details = f"unable to add one or more rules as they already exists within instance of '{self.__class__.__name__}; "
            _error_details += ', '.join([(f'{i.rule_head} ---> {i.rule_body}') for i in _rule_exist])
            _error_details += f' and {_last_rule.rule_head} ---> {_last_rule.rule_body}'
            raise RuntimeError(_error_details)
        if rules:
            self._symbols_cache = None
            self._terminals_cache = None
            self._non_terminals_cache = None
            self._item_states_cache = None

    def remove_rule(self, selector):
        _selected_rules = self.select(selector)
        if not _selected_rules:
            # TODO: create and raise custom error here
            _error_details = f"unable to remove rule(s) which satisfy selector: {selector}; please verify rule(s) exist within this instance of '{self.__class__.__name__}' and try again..."
            raise RuntimeError(_error_details)
        self._rules = [i for i in self._rules if i not in _selected_rules]
        return _selected_rules

    def symbols(self):
        _symbols = self.terminals()
        _symbols.extend(self.non_terminals())
        if self._symbols_cache is None:
            self._symbols_cache = _symbols
        return self._symbols_cache

    def rules(self):
        return self._rules

    def select(self, selector, copy=False, deepcopy=True):
        return tuple([i for i in self.rules() if selector.select(i)])

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

    def copy(self, *, deepcopy=False):
        _new_cls = type(self)(grammar_id=self.grammar_id)
        _new_cls._rules = [i.copy(deepcopy=deepcopy) for i in self.rules()]
        return _new_cls

    @classmethod
    def from_rules(cls, rules: list | tuple, grammar_id: str = "", grammar_rule: GrammarRule = GrammarRule):
        _new_cls = cls(grammar_id=grammar_id, rule_factory=grammar_rule)
        _new_cls.add_rule(*rules)
        return _new_cls

    def build_table(self, table):
        _rules = self.rules()
        item_states = self.generate_states()
        _init_rule = _rules[0]
        _init_rule_head = _init_rule.rule_head
        _terminals = self.terminals()
        for state, items in item_states.items():
            for item in items:
                next_symbol = item.next_symbol()
                if item.can_reduce:
                    _aug_start_rule_head = _init_rule.rule_head
                    if item.rule_head == _aug_start_rule_head:
                        table.add_action(state, _aug_start_rule_head, (ParserActionType.ACCEPT, item))
                    else:
                        for terminal in _terminals:
                            table.add_action(state, terminal, (ParserActionType.REDUCE, item))
                        table.add_action(state, _init_rule_head, (ParserActionType.REDUCE, item))
                elif next_symbol in _terminals:
                    next_state = self.find_next_state(item_states, item)
                    table.add_action(state, next_symbol, (ParserActionType.SHIFT, next_state, item))
                else:
                    next_state = self.find_next_state(item_states, item)
                    table.add_goto(state, next_symbol, (next_state, item))

    def find_next_state(self, item):
        _item_copy = item.copy()
        _item_copy.advance()
        for state, items in self.item_states.items():
            for _item in items:
                if _item_copy == _item:
                    return state
        return None


if __name__ == "__main__":
    _rule_lst = [
        GrammarRule("$", ("E",), rule_id="INIT_RULE"),
        GrammarRule("E", ("E", "*", "B"), rule_id="E_rule_1"),
        GrammarRule("E", ("E", "+", "B"), rule_id="E_rule_2"),
        GrammarRule("E", ("B",), rule_id="E_rule_3"),
        GrammarRule("B", ("0",), rule_id="B_rule_1"),
        GrammarRule("B", ("1",), rule_id="B_rule_2")
    ]

    _test_grammar = Grammar.from_rules(_rule_lst, grammar_id="[ • -- TEST_GRAMMR -- • ]")

    # _test_grammar = Grammar(grammar_id="[ • -- TEST_GRAMMR -- • ]")
    
    # init_rule = _test_grammar.create_rule("$", ("E",), rule_id="INIT_RULE")
    # # init_rule.bind_state(0, "E", 3)
    # # init_rule.bind_action(3, "$", ParserActionType.ACCEPT)

    # E_rule_1 = _test_grammar.create_rule("E", ("E", "*", "B"), rule_id="E_rule_1")
    # # E_rule_1.bind_state(0, "E", 3).bind_state(3, "E", 5).bind_state(5, "E", 7)
    # # E_rule_1.bind_goto(0, "E", 3)
    # # E_rule_1.bind_action()

    # E_rule_2 = _test_grammar.create_rule("E", ("E", "+", "B"), rule_id="E_rule_2")
    # # E_rule_2.bind_state(0, "E", 3).bind_state(3, "E", 6).bind_state(6, "E", 8)
    # # E_rule_2.bind_goto(0, "E", 3)

    # E_rule_3 = _test_grammar.create_rule("E", ("B",), rule_id="E_rule_3")
    # # E_rule_3.bind_state(0, "B", 4)
    # # E_rule_3.bind_goto(0, "E", 3)

    # B_rule_1 = _test_grammar.create_rule("B", ("0",), rule_id="B_rule_1")
    # # B_rule_1.bind_state(0, "0", 1)
    # # B_rule_1.bind_goto(0, "B", 4)
    # # B_rule_1.bind_action(0, "0", (ParserActionType.SHIFT, 1))

    # B_rule_2 = _test_grammar.create_rule("B", ("1",), rule_id="B_rule_2")
    # # B_rule_2.bind_state(0, "1", 2)
    # # B_rule_2.bind_goto(0, "B", 4)
    # # B_rule_2.bind_action(0, "1", (ParserActionType.SHIFT, 2))


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

    # init_rule = _test_grammar.filter(RuleByID("INIT_RULE"))
    # init_rule = init_rule[0] if init_rule else None
    # if init_rule:
    #     print(f"RULE ID: '{init_rule.rule_id}':  {init_rule.rule_head} ---> {init_rule.rule_body}")
    # else:
    #     print(f"RULE BY ID: 'INIT_RULE' COULD NOT BE FOUND WITHIN GRAMMAR...\n")

    # _current_state = 0
    # _next_symbol = "E"
    # _next_state = init_rule.state(_current_state, _next_symbol)
    # print(f"WHEN PARSER IS IN STATE: {_current_state} ON RULE ID: {init_rule.rule_id} TRANSITION TO STATE: {_next_state}")
    # print()
    # print()


    # _COLOR_ID = 172
    # print()
    # _init_grammar_rules_len = len(_test_grammar)
    # print(underline_text(bold_text(apply_color(_COLOR_ID, f"GRAMMAR ID: {_test_grammar.grammar_id} INITIALILY CONTAINS {_init_grammar_rules_len} {'RULE' if _init_grammar_rules_len == 1 else 'RULES'}"))))
    # print()
    # _arrow_txt = ""
    # for _ in range(3):
    #     _arrow_txt += bold_text(apply_color(201, "                     |\r\n"))
    # _arrow_txt += bold_text(apply_color(201, "                     |\n"))
    # _arrow_txt += bold_text(apply_color(201, "                     ↓"))
    # print(_arrow_txt)
    # print()
    # _composite_filter = RuleByID("INIT_RULE") | RuleByID("B_rule_2")
    # _removed_init_rule = _test_grammar.remove_rule(_composite_filter)
    # _removed_init_rule_len = len(_removed_init_rule)
    # print(underline_text(bold_text(apply_color(226, f"REMOVED RULE(S) (NOTE: {_removed_init_rule_len} RULE(S) HAVE BEEN REMOVED):"))))
    # print()
    # for i in _removed_init_rule:
    #     print(i)
    # print()
    # print()
    # _current_grammar_rules = _test_grammar.rules()
    # _current_grammar_rules_len = len(_current_grammar_rules)
    # print(underline_text(bold_text(apply_color(226, f"RULES FOR GRAMMAR ID: {_test_grammar.grammar_id} (NOTE: GRAMMAR CONTAINS {_current_grammar_rules_len} {'RULE' if _current_grammar_rules_len == 1 else 'RULES'}):"))))
    # print()
    # for i in _current_grammar_rules:
    #     print(i)
    # print()

    # _sel_1 = _test_grammar.select(RuleIDSelector("E_rule_1"))
    # _sel_2 = _test_grammar.select(RuleIDSelector("E_rule_2"))
    # _sel_3 = _test_grammar.select(RuleIDSelector("E_rule_3"))
    # _sel_4 = _test_grammar.select(RuleIDSelector("B_rule_1"))
    # _sel_5 = _test_grammar.select(RuleIDSelector("B_rule_2"))
    # _sel_6 = _test_grammar.select(RuleIDSelector("INIT_RULE"))

    # _test_list = [_sel_1, _sel_2, _sel_3, _sel_4, _sel_5, _sel_6]

    # print(f"SEARCHING THROUGH GRAMMAR RULE/ITEM SELECTIONS")
    # print()
    # for i in _test_list:
    #     print(f"SELECTION:")
    #     _item = None
    #     if i:
    #         _item = i[0]
    #         print(f"RULE/ITEM ID: {_item.rule_id}")
    #     print()
            

    # def find_item(filter, grammar):
    #     _retval = (None, None)
    #     _item_states = grammar.generate_states()
    #     for state, items in _item_states.items():
    #         for _item in items:
    #             _filtered = filter.filter(_item)
    #             if _filtered:
    #                 _retval = _item
    #                 break
    #     return _retval


    # _filter = AugItemStatus(_sel_e_rule_1)
    # _possible_item = find_item(_filter, _test_grammar)[0: 2]
    # # _possible_item = find_item(_filter, _test_grammar)
    # print()
    # print(f"ATTEMPTED TO FIND MATCH OF AUGMENTED ITEM USING FILTER:")
    # print()
    # print(_filter)
    # print()
    # if _possible_item:
    #     print(f"FOUND MATCH:")
    #     print()
    #     print(f"ORIGINAL:")
    #     print(_sel_e_rule_1)
    #     print()
    #     print(f"FOUND VALUE:")
    #     print(_possible_item)
    #     print()
    # else:
    #     print()
    #     print(f"NO MATCH FOUND WITH RULE ID: {_sel_e_rule_1.rule_id} WITH THE STATE OF:\n\n\t{_sel_e_rule_1.status()}")
