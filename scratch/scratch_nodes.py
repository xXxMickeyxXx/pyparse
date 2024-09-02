from pyevent import PyChannel

from .scratch_utils import generate_id


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

	def emit(self, node):
		def _retvals(**node_ids):
			_node_id = node.node_id
			_result_eval = self.channel.emit(_node_id, self)
			return _result_eval if len(_node_id) <= 0 else {kk: vv for kk, vv in _result_eval.items() if k in node_ids}
		return _retvals

	def register(self, signal_id, receiver=None, receiver_id=None, overwrite=False):
		_signal = self.channel.signal(signal_id=signal_id)
		return _signal.register(receiver, receiver_id=receiver_id, overwrite=overwrite)

	def remove(self, receiver_id):
		return self.channel.remove(receiver_id)

	def update(self, key, value, overwrite=False):
		if key not in self._environment or overwrite:
			self._environment[key] = value

	def eval(self, node, **node_ids):
		node.set_evaluator(self)
		_filtered_retvals = self.emit(node)(**node_ids)
		if _handler:
			return _handler(node)

	def walk(self, node):
		return node.eval(self)


class Node:

	def __init__(self, node_id):
		self._node_id = node_id
		self._root = None
		self._evaluator = None
		self._next = {}
		self._branches = []

	@property
	def node_id(self):
		return self._node_id

	@property
	def root(self):
		return self._root

	@property
	def evaluator(self):
		if self._evaluator is None:
			_error_details = f"unable to access 'evaluator' as one has not yet been associated with this node..."
			raise RuntimeError(_error_details)
		return self._evaluator

	def branches(self):
		return self._branches

	def add(self, node):
		self._branches.append(node)
		node.set_root(self)

	def remove(self, node_id):
		_retval = None
		for i in range(len(self._branches)):
			_curr_node = self._branches[i]
			if _curr_node.node_id == node_id:
				_retval = self._branches.pop(i)
				break
		return _retval

	def set_evaluator(self, evaluator):
		self._evaluator = evaluator

	def set_root(self, node):
		if self._root is not None:
			_error_details = f"unable to assign 'root' as one has already been set for this node...please reset root (via 'root_reset') and try again..."
			raise RuntimeError(_error_details)	
		self._root = node

	def root_reset(self):
		self._root = None

	def eval(self, evaluator):
		return evaluator.eval(self)


class NodeByClassName(Node):

	def __init__(self):
		super().__init__(self.__class__.__name__)


class Root(NodeByClassName):
	pass


class Expression(NodeByClassName):
	pass


class Statement(NodeByClassName):
	pass


class BinOp(Expression):

	def __init__(self, left, op, right, variable=None):
		super().__init__()
		self.left = left
		self.op = op
		self.right = right
		self.variable = variable


class Number(Expression):

	def __init__(self, number):
		super().__init__()
		self.number = number


class Variable(Expression):

	def __init__(self, name):
		super().__init__()
		self.name = name


class Assignment(Statement):

	def __init__(self, variable, expression):
		super().__init__()
		self.variable = variable
		self.expression = expression


class PrintStatement(Statement):

	def __init__(self, expression):
		super().__init__()
		self.expression = expression


def handle_number(node):
	return node.number  # Simply return the numeric value


def handle_binary_operation(node):
	left_value = node.evaluator.walk(node.left)  # Evaluate the left operand
	right_value = node.evaluator.walk(node.right)  # Evaluate the right operand
	_retval = None
	if node.op == "/":
		if right_value == 0:
			raise ZeroDivisionError("Division by zero error!")
		_retval = left_value / right
	elif node.op == '+':
		_retval = left_value + right_value
	elif node.op == '-':
		_retval = left_value - right_value
	elif node.op == '*':
		_retval = left_value * right_value
	else:
		raise ValueError(f"Unsupported operator: {node.op}")

	_variable = node.evaluator.environment["x"]
	node.variable = _variable

	return _retval


def handle_variable(node):
	if node.name in node.evaluator.environment:
		return node.evaluator.environment[node.name]
	else:
		node.evaluator.update_env(node.name, None, overwrite=True)
		node.evaluator.walk()


def handle_assignment(node):
	value = node.evaluator.walk(node.expression)  # Evaluate the expression to be assigned
	node.evaluator.environment.update_env(node.variable.name, value)
	return value


def handle_print_statement(node):
	value = node.evaluator.walk(node.expression)  # Evaluate the expression to be printed
	print(value)  # Output the value
	return value  # Optionally return the printed value


def handle_root(node):
	print(f"ROOT!")
	_evaluator = node.evaluator
	for _node in node.branches():
		print(f"NODE: {_node}")
		_evaluator.eval(_node)


def test_emitter_callback(node):
	print()
	print(f"NODE IN 'test_emitter_callback' BODY:")
	print(node)
	print(f"HEY FROM TEST EMITTER CALLBACK ON NODE:")
	print(f"\t• {node.node_id}")
	print(f"\t• {node.__class__.__name__}")
	print()
	print()


_variable = Variable("x")
_expr_1 = Number(4)
_expr_2 = Number(102)
_add_exp = BinOp(_expr_1, "+", _expr_2, variable=_variable)

_expr_3 = Number(8)
_mult_exp = BinOp(_add_exp, "-", _expr_3)

_print_stmt = PrintStatement(_variable)


_root = Root()
_root.add(_mult_exp)


TEST_NODE = _root
TEST_NODE_ID = _root.node_id
TEST_RECEIVER_ID = "[TEST_RECEIVER_ID]"
test_evaluator = Evaluator(evaluator_id="TEST_EVALUATOR")
test_evaluator.register(TEST_NODE_ID, test_emitter_callback, receiver_id=TEST_RECEIVER_ID)
# test_evaluator.add_handler("Root", handle_root)
# test_evaluator.add_handler("Number", handle_number)
# test_evaluator.add_handler("BinOp", handle_binary_operation)
# test_evaluator.add_handler("Variable", handle_variable)
# test_evaluator.add_handler("Assignment", handle_assignment)
# test_evaluator.add_handler("PrintStatement", handle_print_statement)


def main():
	print()
	_emitter = test_evaluator.eval(TEST_NODE)
	print(_emitter())
	print()


if __name__ == "__main__":
	main()
