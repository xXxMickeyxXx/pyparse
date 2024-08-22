from .scratch_utils import generate_id
from .utils import apply_color, bold_text, underline_text


class Table:

    def __init__(self, table_id=None):
        self._table_id = table_id or generate_id()
        self._table = []
        self._indexs = {}

    @property
    def table_id(self):
        return self._table_id

    def size(self, include_header=True):
        return 0 if not self._table else (len(self._table) if include_header else len(self._table) - 1)

    def add_column(self, column_id):
        self._verify_header()
        _col_lst = self._table[0]
        _col_lst.append(column_id)

    def add_row(self, *row_vals):
        self._verify_header()
        _new_row = [*row_vals]
        _new_index = {len(self._table)-1: _new_row}
        self._table.append(_new_row)

    def _verify_header(self):
        if not self._table:
            self._table.append([])

    def select(self, idx):
        raise NotImplementedError

    def search(self, by):
        raise NotImplementedError


class ParseTable:
    def __init__(self, table_id=None):
        self._table_id = table_id or generate_id()
        self._item_states = None
        self._action = {}
        self._goto = {}

    @property
    def table_id(self):
        return self._table_id

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

    def build(self, builder):
        return builder.build_table(self)

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
