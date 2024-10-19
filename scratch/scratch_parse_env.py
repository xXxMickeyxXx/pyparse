from abc import ABC, abstractmethod

from pylog import PyLogger, LogType

from .scratch_cons import PyParseLoggerID
from .scratch_utils import generate_id


_parse_env_default_logger = PyLogger.get(PyParseLoggerID.PARSE_ENV)


class ParserEnvironment(ABC):

	def __init__(self, parser=None, grammar=None, env_id=None):
		self._env_id = env_id or generate_id()
		self._fields = {}
		self._parser = parser
		self._grammar = grammar

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

	@property
	def grammar(self):
		if self._grammar is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access the 'grammar' field as one has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._grammar

	def set_parser(self, parser):
		self._parser = parser

	def set_grammar(self, grammar):
		self._grammar = grammar

		self._fields = {}

	def add_field(self, field_key, field_val, overwrite=True):
		if field_key not in self._fields or overwrite:
			self._fields[field_key] = field_val
			return True
		return False

	def remove_field(self, field_key):
		if field_key not in self._fields:
			# TODO: create and raise custom error here
			_error_details = f"invalid 'field_key' argument; field key has not yet been associated with this command..."
			raise AttributeError(_error_details)
		return self._fields.pop(field_key)

	def field(self, field_key, default=None):
		if field_key not in self._fields:
			_retval = default
		else:
			_retval = self._fields[field_key]
		return _retval

	@abstractmethod
	def execute(self, *args, **kwargs):
		raise NotImplementedError


if __name__ == "__main__":
	pass
