from abc import ABC, abstractmethod
from enum import IntEnum, StrEnum, auto
import copy

from pyparse import (
    TransitionError
)
from pyparse.library import PySignal, PyChannel
from .scratch_marker_symbol import MarkerSymbol
from .scratch_augmented_grammar_rule import AugmentedGrammarRule
from .scratch_utils import generate_id
from .utils import underline_text, bold_text, apply_color


class GrammarRule:

    """

        #######################################################
        #                                                     #
        # • -------------------- TO-DO -------------------- • #
        #                                                     #
        #######################################################


    -•- Perhaps utilize the 'flyweight' pattern in order to better manage memory/space
    complexity (though this should not be done until after implementation, testing,
    documentation, benchmarking and pretty much everything else have been completed)
 
    -•- Determine how the rule goes about augmenting item to make it's associated item
    and further, how to initialize it (i.e. call 'advance' once to prime or create an
    'augment' method and call it once to prime)

    -•- Create a new class, 'AugmentedGrammarRule' or 'AugmentedGrammarItem'
    to encapsulate the logic related to grammar rule augmentation; it
    also better separates concerns and responsibilities in the
    overall design. In brainstorming, I could create the class,
    and have that be what's returned when I call the 'augment'
    method (though I'll have to re-instante it, as I deleted the
    method in favor of using only 'advance' to manage augmentation)
    NOTE: current implementation auto primes augmented item by calling
    'advance' within objects '__init__' method (as well as when calling
    'reset')

    -•- Possibly add descriptors to this implementation so that
    constraints can be enforced (e.g. making sure that the
    rule body contains a list of 0 or more single/individual
    symbols/characters, which make up the whole of the rule body
    such as:)

    -•- Have this item be what's added to the 'Grammar' object as a rule
    (see 'TODO' directly below about using a 'GrammarRules' object
    as the container which these 'GrammarRule' instances are added
    to)

    -•- Possibly create another class, 'GrammarRules' which represents a
    collection of rules, and THAT is what these 'GrammarRule' instances
    are added to, then the grammar can have an instance of 'GrammarRules'
    which could be copied as desired

    """

    __slots__ = ("_rule_head", "_rule_body", "_marker_symbol", "_marker_pos", "_augmented_item", "_status", "_can_reduce", "_track_goto", "_goto", "_rule_id", "_augmented", "_current_state", "__at_end", "__at_beginning")

    def __init__(self, rule_head: str, rule_body: list | tuple, marker_symbol: MarkerSymbol | None = None, rule_id=None):
        self._rule_id = rule_id or generate_id()
        self._rule_head = rule_head
        self._rule_body = rule_body
        self._marker_symbol = marker_symbol or MarkerSymbol("•")
        self._marker_pos = 0
        self._augmented_item = None
        self._augmented = False
        self._status = None
        self._current_state = None
        self.__at_end = False
        self.__at_beginning = False

    @property
    def rule_id(self):
        return self._rule_id

    @property
    def augmented(self):
        return self._augmented

    @property
    def rule_head(self):
        return self._rule_head

    @property
    def rule_body(self):
        return self._rule_body

    @property
    def rule_size(self):
        return len(self.rule_body)

    @property
    def marker_symbol(self):
        return self._marker_symbol

    @property
    def at_end(self):
        return self.augmented_item[-1] == self.marker_symbol

    @property
    def at_start(self):
        return self.augmented_item[0] == self.marker_symbol

    @property
    def marker_pos(self):
        return self._marker_pos

    @property
    def can_reduce(self):
        return self.at_end is True

    @property
    def augmented_item(self):
        if self._augmented_item is None:
            self._augment_rule()
        return self._augmented_item

    @property
    def current_state(self):
        if self._current_state is None:
            # TODO: create and raise custom error here
            _error_details = f"unable to access current state as it has not yet been set..."
            raise RuntimeError(_error_details)
        return self._current_state

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(rule_head={self.rule_head}, rule_body={self.rule_body}, marker_symbol={self.marker_symbol})"

    def __eq__(self, other):
        # return isinstance(self, type(other)) and (self.rule_id == other.rule_id and self.rule_body == other.rule_body)  # NOTE: this is how 'GrammarRule' should identify equality
        return isinstance(self, type(other)) and (self.rule_id == other.rule_id and self.status() == other.status())  # NOTE: this is how 'AugmentedGrammarRule' or 'AugmentedItem' should handle equality

    def __hash__(self):
        # return hash((self.rule_id, "".join(self.rule_body)))  # NOTE: this is how 'GrammarRule' should handle hashing
        return hash((self.rule_id, tuple(self.status())))  # NOTE: this is how 'AugmentedGrammarRule' or 'AugmentedItem' should handle hashing

    def __len__(self):
        return self.rule_size

    def __iter__(self):
        return self

    def __next__(self):
        if self.__at_end:
            self.reset()
            raise StopIteration
        if self.at_end:
            self.__at_end = True
        _item_copy = self.copy()
        _retval = _item_copy.status()
        self.advance()
        return _retval

    def update_state(self, state):
        _prev_state, self._current_state = self._current_state, state
        return _prev_state

    def augmented_item_factory(self):
        # TODO: replace 'GrammarRule' logic relating to augmentation with
        #       'AugmenteGrammarRule' (which may be called something different
        #       by the time this 'TODO' is handled)
        return AugmentedGrammarRule(self)

    def next_symbol(self, default=None):
        _look_ahead = self.look_ahead()
        return _look_ahead[0] if _look_ahead else default

    def _augment_rule(self):
        if self._augmented_item is None:
            _rule_body, _marker_symbol = self.rule_body, self.marker_symbol        
            _augmented_rule_lst = [_marker_symbol]
            _augmented_rule_lst.extend(_rule_body)
            self._augmented_item = _augmented_rule_lst
            self._augmented = True

    def advance(self):
        _at_end = self.at_end
        if not _at_end:        
            if self.rule_size > self.marker_pos:
                _current_pos = self._marker_pos
                self._marker_pos += 1
                _marker_sym = self.augmented_item.pop(_current_pos)
                self.augmented_item.insert(self._marker_pos, _marker_sym)
        return self.status()

    def reverse(self):
        if self.marker_pos > 0:
            _current_pos = self._marker_pos
            self._marker_pos -= 1
            _marker_sym = self.augmented_item.pop(_current_pos)
            self.augmented_item.insert(self._marker_pos, _marker_sym)

    def status(self):
        return self.augmented_item

    def look_behind(self):
        _at_start = self.at_start
        if _at_start:
            return []
        return self.augmented_item[:self._marker_pos]

    def look_ahead(self):
        _right_of_lst = []
        _at_end = self.at_end
        if _at_end:
            return _right_of_lst
        return self.augmented_item[self._marker_pos + 1:]

    def copy(self, *, deepcopy=False):
        _cls_type = type(self)
        return self._deepcopy(_cls_type) if deepcopy else self._copy(_cls_type)
        
    def _copy(self, cls_type):
        _rule_head = copy.copy(self.rule_head)
        _rule_body = copy.copy(self.rule_body)
        _marker_symbol = copy.copy(self.marker_symbol)
        _marker_pos = copy.copy(self.marker_pos)
        _augmented_item = copy.copy(self._augmented_item)
        _rule_id = copy.copy(self.rule_id)

        _new_instance = cls_type(_rule_head, _rule_body, marker_symbol=_marker_symbol)
        _new_instance._augmented_item = _augmented_item
        _new_instance._marker_pos = _marker_pos
        _new_instance._rule_id = _rule_id
        return _new_instance

    def _deepcopy(self, cls_type):
        _rule_head = copy.deepcopy(self.rule_head)
        _rule_body = copy.deepcopy(self.rule_body)
        _marker_symbol = copy.deepcopy(self.marker_symbol)
        _marker_pos = copy.deepcopy(self.marker_pos)
        _augmented_item = copy.deepcopy(self._augmented_item)
        _rule_id = copy.deepcopy(self.rule_id)

        _new_instance = cls_type(_rule_head, _rule_body, marker_symbol=_marker_symbol)
        _new_instance._augmented_item = _augmented_item
        _new_instance._marker_pos = _marker_pos
        _new_instance._rule_id = _rule_id
        return _new_instance

    def reset(self):
        self._marker_pos = 0
        self._augmented_item = None
        self._augmented = False
        self._status = None
        self._can_reduce = False
        self.__at_end = False
        self.__at_beginning = False
        # self._state_updates = 0

    def save(self):
        raise NotImplementedError

    def load_from(self, snapshot):
        raise NotImplementedError


def _grammar_rule_main():
    print()
    test_rule = GrammarRule("S", ["T", "i", "l", "l", "y"])
    _test_rule_2 = test_rule.copy()
    test_rule.advance()
    _test_rule_2.advance()

    print(test_rule == _test_rule_2)
    print(hash(test_rule) == hash(_test_rule_2))


if __name__ == "__main__":
    _grammar_rule_main()
