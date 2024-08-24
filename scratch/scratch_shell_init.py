from pylog import PyLogger, LogType
from pyutils import (
    cmd_argument,
    DEFAULT_PARSER,
    type_conversion,
    NoneTypeConversionCondition
)
from .scratch_package_paths import LOGGING_ROOT
from .scratch_cons import PyParseLoggerID, PyParseLogName


_shell_init_logger = PyLogger.get(PyParseLoggerID.SHELL_INIT)


def _set_logging_level(callback_list):
    _DEFAULT_LEVEL = "INFO"
    DEFAULT_PARSER.register_argument(
        "-logging_level",
        default=_DEFAULT_LEVEL,
        type=str,
        help=f"set's server's logging level; defaults to 'INFO' (as per python's built-in 'logging' module's 'INFO' constant')...",
    )
    _logging_callback = lambda: _shell_init_logger.submit_log(
        message=f"'-logging_level' command-line argument has been registered with the application and is now available for use",
        command=f"-logging_level",
        default=_DEFAULT_LEVEL,
        logger_id=f"{_shell_init_logger.logger_id}",
        help=f"set's server's logging level; defaults to 'INFO' (as per python's built-in 'logging' module's 'INFO' constant')...",
    )
    callback_list.append(_logging_callback)


def _set_logging_dir(callback_list):
    _DEFAULT_LOGGING_FILENAME = str(LOGGING_ROOT)
    DEFAULT_PARSER.register_argument(
        "-logging_dir",
        default=_DEFAULT_LOGGING_FILENAME,
        type=str,
        help=f"set name to use for log file, regardless of selected runtime"
    )
    _logging_callback = lambda: _shell_init_logger.submit_log(
        message=f"'-log_filename' command-line argument has been registered with the application and is now available for use",
        command=f"-log_filename",
        default=_DEFAULT_LOGGING_FILENAME,
        logger_id=f"{_shell_init_logger.logger_id}",
        help=f"set name to use for log file"
    )
    callback_list.append(_logging_callback)


def _set_logging_filename(callback_list):
    _DEFAULT_LOGGING_FILENAME = str(PyParseLogName.SCRATCH_FILENAME)
    DEFAULT_PARSER.register_argument(
        "-log_filename",
        default=_DEFAULT_LOGGING_FILENAME,
        type=str,
        help=f"set name to use for log file, regardless of selected runtime"
    )
    _logging_callback = lambda: _shell_init_logger.submit_log(
        message=f"'-log_filename' command-line argument has been registered with the application and is now available for use",
        command=f"-log_filename",
        default=_DEFAULT_LOGGING_FILENAME,
        logger_id=f"{_shell_init_logger.logger_id}",
        help=f"set name to use for log file"
    )
    callback_list.append(_logging_callback)


def _set_use_logging(callback_list):
    DEFAULT_PARSER.register_argument(
        "-log",
        action="store_true",
        default=False,
        help="When this flag is included, logging commands will run, i.e. if this flag is **NOT** included, then that means application will **NOT** perform associated logging actions"
    )
    _logging_callback = lambda: _shell_init_logger.submit_log(
        message=f"Flag which, when included, will enable logging",
        default=False,
        help=f"Include this flag to enable logging",
        logger_id=f"{_shell_init_logger.logger_id}"
    )
    callback_list.append(_logging_callback)


def initialize_shell():
    _callback_list = []
    _set_use_logging(_callback_list)
    _set_logging_dir(_callback_list)
    _set_logging_filename(_callback_list)
    _set_logging_level(_callback_list)
    return _callback_list


if __name__ == "__main__":
    pass
