from abc import ABC, abstractmethod

from .scratch_utils import generate_id


class Handler(ABC):

    def __init__(self, handler_id):
        self._handler_id = handler_id
        self._input = None
        self._input_set = False

    @property
    def handler_id(self):
        return self._handler_id

    def input(self):
        if not self._input_set:
            # TODO: create and raise custom error here
            _error_details = f"unable to access 'input' as it does not yet exists within instance of '{self.__class__.__name__}'; via the 'set_input' method, please set input before making another attempt to retrieve field (NOTE: 'inpu't field and it's lifecycle are automatically managed when passing as an argument to instance's 'handle' method)"
            raise AttributeError(_error_details)
        return self._input

    def set_input(self, input):
        self._input = input
        self._input_set = True

    def reset(self):
        self._input = None
        self._input_set = False

    @abstractmethod
    def handle(self, chain):
        raise NotImplementedError


class Chain:

    def __init__(self, chain_id=None):
        self._chain_id = chain_id or generate_id()
        self._handlers = {}
        self._continue = True

    @property
    def chain_id(self):
        return self._chain_id

    def stop(self):
        self._continue = False

    def add(self, handler, overwrite=False):
        _handler_id = handler.handler_id
        if _handler_id not in self._handlers or overwrite:
            self._handlers[_handler_id] = handler
            return True
        return False

    def remove(self, handler_id):
        _removed_handler = self._handlers.get(handler_id, False)
        if not _removed_handler:
            # TODO: create and raise custom error here
            _error_details = f"invalid 'handler_id' argument; handler_id: {handler_id} does not exists within instance of '{self.__class__.__name__}'..."
            raise KeyError(_error_details)

    def select(self, handler_id):
        _handler = None
        for _handler_id, _handler_val in self._handlers.items():
            if _handler_id == handler_id:
                _handler = _handler_val
                break
        else:
            _error_details = f"instance of '{self.__class__.__name__}' does not contain a handler with the ID: {handler_id}; please verify 'handler_id' argument and try again..."
        return _handler

    def handle(self, input):
        _retval = {}
        self._continue = True
        for _handler_id, handler in self._handlers.items():
            print(f"HANDLER ID: {handler.handler_id} IN chain's 'handle' method")
            handler.set_input(input)
            _retval[_handler_id] = handler.handle(self)
            handler.reset()
            if not self._continue:
                break
        return _retval


if __name__ == "__main__":
    pass
