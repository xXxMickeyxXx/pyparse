from pylog import PyLogger, LogType
from pyutils import (
    cmd_argument,
    DEFAULT_PARSER,
    type_conversion,
    NoneTypeConversionCondition
)
from .scratch_package_paths import LOGGING_ROOT
from .scratch_cons import (
    LanguageType,
    SimpleLangVersion,
    DateLangVersion,
    PyParseLoggerID,
    PyParseLogName
)


_shell_init_logger = PyLogger.get(PyParseLoggerID.SHELL_INIT)
_callback_list = []
_lang_versions = {
    LanguageType.SIMPLE_LANG: SimpleLangVersion.V0_0_1,
    LanguageType.DATE_LANG: DateLangVersion.V0_0_1
}

_simple_lang_version = f"{str(LanguageType.SIMPLE_LANG)}_{_lang_versions[LanguageType.SIMPLE_LANG]}"
_date_lang_version = f"{str(LanguageType.DATE_LANG)}_{_lang_versions[LanguageType.DATE_LANG]}"


def _set_logging_level(logger=_shell_init_logger):
    _DEFAULT_LEVEL = "INFO"
    DEFAULT_PARSER.register_argument(
        "-logging_level",
        default=_DEFAULT_LEVEL,
        type=str,
        help=f"set's server's logging level; defaults to 'INFO' (as per python's built-in 'logging' module's 'INFO' constant')...",
    )
    _callback_list.append(lambda: logger.submit_log(
            message=f"'-logging_level' command-line argument has been registered with the application and is now available for use",
            command=f"-logging_level",
            default=_DEFAULT_LEVEL,
            version=str(version),
            logger_id=f"{logger.logger_id}",
            help=f"set's server's logging level; defaults to 'INFO' (as per python's built-in 'logging' module's 'INFO' constant')...",
        ))
    _callback_list.append


def _set_logging_dir(logger=_shell_init_logger):
    _DEFAULT_LOGGING_FILENAME = str(LOGGING_ROOT)
    DEFAULT_PARSER.register_argument(
        "-logging_dir",
        default=_DEFAULT_LOGGING_FILENAME,
        type=str,
        help=f"set name to use for log file, regardless of selected runtime"
    )
    _callback_list.append(lambda: logger.submit_log(
        message=f"'-log_filename' command-line argument has been registered with the application and is now available for use",
        command=f"-log_filename",
        default=_DEFAULT_LOGGING_FILENAME,
        version=str(version),
        logger_id=f"{logger.logger_id}",
        help=f"set name to use for log file"
    ))


def _set_logging_filename(logger=_shell_init_logger):
    _DEFAULT_LOGGING_FILENAME = str(PyParseLogName.SCRATCH_FILENAME)
    DEFAULT_PARSER.register_argument(
        "-log_filename",
        default=_DEFAULT_LOGGING_FILENAME,
        type=str,
        help=f"set name to use for log file, regardless of selected runtime"
    )
    _callback_list.append(lambda: logger.submit_log(
        message=f"'-log_filename' command-line argument has been registered with the application and is now available for use",
        command=f"-log_filename",
        default=_DEFAULT_LOGGING_FILENAME,
        version=str(version),
        logger_id=f"{logger.logger_id}",
        help=f"set name to use for log file"
    ))


def _set_use_logging(logger=_shell_init_logger):
    DEFAULT_PARSER.register_argument(
        "-log",
        action="store_true",
        default=False,
        help="When this flag is included, logging commands will run, i.e. if this flag is **NOT** included, then that means application will **NOT** perform associated logging actions"
    )
    _callback_list.append(lambda: logger.submit_log(
        message=f"Flag which, when included, will enable logging",
        default=False,
        version=str(version),
        help=f"Include this flag to enable logging",
        logger_id=f"{logger.logger_id}"
    ))


def _set_use_debugger(logger=_shell_init_logger):
    DEFAULT_PARSER.register_argument(
        "-debug_mode",
        action="store_true",
        default=False,
        help="When this flag is included, debug statements and actions will run application-wide, i.e. if this flag is **NOT** included, then that means application will **NOT** perform associated application-wide debug statements and actions"
    )
    _callback_list.append(lambda: logger.submit_log(
        message=f"Flag which, when included, will enable application-wide debugging",
        default=False,
        version=str(version),
        help=f"Include this flag to enable application-wide debugging",
        logger_id=f"{logger.logger_id}"
    ))


def _run_date_lang_testing(version="date_lang_v0_0_1", logger=_shell_init_logger):
    DEFAULT_PARSER.register_argument(
        "-date_lang",
        action="store_true",
        default=False,
        help="When this flag is included, the testing logic associated with the 'DateLang' language will run."
    )
    _callback_list.append(lambda: logger.submit_log(
        message=f"Flag which, when included, will run the testing logic associated with the 'DateLang' language.",
        default=False,
        version=str(version),
        help=f"Include this flag to run testing logic associated with the 'DateLang' language",
        logger_id=f"{logger.logger_id}"
    ))


def _run_simple_lang_testing(version="simple_lang_v0_0_1", logger=_shell_init_logger):
    DEFAULT_PARSER.register_argument(
        "-simple_lang",
        action="store_true",
        default=False,
        help="When this flag is included, the testing logic associated with the 'SimpleLang' language will run."
    )
    _callback_list.append(lambda: logger.submit_log(
        message=f"Flag which, when included, will run the testing logic associated with the 'SimpleLang' language.",
        default=False,
        version=str(version),
        help=f"Include this flag to run testing logic associated with the 'SimpleLang' language",
        logger_id=f"{logger.logger_id}"
    ))


def initialize_shell(logger=_shell_init_logger, version=""):
    _set_use_logging(logger=logger)
    _set_logging_dir(logger=logger)
    _set_logging_filename(logger=logger)
    _set_logging_level(logger=logger)
    _set_use_debugger(logger=logger)
    match version:
        case _simple_lang_version:
            _run_simple_lang_testing(version=version, logger=logger)
        case _date_lang_version:
            _run_date_lang_testing(version=version, logger=logger)
    return _callback_list


if __name__ == "__main__":
    pass
