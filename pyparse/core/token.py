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

from ..utils import generate_id
from ..errors import TokenError


class Token:

    def __init__(self, name, value=None):
        self._name = name
        self._value = value
        self._value_set = not (self._value is None)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        _error_details = f"unable to update token's 'name' attribute, once object has established it (via instantiation)..."
        raise TokenError(details=_error_details)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        _error_details = f"unable to assign token's 'value' attribute using dot notation (i.e. using {self.__class__.__name__}.value); please use the 'set_value' method to set or update..."
        raise TokenError(details=_error_details)

    def set_value(self, val):
        if self._value_set or self._value is not None:
            _error_details = f"token's 'value' attribute is immutable, once it has been established; create new token instance to use value..."
            raise TokenError(details=_error_details)
        self._value = val
        self._value_set = True

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.name == other.name and self.value == other.value)


if __name__ == "__main__":
    pass
