from abc import ABC, abstractmethod

from .scratch_utils import generate_id


class Handler(ABC):

    def __init__(self, handler_id):
        self._handler_id = handler_id
        self._chain = None

    @property
    def handler_id(self):
        return self._handler_id

    @property
    def chain(self):
        if self._chain is None:
            _error_details = f"unable to access 'chain' property as one has not yet been set for this insnace of '{self.__class__.__name__}' (ID: {self.handler_id})..."
            raise AttributeError(_error_details)
        return self._chain

    def set_chain(self, chain):
        self._chain = chain

    def reset(self):
        self._chain = None

    @abstractmethod
    def handle(self, data):
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

    # def select(self, handler_id):
    #     _handler = None
    #     for _handler_id, _handler_val in self._handlers.items():
    #         if _handler_id == handler_id:
    #             _handler = _handler_val
    #             break
    #     else:
    #         _error_details = f"instance of '{self.__class__.__name__}' does not contain a handler with the ID: {handler_id}; please verify 'handler_id' argument and try again..."
    #     return _handler

    def handle(self, data):
        _retval = {}
        self._continue = True
        for _handler_id, handler in self._handlers.items():
            handler.set_chain(self)
            _retval[_handler_id] = handler.handle(data)
            handler.reset()
            if not self._continue:
                break
        return _retval


if __name__ == "__main__":
    from time import sleep as sleepy

    from pyprofiler import profile_callable, SortBy
    from .scratch_utils import countdown_helper


    class Handler1(Handler):

        _instances = 0

        def __new__(cls, *args, **kwargs):
            _new_cls = super().__new__(cls)
            cls._instances += 1
            return _new_cls

        def __init__(self, stop_text, sleep=False):
            super().__init__(f"{self.__class__.__name__}v{self._instances}")
            self._stop_text = stop_text
            self._sleep = sleep

        def handle(self, data):
            _input = data
            print(f"INPUT:     {_input}")
            print(f"STOP TEXT: {self._stop_text}")
            if _input != self._stop_text:
                print(f"MATCH COULD NOT BE FOUND WITH HANDLER ID: {self.handler_id}...CONINTUING ON...")
            else:
                if self._sleep:
                    print(f"MATCH FOUND WITH {self.handler_id}...STOPPING HANDLER CHAIN IN...")
                    for i in countdown_helper(3):
                        print(f"{i} SECOND(S)")
                        sleepy(1)
                self.chain.stop()
            print()


    @profile_callable(sort_by=SortBy.TIME)
    def test_main():
        _chain = Chain(chain_id="[ • --- TEST_CHAIN_HANDLER --- • ]")
        _chain.add(Handler1("GOODBYE_MOTO!!!"))
        _chain.add(Handler1("!SHIT!", sleep=True))        
        _chain.add(Handler1("HELLO_MOTO!!!"))
        print()
        _single_input_1 = "GOODBYE_MOTO!!!"
        _single_input_2 = "HELLO_MOTO!!!"
        _single_input_3 = "!SHIT!"
        _chain.handle(_single_input_3)
        print()


    test_main()
