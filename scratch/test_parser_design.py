from pyparse import (
    Grammar,
    Tokenizer,
    ShiftReduceParser,
    Parser,
    TransitionError
)
from pyparse.library import PySignal
from .utils import generate_id, apply_color, underline_text, bold_text, center_text


def shift_reduce_parse_tester(tokens):

	# NOTE: moved over from 'automaton_designing' module; saving here in case
	# 		I want to reference it in the future (though I'll likely delete it)

    state_stack = [0]  # Initialize the state stack with the initial state
    token_stack = []  # Initialize the token stack as empty

    stack = [(0, "$")]

    # Start parsing loop
    for token in tokens:
        state = stack[-1][0]
        _token = token[1]
        print(f"CURRENT STATE ---> {state}")
        print(f"CURRENT TOKEN ---> {token}")
        if _token in parse_table[state]:
            _item = parse_table[state][_token]
            print(f"ITEM ---> {_item}")
            state_stack.append(parse_table[state][_token])
            token_stack.append(_token)

        else:
            # Reduce action
            for production in grammar:
                if token in parse_table[state]:
                    # Replace the right-hand side of the production with the left-hand side
                    for _ in grammar[production]:
                        state_stack.pop()
                        token_stack.pop()
                    state = state_stack[-1]
                    state_stack.append(parse_table[state][production])
                    token_stack.append(production)
                    break
            else:
                # Error: No valid action found
                return "Syntax Error"

    # Check if the parsing process completes successfully
    if len(state_stack) == 2 and state_stack[1] == 3:
        return True
    else:
        return False


if __name__ == "__main__":
	pass
