from copy import copy as COPY_BUILINT, deepcopy as DEEPCOPY_BUILTIN

from pyevent import PyChannel
from .scratch_utils import generate_id


# class Evaluator:

# 	def __init__(self, evaluator_id=None):
# 		self._evaluator_id = evaluator_id or generate_id()
# 		self._handlers = {}
# 		self._environment = {}

# 	@property
# 	def evaluator_id(self):
# 		return self._evaluator_id

# 	@property
# 	def environment(self):
# 		return self._environment

# 	def reset(self):
# 		self._handlers = {}
# 		self._environment = {}

# 	def update(self, env_key, value, overwrite=False):
# 		if env_key not in self._environment or overwrite:
# 			self._environment[env_key] = value
# 			return True
# 		return False

# 	def pop(self, env_key):
# 		return self._environment.pop(env_key)

# 	def register(self, handler, node_id, overwrite=False):
# 		if node_id not in self._handlers or overwrite:
# 			self._handlers[node_id] = handler

# 	def remove(self, node_id):
# 		return self._handlers.pop(node_id)

# 	def eval(self, node):
# 		node.set_evaluator(self)
# 		_handler = self._handlers.get(node.node_id, None)
# 		if _handler:
# 			return _handler(node)

# 	def walk(self, node):
# 		return node.eval(self)

# 	def copy(self, *, deepcopy=False):
#         _cls_type = type(self)
#         return self._deepcopy(_cls_type) if deepcopy else self._copy(_cls_type)

#     def _copy(self, cls_type):
#         _new_instance = cls_type(evaluator_id=COPY_BUILINT(self.evaluator_id))
#         _new_instance._handlers = COPY_BUILINT(self._handlers)
#         _new_instance._environment = COPY_BUILINT(self._environment)
#         return _new_instance

# 	def _deepcopy(self, cls_type):
#         _new_instance = cls_type(evaluator_id=DEEPCOPY_BUILTIN(self.evaluator_id))
#         _new_instance._handlers = DEEPCOPY_BUILTIN(self._handlers)
#         _new_instance._environment = DEEPCOPY_BUILTIN(self._environment)
#         return _new_instance


class Evaluator:

	def __init__(self, evaluator_id=None):
		self._evaluator_id = evaluator_id or generate_id()
		self._handlers = {}
		self._channel = None
		self._environment = {}

	@property
	def evaluator_id(self):
		return self._evaluator_id

	@property
	def channel(self):
		if self._channel is None:
			self._channel = PyChannel(channel_id=self.evaluator_id)
		return self._channel

	@property
	def environment(self):
		return self._environment

	def captured(self, key, *, value=None):
		for _key, _value in self._environment.items():
			if _key != key or value != _value:
				return False
			elif isinstance(_value, (list, tuple, dict, set)):
				return _value in _value
			elif key == _key or value == _value:
				return True
		return False

	def capture(self, key, value, overwrite=False):
		_retval = False
		if key in self._environment:
			if not overwrite:
				_retval = True
			else:
				self._environment[key] = value
				_retval = True
		else:
			self._environment[key] = value
			_retval = True
		return _retval

	def emit(self, signal_id, *args, **kwargs):
		_raw_results = self.channel.emit(signal_id, *args, **kwargs)
		return _raw_results

	def register(self, signal_id, receiver=None, receiver_id=None, overwrite=False):
		_signal = self.channel.signal(signal_id=signal_id)
		return _signal.register(receiver, receiver_id=receiver_id, overwrite=overwrite)

	def remove(self, receiver_id):
		return self.channel.remove(receiver_id)

	def update(self, key, value, overwrite=False):
		if key not in self._environment or overwrite:
			self._environment[key] = value

	def eval(self, node, *node_ids):
		node.set_evaluator(self)
		_handler = self.emit(node.node_id, node)
		if _handler:
			return [v for k, v in _handler.items()][-1]

	def walk(self, node):
		return node.eval(self)


if __name__ == "__main__":
	pass
