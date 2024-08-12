from abc import ABC, abstractmethod

from pylog import PyLogger, LogType
from pyevent import PyChannels, PyChannel, PySignal

from .scratch_cons import PyParseLoggerID
from .scratch_utils import generate_id, CircularBuffer, copy_items, copy_item


_parse_env_default_logger = PyLogger.get(PyParseLoggerID.PARSE_ENV)


class ParseEnvironment(ABC):

	def __init__(self, parser=None):
		self._parser = parser

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
	def parse_mainloop(self, parse_context):
		raise NotImplementedError


if __name__ == "__main__":
	pass
