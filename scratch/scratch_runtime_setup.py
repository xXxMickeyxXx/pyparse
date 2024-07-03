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

from pyparse import Parser
from pysynchrony import PySynchronyEvent
from .scratch_parse_table import ParseTable
from .test_automaton_design import Automaton
from .scratch_init_grammar import grammar_factory, init_grammar_1, init_grammar_2, init_grammar_3
from .source_descriptor import SourceFile
from .scratch_utils import generate_id, CircularBuffer, copy_items, copy_item
from .utils import apply_color, bold_text, underline_text, center_text
from .scratch_cons import ParserAction, GrammarRuleBy, TableConstructionEvent, TEST_INPUT


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


ITEM_STATES_TEXT = """
#########################################################################################################################
#                                                                                                                       #
# • -------------------------------------------------- ITEM STATES -------------------------------------------------- • #
#                                                                                                                       #
#########################################################################################################################
"""


TEST_PARSING_TEXT = """
##########################################################################################################################
#                                                                                                                        #
# • -------------------------------------------------- TEST PARSING -------------------------------------------------- • #
#                                                                                                                        #
##########################################################################################################################
"""


class Chain:

    def __init__(self, chain_id=None):
        self._chain_id = chain_id or generate_id()
        self._handlers = []

    @property
    def chain_id(self):
        return self._chain_id

    def add_handler(self, handler, handler_id=None, overwrite=False):
        _handlers = self._handlers
        _handler_id = handler_id if bool(handler_id) else (handler.handler_id if hasattr(handler, "handler_id") else generate_id())
        if _handler_id not in _handlers or overwrite:
            if _handlers:
                _prev_handler = _handlers[-1][1]
                _prev_handler.next_handler(handler)
            _handlers.append((_handler_id, handler))
            return True
        return False

    def remove_handler(self, handler_id):
        _handlers = self._handlers
        _prev_handler_idx, _next_handler_idx = None, None
        for idx, i in enumerate(range(len(_handlers))):
            _handler_id, _handler in _handlers[i]
            if _handler_id == handler_id:
                if idx > 0:
                    _prev_handler_idx, _next_handler_idx = idx - 1, idx + 1
                    _handlers[_prev_handler_idx].next_handler(_handlers[_next_handler_idx])
                return _handlers.pop(idx)
        return None

    def select_handler(self, handler_id):
        _handlers = self._handlers
        for idx, i in enumerate(range(len(_handlers))):
            _handler_id, _ in self._handlers[i]
            if _handler_id == handler_id:
                return _handlers[idx]

    def handle(self, input):
        if self._handlers:
            return self._handlers[0][1].handle(input)
        return False


class ParserSettings:

    def __init__(self, parser=None):
        self._parser = parser
        self._settings = {}

    @property
    def parser(self):
        if not bool(self._parser):
            # TODO: create and raise custom error here
            _error_details = f"unable to access 'parser' as one has not yet been associated with instance of {self.__class__.__name__}..."
            raise AttributeError(_error_details)
        return self._parser

    def set_parser(self, parser):
        self._parser = parser

    def contains(self, setting_key):
        return setting_key in self._settings

    def add_setting(self, setting_key, setting_value, overwrite=False):
        if setting_key not in self._settings or overwrite:
            self._settings[setting_key] = setting_value
            return True
        return False

    def remove_setting(self, setting_key):
        return self._settings.pop(setting_key) if setting_key in self._settings else None

    def get_setting(self, setting_key, default=None):
        return self._settings.get(setting_key, default)


class ParserEvent(PySynchronyEvent):
    pass


class ParserDesign:

    # TODO: create a class representing the context of an input's given parse; this
    #       is to avoid cluttering the 'ParserDesign' namespace, and should provide
    #       better encapsulation, seperations of concerns, and so on. It would also
    #       provide for the ability to add handling different parses from different
    #       inputs/input sources using the same parser and/or the ability to add
    #       undo/redo (or backtracking) operations

    def __init__(self, grammar=None, parse_table=None, parser_id=None):
        self._parser_id = parser_id or generate_id()
        self._grammar = grammar
        self._parse_table = parse_table
        self._stack = None
        self._input_queue = None
        self._validator_chain = None
        self._parser_settings = ParserSettings(self)
        self._channel = PyChannel(channel_id=self.parser_id)        
        self._continue_parsing = False
        self._input_valid = False

    @property
    def parser_id(self):
        return self._parser_id

    @property
    def grammar(self):
        if not bool(self._grammar):
            # TODO: create and raise custom error here
            _error_details = f"unable to access 'grammar' as one has not yet been associated with instance of {self.__class__.__name__}..."
            raise RuntimeError(_error_details)
        return self._grammar

    @property
    def parse_table(self):
        if self._parse_table is None:
            # TODO: create and raise custom error here
            _error_details = f"unable to access 'parse_table' as one has not yet been associated with instance of {self.__class__.__name__}..."
            raise RuntimeError(_error_details)
        return self._parse_table

    @property
    def stack(self):
        if self._stack is None:
            self._stack = self.stack_factory()
        return self._stack

    @property
    def input_queue(self):
        if self._input_queue is None:
            self._input_queue = self.queue_factory()
        return self._input_queue

    @property
    def is_valid(self):
        return bool(self._input_valid)

    def stack_factory(self, *args, **kwargs):
        return deque(*args, **kwargs)

    def queue_factory(self, *args, **kwargs):
        return deque(*args, **kwargs)

    def stack_push(self, element):
        self.stack.append(element)
        return True

    def stack_pop(self):
        return self.stack.pop()

    def stack_top(self):
        return self.stack[-1] if self.stack else None

    def stack_bottom(self):
        return self.stack[0] if self.stack else None

    def queue_extend(self, elements):
        self.input_queue.extend(elements)
        return True

    def enqueue_input(self, element):
        self.input_queue.append(element)
        return True

    def dequeue_input(self):
        return self.input_queue.popleft()

    def queue_peek(self, start=0, stop=None, step=1):
        _input_queue_len = len(self.input_queue)
        _stop = _input_queue_len if (stop is None or stop > _input_queue_len - 1) else stop
        return [self.input_queue[i] for i in range(start, _stop, step)]

    def setting(self, setting_key, default=None):
        return self._parser_settings.get_setting(setting_key, default=default)

    def config(self, setting_key, setting_value, overwrite=False):
        return self._parser_settings.add_setting(setting_key, setting_value, overwrite=overwrite)

    def register(self, event_id, receiver=None, receiver_id=None):
        self._channel.register(event_id, receiver=receiver, receiver_id=receiver_id)

    def set_table(self, parse_table):
        self._parse_table = parse_table

    def input_valid(self, bool_val):
        self._input_valid = bool_val

    def reset(self):
        self._stack = None
        self._input_queue = None
        self._continue_parsing = False
        self._input_valid = False

    def stop(self):
        self._continue_parsing = False

    def action(self, state, symbol):
        _action_search = self._parse_table.action(state, symbol)
        if not bool(_action_search):
            # TODO: create and raise custom error here
            return ParserAction.ERROR, None
        return _action_search

    def init_input(self, input_string):
        self.queue_extend([i for i in input_string])

    def parse(self, input_string):
        self._continue_parsing = True
        # _shifts = 0
        # _reduces = 0
        self.init_input(input_string)
        _input_len = len(self.input_queue)
        
        print(f"QUEUE PEEK: {self.queue_peek()}")
        _init_input = (0, self.queue_peek(0, 1)[0])
        self.stack_push(_init_input)
        _event_counter = 0
        while self.is_valid or True:
            _current_state, _previous_symbol = self.stack_top()
            if self.input_queue:
                _next_symbol = self.dequeue_input()
            print(f"\tSTACK:")
            print(f"\t{self.stack}")
            print()

            _next_action, _next_state = _action = self.action(_current_state, _next_symbol)
            _next_event = ParserEvent(_event_counter, parser=self, current_state=_current_state, next_symbol=_next_symbol, next_action=_next_action, next_state=_next_state, previous_symbol=_previous_symbol)
            self._channel.emit(_next_action, _next_event)
            # if _next_action == ParserAction.SHIFT:
            #     self._channel.emit(ParserAction.SHIFT, _next_event)  # This emits 'SHIFT' event, passing a single argument, the parser itself
            # elif _next_action == ParserAction.ACCEPT:
            #     self._channel.emit(ParserAction.ACCEPT, _next_event)  # This emits 'REDUCE' event, passing a single argument, the parser itself
            # elif _next_action == ParserAction.ERROR:
            #     self._channel.emit(ParserAction.ERROR, _next_event)
            # elif _next_action == ParserAction.REDUCE:
            #     self._channel.emit(ParserAction.REDUCE, _next_event)  # This emits 'REDUCE' event, passing a single argument, the parser itself
            if not self._continue_parsing:
                break
            print(f"\t--------------------")
            print()
            _event_counter += 1
        _input_valid = self.is_valid
        self.reset()
        return _input_valid


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
    parse_table.print()


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
    print(ITEM_STATES_TEXT)
    print()
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


def generate_parse_table(grammar, item_states):
    _parse_table = ParseTable()

    _rules = grammar.rules()
    _init_rule = _rules[0]

    _terminals = grammar.terminals()
    # _non_terminals = grammar.non_terminals()


    # action_table = {}
    # goto_table = {}

    for state, items in item_states.items():
        for item in items:
            next_symbol = item.next_symbol()
            if next_symbol is None:  # Reduce action
                _aug_start_rule_head = _init_rule.rule_head
                if item.rule_head == _aug_start_rule_head:
                    # action_table[(state, _aug_start_rule_head)] = 'accept'
                    _parse_table.add_action(state, _aug_start_rule_head, (ParserAction.ACCEPT, None))
                else:
                    for terminal in _terminals:
                        # action_table[(state, terminal)] = f'reduce {item.rule_id}'
                        _parse_table.add_action(state, terminal, (ParserAction.REDUCE, item.rule_head))
            elif next_symbol in _terminals:
                next_state = find_next_state(item_states, item)
                # action_table[(state, next_symbol)] = f'shift {next_state}'
                _parse_table.add_action(state, next_symbol, (ParserAction.SHIFT, next_state))
            else:
                next_state = find_next_state(item_states, item)
                # goto_table[(state, next_symbol)] = next_state
                _parse_table.add_goto(state, next_symbol, next_state)

    # return action_table, goto_table
    return _parse_table


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
    return parser.parse(source_data)


def parse_and_display(test_data, parser, count=-1):
    print(TEST_PARSING_TEXT)
    print()
    _test_data_queue = deque(test_data)
    _counter = 0
    while _test_data_queue and (_counter < count if (isinstance(count, int) and count > 0) else True):
        _next_test_data_piece = _test_data_queue.popleft()
        _text = underline_text(bold_text(apply_color(11, f"NEXT TEST DATA PIECE"))) + bold_text(" ---> ") + underline_text(bold_text(apply_color(11, f"{_next_test_data_piece}"))) + "\n"
        print(_text)
        _parse_result = parse_data(_next_test_data_piece, parser)
        display_result(_next_test_data_piece, _parse_result)
        for _ in range(2):
            print()
        _counter += 1
    print()


class ParseActionEvents:

    @staticmethod
    def _parser_shift_(event):
        parser = event.data("parser", default=None)
        parser.stack_push((event.data("next_state", default=None), event.data("next_symbol", default=None)))
        print(f"\tSTACK IN SHIFT HANDLER:")
        print(f"\t{parser.stack}")
        if not parser.stack or not parser.input_queue:
            parser.stop()
        print()
        print(f"INPUT QUEUE PEEK:")
        print(parser.queue_peek())

    @staticmethod
    def _parser_reduce_(event):
        parser = event.data("parser", default=None)
        print(f"\tSTACK IN REDUCE HANDLER:")
        print(f"\t{parser.stack}")
        if not parser.stack or not parser.input_queue:
            parser.stop()
        print(f"INPUT QUEUE PEEK:")
        print(parser.queue_peek())

    @staticmethod
    def _parser_error_(event):
        parser = event.data("parser", default=None)
        parser.input_valid(False)
        # _error_details = f"a parsing error occurred; parser has stopped running and will now exit..."
        # raise RuntimeError(_error_details)

    @staticmethod
    def _parser_accept_(event):
        parser = event.data("parser", default=None)
        _text = f"PARSE IS VALID"
        parser.input_valid(True)


def _init_parser_events(parser):

    parser.register(ParserAction.SHIFT, ParseActionEvents._parser_shift_)
    parser.register(ParserAction.REDUCE, ParseActionEvents._parser_reduce_)
    parser.register(ParserAction.ACCEPT, ParseActionEvents._parser_accept_)
    parser.register(ParserAction.ERROR, ParseActionEvents._parser_error_)


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


    # Create parse table, used to guide the LR(0) automaton that makes
    # up the design for the shift/reduce parser
    _parse_table = generate_parse_table(GRAMMAR, _item_states)

    # Display parse table
    # display_table(_parse_table)


    # Instantiate parser back-end (actual parsing implementation)
    # _parser_impl = ShiftReduceParser()
    _parser_impl = ParserDesign()
    _parser_impl.set_table(_parse_table)


    # Initialize parser events
    _init_parser_events(_parser_impl)

    # Instantiate parser front-end (bridge between different parser designs)
    parser = Parser(parser=_parser_impl)


    # Initialize source file object and get data contained within file
    _source_file = SourceFile(path=TEST_INPUT)
    _source_file_data = read_source(_source_file)
    # display_test_data(_source_file_data)
    

    # Parse and display results; once this works, the next step(s) will be to
    # finilize design (implement additional design/concepts as needed), organize
    # 'pyparse' files (taking the concepts contained with this module and the
    # 'scratch' sub-package in general), re-organize git, and then use and see how
    # I can make it better, more robust, etc.
    parse_and_display(_source_file_data, parser, count=1)


if __name__ == "__main__":
    pass
