from pyevent import PyChannel

from .scratch_evaluator import Evaluator
from .scratch_utils import generate_id


class Node:

	def __init__(self, node_id=None):
		self._node_id = node_id or generate_id()
		self._root = None
		self._evaluator = None
		self._branches = {}

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
		self._branches.update({node.node_id: node})
		node.set_root(self)

	def remove(self, node_id):
		return self._branches.pop(node_id)

	def node(self, node_id):
		if self.node_id == node_id:
			return self
		for _node_id, _node in self.branches().items():
			_result = _node.node(node_id)
			if _result is not None:
				return _result
		return None

	def set_evaluator(self, evaluator):
		self._evaluator = evaluator

	def set_root(self, node):
		self._root = node

	def root_reset(self):
		self._root = None

	def eval(self, evaluator):
		return evaluator.eval(self)


class NodeByClassName(Node):

	def __init__(self, node_id=None):
		super().__init__(node_id=node_id or self.__class__.__name__)


class Root(NodeByClassName):
	pass


class Expression(NodeByClassName):
	pass


class Statement(NodeByClassName):
	pass


class BinOp(Expression):

	def __init__(self, left, op, right):
		super().__init__()
		self.add(left)
		self.op = op
		self.add(right)


class Number(Expression):

	def __init__(self, number):
		super().__init__()
		self.number = number


class Variable(Expression):

	def __init__(self, identifier: str):
		super().__init__()
		self._identifier = identifier

	@property
	def identifier(self):
		return self._identifier


class Assignment(Statement):

	def __init__(self, variable: Variable = None, expression: Expression = None):
		super().__init__()
		if variable is not None:
			self.add(variable)
		if expression is not None:
			self.add(expression)

	# def eval(self, evaluator):
	# 	_Variable_node = self.node("Variable")
	# 	_Variable_node_id = _Variable_node.identifier
	# 	evaluator.environment.update({_Variable_node_id: _Variable_node})
	# 	return evaluator.eval(self)


class PrintStatement(Statement):

	def __init__(self, expression=None):
		super().__init__()
		if expression:
			self.add(expression)


class TestEvaluator(Evaluator):

	def __init__(self, evaluator_id=None):
		super().__init__(evaluator_id=evaluator_id)
		self.init()

	def init(self):
		self.register("Root", self.handle_root)
		self.register("Number", self.handle_number)
		self.register("BinOp", self.handle_binary_operation)
		self.register("Variable", self.handle_variable)
		self.register("Assignment", self.handle_assignment)
		self.register("PrintStatement", self.handle_print_statement)

	def handle_number(self, node):
		return node.number  # Simply return the numeric value

	def handle_binary_operation(self, node):
		for k, v in node.branches().items():
			print(f"{k}: {v}")
			print()
		left_value = node.node("Number").number
		right_value = node.node("Number").number
		print(f"CALCULATING ---> {left_value} {node.op} {right_value}")
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
		return _retval

	def handle_variable(self, node):
		_val = node.identifier
		return _val

	def handle_assignment(self, node):
		value = self.walk(node.node("Variable"))
		_expr = self.walk(node.node("BinOp"))
		print(f"handle_assignment@: 'Variable' ---> {value}")
		print(f"handle_assignment@: 'BinOp' ---> {_expr}")
		self.capture(value, _expr, overwrite=False)
		return value

	def handle_print_statement(self, node):
		value = self.eval(node.node("Number"))
		print(f"'handle_print_statement'@: 'BinOp' ---> {value}")
		return value

	def handle_root(self, node):
		for _node_id, _node in node.branches().items():
			self.eval(_node)
		return self.environment["x"]


_expr_1 = Number(4)
_expr_2 = Number(12)
_bin_op_expr = BinOp(_expr_1, "*", _expr_2)
_bb = BinOp(Number(3), "*", Number(2))
_variable = Variable("x")
_assignment = Assignment()
_assignment.add(_variable)
_assignment.add(_bin_op_expr)
_print_stmt = PrintStatement()
_print_stmt.add(_bb)


_root = Root()
_root.add(_assignment)
_root.add(_print_stmt)
# _root.add(_print_stmt_2)


test_evaluator = TestEvaluator(evaluator_id="TEST_EVALUATOR")


def main():
	_retval = test_evaluator.eval(_root)
	print()
	print(f"RESULT ---> {_retval}")
	# _found_node = _root.node("BinOp")
	# print()
	# _text = ""
	# if _found_node:
	# 	_text = f"NODE **FOUND**: {_found_node}!!!"
	# else:
	# 	_text = f"NODE **NOT** FOUND..."
	# print(_text)
	# print()
	# test_evaluator.walk(_assignment)
	# retval = test_evaluator.eval(TEST_NODE)
	# print(retval)
	print()


if __name__ == "__main__":
	main()
