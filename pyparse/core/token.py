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
    runtime_checkable
)

from ..utils import generate_id
from ..errors import TokenError


class Token(ABC):

    _token_cache = {}

    def __new__(cls, token_type, token_val, token_id=None):
        _token_cache = cls._token_cache
        _cache_key = (token_type, token_val)
        if _cache_key in _token_cache:
            return _token_cache[_cache_key]
        _new_cls = super().__new__(cls)
        _token_cache.update({_cache_key: _new_cls})
        return _new_cls

    def __init__(self, token_type, token_val, token_id=None):
        self._token_id = token_id or generate_id()
        self._token_type = token_type
        self._token_val = token_val

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(token_type={self.token_type}, token_val={self.token_val}, token_id={self.token_id})"

    def __eq__(self, other):
        return isinstance(other, type(self)) and (self.token_type == other.token_type and self.token_val == other.token_val)

    def __hash__(self):
        return hash((self.token_type, self.token_val))

    @property
    def token_id(self):
        return self._token_id

    @property
    def token_type(self):
        return self._token_type

    @property
    def token_val(self):
        return self._token_val

    def copy(self, deepcopy=False):
        raise NotImplementedError


if __name__ == "__main__":
    pass
