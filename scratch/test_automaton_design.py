from collections import deque

from pyevent import (
	PyChannels,
	PyChannel,
	PySignal
)
from .scratch_utils import generate_id


# class State:

# 	def __init__(self, id=None, context=None):
# 		self._id = id or str(self.__class__.__name__)
# 		self._context = context
# 		self._fields = {}

# 	@property
# 	def id(self):
# 		return self._id

# 	@id.setter
# 	def id(self, val):
# 		_error_details = f"unable to set/change/update 'id' attribute, as it's immutable. To use a different 'id', instantiate a new class the desired value to the 'id' argument..."
# 		raise AttributeError(_error_details)

# 	@property
# 	def context(self):
# 		return self._context

# 	def set_context(self, context):
# 		if self._context is not None:
			

# 	def add(self, key, value, overwrite=False):
# 		if key in self._fields and not overwrite:
# 			raise KeyError(f"unable to add key/value pair as the key: '{key}' has already been associated with a value (and the 'overwrite' argument has been set to 'False')...")
# 		self._fields.update({key: value})

# 	def remove(self, key):
# 		if key not in self._fields:
# 			raise KeyError(f"key: {key} does not exists within this state object...")
# 		return self._fields.pop(key)

# 	def get(self, key, default=None):
# 		_retval = default
# 		if key in self._fields:
# 			_retval = self._fields[key]
# 		return _retval


class Automaton:

	__slots__ = ("_id", "_event_channel", "_state_stack")

	_channels = PyChannels()

	def __init__(self, id=generate_id()):
		self._id = id
		self._event_channel = None
		self._state_stack = deque()
		self._prev_state_stack = deque()
		self._status = None

	@property
	def id(self):
		return self._id

	@property
	def event_channe(self):
		if self._event_channel is None:
			self._event_channel = _channels.channel(channel_id=self.id)
		return self._event_channel

	def status(self):
		if self._status is None:
			# TODO: Create and raise custom error here
			_error_details = f"unable to get attribute; state machine has either not started or the underlying state field has somehow not been associated with a state object..."
			raise AttributeError(_error_details)
		return self._status

	def advance(self):
		if not self._state_stack:
			return False
		return self._state_stack.popleft()

	def reverse(self):
		if not self._prev_state_stack:
			return False
		return self._prev_state_stack.pop()

	def add_state(self, state):
		self._state_stack.append(state)

	def remove_state(self, state_id):
		raise NotImplementedError

	def reset(self):
		self._event_channel




if __name__ == "__main__":
    pass
