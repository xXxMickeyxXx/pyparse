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
		self._environment = {}

	@property
	def evaluator_id(self):
		return self._evaluator_id

	@property
	def handlers(self):
		return self._handlers

	@property
	def environment(self):
		return self._environment

	def get(self, key, default=None):
		if key not in self._environment:
			return default
		return self._environment[key]

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

	def handle(self, handler_id, *args, **kwargs):
		_handler = self.handlers.get(handler_id, None)
		if _handler is None:
			# TODO: create and raise custom error here
			_error_details = f"invalid 'handler_id' {handler_id}; please update argument and try again..."
			raise RuntimeError(_error_details)
		return _handler(*args, **kwargs)

	def add_handler(self, handler_id, handler, overwrite=True):
		if handler_id in self.handlers and not overwrite:
			# TODO: create and raise custom error here
			_error_details = f"unable to add handler under ID: {handler_id}) as one is already associated by that reference and the 'overwrite' argument was 'False' and it could not thus be overwritten; please review and try again..."
			raise RuntimeError(_error_details)
		self.handlers[handler_id] = handler

	def remove_handler(self, handler_id):
		return self.handlers.pop(handler_id)

	def update(self, key, value, overwrite=False):
		if key not in self._environment or overwrite:
			self._environment[key] = value

	def eval(self, node):
		node.set_evaluator(self)
		return self.handle(node.node_id, node)

	def walk(self, node):
		for node in node.branches():
			node.eval(self)


if __name__ == "__main__":
	pass
