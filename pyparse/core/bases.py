from abc import ABC, abstractmethod
from typing import (
    Protocol,
    Callable,
    Union,
    Any,
    List,
    Dict,
    Tuple,
    LiteralString,
    Type,
    Optional,
    runtime_checkable,
)


"""


    ###################################################
    #                                                 #
    # • --------------- TO-DO TASKS --------------- • #
    #                                                 #
    ###################################################


         ---------------------------
        | • ------- INPUT ------- • |
         ---------------------------

            - Create 'Tokens'

                • Represents a known piece of an overall input


            - Create 'Tokenizer'


            - Create 'Parser'

            - Create Component/Composite Tree

                • Represents all of the parts and levels that come together
                    to build an object, which has meaning, action, interaction,
                    reaction, etc.

                • Utilize builders for fiscilitating


         ----------------------------
        | • ------- OUTPUT ------- • |
         ----------------------------
        
            - 


"""

from functools import cached_property

from ....library import generate_id, PyRegistry, PyChannel
from ._request_obj import Request
from ....utils import apply_color, underline_text, bold_text, center_text


# TODO: recreate some of the 'quick-n-diry' implementations contained in this
#       module so that they are more object oriented


# Token Types
METHOD = 'METHOD'
PATH = 'PATH'
HTTP_VERSION = 'HTTP_VERSION'
HEADER_NAME = 'HEADER_NAME'
HEADER_VALUE = 'HEADER_VALUE'
CRLF = 'CRLF'
BODY = 'BODY'


class ShiftReduceParser:

    def __init__(self, grammar=None, end_match="request"):
        self._grammar = grammar
        self.stack = []
        self.end_match = end_match
        self._tokens = None
        self._get_grammar = None
        self._actions = None

    @property
    def grammar(self):
        if self._grammar is None or not self._grammar:
            _error_details = f"'grammar' have not yet been associated with this object; please set them either during object's instantiation ('__init__') or using the 'set_grammar' setter method"
            raise ValueError(_error_details)
        return self._grammar

    @property
    def tokens(self):
        return self._tokens

    @property
    def actions(self):
        if self._actions is None:
            self._actions = self.actions_factory()
        return self._actions

    def register_action(self, rule, action, action_id=None):
        self.actions.register(rule, action, receiver_id=action_id)

    def remove_action(self, rule, action_id=None):
        if action_id is None:
            _retval = self.actions.remove(rule)
        else:
            _action_signal = self.actions.select(rule)
            _retval = _action_signal.remove(action_id)
        return _retval

    def actions_factory(self):
        return PyChannel()

    def get_grammar(self):
        if self._get_grammar is None:
            self._get_grammar = self.grammar.get_grammar()
        return self._get_grammar

    def reset(self):
        self._tokens = None
        self.stack = []
        self._get_grammar = None

    def set_grammar(self, grammar):
        self._grammar = grammar

    def stack_peek(self, index=-1):
        if self.stack:
            return self.stack[index]
        return None

    def pop_stack(self, index=-1):
        if self.stack:
            return self.stack.pop(index)
        return None

    def token_peek(self, index=-1):
        if self.tokens:
            return self.tokens[index]
        return None

    def pop_token(self, index=-1):
        return self.tokens.pop(index)

    def shift(self):
        if self.tokens:
            token_type, token_value = self.pop_token(0)
            self.stack.append((token_type, token_value))
        else:
            self.raise_error()

    def raise_error(self, error=Exception, error_text="Unexpected end of input"):
        raise error(error_text)

    def can_reduce(self):
        for prod_rule, match_cases in self.get_grammar():
            if len(match_cases) <= len(self.stack) and [i[0] for i in self.stack[-len(match_cases):][0:]] == match_cases:
                return prod_rule, match_cases
        return False

    def reduce(self, matched_grammar):
        production_rule, match_cases = matched_grammar
        _matched_tokens = [self.pop_stack() for i in match_cases][::-1]
        self.actions.signal(production_rule, _matched_tokens)
        self.stack.append((production_rule, match_cases))

    def parse(self, tokens):
        self._tokens = tokens
        while self.tokens:
            potential_prod_rules = self.can_reduce()
            if potential_prod_rules:
                self.reduce(potential_prod_rules)
                continue
            self.shift()

        _potential_prod_rules = self.can_reduce()
        while _potential_prod_rules:
            self.reduce(_potential_prod_rules)
            _potential_prod_rules = self.can_reduce()

        _end_stack_pop = self.pop_stack(index=-1)
        if self.end_match == (_end_stack_pop[0] if _end_stack_pop else None):
            _retval = True
        else:
            _retval = False
        self.reset()
        return _retval


# Tokenizer Function (Assuming a simple tokenizer for demonstration)
def tokenize(input_string):
    tokens = []
    lines = input_string.splitlines()
    _headers_done = False
    _body_done = False

    for line in lines:
        if line.startswith('GET'):
            tokens.append(('METHOD', 'GET'))
            tokens.append(('PATH', line.split()[1]))
            tokens.append(('HTTP_VERSION', line.split()[-1]))
        elif line.startswith("POST"):
            tokens.append(('METHOD', 'POST'))
            tokens.append(('PATH', line.split()[1]))
            tokens.append(('HTTP_VERSION', line.split()[-1]))
        elif ": " in line and not _headers_done:
            _split_line = line.split(": ")
            tokens.append(("HEADER_NAME", _split_line[0]))
            tokens.append(("HEADER_VALUE", _split_line[1]))
        elif ":" in line and not _headers_done:
            _split_line = line.split(":")
            tokens.append(("HEADER_NAME", _split_line[0]))
            tokens.append(("HEADER_VALUE", _split_line[1]))
        elif line == "":
            if not _headers_done:
                tokens.append(('CRLF', ''))
                _headers_done = True
        else:
            if _headers_done:
                tokens.append(('BODY', line))
    return tokens


class Grammar:

    # TODO: update this class to be more of a container for grammar, allowing the 
    #       parser to more easily interact with the rules it uses to parse.

    # TODO/NOTE: should separate a callable that acts on the parser, closer to a 'rule'
    #            and then have the grammar be able to add 'action' callables, which can
    #            be used to build a structure, based on whatever is happening during
    #            parsing (such as building a request object for use in application
    #            code/for building some sort of composite/etc.). Should also create
    #            a way to associate an action for with a rule or many rules (i.e. a
    #            one-to-many relationship or a many-many relationship)

    def __init__(self, grammar_id=None):
        self._grammar_id = grammar_id or generate_id()
        self._rules = []

    @property
    def grammar_id(self):
        return self._grammar_id

    def add_rule(self, non_terminal, rule):
        _new_rule = [non_terminal, rule]
        self._rules.append(_new_rule)

    def get_grammar(self):
        return self._rules


# Productions/Grammar-Rules
productions_list = [
    ("request", ["request", "BODY"]),
    ('request', ["request_line", 'headers', "CRLF", 'BODY']),
    ('request', ["request_line", 'headers', "CRLF"]),
    ('request', ["request_line", 'header', "CRLF", 'BODY']),
    ('request', ["request_line", "CRLF", "BODY"]),
    ('request', ["request_line", "headers", "CRLF", "BODY"]),
    ('request', ["request_line", "header", "CRLF"]),
    ("request", ["request_line", "CRLF"]),
    ("request_line", ["METHOD", "PATH", "HTTP_VERSION"]),
    ("headers", ["headers", "header"]),
    ("headers", ["header"]),
    ("headers", ["header", "header"]),
    ('header', ['HEADER_NAME', 'HEADER_VALUE'])
]


def http_grammar_factory():
    _http_grammar = Grammar(grammar_id="HTTP_GRAMMAR")  # TODO: create a 'HTTP_GRAMMAR' enum
    _http_grammar.add_rule("request", ["request_line", 'headers', "CRLF", 'BODY'])
    _http_grammar.add_rule("request", ["request_line", 'headers', "CRLF"])
    _http_grammar.add_rule("request", ["request_line", 'header', "CRLF", 'BODY'])
    _http_grammar.add_rule("request", ["request_line", "CRLF", "BODY"])
    _http_grammar.add_rule("request", ["request_line", "header", "CRLF"])
    _http_grammar.add_rule("request", ["request_line", "CRLF"])
    _http_grammar.add_rule("request_line", ["METHOD", "PATH", "HTTP_VERSION"])
    _http_grammar.add_rule("headers", ["headers", "header"])
    _http_grammar.add_rule("headers", ["header"])
    _http_grammar.add_rule("headers", ["header", "header"])
    _http_grammar.add_rule("header", ['HEADER_NAME', 'HEADER_VALUE'])
    return _http_grammar


def http_parser_factory():
    _grammar = http_grammar_factory()
    return ShiftReduceParser(grammar=_grammar, end_match="request")


def http_request_is_valid(raw_request, parser):
    _tokens = tokenize(raw_request)
    return parser.parse(_tokens)


# # NOTE: Register closure to allow parser, and it's action, to interact with
# #       request object
# def register_action(request_obj, action):
#     def _handle_action(matched_tokens):
#         return action(matched_tokens, request=request_obj)
#     return _handle_action


# # NOTE: request line action
# def _request_line_action(matched_tokens, request=None):
#     print(f"HAPPENING WITHIN THE '_request_line_action' FUNCTION")
#     _request_obj_not_None = request is not None
#     print(f"REQUEST IS NOT NONE WITHIN THE '_request_line_action' FUNCTION ---> {_request_obj_not_None}")
#     for i in matched_tokens:
#         if _request_obj_not_None:
#             request.add(i[0].lower(), i[1], overwrite=False)


# # NOTE: request action (specifically for one that includes a request body)
# def _request_body_action(matched_tokens, request=None):
#     _request_obj_not_None = request is not None
#     for i in matched_tokens:
#         if _request_obj_not_None and i[0] == "BODY":
#             request.add(i[0].lower(), i[1], overwrite=False)
#             break


# # TODO: make it so that a request object can be copied every time a request
# #       is made, only passing to it 'extrinsic' state, unique to that specific
# #       occurrence; when the function is called, the request object is copied,
# #       it's extrinsic state is passed, and it's parsed as it usually is. This
# #       happens every request (i.e. every time the 'get_http_request' function
# #       is called)
# # REQUEST = Request()
# def get_http_request(raw_request):
#     # _request_obj = REQUEST.copy()
#     _request_obj = Request()
#     _parser = http_parser_factory()

#     _parser.register_action("request_line", register_action(_request_obj, _request_line_action))
#     _parser.register_action("request", register_action(_request_body_action, _request_body_action))
#     _http_request_valid = http_request_is_valid(raw_request, _parser)
#     if _http_request_valid:
#         return _request_obj
#     return False


# NOTE: register actions, via closures, within the main 'get_http_request'
#       function
def get_http_request(raw_request):
    _request_obj = Request()
    _parser = http_parser_factory()


    def _request_line_action_closure(matched_tokens):
        for i in matched_tokens:
            _request_obj.add(i[0].lower(), i[1], overwrite=False)


    # NOTE: request action (specifically for one that includes a request body)
    def _request_body_action_closure(matched_tokens):
        for i in matched_tokens:
            if i[0] == "BODY":
                _request_obj.add(i[0].lower(), i[1], overwrite=False)
                break


    _parser.register_action("request_line", _request_line_action_closure)
    _parser.register_action("request", _request_body_action_closure)
    _http_request_valid = http_request_is_valid(raw_request, _parser)
    if _http_request_valid:
        return _request_obj
    return False


if __name__ == "__main__":
    pass


if __name__ == "__main__":
    pass
