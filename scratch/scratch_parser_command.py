from abc import ABC, abstractmethod

from .scratch_utils import generate_id


class ParserCommand(ABC):

	def __init__(self, command_id=None):
		self._command_id = command_id if command_id is not None else self.__class__.__name__
		self._fields = {}

	@property
	def command_id(self):
		return self._command_id

	def add_field(self, field_key, field_val, overwrite=True):
		if field_key not in self._fields or overwrite:
			self._fields[field_key] = field_val

	def remove_field(self, field_key):
		if field_key not in self._fields:
			# TODO: create and raise custom error here
			_error_details = f"invalid 'field_key' argument; field key has not yet been associated with this command..."
			raise AttributeError(_error_details)
		return self._fields.pop(field_key)

	def select_field(self, field_key, default=None):
		if field_key not in self._fields:
			_retval = default
		else:
			_retval = self._fields[field_key]
		return _retval

	@abstractmethod
	def execute(self):
		raise NotImplementedError


if __name__ == "__main__":
	pass
