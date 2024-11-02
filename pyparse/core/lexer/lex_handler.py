from abc import ABC, abstractmethod

from ...utils import generate_id


class LexHandler(ABC):

    def __init__(self, handler_id=None):
        self._handler_id = handler_id or generate_id()

    @property
    def handler_id(self):
        return self._handler_id

    @abstractmethod
    def handle(self, tokenizer):
        raise NotImplementedError


if __name__ == "__main__":
    pass
