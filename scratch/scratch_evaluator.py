from copy import copy as COPY_BUILINT, deepcopy as DEEPCOPY_BUILTIN

from .scratch_utils import generate_id


class Evaluator:

	def __init__(self, evaluator_id=None):
		self._evaluator_id = evaluator_id or generate_id()
		self._handlers = {}
		self._environment = {}

	@property
	def evaluator_id(self):
		return self._evaluator_id

	@property
	def environment(self):
		return self._environment

	def reset(self):
		self._handlers = {}
		self._environment = {}

	def update(self, env_key, value, overwrite=False):
		if env_key not in self._environment or overwrite:
			self._environment[env_key] = value
			return True
		return False

	def pop(self, env_key):
		return self._environment.pop(env_key)

	def register(self, handler, node_id, overwrite=False):
		if node_id not in self._handlers or overwrite:
			self._handlers[node_id] = handler

	def remove(self, node_id):
		return self._handlers.pop(node_id)

	def eval(self, node):
		node.set_evaluator(self)
		_handler = self._handlers.get(node.node_id, None)
		if _handler:
			return _handler(node)

	def walk(self, node):
		return node.eval(self)

	def copy(self, *, deepcopy=False):
        _cls_type = type(self)
        return self._deepcopy(_cls_type) if deepcopy else self._copy(_cls_type)

    def _copy(self, cls_type):
        _new_instance = cls_type(evaluator_id=COPY_BUILINT(self.evaluator_id))
        _new_instance._handlers = COPY_BUILINT(self._handlers)
        _new_instance._environment = COPY_BUILINT(self._environment)
        return _new_instance

	def _deepcopy(self, cls_type):
        _new_instance = cls_type(evaluator_id=DEEPCOPY_BUILTIN(self.evaluator_id))
        _new_instance._handlers = DEEPCOPY_BUILTIN(self._handlers)
        _new_instance._environment = DEEPCOPY_BUILTIN(self._environment)
        return _new_instance


if __name__ == "__main__":
	pass
