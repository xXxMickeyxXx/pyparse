from abc import ABC, abstractmethod


class LexHandler(ABC):

    def __init__(self, tokenizer=None):
        self._tokenizer = tokenizer

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            # TODO: create and raise custom error here
            _error_details = f"unable to access 'tokenizer' property as one has not yet been asociated with this instance of '{self.__class__.__name__}'..."
            raise AttributeError(_error_details)
        return self._tokenizer

    def set_tokenizer(self, tokenizer):
        self._tokenizer = tokenizer

    @abstractmethod
    def handle(self):
        raise NotImplementedError


if __name__ == "__main__":
    pass
