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

from abc import ABC, abstractmethod
from collections import deque, defaultdict
from pathlib import Path

from pylog import PyLogger, LogType
from pyprofiler import profile_callable, SortBy
from pyevent import PyChannels, PyChannel, PySignal

from pyparse import Parser, Tokenizer
from pysynchrony import PySynchronyEvent, PySynchronyContext
from .scratch_parse_table import ParseTable
from .test_automaton_design import Automaton
from .scratch_init_grammar import grammar_factory, init_grammar_1, init_grammar_2, init_grammar_3, init_grammar_4, init_grammar_5, init_grammar_6
from .source_descriptor import SourceFile
from .scratch_utils import generate_id, CircularBuffer, copy_items, copy_item
from .utils import apply_color, bold_text, underline_text, center_text
from .scratch_cons import PyParseLoggerID, ParserAction, GrammarRuleBy, TableConstructionEvent, TEST_INPUT


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


_PARSER_LOGGER = PyLogger.get(PyParseLoggerID.PARSER)
GRAMMAR = grammar_factory()
GRAMMAR_RULES = GRAMMAR.rules()
NON_TERMINALS = GRAMMAR.non_terminals()
TERMINALS = GRAMMAR.terminals()
SYMBOLS = NON_TERMINALS + TERMINALS



ITEM_STATES_TEXT = apply_color(200, """
#########################################################################################################################
#                                                                                                                       #
# • -------------------------------------------------- ITEM STATES -------------------------------------------------- • #
#                                                                                                                       #
#########################################################################################################################
""")


TEST_PARSING_TEXT = apply_color(200, """
##########################################################################################################################
#                                                                                                                        #
# • -------------------------------------------------- TEST PARSING -------------------------------------------------- • #
#                                                                                                                        #
##########################################################################################################################
""")


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


class ParserHandle:

    __slots__ = ("_state", "_parser", "_context_id", "_stack", "_input_pointer")

    def __init__(self, init_state=None, parser=None, context_id=None):
        self._state = init_state
        self._parser = parser
        self._context_id = context_id or generate_id()
        self._stack = None
        self._input_pointer = 0

    @property
    def init_state(self):
        return self._init_state

    @property
    def parser(self):
        return self._parser

    @property
    def context_id(self):
        return self._context_id

    @property
    def stack(self):
        return self._stack

    def add_listener(self, receiver, receiver_id=None, overwrite=False):
        self.signal.register(receiver, receiver_id=receiver_id, overwrite=overwrite)
        return True

    def remove_listener(self, receiver_id):
        return self.signal.remove(receiver_id)

    def state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def stack_factory(self):
        return deque()

    def set_parser(self, parser):
        if self._parser is not None:
            # TODO: create and raise custom error here
            _error_details = f"unable to set parser as one has already been associated with instance of {self.__class__.__name__}..."
            raise RuntimeError(_error_details)
        self._parser = parser

    def save(self, parser):
        raise NotImplementedError

    def restore(self, parser):
        raise NotImplementedError


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


class ParserEvent:

    # NOTE: this is the implementation of 'PySynchronyEvent'; redefined it here
    #       to allow to ensure it uses '__slots__" and doesn't have a "__dict__"
    #       attribute

    __slots__ = ("_event_id", "_data")

    def __init__(self, event_id=None, **data):
        self._event_id = event_id or generate_id()
        self._data = {k: v for k, v in data.items()}

    @property
    def event_id(self):
        return self._event_id

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(event_id={self.event_id}, {', '.join([f'{k}={v}' for k, v in self._data.items()])})"

    def add_data(self, key, value, overwrite=False):
        if key not in self._data or overwrite:
            self._data.update({key: value})
        elif key in self._data and not overwrite:
            # TODO: create and raise custom error here
            _error_details = f"unable to add data using the key: {key} to value: {value} relationship, as it already exists within this object; update 'overwrite' kwarg to receive 'True' (initializes to 'False')..."
            raise KeyError(_error_details)
        else:
            # TODO: create and raise custom error here
            _error_details = f"an error occurred when attempting to add data using the 'add_data' method on instance of the '{self.__class__.__name__}' class; please review and then try again..."

    def remove_data(self, key, pop=True):
        _retval = None
        if pop:
            _retval = self.pop_data(key)
        else:
            del self._data[key]
        return _retval

    def pop_data(self, key):
        return self._data.pop(key)

    def data(self, key, default=None):
        if key not in self._data:
            retval = default
        else:
            retval = self._data[key]
        return retval


class TestGrammar6(Tokenizer):

    def __init__(self, input=None):
        super().__init__(input=input)
        self.on_loop(self._tokenize)
        self._valid_symbols = SYMBOLS

    def _tokenize(self):
        if not self.can_consume:
            self.quit()
            return

        _next_token = None
        _next_char = self.consume()
        if _next_char in {" ", "\r\n", "\r", "\n", "\t"}:
            return
        elif _next_char == "i":
            _expected_d = self.consume()
            if _expected_d:
                _next_char += _expected_d
                _next_token = ("id", _next_char)
                self.push_token(_next_token)
            else:
                print(f"ACTUAL VALUE OF EXPECTED VALUE @ RUNTIME ERROR ---> {_expected_d}")
                _error_details = f"unable to tokenize; expected 'd' after encountering an 'i'..."
                raise RuntimeError(_error_details)

        elif _next_char == "+":
            _next_token = ("PLUS", _next_char)
            self.push_token(_next_token)
        elif _next_char == "*":
            _next_token = ("MULTIPLY", _next_char)
            self.push_token(_next_token)
        elif _next_char == "-":
            _next_token = ("MINUS", _next_char)
            self.push_token(_next_token)
        else:
            _error_details = f"error tokenizing input on character: '{_next_char}'..."
            raise RuntimeError(_error_details)


class CoreParser:

    # TODO: create a class representing the context of an input's given parse; this
    #       is to avoid cluttering the 'CoreParser' namespace, and should provide
    #       better encapsulation, seperations of concerns, and so on. It would also
    #       provide for the ability to add handling different parses from different
    #       inputs/input sources using the same parser and/or the ability to add
    #       undo/redo (or backtracking) operations

    __slots__ = ("_parser_id", "_grammar", "_parse_table", "_parser_settings", "_channel", "_logger", "_init_state", "_state")

    def __init__(self, init_state=0, grammar=None, parse_table=None, parser_id=None):
        self._parser_id = parser_id or generate_id()
        self._grammar = grammar
        self._parse_table = parse_table
        self._parser_settings = ParserSettings(self)
        self._init_state = init_state
        self._state = None
        self._channel = None
        self._logger = None

    # TODO: interface should include (as 'NotImplementedError' until implemented)
    @property
    def parser_id(self):
        return self._parser_id

    # TODO: interface should include (as 'NotImplementedError' until implemented)
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

    # TODO: interface should include (as 'NotImplementedError' until implemented)
    @property
    def init_state(self):
        return self._init_state

    @property
    def channel(self):
        if self._channel is None:
            self._channel = PyChannel(channel_id=self.parser_id)
        return self._channel

    @property
    def logger(self):
        if self._logger is None:
            self._logger = _PARSER_LOGGER
        return self._logger

    def __str__(self):
        return f"{self.__class__.__name__}"

    # TODO: interface should include this as an 'abstractmethod' 
    def register(self, signal_id, receiver=None, receiver_id=None):
        return self.channel.register(signal_id, receiver=receiver, receiver_id=receiver_id)

    # TODO: interface should include this as an 'abstractmethod' 
    def setting(self, setting_key, default=None):
        return self._parser_settings.get_setting(setting_key, default=default)

    # TODO: interface should include this as an 'abstractmethod' 
    def config(self, setting_key, setting_value, overwrite=False):
        return self._parser_settings.add_setting(setting_key, setting_value, overwrite=overwrite)

    # TODO: interface should include this as an 'abstractmethod' 
    def set_grammar(self, grammar):
        # TODO: perhaps create and raise custom error here if '_grammar' has already been set
        self._grammar = grammar

    def set_table(self, parse_table):
        # TODO: perhaps create and raise custom error here if '_grammar' has already been set
        self._parse_table = parse_table

    # TODO: interface should include this as an 'abstractmethod' 
    def set_logger(self, logger):
        # TODO: perhaps create and raise custom error here if '_grammar' has already been set
        self._logger = logger

    # TODO: interface should include this as an 'abstractmethod' 
    def state(self):
        # NOTE: this could be an abstract method for a 'Parser' interface/base class
        # return self.stack_top() or ()
        return self._state

    # TODO: interface should include this as an 'abstractmethod' 
    def update_state(self, state):
        # TODO: determine how this can/should be used
        # NOTE: this could be an abstract method for a 'Parser' interface/base class
        self._state = state
        self.channel.emit(ParserAction.UPDATE, self)

    # TODO: interface should include this as an 'abstractmethod' 
    def stack_factory(self, *args, **kwargs):
        return deque(*args, **kwargs)

    # TODO: interface should include this as an 'abstractmethod' 
    def action(self, state, symbol, default=None):
        return self._parse_table.action(state, symbol, default=default)

    # TODO: interface should include this as an 'abstractmethod' 
    def goto(self, state, non_terminal, default=None):
        _goto_state = self._parse_table.goto(state, non_terminal, default=default)
        return _goto_state

    # TODO: interface should include this as an 'abstractmethod' 
    def parse(self, input):
        """
        @NOTE: need to make it so that I can have '_next_symbol' be either 'None' or
               use some default value (such as '$') (in order to do this, I may have to break
               out of the first, top-level loop, then go into another 'while' loop that
               reduces until a reduction can no longer occur, so maybe there's always two
               while loops, with one being an inner while loop to the top-level while loop,
               or maybe two different top-level while loops, one after the other).
               Basically, I want to be able to use the 'ParseAction.ERROR' and
               'ParAction.ACCEPT', because as it stands right now, I can't due to how the
               parser works with the next symbol being 'None' or a default value
               (such as '$') when it reaches the end of the input (i.e. the input pointer
               reaches the length of input minus 1, or the last index of the input
               list/array/container/whatever)

        """

        # input += "$"
        _input_pointer = 0
        _input_len = len(input)
        _pointer_max = _input_len - 1
        _end_of_input = False
        _state_stack = self.stack_factory()
        _state_stack.append(self.init_state)
        self.update_state(_state_stack[-1])
        _next_symbol = input[_input_pointer][1]
        _parser_action = self.action(self.state(), _next_symbol, default=None)
        _action = _parser_action[0] if _parser_action else ParserAction.ERROR
        while not _end_of_input:
            print()
            print(f"MAINLOOP TOP:")
            print()
            print(f"STATE STACK: {_state_stack}")
            print(f"INPUT LENGTH: {_input_len}")
            print(f"NEXT SYMBOL: {_next_symbol}")
            print(f"POINTER AT: {_input_pointer} (POINTER MAX: {_pointer_max})")
            print(f"AT END OF INPUT: {_end_of_input is True}")
            print(f"CURRENT STATE: {self.state()}")
            print(f"PARSER ACTION: {_parser_action}")
            print(f"ACTION: {_action}")
            print()

            # NOTE: perhaps this goes at the bottom of the loop; that way we can avoid
            #       another cycle if input parse is valid (or not valid)
            if _action == ParserAction.SHIFT:
                _next_ = _parser_action[1]
                _item = _parser_action[2]
                _state_stack.append(_next_)
                self.update_state(_next_)
                # NOTE: may need to re-add that 'else' block to make sure the '_end_of_input' gets set
                if _pointer_max > _input_pointer:
                    _input_pointer += 1
                    _next_symbol = input[_input_pointer][1]
                    if _input_pointer == _pointer_max:
                        _end_of_input = True
            elif _action == ParserAction.REDUCE:
                _item = _parser_action[1]
                for _ in range(_item.rule_size):
                    _state_stack.pop()
                    self.update_state(_state_stack[-1] if _state_stack else None)
                _next_ = self.goto(self.state(), _item.rule_head, default=None)
                print(f"GOTO: {_next_}")
                _state_stack.append(_next_[0])
                self.update_state(_state_stack[-1] if _state_stack else None)
            elif _action == ParserAction.ERROR:
                print()
                print()
                print(f"STATE STACK @ ERROR: {_state_stack}")
                print(f"INPUT LENGTH @ ERROR: {_input_len}")
                print(f"NEXT SYMBOL @ ERROR: {_next_symbol}")
                print(f"POINTER AT @ ERROR: {_input_pointer} (POINTER MAX: {_pointer_max})")
                print(f"AT END OF INPUT @ ERROR: {_end_of_input is True}")
                print(f"CURRENT STATE @ ERROR: {self.state()}")
                print(f"PARSER ACTION @ ERROR: {_parser_action}")
                print(f"ACTION @ ERROR: {repr(_action)}")
                print()
                print()
                break
            elif _action == ParserAction.ACCEPT:
                return True

            _parser_action = self.action(self.state(), _next_symbol, default=None)
            _action = _parser_action[0] if _parser_action else ParserAction.ERROR


            # # TODO: this part of the method isn't correct; once all the input is read, an
            # #       additional 'while' loop will need to run, attempting to reduce further
            # if self.state() == 1 and _end_of_input:
            #     return True

        # print(f"HERE @ break")
        # print(f"CURRENT STATE @ break: {self.state()}")
        # print(f"NEXT SYMBOL @ break: {_next_symbol}")
        _top_level_rule_head = self.grammar.init_symbol
        _parser_action = self.action(self.state(), _next_symbol, default=(ParserAction.ERROR,))
        _action = _parser_action[0]
        _continue = True
        while _continue:
            _continue = False
            print()
            print(f"2nd MAINLOOP TOP:")
            print()
            print(f"STATE STACK: {_state_stack}")
            print(f"INPUT LENGTH: {_input_len}")
            print(f"NEXT SYMBOL: {_next_symbol}")
            print(f"POINTER AT: {_input_pointer} (POINTER MAX: {_pointer_max})")
            print(f"AT END OF INPUT: {_end_of_input is True}")
            print(f"CURRENT STATE: {self.state()}")
            print(f"PARSER ACTION: {_parser_action}")
            print(f"ACTION: {_action}")

            if _action == ParserAction.REDUCE:
                _item = _parser_action[1]
                for _ in range(_item.rule_size):
                    _state_stack.pop()
                    self.update_state(_state_stack[-1] if _state_stack else None)
                _next_ = self.goto(self.state(), _item.rule_head, default=None)
                _state_stack.append(_next_[0])
                self.update_state(_state_stack[-1] if _state_stack else None)
                _continue = True

            _parser_action = self.action(self.state(), _next_symbol, default=(ParserAction.ERROR,))
            _action = _parser_action[0]
        _next_symbol = _top_level_rule_head
        _parser_action = self.action(self.state(), _next_symbol, default=(ParserAction.ERROR,))
        _action = _parser_action[0]
        print(f"ACTION AT VERY END: {_action}")
        return _action == ParserAction.ACCEPT


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


def tokenize(input, tokenizer):
    tokenizer.set_input(input)
    _tokens = tokenizer.tokenize()
    tokenizer.reset()
    return _tokens


def parse_data(source_data, parser):
    return parser.parse(source_data)


def parse_and_display(test_data, tokenizer, parser, count=-1):
    print(TEST_PARSING_TEXT)
    _test_data_queue = deque(test_data)
    _counter = 0
    while _test_data_queue and (_counter < count if (isinstance(count, int) and count > 0) else True):
        _next_test_data_piece = _test_data_queue.popleft()
        _request_input_tokens = tokenize(_next_test_data_piece, tokenizer)
        _text = bold_text(apply_color(14, f"NEXT TEST DATA PIECE")) + bold_text(" ---> ") + bold_text(apply_color(14, f"{_next_test_data_piece}")) + bold_text(apply_color(48, f"\nTOKENS"))
        # _parse_result = parse_data(_next_test_data_piece, parser)
        _parse_result = parse_data(_request_input_tokens, parser)
        print(_text)
        for _token in _request_input_tokens:
            print(f"• {_token}")
        print()
        display_result(_next_test_data_piece, _parse_result)
        for _ in range(2):
            print()
        _counter += 1
    print()


class ParserActionEvents(ABC):

    def init_events(self, parser):
        raise NotImplementedError


class TestParserActionEvents(ParserActionEvents):

    def init_events(self, parser):
        parser.register(ParserAction.SHIFT, self._parser_shift_)
        parser.register(ParserAction.REDUCE, self._parser_reduce_)
        parser.register(ParserAction.ACCEPT, self._parser_accept_)
        parser.register(ParserAction.ERROR, self._parser_error_)
        parser.register(ParserAction.UPDATE, self._parser_update_)        

    @staticmethod
    def _parser_shift_(handle):
        pass

    @staticmethod
    def _parser_reduce_(handle):
        pass

    @staticmethod
    def _parser_error_(handle):
        pass

    @staticmethod
    def _parser_accept_(handle):
        pass

    @staticmethod
    def _parser_update_(parser):
        print()
        print(bold_text(apply_color(214, f" • --- UPDATING PARSER --- • ")))
        print(bold_text(apply_color(214, f"\t{parser.state()}")))
        print()


# @profile_callable(sort_by=SortBy.TIME)
def parse_main():
    # Initialize grammar object so that it contains all grammar rules
    # related to scratch language implementation (refer to top of
    # this module, within the docstring under the
    # '__________SCRATCH GRAMMAR SPEC__________' section for grammar
    # spec)
    # init_grammar_1(GRAMMAR)
    # init_grammar_2(GRAMMAR)
    # init_grammar_3(GRAMMAR)
    # init_grammar_4(GRAMMAR)
    # init_grammar_5(GRAMMAR)
    init_grammar_6(GRAMMAR)


    # Generate (and display) item sets/states then create GOTO and actions
    # mapping which together when combined with an enumeration of the all
    # grammar symbols, build the parse table (which is used to guid the LR(0)
    # automaton component of the shift-reduce parser)
    _item_states = GRAMMAR.generate_states()
    display_item_states(_item_states)


    # Create parse table, used to guide the LR(0) automaton that makes
    # up the design for the shift/reduce parser
    _parse_table = ParseTable(grammar=GRAMMAR, table_id="[ • -- TEST_PARSE_TABLE -- • ]")

    # Display parse table
    display_table(_parse_table)


    # Instantiate parser back-end (actual parsing implementation)
    _parser_impl = CoreParser(init_state=0, grammar=GRAMMAR, parse_table=_parse_table)
    # _parser_impl.set_table(_parse_table)
    # _parser_impl.set_grammar(GRAMMAR)


    # Initialize parser events
    # _parser_events = TestParserActionEvents()
    # _parser_events.init_events(_parser_impl)
    _parser_impl.register(ParserAction.UPDATE, TestParserActionEvents._parser_update_)

    # Instantiate parser front-end (bridge between different parser designs)
    _parser = Parser(parser=_parser_impl)


    # Initialize source file object and get data contained within file
    _source_file = SourceFile(path=TEST_INPUT)
    _source_file_data = read_source(_source_file)
    # display_test_data(_source_file_data)


    # Generate tokens to feed the parser
    _tokenizer = TestGrammar6()
    

    # Parse and display results; once this works, the next step(s) will be to
    # finilize design (implement additional design/concepts as needed), organize
    # 'pyparse' files (taking the concepts contained with this module and the
    # 'scratch' sub-package in general), re-organize git, and then use and see how
    # I can make it better, more robust, etc.
    parse_and_display(_source_file_data, _tokenizer, _parser, count=-1)


if __name__ == "__main__":
    pass
