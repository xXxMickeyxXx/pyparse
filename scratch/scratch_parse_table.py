class ParseTable:
    def __init__(self, grammar=None):
        self._grammar = grammar
        self._action = {}
        self._goto = {}

    @property
    def grammar(self):
        if self._grammar is None:
            # TODO: create and raise custom error here
            _error_details = f"unable to access 'grammar' attribute as one has not yet been associated with instance of {self.__class__.__name__}..."
            raise AttributeError(_error_details)
        return self._grammar

    def add_action(self, state, symbol, action):
        if state not in self._action:
            self._action[state] = {}
        self._action[state][symbol] = action

    def add_goto(self, state, non_terminal, next_state):
        if state not in self._goto:
            self._goto[state] = {}
        self._goto[state][non_terminal] = next_state

    def action(self, state, symbol):
        return self._action.get(state, {}).get(symbol, None)

    def goto(self, state, non_terminal):
        return self._goto.get(state, {}).get(non_terminal, None)

    def table(self):
        raise NotImplementedError

    def print(self):
        print()
        print(f"ACTION TABLE:")
        for _astate, actions in self._action.items():
            for sym, action in actions.items():
                print(f"  ACTION({_astate}, '{sym}') = {action}")
        print()
        print(f"GOTO TABLE:")
        for _gstate, gotos in self._goto.items():
            for non_t, next_state in gotos.items():
                print(f"  GOTO({_gstate}, '{non_t}') = {next_state}")
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
