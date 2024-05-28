from enum import IntEnum, auto


class ParserAction(IntEnum):

    SHIFT = auto()
    REDUCE = auto()
    ACCEPT = auto()
    FAIL = auto()


if __name__ == "__main__":
    pass
