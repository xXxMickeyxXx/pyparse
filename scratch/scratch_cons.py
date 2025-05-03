from pathlib import Path
from enum import StrEnum, IntEnum, auto


class LanguageType(StrEnum):

    SIMPLE_LANG = "SIMPLE_LANG"
    DATE_LANG = "DATE_LANG"
    TODO_LANG = "TODO_LANG"


class SimpleLangVersion(StrEnum):

    V0_0_1 = "v0_0_1"


class DateLangVersion(StrEnum):

    V0_0_1 = "v0_0_1"


class ToDoLangVersion(StrEnum):

    V0_0_1 = "v0_0_1"


# class PyParsePortID(IntEnum):

#     # INPUT = auto()
#     SLEEP = auto()
#     READY = auto()
#     EVENTS = auto()
#     ACTIONS = auto()
#     COMMANDS = auto()


# class PyParseEventID(IntEnum):

#     # ON_ACTION = auto()
#     ON_EVENT = auto()
#     ON_QUIT = auto()
#     ON_FORCE_QUIT = auto()


# class PyParseLoggerID(StrEnum):

#     PARSER = auto()
#     PARSE_ENV = auto()
#     RUNTIME = auto()
#     SHELL_INIT = auto()
#     LOGGING_INIT = auto()
#     FINAL_REDESIGN = auto()


# class ParserActionState(IntEnum):

#     CREATED = auto()
#     SCHEDULED = auto()
#     STAGED = auto()
#     EXECUTING = auto()
#     AWAITING = auto()
#     SLEEPING = auto()
#     FINISHED = auto()


# @NOTE<Remove references to this 'StrEnum' and instead use the desired value directly>
class ParserActionType(StrEnum):

    ACCEPT = auto()
    ERROR = auto()
    SHIFT = auto()
    REDUCE = auto()


# @NOTE<Remove references to this 'StrEnum' and instead use the desired value directly>
class GrammarRuleBy(IntEnum):

    # TODO: determine what this will be used for, as it's currently a vestiage of
    #       a past concept.

    ID = auto()
    HEAD = auto()
    BODY = auto()
    STATUS = auto()


# class FileDescriptorMode(StrEnum):

#     # @TODO<Implement remaining file descriptor modes>

#     # Reading related modes
#     READ = "r"  # NOTE: file must exist
#     READ_BIN = "rb"  # NOTE: file must exist
#     READ_WRITE = "r+"  # NOTE: file must exist
#     READ_WRITE_BIN = "rb+"  # NOTE: file must exist

#     # Writing related modes
#     WRITE = "w"  # NOTE: create new file if not exists or truncate existing one
#     WRITE_BIN = "wb"  # NOTE: create new file if not exists or truncate existing one
#     WRITE_READ = "w+"  # NOTE: create new file if not exists or truncate existing one
#     WRITE_READ_BIN = "wb+"  # NOTE: create new file if not exists or truncate existing one


class __PyParseFileSystemPaths:

    __slots__ = ("__root", "__files", "__logging", "__scratch")

    def __init__(self):
        self.__root = ""
        self.__files = ""
        self.__logging = ""
        self.__scratch = ""

    @property
    def ROOT(self):
        if not self.__root:
            self.__root = str(Path("../pyparse").resolve())
        return self.__root

    @property
    def FILES(self):
        if not self.__files:
            self.__files = str(self.ROOT / Path("files"))
        return self.__files

    @property
    def LOGGING(self):
        if not self.__logging:
            self.__logging = str(self.FILES / Path("logging"))
        return self.__logging

    @property
    def SCRATCH(self):
        if not self.__scratch:
            self.__scratch = str(self.ROOT / Path("scratch"))
        return self.__scratch


PyParseFileSystemPath = __PyParseFileSystemPaths()


if __name__ == "__main__":
    pass
