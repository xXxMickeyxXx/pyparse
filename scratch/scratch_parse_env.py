from abc import ABC, abstractmethod

from pylog import PyLogger, LogType

from .scratch_cons import PyParseLoggerID
from .scratch_utils import generate_id


_parse_env_default_logger = PyLogger.get(PyParseLoggerID.PARSE_ENV)


class ParserEnvironment(ABC):

	def __init__(self, parser=None, env_id=None):
		self._env_id = env_id or generate_id()
		self._parser = parser

	@property
	def env_id(self):
		return self._env_id

	@property
	def parser(self):
		if self._parser is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access the 'parser' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._parser

	def set_parser(self, parser):
		self._parser = parser

	@abstractmethod
	def run(self):
		raise NotImplementedError


if __name__ == "__main__":
	pass
