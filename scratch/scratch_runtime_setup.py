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

from collections import deque, defaultdict
from pathlib import Path

from pyprofiler import profile_callable, SortBy
from pyevent import PyChannels, PyChannel, PySignal

# from pyparse import Parser
from .test_automaton_design import Automaton
from .scratch_init_grammar import grammar_factory, init_grammar_1, init_grammar_2, init_grammar_3
from .source_descriptor import SourceFile
from .scratch_utils import CircularBuffer, copy_items, copy_item
from .utils import apply_color, bold_text, underline_text, center_text
from .scratch_cons import GrammarRuleBy, TableConstructionEvent, TEST_INPUT


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


def display_grammar_info(grammar=None):
    _grammar = GRAMMAR if grammar is None else grammar
    print(f"_______________ORIGINAL GRAMMAR_______________")
    display_grammar(_grammar)
    print()
    display_terminals(_grammar)
    print()
    display_non_terminals(_grammar)
    print()
    _grammar_2 = copy_items(_grammar, deepcopy=True)
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


def display_table(parse_table):
    _action_table, _goto_table = parse_table
    print(f"PARSE TABLE:")
    print()
    print(f"\tACTION TABLE:")
    for ak, av in _action_table.items():
        print(f"\t\t{ak} ---> {av}")

    print()
    print()

    print(f"\tGOTO TABLE:")
    for gk, gv in _goto_table.items():
        print(f"\t\t{gk} ---> {gv}")
    
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


def display_test_data(test_data):
    print()
    print(f"TEST INPUT DATA")
    for i in test_data:
        print(i)
    print()


def display_item_states(item_sets):
    print()
    print(f"ITEM STATES:")
    for item_state, _items in item_sets.items():
        print(f"STATE: {item_state}")
        for _item in _items:
            print(f"\t{_item.rule_head} ---> {_item.status()}")
        print()
    print()


def display_goto_mapping(goto_mapping):
    print()
    for i in goto_mapping:
        print(f"{i}: {goto_mapping[i]}")

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


def find_next_state(item_states, item):
    _item_copy = item.copy()
    _item_copy.advance()
    for state, items in item_states.items():
        if _item_copy in items:
            return state
    return None


def closure(rule, grammar):    
    _non_terminals = grammar.non_terminals()
    _closure_group = [rule]
    _break = False
    _rule_queue = deque(_closure_group)
    while _rule_queue:
        _next_rule = _rule_queue.popleft()
        _next_symbol = _next_rule.next_symbol(default=None)
        if _next_symbol in _non_terminals:
            _rule = grammar.rule(_next_symbol, search_by=GrammarRuleBy.HEAD)
            for _check_rule in _rule:
                if _check_rule in _closure_group:
                    continue
                _closure_group.append(_check_rule)
                _rule_queue.append(_check_rule)
    return tuple(copy_items(_closure_group, deepcopy=True))


def goto(rule):
    pass


def init_I0(grammar):
    _g_rules = grammar.rules()

    if not _g_rules:
        # TODO: create and raise custom error here
        _error_details = f"unable to create item set as no grammar rules have been added to grammar object..."
        raise RuntimeError(_error_details)
    
    _augmented_item = _g_rules[0]
    return closure(_augmented_item, grammar=grammar)


def generate_item_states(grammar) -> None:
    """
    # TODO: create 'GOTO' table - after generating item sets/states,
    #       iterate through them, performing the searches 

    # TODO: be wary of how the below logic (as well as the lib logic
    #       in general) handles concurrency/parallelism

    # TODO: ?? possibly create a stack implementation (possibly
    #       optimized for this lib, perhaps implement in the c
    #       programming language) ??

    # TODO: ?? create a buffer design (possibly optimized for this
    #       lib, perhaps implement in the c programming language) ??

    # TODO: fix goto logic as current implementation is missing some of the
    #       goto transitions for certain state/symbol combinations

    # TODO: add small runtime optimizations (like aliases for methods to reduce
    #       lookup times)


    """

    _terminals = grammar.terminals()
    _non_terminals = grammar.non_terminals()

    _init_item_set = init_I0(grammar)
    _item_sets = [_init_item_set]

    _current_state = 0
    _goto_mapping = {}
    _rule_queue = deque([_init_item_set])
    while _rule_queue:
        _next_item_set = _rule_queue.popleft()
        _current_state = len(_item_sets)
        for _item in _next_item_set:
            _item = _item.copy()
            if _item.can_reduce:
                continue
            _item.advance()
            if _item.next_symbol() in _non_terminals:
                _next_group = closure(_item, grammar)
                if _next_group not in _item_sets:
                    _item_sets.append(_next_group)
                    _rule_queue.append(_next_group)

            else:
                _next_group = [_item]
                if _next_group not in _item_sets:
                    _item_sets.append(_next_group)
                    _rule_queue.append(_next_group)

    _retval = {}
    for idx, i in enumerate(_item_sets):
        _retval[idx] = []
        for k in i:
            _retval[idx].append(k)

    return _retval


# TODO: double check, but this can likely be deleted
def generate_goto_mapping(item_states, grammar=GRAMMAR):
    # _all_symbols = grammar.symbols()
    # _goto_mapping = {_sym: {} for _sym in _all_symbols}
    # # for k, v in _goto_mapping.items():
    # #     print(f"{k}: {v}")
    # # print()

    # _state_item_lst = []
    # for idx, (k, v) in enumerate(item_states.items()):
    #     for _item in v:
    #         _state_item_lst.append((k, _item))

    # _testtest = {}
    # # print(f"ITEM STATES LIST")
    # for i in _state_item_lst:
    #     _state = i[0]
    #     _item = i[1]
    #     if _item not in _testtest:
    #         _testtest[_item] = []
    #     _testtest[_item].append(_state)


    _states = {}
    _item_queue = deque([(k, v) for k, v in item_states.items()])
    while _item_queue:
        _next_item = _item_queue.popleft()
        _state = _next_item[0]
        _items = _next_item[1]
        for _item in _items:
            if _item.rule_id not in _states:
                _states[_item.rule_id] = []
            _states[_item.rule_id].append(_state)


    for k, v in _states.items():
        print(f"{k}: {v}")

    # return _testtest


def generate_parse_table(grammar, item_states):
    _rules = grammar.rules()
    _init_rule = _rules[0]

    _terminals = grammar.terminals()
    _non_terminals = grammar.non_terminals()


    action_table = {}
    goto_table = {}

    for state, items in item_states.items():
        for item in items:
            next_symbol = item.next_symbol()
            if next_symbol is None:  # Reduce action
                if item.rule_head == _init_rule.rule_head:
                    action_table[(state, _init_rule.rule_head)] = 'accept'
                else:
                    for terminal in _terminals:
                        action_table[(state, terminal)] = f'reduce {item.rule_id}'
            elif next_symbol in _terminals:
                next_state = find_next_state(item_states, item)
                action_table[(state, next_symbol)] = f'shift {next_state}'
            else:
                next_state = find_next_state(item_states, item)
                goto_table[(state, next_symbol)] = next_state

    return action_table, goto_table


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
    return [i for i in _file_data.split("\n") if i]


def tokenize(source):
    raise NotImplementedError


def parse_data(source_data, parser):
    raise NotImplementedError


# @profile_callable(sort_by=SortBy.TIME)
def parse_main():
    # Initialize grammar object so that it contains all grammar rules
    # related to scratch language implementation (refer to top of
    # this module, within the docstring under the
    # '__________SCRATCH GRAMMAR SPEC__________' section for grammar
    # spec)
    init_grammar_1(GRAMMAR)
    # init_grammar_2(GRAMMAR)
    # init_grammar_3(GRAMMAR)


    ITEM_STATES = []
    GOTO_MAPPING = {sym: None for sym in SYMBOLS}


    # Generate (and display) item sets/states then create GOTO and actions
    # mapping which together when combined with an enumeration of the all
    # grammar symbols, build the parse table (which is used to guid the LR(0)
    # automaton component of the shift-reduce parser)
    _item_states = generate_item_states(GRAMMAR)
    display_item_states(_item_states)
    # for i in [(k, i.status()) for k, v in _item_states.items() for i in v]:
    #     print(i)
    # for k, v in _item_states.items():
    #     print(f"{k}: {v.status()}")
    # print()


    # _goto_mapping = generate_goto_mapping(_item_states)
    # display_goto_mapping(_goto_mapping)


    # Create parse table, used to guide the LR(0) automaton that makes
    # up the design for the shift/reduce parser
    _parse_table = generate_parse_table(GRAMMAR, _item_states)

    # Display parse table
    display_table(_parse_table)


    # Instantiate parser back-end (actual parsing implementation)
    # _parser_impl = ShiftReduceParser()
    # _parser_impl = None

    # Instantiate parser front-end (bridge between different parser designs)
    # parser = Parser(parser=_parser_impl)


    # Initialize source file object and get data contained within file
    # _source_file = SourceFile(path=TEST_INPUT)
    # _source_file_data = read_source(_source_file)
    # display_test_data(_source_file_data)
    


    # _source_is_valid = parse_data(_source_file_data, parser)

    # # Display result
    # display_result(_source_file_data, _source_is_valid)


if __name__ == "__main__":
    pass
