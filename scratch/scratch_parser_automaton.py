from collections import deque


class ParserStateManager:

	# NOTE: implementation of a pushdown automaton
	
	def __init__(self, init_stack=None, parser=None):
		self._parser = parser
		self._stack = deque([] if init_stack is None else init_stack)
		self._enqueued = len(self._stack)

	@property
	def parser(self):
		if self._parser is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access 'parser' field as one has not yet been associated with instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._parser

	def state(self):
		return self._stack[-1]

	def __len__(self):
		return len(self._stack)

	def reset(self):
		self._parser = None
		self._stack.clear()

	def set_parser(self, parser):
		if self._parser is None:
			self._parser = parser

	def peek(self, offset):
		if offset <= 0:
			return self._stack[-1 + offset]
		return self._stack[-1-offset]

	def push(self, element):
		self._stack.append(element)
		_previous = self._enqueued
		self._enqueued += 1
		assert (_previous + 1) == self._enqueued
		assert len(self) == self._enqueued, f"STACK LEN: {len(self)}\nENQUEUED: {self._enqueued}"

	def pop(self):
		_retval = self._stack.pop()
		_previous = self._enqueued
		self._enqueued -= 1
		assert (self._enqueued + 1) == _previous
		assert len(self) == self._enqueued, f"STACK LEN: {len(self)}\nENQUEUED: {self._enqueued}"
		return _retval


if __name__ == "__main__":
    _automaton = ParserStateManager(init_stack=[6, 9, 3, 6])

    for _ in range(len(_automaton) * 2):
    	_popped_element = _automaton.pop()
    	print(f"ELEMENT ---> '{_popped_element}'")
    	print(f"CURRENT AUTOMATON STATE ---> {_automaton.state()}")
    	print()
