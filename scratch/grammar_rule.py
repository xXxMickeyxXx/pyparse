from abc import ABC, abstractmethod
from enum import IntEnum, StrEnum, auto
import copy

from pyparse import (
    TransitionError
)
from pyparse.library import PySignal, PyChannel
from .utils import generate_id, apply_color, underline_text, bold_text, center_text


class GrammarRule:

    """

        #######################################################
        #                                                     #
        # • -------------------- TO-DO -------------------- • #
        #                                                     #
        #######################################################



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

    __slots__ = ("_rule_head", "_rule_body", "_marker_symbol", "_marker_pos", "_augmented_item", "_status", "_can_reduce", "_state_updates", "__advance")

    def __init__(self, rule_head: str, rule_body: list | tuple, marker_symbol: str = "."):
        self._rule_head = rule_head
        self._rule_body = rule_body
        self._marker_symbol = marker_symbol
        self._marker_pos = 0
        self._augmented_item = None
        self._status = None
        self._can_reduce = False
        self.__advance = False
        self._state_updates = 0
        # self.advance_marker()

    @property
    def augmented(self):
        return self._augmented_item is not None

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
    def marker_pos(self):
        return self._marker_pos

    @property
    def can_reduce(self):
        return self._can_reduce

    @property
    def augmented_item(self):
        # NOTE: if the call to 'augment' is removed from rule's '__init__' method
        #       call, then the below muted block needs to be un-muted
        # if self._augmented_item is None:
        #     # TODO: create and raise custom error here, indicating that an augmented item
        #     #       has not yet been producted (via the 'augment' method)
        #     _error_details = f"'{self.__class__.__name__}' has not yet performed it's augmentation; please agument with the 'augment' method and try again..."
        #     raise RuntimeError(_error_details)
        return self._augmented_item

    @property
    def state_updates(self):
        return self._state_updates

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(rule_head={self.rule_head}, rule_body={self.rule_body}, marker_symbol={self.marker_symbol})"

    def __eq__(self, other):
        return self.rule_head == other.rule_head and other.rule_head and self.rule_body == other.rule_body

    def __hash__(self):
        _rule_head_hash = hash(self.rule_head)
        return hash((_rule_head_hash, "".join(self.rule_body)))

    def __len__(self):
        return self.rule_size

    def __iter__(self):
        return self

    def __next__(self):
        # TODO: update as implementation isn't working
        if self.__advance:
            self.advance_marker()
        _state_updates = self.state_updates
        _current_state = self.status()
        if _state_updates == 0:
            self.__advance = True

        print(f"CURRENT STATUS: {_current_state}")
        print(f"RULE SIZE: {len(self)}\nSTATE UPDATES: {self.state_updates}")
        if self.at_end:
            raise StopIteration
        return _current_state

    def _augment_rule(self):
        _rule_body, _marker_symbol = self.rule_body, self.marker_symbol        
        _augmented_rule_lst = [_marker_symbol]
        _augmented_rule_lst.extend(_rule_body)
        return _augmented_rule_lst

    def augment(self):
        self._augmented_item = self._augment_rule()

    def advance_marker(self):
        # if not self.augmented:
        #     self.augment()
        #     return
        # (NOTE: still need to ensure this doesn't mess anything up, logic-wise, as I
        #        just added this as of 2024-06-20 @ 7:17pm EST)
        _at_end = self.at_end
        if not _at_end:        
            if self.rule_size > self.marker_pos:
                _current_pos = self._marker_pos
                self._marker_pos += 1
                _marker_sym = self.augmented_item.pop(_current_pos)
                self.augmented_item.insert(self._marker_pos, _marker_sym)

            if _at_end:
                if not self._can_reduce:
                    self._can_reduce = True
            else:
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
        # TODO: need to test to ensure this works as intended
        _cls_type = type(self)
        return self._deepcopy(_cls_type) if deepcopy else self._copy(_cls_type)
        
    def _copy(self, cls_type):
        _rule_head = copy.copy(self.rule_head)
        _rule_body = copy.copy(self.rule_body)
        _marker_symbol = copy.copy(self.marker_symbol)
        _marker_pos = copy.copy(self.marker_pos)
        _augmented_item = copy.copy(self._augmented_item)
        _can_reduce = copy.copy(self.can_reduce)

        _new_instance = cls_type(_rule_head, _rule_body, marker_symbol=_marker_symbol)
        _new_instance._augmented_item = _augmented_item
        _new_instance._marker_pos = _marker_pos
        _new_instance._can_reduce = _can_reduce
        return _new_instance

    def _deepcopy(self, cls_type):
        _rule_head = copy.deepcopy(self.rule_head)
        _rule_body = copy.deepcopy(self.rule_body)
        _marker_symbol = copy.deepcopy(self.marker_symbol)
        _marker_pos = copy.deepcopy(self.marker_pos)
        _augmented_item = copy.deepcopy(self._augmented_item)
        _can_reduce = copy.deepcopy(self.can_reduce)

        _new_instance = cls_type(_rule_head, _rule_body, marker_symbol=_marker_symbol)
        _new_instance._augmented_item = _augmented_item
        _new_instance._marker_pos = _marker_pos
        _new_instance._can_reduce = _can_reduce
        return _new_instance

    def save(self):
        raise NotImplementedError

    def load_from(self, snapshot):
        raise NotImplementedError


def _main():
    print()
    _copy_1 = GrammarRule("S", ["a", "A"])
    _copy_1.augment()
    _copy_2 = _copy_1.copy()
    # _copy_2 = _copy_1.copy(deepcopy=True)
    print()
    print(f"COPY 1 is COPY 2 ---> {_copy_1 is _copy_2}")
    print(f"COPY 1 == COPY 2 ---> {_copy_1 == _copy_2}")
    print()


if __name__ == "__main__":
    pass
