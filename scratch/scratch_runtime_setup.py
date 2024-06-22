"""

__________SCRATCH GRAMMAR SPEC__________

    S ::= aA
    A ::= a | b


__________LR(0) AUTOMATON__________


    I.) TEST GRAMMAR:
            
            S ::= aA
            A ::= a | b


    II.) SYMBOLS:

            A.) NON-TERMINALS:
                
                $
                S
                A

            B.) TERMINALS:
                
                a
                b


    III.) Generate Item Sets:

        A.)  Augment grammar

            1.) Create new, starting prodction rule, and ensure it's at the beginning/top of the rule container
                
                $ ---> S

            2.) Create initial item set

                a.) Start with initial, augmented item

                    $ ---> .S

                b.) Close initial, augmented item

                    $ ---> .S
                    S ---> .aA

                c.) Complete initial item set/state 'I0'

                    I0:

                        $ ---> .S
                        S ---> .aA

                d.) Calculate GOTO for each symbol (if able to) for item set/state 'I0'

                        GOTO(0, S) = I1

                    (NOTE: the above 'GOTO' function can be read as, "On seeing the symbol 'S', while in state 0, ")

            3.) Perform transitions and calculate GOTO's, using items from initial item sets (and on), until no new item sets/states can be generated

                a.) Perform transition on first item of item set 'I0' (the starting item)

                    I1:

                        $ ---> S.

                b.) Next, do the transition for the 2nd item of item set 'I0' to create 'I2'

                    S ---> a.A

                c.) Close item to create set/state 'I2'

                    S ---> a.A
                    A ---> b
                    A ---> c

                d.) Complete item set/state 'I2'

                    I2:

                        S ---> a.A
                        A ---> .b
                        A ---> .c

                e.) Transition on first item of item set/state 'I2' to begin item set/state 'I3'

                    I3:

                        S ---> aA.

                f.) Transition on 2nd item of item set/state 'I2'

                    I4:

                        A ---> b.

                g.) Transition on 3rd item of item set/state 'I2'
                
                    I5:

                        A ---> c.


                

                $ ---> .S 
                S ---> .aA


                A ---> .b



    AUGMENTED TEST GRAMMAR:
        $ ---> .S  
        S ---> .aA
        A ---> .b


        I0:
            S ---> .S
            S ---> .aA
            A ---> .b

        I1:
            $ ---> S.

        I2:
            S ---> a.A
            A ---> .b

        I3:
            A ---> b.


        EXAMPLE INPUT ---> ab

                INITIALIZE:
                    [(0, $)]
                
                STEP:
                    [(0, $), (2, a)]

                STEP:
                    [(0, $), (2, a), (3, b)]

                STEP:
                    [(0, $), (2, a), (4, A)]

                STEP:
                    [(0, $), (1, S)]


        EXAMPLE INPUT 2 ---> abbA

                INITIALIZE:
                    [(0, $)]
                
                STEP:
                    [(0, $), (2, a)]

                STEP:
                    [(0, $), (2, a), (3, b)]

                STEP:
                    [(0, $), (2, a), (4, A)]

                STEP:
                    [(0, $), (2, a), (3, A)]

                STEP:
                    [(0, $), (2, a)]

                STEP:
                    [(0, $), (2, a), (4, A)]

                STEP:
                    [(0, $), (1, S)]


__________LR(0) AUTOMATON__________


    TEST GRAMMAR:
        E ---> E * B
        E ---> E + B
        E ---> B
        B ---> 0
        B ---> 1
        B ---> (E)


    TEST AUGMENTED GRAMMAR:
        S ---> .E
        E ---> .E * B
        E ---> .E + B
        E ---> .B
        B ---> .0
        B ---> .1
        B ---> .(E)


        I0:
            KERNEL
                S ---> .E
            CLOSURE
                E ---> .E * B
                E ---> .E + B
                E ---> .B
                B ---> .0
                B ---> .1
                B ---> .(E)
            TRANSITIONS
                GOTO(0, E) = 1
                GOTO(0, B) = 4


        I1:
            KERNEL
                S ---> E.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)
                REDUCE(I1, S) = ACCEPT

        I2:
            KERNEL
                E ---> E .* B
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)

        I3:
            KERNEL
                E ---> E .+ B
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


        I4:
            KERNEL:
                E ---> B.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)
                REDUCE(4, E)

        I5:
            KERNEL
                B ---> 0.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


        I6:
            KERNEL
                B ---> 1.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)

        I7:
            KERNEL
                B ---> (.E)
            CLOSURE
                E ---> .E * B
                E ---> .E + B
                E ---> .B
            TRANSITIONS
                NONE
            ACTION(S)

        I8:
            KERNEL
                E ---> E * .B
            CLOSURE
                B ---> .0
                B ---> .1
            TRANSITIONS
                GOTO(7, B) = 9
            ACTION(S)


        I9:
            KERNEL
                E ---> E + .B
            CLOSURE
                B ---> .0
                B ---> .1
            TRANSITIONS
                GOTO(8, B) = 10
            ACTION(S)


        I10:
            KERNEL
                E ---> E * B.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)


        I11:
            KERNEL
                E ---> E + B.
            CLOSURE
                NONE
            TRANSITIONS
                NONE
            ACTION(S)



    INIT:

        • Parser initializes, adding initial state/accept symbol to the stack

    PARSE

        • Parser 



__________LR(0) AUTOMATON__________


    TEST GRAMMAR:
        E ---> E * B
        E ---> E + B
        E ---> B
        B ---> number
        B ---> (E)


    TEST AUGMENTED GRAMMAR:
        E ---> .E
        E ---> .E * B
        E ---> .E + B
        E ---> .B
        B ---> .NUMBER
        B ---> .(E)


         I0:
            E ---> .E (augmented grammar start symbol)
            E ---> .E * B
            E ---> .E + B
            E ---> .B
            B ---> .NUMBER
            B ---> .(E)

                TRANSITIONS (from I0)
                    GOTO(0, E) = 1
                    GOTO(0, B) = 4
                    GOTO(0, NUMBER) = 


        I1:
            E ---> E.
                
                ACTION: ACCEPT


        I2:
            E ---> E .* B

"""

from collections import deque
from pathlib import Path

from pyprofiler import profile_callable, SortBy
from pyevent import PyChannels, PyChannel, PySignal

from pyparse import Parser
from .test_automaton_design import Automaton
from .scratch_init_grammar import grammar_factory, init_grammar
from .source_descriptor import SourceFile
from .utils import apply_color, bold_text, underline_text, center_text
from .scratch_cons import GrammarRuleBy, TableConstructionEvent



"""
        
        ###########################################################################################################################
        #                                                                                                                         #
        # • -------------------------------------------------- PYPARSE TO-DO -------------------------------------------------- • #
        #                                                                                                                         #
        ###########################################################################################################################


        I.)





        ###################################################################################################################
        #                                                                                                                 #
        # • -------------------------------------------------- NOTES -------------------------------------------------- • #
        #                                                                                                                 #
        ###################################################################################################################


        1.) Use the event loop and context designs from the 'pysynchrony' for implementing and designing components of this library/package


"""




        #####################################################################################################################
        #                                                                                                                   #
        # • -------------------------------------------------- TESTING -------------------------------------------------- • #
        #                                                                                                                   #
        #####################################################################################################################


GRAMMAR = grammar_factory()
GRAMMAR_RULES = GRAMMAR.rules()
NON_TERMINALS = GRAMMAR.non_terminals()
TERMINALS = GRAMMAR.terminals()
SYMBOLS = NON_TERMINALS + TERMINALS

ITEM_STATES = {}
GOTO_MAPPING = {}
TABLE_CHANNEL = PyChannel(channel_id="PARSE_TABLE_CHANNEL")


def display_grammar(grammar):
    print()
    print(grammar)
    print()


def display_terminals(grammar=None):
    _grammar = GRAMMAR if grammar is None else grammar
    _terminals = TERMINALS if grammar is None else _grammar.terminals()
    print()
    print(f"TERMINALS:")
    for terminal in _terminals:
        print(terminal)
    print()


def display_non_terminals(grammar=None):
    _grammar = GRAMMAR if grammar is None else grammar
    _non_terminals = NON_TERMINALS if grammar is None else _grammar.non_terminals()
    print()
    print(f"NON-TERMINALS:")
    for _non_terminal in _non_terminals:
        print(_non_terminal)
    print()


def copy_grammar(grammar=None, *, deepcopy=False):
    _grammar = GRAMMAR if grammar is None else grammar
    return _grammar.copy(deepcopy=deepcopy)


def display_grammar_info(grammar=None):
    _grammar = GRAMMAR if grammar is None else grammar
    print(f"_______________ORIGINAL GRAMMAR_______________")
    display_grammar(_grammar)
    print()
    display_terminals(_grammar)
    print()
    display_non_terminals(_grammar)
    print()
    _grammar_2 = copy_grammar(_grammar, deepcopy=True)
    print(f"_______________COPIED GRAMMAR_______________")
    display_grammar(_grammar_2)
    print()
    display_terminals(_grammar_2)
    print()
    display_non_terminals(_grammar_2)
    print()


def display_rule(rule_input, search_by=GrammarRuleBy.HEAD, grammar=None):
    _grammar = GRAMMAR if grammar is None else grammar
    _g_rule = _grammar.rule(rule_input, search_by=search_by)
    if _g_rule:
        print(f"GETTING GRAMMAR RULE")
        for _test_rule in _g_rule:
            print(f"\t{rule_input}: {_test_rule.rule_body}")
    else:
        print(f"INVALID GRAMMAR RULE INPUT ---> {rule_input}")
    print()


def display_rules(grammar=None):
    _grammar = GRAMMAR if grammar is None else grammar
    _grammar_rules = GRAMMAR_RULES if grammar is None else _grammar.rules()
    print()
    print(f"GRAMMAR RULES:")
    for rule in _grammar_rules:
        print(rule)
    print()


def display_rule_statuses(grammar=None):
    _grammar = GRAMMAR if grammar is None else grammar
    _grammar_rules = GRAMMAR_RULES if grammar is None else _grammar.rules()
    _rule_count = len(_grammar)
    print()
    print(f"STATUS OF GRAMMAR RULES ({_rule_count} RULES):")
    _done_rules = 0
    while _done_rules < _rule_count:
        for rule in _grammar_rules:
            _rule_status = f"{rule.rule_head} ---> {rule.status()}"
            if rule.can_reduce:
                _done_rules += 1
                print(_rule_status + " (COMPLETE)")
            else:
                print(_rule_status)
            rule.advance_marker()
        print()


def display_table(parse_table):
    print()
    print(f"PARSE TABLE:")
    print(parse_table)
    print()


def display_items(items, set_id):
    print()
    _text = underline_text(bold_text(apply_color(11, f"{set_id} ITEMS:")))
    _text += "\n"
    print(_text)
    for _item in items:
        print(f"\t{_item.rule_head}")
        print(f"\t{_item.rule_body}")
        print(f"\t{_item.status()}")
        print()
    print()


def display_item_states(item_sets):
    print()
    print(f"ITEM STATES:")
    for item_state, _items in item_sets.items():
        print(f"STATE: {item_state}")
        for _item in _items:
            print(f"\tITEM SYMBOL: {_item.rule_head}")
            print(f"\tITEM STATE: {_item.status()}")
            print()
        print()
    print()


def display_goto_mapping(goto_mapping):
    print()
    print(underline_text(bold_text(apply_color(211, f"GOTO MAPPING:"))))
    print()
    for (pre_tran, symbol), post_tran in goto_mapping.items():
        print(f"\t{apply_color(208, 'ON')} {bold_text(apply_color(11, symbol))} {apply_color(208, 'IN STATE')} {bold_text(apply_color(11, pre_tran))} {apply_color(208, 'GOTO STATE')}:")
        print(f"\t    |")
        print(f"\t    |")
        print(f"\t    |")
        print(f"\t    • ---> {bold_text(apply_color(11, post_tran))}")
        print()
    print()


def display_result(input, parser_result):
    if parser_result:
        _color = 10
        _text = underline_text(bold_text(apply_color(_color, f"INPUT IS VALID!!!")))
        _text += f"\n    |"
        _text += f"\n    |"
        _text += f"\n    • ----> {bold_text(apply_color(11, input))}"
        _border_text = f"-" * int(len(_text)/2)
        _result = bold_text(apply_color(_color, _text))
    else:
        _color = 9
        _text = underline_text(bold_text(apply_color(_color, f"INPUT IS INVALID!!!")))
        _text += f"\n    |"
        _text += f"\n    |"
        _text += f"\n    • ----> {bold_text(apply_color(11, input))}"
        _border_text = f"-" * int(len(_text)/2)
        _result = _text
    print(apply_color(_color, _border_text))
    print(_result)
    print(apply_color(_color, _border_text))
    print()


def next_symbol(rule, default=None):
    # TODO: figure out if rule is augmented and if it isn't, figure out if it's
    #       safe to do so
    _look_ahead = rule.look_ahead()
    if _look_ahead:
        return _look_ahead[0]
    return default


def closure(rule, grammar=None):
    _grammar = GRAMMAR if grammar is None else grammar
    _non_terminals = NON_TERMINALS if (bool(NON_TERMINALS) and grammar is None) else _grammar.non_terminals()
    _terminals = TERMINALS if (bool(TERMINALS) and grammar is None) else _grammar.terminals()
    
    _closure_group = [rule]
    _break = False
    _rule_queue = deque(_closure_group)
    while _rule_queue:
        _next_rule = _rule_queue.popleft()
        _next_symbol = next_symbol(_next_rule)
        if _next_symbol in _non_terminals:
            _rule = _grammar.rule(_next_symbol, search_by=GrammarRuleBy.HEAD)
            for _check_rule in _rule:
                if _check_rule in _closure_group:
                    continue
                _closure_group.append(_check_rule)
                _rule_queue.append(_check_rule)
    return tuple(_closure_group)


def goto(current_state, rule, transitions=None, item_groups=None):
    # _rule = rule.copy()
    # _info_text = ""
    if not rule.at_end:
        # _info_text += f"PRE-ADVANCE ITEM - STATE @: {current_state}\n\t{rule.status()}\n"
        _new_state = current_state + 1
        rule.advance_marker()
        # _info_text += f"POST-ADVANCE ITEM - STATE @: {_new_state}\n\t{rule.status()}\n"
        _closure_group = closure(rule)

        # _info_text += f"CLOSURE (on state: {current_state} ---> state: {_new_state})"
        # for _item in _closure_group:
        #     _info_text += f"RULE: {_item.rule_head}\n"
        #     _info_text += f"BODY: {_item.rule_body}\n\n"
        # print(_info_text)
        # print()
        return _new_state, _closure_group
    return None


def init_I0(grammar=None):
    _grammar = GRAMMAR if grammar is None else grammar
    _g_rules = GRAMMAR_RULES if grammar is None else _grammar.rules()

    if not _g_rules:
        # TODO: create and raise custom error here
        _error_details = f"unable to create item set as no grammar rules have been added to grammar object..."
        raise RuntimeError(_error_details)
    
    _augmented_item = _g_rules.pop(0)
    return closure(_augmented_item, grammar=_grammar)


def generate_item_sets(grammar=None) -> None:
    # TODO: fix goto logic as current implementation is missing some of the
    #       goto transitions for certain state/symbol combinations

    # TODO: figure out how to ensure items add to the item set/state/group (via
    #       calling the 'closure' function on the item) are taken into account,
    #       otherwise, the parse table may be incomplete

    # TODO: this function should use events to build the final item sets/states
    #       as well as the GoTo mappings, as opposed to returning those values
    #       (using events/event-driven techniques)

    # TODO: need to copy an item in it's state into the it's respective item
    #       state grouping so that it's a separate object or else you'll have
    #       all of the correct rules in their correct groups/states, but they
    #       will all have been advanced (i.e. their marker) to the end of the
    #       augmented rule

    # TODO: add small runtime optimizations (like aliases for methods to reduce
    #       lookup times)


    _initial_item_group = init_I0(grammar=grammar)

    _gotos = {}
    _item_states = {0: _initial_item_group}
    TABLE_CHANNEL.emit(TableConstructionEvent.UPDATE_STATES, 0, _initial_item_group)
    _new_state_added = True
    _current_state = 0
    while _new_state_added:
        _new_state_added = False

        _temp_goto_container = {}
        _next_states = [(next_symbol(i), i) for i in _item_states[0]]
        while _next_states:
            _next_symbol, _next_item_rule = _next_states.pop(0)

            _previous_state = _current_state
            _goto_result = goto(_current_state, _next_item_rule)
            if _goto_result is None:
                continue

            _current_state, _new_item_group = _goto_result
            print(f"IN STATE: {_current_state}")
            if TABLE_CHANNEL.emit(TableConstructionEvent.UPDATE_STATES, _current_state, _new_item_group)["UPDATE_STATES"]:
                TABLE_CHANNEL.emit(TableConstructionEvent.UPDATE_GOTO_MAPPING, _next_symbol, _previous_state, _current_state)
                _item_states[_current_state] = _new_item_group
                _new_state_added = True


def generate_parse_table(grammar=None):
    return []


def read_source(source_file):
    _filepath = source_file.get()
    if not isinstance(_filepath, Path):
        _filepath = Path(_filepath)
    _file_data = ""
    with open(_filepath, "r") as in_file:
        _file_data = in_file.read()

    if not bool(_file_data):
        # TODO: create and raise custom error here
        _error_details = f"Error Reading Source File Contents -- unable to read data contained within file @: {filepath}"
        raise RuntimeError
    return _file_data


def tokenize(source):
    raise NotImplementedError


def parse_data(source_data, parser):
    return parser.parse(source_data)


def update_item_sets_tblevent(state, item_sets):
    # TODO: ?? raise an error if 'state' already exists within
    #       'ITEM_STATES' ??
    if state not in ITEM_STATES:
        ITEM_STATES.update({state: [i.copy() for i in item_sets]})
        return True
    return False


def update_goto_mapping_tblevent(next_symbol, previous_state, current_state):
    # TODO: ?? raise an error if 'previous_state' already exists within
    #       'GOTO_MAPPING' ??
    if previous_state not in GOTO_MAPPING:
        _goto_key = (previous_state, next_symbol)
        GOTO_MAPPING[_goto_key] = current_state


# @profile_callable(sort_by=SortBy.CALLS)
def parse_main():

    #### • ----------**4TESTING**---------- • ####
    from .grammar_designing import Grammar
    from .grammar_rule import GrammarRule


    # Initialize grammar object so that it contains all grammar rules
    # related to scratch language implementation (refer to top of
    # this module, within the docstring under the
    # '__________SCRATCH GRAMMAR SPEC__________' section for grammar
    # spec)
    init_grammar(GRAMMAR)


    # TODO
    #  |
    #  • ---> Deserialize parse table


    # Register events associated with building parse table (if one hasn't been
    # serialized and saved to disk)
    TABLE_CHANNEL.register(TableConstructionEvent.UPDATE_STATES, receiver=update_item_sets_tblevent, receiver_id="UPDATE_STATES")
    TABLE_CHANNEL.register(TableConstructionEvent.UPDATE_GOTO_MAPPING, receiver=update_goto_mapping_tblevent, receiver_id="UPDATE_GOTO_MAPPING")


    # Generate (and display) item sets/states then create parse table (for use
    # in guiding the LR(0) automaton component of the shift-reduce parser)
    # _item_states = generate_item_sets()
    # display_item_states(_item_states)

    generate_item_sets()    
    display_item_states(ITEM_STATES)

    display_goto_mapping(GOTO_MAPPING)


    # # Create parse table, used to guide the LR(0) automaton that makes
    # # up the design for the shift/reduce parser
    # _parse_table = generate_parse_table(GRAMMAR)

    # # Display parse table
    # display_table(_parse_table)


    # # Instantiate parser back-end (actual parsing implementation)
    # # _parser_impl = ShiftReduceParser()
    # _parser_impl = None

    # # Instantiate parser front-end (bridge between different parser designs)
    # parser = Parser(parser=_parser_impl)


    # # Initialize source file
    # _source_file = SourceFile(path=r"/Users/mickey/Desktop/Python/custom_packages/pyparse/files/data/example_grammar_input_2024_06_13.txt")

    # # Parse input to verify that it adheres to the specified language (as
    # # defined by the grammar)
    # _source_file_data = read_source(_source_file)
    # _source_is_valid = parse_data(_source_file_data, parser)

    # # Display result
    # display_result(_source_file_data, _source_is_valid)


if __name__ == "__main__":
    pass
