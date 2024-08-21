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


"""
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


if __name__ == "__main__":
    class Handler1(Handler):

        _instances = 0
        _pass = 0

        def __new__(cls, *args, **kwargs):
            _new_cls = super().__new__(cls)
            cls._instances += 1
            return _new_cls

        def __init__(self, stop_text):
            super().__init__(f"{self.__class__.__name__}v{self._instances}")
            self._stop_text = stop_text
            self._first_stop_find = 0

        def handle(self, chain):
            _input = self.input()
            print(f"INPUT:     {_input}")
            print(f"STOP TEXT: {self._stop_text}")
            if _input == self._stop_text:
                if self._pass <= 0:
                    self.__class__._pass += 1
                    print(f"MATCH FOUND HOWEVER ONE MORE CYCLE IS REQUIRED...")
                    return True
                else:
                    print(f"MATCH FOUND WITH {self.handler_id}...STOPPING HANDLER CHAIN...")
                    chain.stop()
            return False


    def test_main():
        _chain = Chain(chain_id="[ • --- TEST_CHAIN_HANDLER --- • ]")
        _chain.add(Handler1("GOODBYE_MOTO!!!"))
        _chain.add(Handler1("!SHIT!"))        
        _chain.add(Handler1("HELLO_MOTO!!!"))
        print()
        _single_input_1 = "GOODBYE_MOTO!!!"
        _single_input_2 = "HELLO_MOTO!!!"
        _single_input_3 = "!SHIT!"
        _chain.handle(_single_input_1)
        print()
        print()
        _chain.handle(_single_input_2)
        print()
        print()
        _chain.handle(_single_input_3)


    test_main()
