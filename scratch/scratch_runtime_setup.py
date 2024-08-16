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
import inspect
from collections import deque, defaultdict
from pathlib import Path

from pylog import PyLogger, LogType
from pyprofiler import profile_callable, SortBy
from pyevent import PyChannels, PyChannel, PySignal

from pyparse import Parser, Tokenizer
from pysynchrony import PySynchronyEventLoop, PySynchronyContext, PySynchronyCoroutineTask, PySynchronyPort, PySynchronyEvent, PySynchronySysCall
from .scratch_parse_table import ParseTable
from .scratch_parse_env import ParseEnvironment
# from .test_automaton_design import Automaton
from .scratch_init_grammar import test_grammar_factory, init_grammar_1, init_grammar_2, init_grammar_3, init_grammar_4, init_grammar_5, init_grammar_6
from .source_descriptor import SourceFile
from .scratch_utils import generate_id, CircularBuffer, copy_items, copy_item
from .utils import apply_color, bold_text, underline_text, center_text
from .scratch_cons import PyParsePortID, PyParseEventID, PyParseLoggerID, ParserActionEnum, GrammarRuleBy, TableConstructionEvent, TEST_INPUT_1, TEST_INPUT_2


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
GRAMMAR = test_grammar_factory()
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


# 'Chain' and 'ParserHandle' implementations
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
"""


class TestGrammar6(Tokenizer):

    # TODO/NOTE: use some sort of chain which has handlers to work with input stream

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


class InputStream:
    """NOTE: will be responsible for actually containing/managing a given input/input
    stream. Each instance of 'ParseContext' will contain an instance of this class."""


class CoreParser2:

    # TODO: definitely need to split this class up into separate components; verify all of the additional overhead is needed as well

    __slots__ = ("_scheduler", "_parser_id", "_grammar", "_parse_table", "_parser_settings", "_init_state", "_state", "_channel", "_logger", "_ports")

    def __init__(self, scheduler, init_state=0, grammar=None, parse_table=None, parser_id=None):
        self._parser_id = parser_id or generate_id()
        self._scheduler = scheduler
        self._grammar = grammar
        self._parse_table = parse_table
        self._parser_settings = ParserSettings(self)
        self._init_state = init_state
        self._state = None
        self._logger = None
        self._ports = {}

    @property
    def parser_id(self):
        return self._parser_id

    @property
    def scheduler(self):
        if self._scheduler is None:
            _error_details = f"unable to access 'scheduler' attribute as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
            raise AttributeError(_error_details)
        return self._scheduler

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
    def init_state(self):
        return self._init_state

    @property
    def logger(self):
        if self._logger is None:
            self._logger = _PARSER_LOGGER
        return self._logger

    def __str__(self):
        return f"{self.__class__.__name__}"

    def set_scheduler(self, scheduler):
        self._scheduler = scheduler

    def setting(self, setting_key, default=None):
        return self._parser_settings.get_setting(setting_key, default=default)

    def config(self, setting_key, setting_value, overwrite=False):
        return self._parser_settings.add_setting(setting_key, setting_value, overwrite=overwrite)

    def set_grammar(self, grammar):
        # TODO: perhaps create and raise custom error here if '_grammar' has already been set
        self._grammar = grammar

    def set_table(self, parse_table):
        # TODO: perhaps create and raise custom error here if '_grammar' has already been set
        self._parse_table = parse_table

    def set_logger(self, logger):
        # TODO: perhaps create and raise custom error here if '_grammar' has already been set
        self._logger = logger

    def create_event(self, event_id, **data):
        return PySynchronyEvent(event_id, **data)

    # TODO: interface should include this as an 'abstractmethod' 
    def parse(self, parse_context):
        # NOTE: passing 'None' argument to the 'event_id' until a consistent one is specified for this implementation/system

        _parse_context = parse_context
        parse_context.append_state(self.init_state)

        _action_search = None
        _previous_action = None
        _action = None
        _previous_symbol = None
        _current_symbol = parse_context.current_symbol()
        _current_state = parse_context.state
        while not parse_context.done_parsing:
            _current_symbol = parse_context.current_symbol()
            _current_state = parse_context.state            

            _action_search = self.action(_current_state, _current_symbol, default=(ParserActionEnum.ERROR, None, None))
            _action = _action_search[0]
            print()
            print(f"STATE STACK: {parse_context.stack}")
            print(f"SYMBOL STACK: {parse_context.symbol_stack}")
            print(f"CURRENT STATE: {_current_state}")
            print(f"CURRENT SYMBOL: {_current_symbol}")
            print(f"PREVIOUS SYMBOL: {_previous_symbol}")
            print(f"ACTION SEARCH: {_action_search}")
            print(f"ACTION: {_action}")
            if _action == ParserActionEnum.SHIFT:
                _next_state_ = _action_search[1]
                _item = _action_search[2]
                parse_context.append_state(_next_state_)
                _previous_symbol = _current_symbol
                parse_context.append_symbol(_current_symbol)
                parse_context.advance()
                print(f"STATE AFTER SHIFT: {parse_context.state}")
            elif _action == ParserActionEnum.REDUCE:
                _item = _action_search[1]
                for _ in range(_item.rule_size):
                    _popped_state = parse_context.pop_state()
                    _popped_symbol = parse_context.pop_symbol()
                _goto_state = self.goto(parse_context.state, _item.rule_head)
                _next_state = _goto_state[0]
                parse_context.append_state(_next_state)
                parse_context.append_symbol(_item.rule_head)
                print(f"ON GOTO IN REDUCE ({parse_context.state}, {_item.rule_head}): {_goto_state}")
            elif _action == ParserActionEnum.ERROR:
                parse_context.set_result(False)
            elif _action == ParserActionEnum.ACCEPT:
                parse_context.set_result(True)
        return _parse_context

    def event_factory(self, event_id, **data):
        return PySynchronyEvent(event_id, **data)

    @staticmethod
    def _default_executor(parser, parse_context):
        print()
        print(f"PARSER ---> {parser}")
        print(f"PARSE CONTEXT ---> {parse_context}")
        print()


class ParseContext:

    def __init__(self, input=None, start_symbol="$"):
        self._input = input
        self._input_len = len(input)
        self._start_symbol = start_symbol
        self._result = None
        self._result_set = False
        self._pointer = 0
        self._state = None
        self._stack = None
        self._symbol_stack = None

    @property
    def input(self):
        if not bool(self._input):
            _error_details = f"input has not yet been set for instance of '{self.__class__.__name__}'..."
            raise RuntimeError(_error_details)
        return self._input

    @property
    def stack(self):
        if self._stack is None:
            self._stack = self.stack_factory()
        return self._stack

    @property
    def symbol_stack(self):
        if self._symbol_stack is None:
            self._symbol_stack = self.stack_factory()
        return self._symbol_stack

    @property
    def can_advance(self):
        return self._pointer < self._input_len

    @property
    def at_end(self):
        return not self.can_advance

    @property
    def state(self):
        return self.stack[-1] if self.stack else None

    @property
    def done_parsing(self):
        return self._result_set and self._result is not None

    def result(self):
        return self._result

    def set_result(self, result):
        if not self._result_set and self._result is None:
            self._result = result
            self._result_set = True

    def append_state(self, element):
        self.stack.append(element)
        self.update(element)

    def pop_state(self):
        _retval = self.stack.pop()
        self.update(self.stack[-1] if self.stack else None)
        return _retval

    def append_symbol(self, element):
        self.symbol_stack.append(element)

    def pop_symbol(self):
        return self.symbol_stack.pop()

    def update(self, state):
        self._state = state

    def stack_factory(self):
        return deque()

    def set_input(self, input):
        if not bool(self._input):
            self._input = input

    def current_symbol(self):
        if self._pointer < self._input_len:
            return self.input[self._pointer]
        return self._start_symbol

    def advance(self):
        if not self.can_advance:
            _error_details = f"unable to consume any further symbols as the end of input has been reached..."
            raise RuntimeError(_error_details)
        self._pointer += 1

    def consume(self):
        if not self.can_advance:
            _error_details = f"unable to consume any further symbols as the end of input has been reached..."
            raise RuntimeError(_error_details)
        _retval = self.current_symbol()
        self.advance()
        return _retval


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
    print(f"ITEM SETS:")
    print()
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


def parse_data(parse_context, parser):
    _parse_context = parser.parse(parse_context)
    print()
    print(f"SYMBOL STACK:")
    print(_parse_context.symbol_stack)
    return _parse_context.result()


# def parse_and_display(test_data, tokenizer, parser, count=-1):
#     _test_data_queue = deque(test_data)
#     _counter = 0
#     while _test_data_queue and (_counter < count if (isinstance(count, int) and count > 0) else True):
#         _next_test_data_piece = _test_data_queue.popleft()
#         # _request_input_tokens = tokenize(_next_test_data_piece, tokenizer)
#         _text = bold_text(apply_color(14, f"NEXT TEST DATA PIECE")) + bold_text(" ---> ") + bold_text(apply_color(14, f"{_next_test_data_piece}"))
#         # _text += bold_text(apply_color(48, f"\nTOKENS"))
#         print()
#         print(_text)
#         # for _token in _request_input_tokens:
#         #     print(f"• {_token}")
#         print()
#         _parse_context = ParseContext(input=_next_test_data_piece, start_symbol="$")
#         _parse_result = parse_data(_parse_context, parser)
#         # _parse_result = parse_data(_request_input_tokens, parser)
#         display_result(_next_test_data_piece, _parse_result)
#         for _ in range(2):
#             print()
#         _counter += 1
#     print()


def parse_and_display(test_data, tokenizer, parser, count=-1):
    _test_data_queue = deque(test_data)
    _counter = 0
    while _test_data_queue and (_counter < count if (isinstance(count, int) and count > 0) else True):
        _next_test_data_piece = _test_data_queue.popleft()
        # _request_input_tokens = tokenize(_next_test_data_piece, tokenizer)
        _text = bold_text(apply_color(14, f"NEXT TEST DATA PIECE")) + bold_text(" ---> ") + bold_text(apply_color(14, f"{_next_test_data_piece}"))
        # _text += bold_text(apply_color(48, f"\nTOKENS"))
        print()
        print(_text)
        # for _token in _request_input_tokens:
        #     print(f"• {_token}")
        print()
        _parse_context = ParseContext(input=_next_test_data_piece, start_symbol="$")
        _parse_result = parse_data(_parse_context, parser)
        # _parse_result = parse_data(_request_input_tokens, parser)
        display_result(_next_test_data_piece, _parse_result)
        for _ in range(2):
            print()
        _counter += 1
    print()


def parse_and_display_custom_input(tokenizer, parser, count=-1):
    _tokenizer = TestGrammar6()
    print(TEST_PARSING_TEXT)
    while True:
        _input = input(">>> ")
        if not _input:
            break
        parse_and_display([_input], tokenizer, parser, count=count)


class Configurator(ABC):

    def init(self, parser):
        raise NotImplementedError


class ParserConfig(Configurator):

    _events_port_id = PyParsePortID.EVENTS
    _actions_port_id = PyParsePortID.ACTIONS
    _executor = None

    def __init__(self):
        self._events_port = None
        self._actions_port = None

    @property
    def events_port(self):
        if self._events_port is None:
            self._events_port = self.create_port(port_id=self._events_port_id)
        return self._events_port

    @property
    def actions_port(self):
        if self._actions_port is None:
            self._actions_port = self.create_port(port_id=self._actions_port_id)
        return self._actions_port

    @classmethod
    def set_executor(cls, executor):
        cls._executor = executor

    def create_port(self, port_id=None):
        return PySynchronyPort(port_id=port_id)

    def init(self, parser):
        parser.add_port(self.actions_port)
        parser.register_handler(self._actions_port_id, self._actions_handler)
        parser.register(PyParseEventID.NEW_ACTION)

    @classmethod
    def _actions_handler(cls, port):
        while port.pending():
            _next_action = port.receive()


    def _emit_event(self, event):
        self.events_port.send(event)


class TestGrammar4ParseEnv(ParseEnvironment):

    def __init__(self, parser=None, grammar=None, tokenizer=None):
        super().__init__(parser=parser)
        self._grammar = grammar
        self._tokenizer = tokenizer

    @property
    def grammar(self):
        if self._grammar is None:
            # TODO: create and raise custom error here
            _error_details = f"unable to access the 'grammar' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
            raise AttributeError(_error_details)
        return self._grammar

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            # TODO: create and raise custom error here
            _error_details = f"unable to access the 'tokenizer' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
            raise AttributeError(_error_details)
        return self._tokenizer

    def set_grammar(self, grammar):
        self._grammar = grammar

    def set_tokenizer(self, tokenizer):
        self._tokenizer = tokenizer

    def parse_mainloop(self, parse_context):
        raise NotImplementedError                


# @profile_callable(sort_by=SortBy.TIME)
def parse_main():
    # Initialize a single parse of a pre-determined and temporarily
    # hard-coded input, following the grammar defined via the
    # current value for the 'GRAMMAR' constant called: the parse
    # environment. Set the grammar via the defacto constructor
    # parameter, 'grammar' (though using 'set_grammar' is just as
    # valid and sometimes preferred)
    _test_grammar_4_env = TestGrammar4ParseEnv(grammar=GRAMMAR)


    # Initialize grammar object so that it contains all grammar rules
    # related to scratch language implementation (refer to top of
    # this module, within the docstring under the
    # '__________SCRATCH GRAMMAR SPEC__________' section for grammar
    # spec)
    # init_grammar_1(GRAMMAR)
    # init_grammar_2(GRAMMAR)
    # init_grammar_3(GRAMMAR)
    init_grammar_4(GRAMMAR)
    # init_grammar_5(GRAMMAR)
    # init_grammar_6(GRAMMAR)


    # Generate (and display) item sets/states then create GOTO and actions
    # mapping which together when combined with an enumeration of the all
    # grammar symbols, build the parse table (which is used to guid the LR(0)
    # automaton component of the shift-reduce parser)
    _item_states = GRAMMAR.generate_states()
    display_item_states(_item_states)


    # Create parse table, used to guide the LR(0) automaton that makes
    # up the design for the shift/reduce parser
    _parse_table = ParseTable(grammar=GRAMMAR, table_id="[ • -- TEST_PARSE_TABLE -- • ]", start_symbol="$")

    # Display parse table
    display_table(_parse_table)


    # Instantiate parser back-end (actual parsing implementation)
    # _parser_impl = CoreParser(init_state=0, grammar=GRAMMAR, parse_table=_parse_table)
    _parser_impl = CoreParser2(init_state=0, grammar=GRAMMAR, parse_table=_parse_table)

    # Set event loop
    _event_loop = PySynchronyEventLoop(loop_id="[ • ---• TEST_PYPARSE_EVENT_LOOP • --- • ]")
    _parser_impl.set_loop(_event_loop)

    # Configure parser and parser events
    _parser_config = ParserConfig()
    _parser_config.init(_parser_impl)


    # _parser_impl.set_table(_parse_table)
    # _parser_impl.set_grammar(GRAMMAR)



    # NOTE: what if I make the abstract component, 'Parser' (which takes a
    #       parser implementation) a sub-class of the 'PySynchronyContext'
    #       implementation, as opposed of the implementation itself?? Worth
    #       thinking about
    # Instantiate parser front-end (bridge between different parser designs)
    _parser = Parser(parser=_parser_impl)

    # Assign the newly created parser to the 'parser' (the highest level parser
    # object) field of the parse environment object, currently defined as
    # '_test_grammar_4_env'
    _test_grammar_4_env.set_parser(_parser)


    # Initialize source file object and get data contained within file
    _source_file = SourceFile(path=TEST_INPUT_1)
    _source_file_data = read_source(_source_file)
    # display_test_data(_source_file_data)


    # Generate tokens to feed the parser
    _tokenizer = TestGrammar6()


    # Set tokenizer to the parse environment (even if it's not ultimately used,
    # initialize the usage of it so that it's easy to hook in)
    _test_grammar_4_env

    # Parse and display results; once this works, the next step(s) will be to
    # finilize design (implement additional design/concepts as needed), organize
    # 'pyparse' files (taking the concepts contained with this module and the
    # 'scratch' sub-package in general), re-organize git, and then use and see how
    # I can make it better, more robust, etc.
    #
    # Pass the parse environment to the newly re-defined 'parse_and display' function
    # to kick off this round of design testing (which will both display some of the
    # debugging info that is currently enabled and display success and/or failure)
    # parse_and_display(_source_file_data, _test_grammar_4_env, count=1)

    parse_and_display(_source_file_data, _tokenizer, _parser, count=1)
    # parse_and_display_custom_input(_tokenizer, _parser)


    # Add white space below final text that displays in order to better separate the text
    # displayed from running this function and the profiler results displaying
    for _ in range(5):
        print()


if __name__ == "__main__":
    pass
