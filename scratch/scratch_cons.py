from enum import StrEnum, IntEnum, auto


class ParserAction(IntEnum):

    ACCEPT = auto()
    ERROR = auto()
    SHIFT = auto()
    REDUCE = auto()
    UPDATE = auto()


class  GrammarRuleBy(IntEnum):

    HEAD = auto()
    BODY = auto()


class FileDescriptorMode(StrEnum):

    # Reading related modes
    READ = "r"  # NOTE: file must exist
    READ_BIN = "rb"  # NOTE: file must exist
    READ_WRITE = "r+"  # NOTE: file must exist
    READ_WRITE_BIN = "rb+"  # NOTE: file must exist

    # Writing related modes
    WRITE = "w"  # NOTE: create new file if not exists or truncate existing one
    WRITE_BIN = "wb"  # NOTE: create new file if not exists or truncate existing one
    WRITE_READ = "w+"  # NOTE: create new file if not exists or truncate existing one
    WRITE_READ_BIN = "wb+"  # NOTE: create new file if not exists or truncate existing one

    # TODO: implement remaining file descriptor modes
    # Appending related modes


class TableConstructionEvent(StrEnum):

    INIT_I0 = auto()
    UPDATE_STATES = auto()
    UPDATE_GOTO_MAPPING = auto()


TEST_INPUT = r"/Users/mickey/Desktop/Python/custom_packages/pyparse/files/data/example_grammar_input_2024_06_13.txt"


if __name__ == "__main__":
    pass
