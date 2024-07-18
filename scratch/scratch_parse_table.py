from .scratch_utils import generate_id
from .scratch_cons import ParserAction
from .utils import apply_color, bold_text, underline_text


class ParseTable:
    def __init__(self, grammar=None, table_id=None, start_symbol="$"):
        self._table_id = table_id or generate_id()
        self._grammar = grammar
        self._start_symbol = start_symbol
        self._item_states = None
        self._action = {}
        self._goto = {}
        if self._grammar:
            self.init_table()

    @property
    def table_id(self):
        return self._table_id

    @property
    def grammar(self):
        if self._grammar is None:
            # TODO: create and raise custom error here
            _error_details = f"unable to access 'grammar' as it has not yet been assigned to this parse table..."
            raise RuntimeError(_error_details)
        return self._grammar

    @property
    def item_states(self):
        if self._item_states is None:
            self._item_states = self.grammar.generate_states()
        return self._item_states

    def set_grammar(self, grammar):
        self._grammar = grammar
        self.init_table()

    def add_action(self, state, symbol, action):
        _action_key = (state, symbol)
        if _action_key not in self._action:
            self._action[_action_key] = action
            return True
        return False

    def add_goto(self, state, non_terminal, next_state):
        _goto_key = (state, non_terminal)
        if _goto_key not in self._goto:
            self._goto[_goto_key] = next_state
            return True
        return False

    def action(self, state, symbol, default=None):
        _action_key = (state, symbol)
        return self._action.get(_action_key, default)

    def goto(self, state, non_terminal, default=None):
        _goto_key = (state, non_terminal)
        return self._goto.get(_goto_key, default)

    def find_next_state(self, item_states, item):
        _item_copy = item.copy()
        _item_copy.advance()
        for state, items in item_states.items():
            if _item_copy in items:
                return state
        return None

    def init_table(self):
        _rules = self.grammar.rules()
        item_states = self.item_states
        _init_rule = _rules[0]
        _init_rule_head = _init_rule.rule_head
        _terminals = self.grammar.terminals()
        for state, items in item_states.items():
            for item in items:
                next_symbol = item.next_symbol()
                if item.can_reduce:
                    _aug_start_rule_head = _init_rule.rule_head
                    if item.rule_head == _aug_start_rule_head:
                        self.add_action(state, _aug_start_rule_head, (ParserAction.ACCEPT, item))
                    else:
                        for terminal in _terminals:
                            self.add_action(state, terminal, (ParserAction.REDUCE, item))
                        self.add_action(state, self._start_symbol, (ParserAction.REDUCE, item))
                elif next_symbol in _terminals:
                    next_state = self.find_next_state(item_states, item)
                    self.add_action(state, next_symbol, (ParserAction.SHIFT, next_state, item))
                else:
                    next_state = self.find_next_state(item_states, item)
                    self.add_goto(state, next_symbol, (next_state, item))

    def print(self):
        print()
        print(underline_text(bold_text(apply_color(208, f"ACTION TABLE:"))))
        for action_key, action_value in self._action.items():
            print(f"  ACTION({action_key})={action_value}")
        print()
        print(underline_text(bold_text(apply_color(208, f"GOTO TABLE:"))))
        for goto_key, goto_value in self._goto.items():
            print(f"  GOTO({goto_key[0]}, {goto_key[1]}) ---> {goto_value}")
        print()


def _parse_table_main():
    # Constructing the parse table
    parse_table = ParseTable()

    # Adding ACTION entries
    parse_table.add_action(0, 'a', ('SHIFT', 2))
    parse_table.add_action(1, '$', ('ACCEPT',))
    parse_table.add_action(2, 'b', ('SHIFT', 4))
    parse_table.add_action(3, 'a', ('REDUCE', 'S'))
    parse_table.add_action(3, 'b', ('REDUCE', 'S'))
    parse_table.add_action(4, 'a', ('REDUCE', 'A'))
    parse_table.add_action(4, 'b', ('REDUCE', 'A'))

    # Adding GOTO entries
    parse_table.add_goto(0, 'S', 1)
    parse_table.add_goto(2, 'A', 3)

    # Display parse table (ACTION + GOTO tables)
    parse_table.print()


if __name__ == "__main__":
    _parse_table_main()
