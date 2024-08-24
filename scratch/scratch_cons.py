from enum import StrEnum, IntEnum, auto


class PyParseLogName(StrEnum):

    SCRATCH_FILENAME = "scratch_logfile.log"


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
    RUNTIME = auto()
    SHELL_INIT = auto()
    LOGGING_INIT = auto()


class ParserActionState(IntEnum):

    CREATED = auto()
    SCHEDULED = auto()
    STAGED = auto()
    EXECUTING = auto()
    AWAITING = auto()
    SLEEPING = auto()
    FINISHED = auto()


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


if __name__ == "__main__":
    pass
