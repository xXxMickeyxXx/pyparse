from pyevent import PyChannel

from .scratch_evaluator import Evaluator
from .scratch_utils import generate_id


class Node:

	def __init__(self, node_id):
		self._node_id = node_id
		self._root = None
		self._evaluator = None
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

	def __init__(self, name, value=None):
		super().__init__()
		self.name = name
		self._value = value
		self._value_set = False

	@property
	def value(self):
		return self._value

	def set_value(self, value):
		self._value = value
		self._value_set = True

	def reset(self):
		self._value = None
		self._value_set = False


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

	print(f"NODE:")
	print(node.left)
	print(node.right)
	print(f"NODE ENV:")
	_curr = node.evaluator
	_variable = Variable(Number(_retval))
	node.evaluator.environment["x"] = _variable
	return _retval


def handle_variable(node):
	_val = node.name
	return _val

def handle_assignment(node):
	value = node.evaluator.walk(node.expression)  # Evaluate the expression to be assigned
	node.evaluator.environment.update_env(node.variable.name, value)
	return value


def handle_print_statement(node):
	value = node.evaluator.walk(node.expression)  # Evaluate the expression to be printed
	print(value)  # Output the value
	return value  # Optionally return the printed value


def handle_root(node):
	_evaluator = node.evaluator
	for _node in node.branches():
		_evaluator.eval(_node)
	return _evaluator.environment["x"]


def test_emitter_callback(node):
	print()
	print(f"NODE IN 'test_emitter_callback' BODY:")
	print(node)
	print(f"HEY FROM TEST EMITTER CALLBACK ON NODE:")
	print(f"\t• {node.node_id}")
	print()
	print()


_variable = Variable("x")
_variable_2 = Variable("_test_1")
_expr_1 = Number(4)
_expr_2 = Number(102)
_add_exp = BinOp(_expr_1, "+", _expr_2, variable=_variable)
_mult_exp_2 = BinOp(_add_exp, "*", Number(3), variable=_variable_2)

_expr_3 = Number(8)
_mult_exp = BinOp(_add_exp, "*", _expr_3)
_add_exp_2 = BinOp(_mult_exp, "+", Number(7), variable=_variable_2)

_print_stmt = PrintStatement(_variable)
_print_stmt_2 = PrintStatement(_variable_2)


_root = Root()
_root.add(_mult_exp)
# _root.add(_print_stmt)
# _root.add(_print_stmt_2)


TEST_NODE = _root
TEST_NODE_ID = _root.node_id
TEST_RECEIVER_ID = "[TEST_RECEIVER_ID]"
test_evaluator = Evaluator(evaluator_id="TEST_EVALUATOR")
test_evaluator.register(TEST_NODE_ID, test_emitter_callback, receiver_id=TEST_RECEIVER_ID)
test_evaluator.register("Root", handle_root)
test_evaluator.register("Number", handle_number)
test_evaluator.register("BinOp", handle_binary_operation)
test_evaluator.register("Variable", handle_variable)
test_evaluator.register("Assignment", handle_assignment)
test_evaluator.register("PrintStatement", handle_print_statement)


def main():
	print()
	retval = test_evaluator.eval(TEST_NODE)
	print(retval)
	print()


if __name__ == "__main__":
	main()
