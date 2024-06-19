from pathlib import Path
from collections import deque
from io import (
	StringIO,
	BytesIO,
	BufferedReader,
	BufferedWriter
)

from .scratch_cons import FileDescriptorMode
from .utils import generate_id


class InputBuffer:

	# NOTE: unbounded

	def __init__(self, buffer_id=None):
		self._buffer_id = buffer_id or generate_id()
		self._buffer = deque

	@property
	def buffer_id(self):
		return self._buffer_id

	def feed(self, input):
		self._buffer.append(input)

	def pop(self):
		return self._buffer.popleft()


class SourceFileDescriptor:
	pass


class SourceFile:

	def __init__(self, path=None):
		self._path = path

	def set(self, path):
		if self._path is None:
			self._path = path
			return
		_error_details = f"unable to set 'path' attribute, as a path has already been associated with this instance of '{self.__class__.__name__}'..."
		raise RuntimeError(_error_details)

	def get(self):
		if self._path is None:
			_error_details = f"unable to access 'path' attribute; a path has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise RuntimeError(_error_details)
		return self._path


if __name__ == "__main__":
	pass
