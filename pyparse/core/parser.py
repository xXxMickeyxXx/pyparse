from ..library import PyChannel


class Parser:

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


if __name__ == "__main__":
    pass
