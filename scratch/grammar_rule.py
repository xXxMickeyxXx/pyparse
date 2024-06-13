from abc import ABC, abstractmethod
from enum import IntEnum, StrEnum, auto
import copy

from pyparse import (
    TransitionError
)
from pyparse.library import PySignal, PyChannel
from .utils import generate_id, apply_color, underline_text, bold_text, center_text


class GrammarRule:

    # TODO: possibly make into python 'descriptor' (eithe a 'data descriptor' or
    #       a 'non-data descriptor')

    # TODO: possibly add ability to save/load state and copy/deepcopy the object

    # TODO: have this item be what's added to the 'Grammar' object as a rule



    def __init__(self, rule_head: str, rule_body: list | tuple, marker_symbol: str = "."):
        self._rule_head = rule_head
        self._rule_body = rule_body
        self._marker_symbol = marker_symbol
        self._marker_pos = 0
        self._augmented_item = None
        self._status = None
        self._can_reduce = False

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
        if self._augmented_item is None:
            # TODO: create and raise custom error here, indicating that an augmented item
            #       has not yet been producted (via the 'augment' method)
            _error_details = f"'{self.__class__.__name__}' has not yet performed it's augmentation; please agument with the 'augment' method and try again..."
            raise RuntimeError(_error_details)
        return self._augmented_item

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self._augmented_item is None:
            return f"RULE HEAD ---> {self.rule_head}\nRULE BODY ---> {self.rule_body}\nSTATUS ---> None"
        return f"RULE HEAD ---> {self.rule_head}\nRULE BODY ---> {self.rule_body}\nSTATUS ---> {self.augmented_item}"

    def __eq__(self, other):
        # TODO: update so that this logic makes sense as it relates to this
        #       implementation (making sure to take into account the ability
        #       to 'copy')

        return True if self.rule_head == other.rule_head and self.rule_body == other.rule_body else False

    def _augment_rule(self):
        _rule_body, _marker_symbol = self.rule_body, self.marker_symbol        
        _augmented_rule_lst = [_marker_symbol]
        _augmented_rule_lst.extend(_rule_body)
        return _augmented_rule_lst

    def augment(self):
        self._augmented_item = self._augment_rule()

    def advance_marker(self):
        if self.rule_size > self.marker_pos:
            _current_pos = self._marker_pos
            self._marker_pos += 1
            _marker_sym = self.augmented_item.pop(_current_pos)
            self.augmented_item.insert(self._marker_pos, _marker_sym)

        if self.at_end and not self._can_reduce:
            self._can_reduce = True

    def status(self):
        return self.augmented_item

    def look_ahead(self):
        _left_of_lst = []
        if self._marker_pos > 0:
            _left_of_lst = self.augmented_item[:self._marker_pos]
        return _left_of_lst

    def look_behind(self):
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
