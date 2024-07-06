from .scratch_utils import generate_id
from .scratch_cons import ParserAction


class ParseTable:
    def __init__(self, grammar=None, table_id=None):
        self._table_id = table_id or generate_id()
        # self._item_states = item_states
        self._grammar = grammar
        self._action = {}
        self._goto = {}

    @property
    def table_id(self):
        return self._table_id

    @property
    def grammar(self):
        if self._grammar is None:
            # TODO: create and raise custom error here
            _error_details = f"unable to access 'grammar' attribute as one has not yet been associated with instance of {self.__class__.__name__}..."
            raise AttributeError(_error_details)
        return self._grammar

    def set_grammar(self, grammar):
        self._grammar = grammar

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

    def table(self):
        raise NotImplementedError

    def print(self):
        print()
        print(f"ACTION TABLE:")
        for action_key, action_value in self._action.items():
            if ParserAction.ACCEPT in action_value:
                print(f"  ACTION({action_key[0]}, {action_key[1]}) ---> {action_value[0]} {ParserAction.ACCEPT}")
            elif ParserAction.ERROR in action_value:
                print(f"  ACTION({action_key[0]}, {action_key[1]}) ---> {ParserAction.ERROR}")
            elif ParserAction.SHIFT in action_value:
                print(f"  ACTION({action_key[0]}, {action_key[1]}) ---> {action_value[0]} TO {action_value[1]}")
            elif ParserAction.REDUCE in action_value:
                # print(f"  IN STATE: {action_key[0]} ON SYMBOL: {action_key[1]} {action_value[0]} TO {action_value[1]}")
                print(f"  ACTION({action_key[0]}, {action_key[1]}) --->  {action_value[0]} TO {action_value[1]}")
            else:
                # TODO: create and raise custom error here
                _error_details = f"invalid parser action; must be one of either 'SHIFT', 'REDUCE', 'ACCEPT' or 'ERROR'..."
                raise RuntimeError(_error_details)

        print()
        print(f"GOTO TABLE:")
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

    # Function to display the parse table
    def display_parse_table(parse_table):
        print("ACTION TABLE:")
        for state, actions in parse_table.action.items():
            for symbol, action in actions.items():
                print(f"  ACTION({state}, '{symbol}') = {action}")

        print("\nGOTO TABLE:")
        for state, gotos in parse_table.goto.items():
            for non_terminal, next_state in gotos.items():
                print(f"  GOTO({state}, '{non_terminal}') = {next_state}")

    # Display the constructed parse table
    display_parse_table(parse_table)


if __name__ == "__main__":
    _parse_table_main()
