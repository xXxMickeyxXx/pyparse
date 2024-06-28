from abc import ABC, abstractmethod
from enum import IntEnum, StrEnum, auto
import copy

from pyparse import (
    TransitionError
)
from pyparse.library import PySignal, PyChannel
from .scratch_utils import generate_id


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

    __slots__ = ("_rule_head", "_rule_body", "_marker_symbol", "_marker_pos", "_augmented_item", "_status", "_can_reduce", "_state_updates", "_track_goto", "_goto", "_rule_id", "_augmented")

    def __init__(self, rule_head: str, rule_body: list | tuple, marker_symbol: str = ".", rule_id=None):
        self._rule_id = rule_id or generate_id()
        self._rule_head = rule_head
        self._rule_body = rule_body
        self._marker_symbol = marker_symbol
        self._marker_pos = 0
        self._augmented_item = None
        self._augmented = False
        self._status = None
        self._state_updates = 0

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
        return self.state_updates == self.rule_size

    @property
    def marker_pos(self):
        return self._marker_pos

    @property
    def can_reduce(self):
        return self.at_end is True

    @property
    def augmented_item(self):
        if self._augmented_item is None:
            # # TODO: create and raise custom error here
            # _error_details = f"unable to acces 'augmented_item'; must prime augmentation via the 'advance' method..."
            # raise RuntimeError(_error_details)
            self._augment_rule()
        return self._augmented_item

    @property
    def state_updates(self):
        return self._state_updates

    def goto(self):
        raise NotImplementedError

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(rule_head={self.rule_head}, rule_body={self.rule_body}, marker_symbol={self.marker_symbol})"

    def __eq__(self, other):
        return self.rule_id == other.rule_id and (self.rule_head == other.rule_head) and (self.status() == other.status())

    # def __hash__(self):
    #     return hash(self.rule_id)

    def __len__(self):
        return self.rule_size

    # def __iter__(self):
    #     return self

    # def __next__(self):
    #     pass

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
                self._state_updates += 1

    def status(self):
        return self.augmented_item

    def look_behind(self):
        _left_of_lst = []
        if self._marker_pos > 0:
            _left_of_lst = self.augmented_item[:self._marker_pos]
        return _left_of_lst

    def look_ahead(self):
        _right_of_lst = []
        if not self.at_end:
            _right_of_lst = self.augmented_item[self._marker_pos + 1:]
        return _right_of_lst

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
        self._state_updates = 0

    def save(self):
        raise NotImplementedError

    def load_from(self, snapshot):
        raise NotImplementedError


def _main():
    print()
    _copy_1 = GrammarRule("S", ["a", "A"])
    _copy_1.advance()
    _copy_2 = _copy_1.copy()
    # _copy_2 = _copy_1.copy(deepcopy=True)
    print()
    print(f"COPY 1 is COPY 2 ---> {_copy_1 is _copy_2}")
    print(f"COPY 1 == COPY 2 ---> {_copy_1 == _copy_2}")
    print()


if __name__ == "__main__":
    pass
