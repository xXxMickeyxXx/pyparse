from pyutils import (
    cmd_argument,
    DEFAULT_PARSER,
    type_conversion,
    NoneTypeConversionCondition
)
from pylog import PyLogger, LogType
from .scratch_package_paths import (
    LOGGING_ROOT
)
from .scratch_cons import PyParseLoggerID, PyParseLogName


_logging_init_logger = PyLogger.get(PyParseLoggerID.LOGGING_INIT)


def init_logging(*args, use_logging=True, logging_callbacks=None, **kwargs):
    """CURRENT POSSIBLE PARAMETERS:
            (NOTE: command line args assigned with anything other than 'None' are their default values)

    • logging_level: LogType | INT | STR = INFO
    • overwrite: bool = True
    """

    if use_logging:
        _updated_kwargs = {
            "logging_dir": (
                str(kwargs.pop("logging_dir"))
                if "logging_dir" in kwargs
                else str(LOGGING_ROOT)
            ),
            "log_filename": (
                str(kwargs.pop("log_filename"))
                if "log_filename" in kwargs
                else str(PyParseLogName.SCRATCH_FILENAME)
            ),
            **kwargs,
        }

    if use_logging:
        PyLogger.config(*args, **_updated_kwargs)
        _updated_kwargs_for_logging = f", ".join(
            {f"{k}={v}" for k, v in _updated_kwargs.items()}
        )
        _logging_init_logger.submit_log(
            message=f"Logging has been setup and initialized...",
            logger_id=f"{_logging_init_logger.logger_id}",
        )
        _logging_callbacks = [] if (logging_callbacks is None or not logging_callbacks) else logging_callbacks
        for logging_callback in _logging_callbacks:
            logging_callback()


if __name__ == "__main__":
    pass
