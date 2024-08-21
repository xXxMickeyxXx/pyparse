from enum import StrEnum, IntEnum, auto


class PyParsePortID(IntEnum):

    # INPUT = auto()
    SLEEP = auto()
    READY = auto()
    EVENTS = auto()
    ACTIONS = auto()
    PARSE_REQUEST = auto()


class PyParseEventID(IntEnum):

    # ON_ACTION = auto()
    ON_EVENT = auto()
    ON_QUIT = auto()
    ON_FORCE_QUIT = auto()


class PyParseLoggerID(StrEnum):

    PARSER = auto()
    PARSE_ENV = auto()


class ParserActionState(IntEnum):

    CREATED = auto()
    SCHEDULED = auto()



class ParserActionType(StrEnum):

    ACCEPT = auto()
    ERROR = auto()
    SHIFT = auto()
    REDUCE = auto()


class GrammarRuleBy(IntEnum):

    ID = auto()
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


TEST_INPUT_1 = r"/Users/mickey/Desktop/Python/custom_packages/pyparse/files/data/example_grammar_input_2024_06_13.txt"
TEST_INPUT_2 = r"/Users/mickey/Desktop/Python/custom_packages/pyparse/files/data/example_grammar_input_2024_07_16.txt"


if __name__ == "__main__":
    pass
