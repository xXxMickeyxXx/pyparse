from abc import ABC, abstractmethod
from threading import Lock, Condition
from pathlib import Path
from collections import deque
from io import (
	StringIO,
	BytesIO,
	BufferedReader,
	BufferedWriter
)

from .scratch_utils import generate_id
from .scratch_cons import FileDescriptorMode


class iBuffer(ABC):

	@property
	@abstractmethod
	def size(self):
		raise NotImplementedError

	@property
	@abstractmethod
	def is_full(self):
		raise NotImplementedError

	@property
	@abstractmethod
	def is_empty(self):
		raise NotImplementedError

	@property
	@abstractmethod
	def remaining_space(self):
		raise NotImplementedError

	@abstractmethod
	def reset(self):
		raise NotImplementedError

	@abstractmethod
	def read(self, reader):
		raise NotImplementedError

	@abstractmethod
	def write(self, element, writer):
		raise NotImplementedError

	@abstractmethod
	def append(self, element):
		raise NotImplementedError

	@abstractmethod
	def append_left(self, element):
		raise NotImplementedError

	@abstractmethod
	def pop(self, idx=0):
		raise NotImplementedError

	@abstractmethod
	def pop_left(self):
		raise NotImplementedError


class CircularBuffer:
    def __init__(self, size, init_value=None):
        self._size = size
        self.buffer = ([init_value] * size) if not isinstance(init_value, (list, tuple, set, dict)) else ([None] * size)
        self.head = 0
        self.tail = 0
        self.count = 0
        self.lock = Lock()
        self.not_full = Condition(self.lock)
        self.not_empty = Condition(self.lock)

    @property
    def size(self):
    	return self._size

    def append(self, item):
        with self.lock:
            while self.count == self._size:
                self.not_full.wait()  # Wait until buffer has space
            self.buffer[self.tail] = item
            self.tail = (self.tail + 1) % self._size
            self.count += 1
            self.not_empty.notify()  # Notify that buffer is not empty

    def retrieve(self):
        with self.lock:
            while self.count == 0:
                self.not_empty.wait()  # Wait until buffer has items
            item = self.buffer[self.head]
            self.buffer[self.head] = None  # Optional: Clear the slot
            self.head = (self.head + 1) % self._size
            self.count -= 1
            self.not_full.notify()  # Notify that buffer is not full
            return item

    def is_full(self):
        with self.lock:
            return self.count == self._size

    def is_empty(self):
        with self.lock:
            return self.count == 0

    def __len__(self):
        with self.lock:
            return self.count

# Example Usage
if __name__ == "__main__":
    buffer = CircularBuffer(5)

    # Producer
    def producer():
        for i in range(10):
            buffer.append(i)
            print(f"Produced {i}")

    # Consumer
    def consumer():
        for _ in range(10):
            item = buffer.retrieve()
            print(f"Consumed {item}")

    from threading import Thread

    producer_thread = Thread(target=producer)
    consumer_thread = Thread(target=consumer)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()


class Buffer:

	def __init__(self, size, buffer_id=None):
		self._size = size
		self._buffer_id = buffer_id or generate_id()
		self._buffer = None
		self._read_pointer
	
	@property
	def buffer_id(self):
		return self._buffer_id

	@property
	def buffer(self):
		if self._buffer is None:
			self._buffer = self.buffer_factory()
		return self._buffer

	@property
	def size(self):
		return len(self)

	def __len__(self):
		return len(self.buffer)

	def reset(self):
		self._read_pointer = 0
		self._write_pointer = 0

	def peek(self, offset=0):
		_data = []
		_offset_counter = 0
		while _offset_counter <= offset:
			_next_data = self.buffer[_offset_counter]
			_data.append(_next_data)
			_offset_counter += 1

	def read_at(self, idx):
		return self.buffer[idx]

	def get(self, start=0, stop=1, step=1):
		_slice = slice(start, stop, step)
		return self.buffer[_slice]

	def feed(self, data):
		self._buffer.append(data)

	def flush(self):
		_data = ""
		while self.buffer:
			_data += self.buffer.popleft()
		self._buffer = None

	@staticmethod
	def buffer_factory():
		return deque()


class SourceFileDescriptor:
	pass


class SourceFile:

	# TODO: re-implement into a 'SourceFileHandle' or just 'FileHandle'

	def __init__(self, path=None):
		self._path = path

	@property
	def path(self):
		if self._path is None:
			_error_details = f"unable to access 'path' attribute; a path has not yet been associated with this instance of '{self.__class__.__name__}'..."
			raise RuntimeError(_error_details)
		return self._path

	def set(self, path):
		if self._path is None:
			self._path = path
			return
		_error_details = f"unable to set 'path' attribute, as a path has already been associated with this instance of '{self.__class__.__name__}'..."
		raise RuntimeError(_error_details)

	def get(self):
		return self.path


class FileHandle:

	# TODO: implement

	_file_descriptors = []

	def __init__(self, source_file, fileno=1):
		self._source_file = source_file
		self._fileno = fileno or max(self._opened_filed) + 1
		self._file_descriptors.append(self._fileno)
		self._buffer = None
		self._read_pointer = 0
		self._write_pointer = 0
	
	@property
	def buffer(self):
		if self._buffer is None:
			self._buffer = self.buffer_factory()
		return self._buffer

	@property
	def fileno(self):
		return self._fileno

	def feed(self, data):
		self._buffer.append(data)

	def flush(self):
		_data = ""
		while self.buffer:
			_data += self.buffer.popleft()
		self._buffer = None

	def buffer_factory(self):
		return deque()


if __name__ == "__main__":
	pass
