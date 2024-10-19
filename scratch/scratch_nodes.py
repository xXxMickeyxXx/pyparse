from pyevent import PyChannel

from pyprofiler import profile_callable, SortBy
from .scratch_evaluator import Evaluator
from .scratch_utils import generate_id


class Node:

	def __init__(self, node_id=None):
		self._node_id = node_id or generate_id()
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
	def is_root(self):
		return True if self._root is None else False

	@property
	def is_leaf(self):
		return True if self._root is not None and not self._branches else False

	@property
	def evaluator(self):
		if self._evaluator is None:
			_error_details = f"unable to access 'evaluator' as one has not yet been associated with this node..."
			raise RuntimeError(_error_details)
		return self._evaluator

	def branches(self):
		return tuple(self._branches)

	def add(self, node):
		self._branches.append(node)
		node.set_root(self)

	def remove(self, node_id):
		_nodes = self._branches
		_retval = None
		for i in range(len(_nodes)):
			_node = _nodes[i]
			if _node.node_id == node_id:
				_retval = self._branches.pop(i)
				break
		return _retval

	def node(self, node_id):
		if self.node_id == node_id:
			return self
		for _node in self._branches:
			_result = _node.node(node_id)
			if _result is not None:
				return _result
		return None

	def nodes(self, node_id):
		_nodes = []
		if self.node_id == node_id:
			return self
		for _node in self._branches:
			_result = _node.nodes(node_id)
			if _result is not None:
				_nodes.extend(_result)
		return _nodes

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

	def __init__(self, left, op, right, node_id=None):
		super().__init__(node_id=node_id)
		self.left = left
		self.op = op
		self.right = right


class Number(Expression):

	def __init__(self, number, node_id=None):
		super().__init__(node_id=node_id)
		self.number = number

	def __mul__(self, other):
		if not isinstance(other, type(self)):
			# TODO: create and raise custom error here
			_error_details = f"invalid operand types; unable to perform multiplication operation between objets ---> '{self.__class__.__name__}' * '{other.__class__.__name__}'..."
			raise TypeError(_error_details)
		return self.number * other.number

	def __rmul__(self, other):
		if not isinstance(other, type(self)):
			# TODO: create and raise custom error here
			_error_details = f"invalid operand types; unable to perform multiplication operation between objets ---> '{other.__class__.__name__}' * '{self.__class__.__name__}'..."
			raise TypeError(_error_details)
		return other.number * self.number


class Variable(Expression):

	def __init__(self, identifier: str, node_id=None):
		super().__init__(node_id=node_id)
		self._identifier = identifier

	@property
	def identifier(self):
		return self._identifier


class Assignment(Statement):

	def __init__(self, variable: Variable = None, expression: Expression = None, node_id=None):
		super().__init__(node_id=node_id)
		self.variable = variable
		self.expression = expression


class PrintStatement(Statement):

	def __init__(self, expression=None, node_id=None):
		super().__init__(node_id=node_id)
		self.expression = expression


class TestEvaluator(Evaluator):

	def __init__(self, evaluator_id=None):
		super().__init__(evaluator_id=evaluator_id)
		self.init()

	def init(self):
		self.add_handler("Root", self.handle_root)
		self.add_handler("Number", self.handle_number)
		self.add_handler("BinOp", self.handle_binary_operation)
		self.add_handler("Variable", self.handle_variable)
		self.add_handler("Assignment", self.handle_assignment)
		self.add_handler("PrintStatement", self.handle_print_statement)

	def handle_number(self, node):
		return node.number

	def handle_binary_operation(self, node):
		left_value = node.left.eval(self)
		right_value = node.right.eval(self)
		# print(f"A ---> {_a}")
		# print(f"B ---> {_b}")
		# if isinstance(node.left, Node):
		# 	left_value = self.eval(node.left)
		# else:
		# 	left_value = node.left
		# if isinstance(node.right, Node):
		# 	right_value = self.eval(node.right)
		# else:
		# 	right_value = node.right
		match node.op:
			case "/":
				return left_value / right_value
			case "*":
				return left_value * right_value
			case "+":
				return left_value + right_value
			case "-":
				return left_value - right_value

	def handle_variable(self, node):
		_val = node.identifier
		return _val

	def handle_assignment(self, node):
		print()
		print(f"\t• ---------- CALLING NODE@: {node.node_id} ----------• ")
		print()
		value = self.eval(node.variable)
		_expr_val = self.eval(node.expression)
		self.update(node.variable, _expr_val)
		return _expr_val

	def handle_print_statement(self, node):
		_res = []
		for _branch in node.branches():
			_res_ = self.eval(_branch)
			_res.append(_res_)
		print(f"RES: {_res}")
		return _res

	def handle_root(self, node):
		_res = []
		_print_node = node.branches()[0]
		return self.eval(_print_node.branches()[0])
		# for _node in node.branches():
		# 	_retv = self.eval(_node)
		# 	_res.append(_retv)
		# return _res


_expr_1 = Number(12)
_expr_2 = Number(4)
_bin_op_expr = BinOp(_expr_1, "*", _expr_2)
_bin_op_expr_2 = BinOp(_bin_op_expr, "+", Number(7))
_bin_op_expr_3 = BinOp(_bin_op_expr_2, "*", _bin_op_expr)
_variable = Variable("x")
_assignment = Assignment(variable=_variable, expression=_bin_op_expr_3)
_print_statement = PrintStatement()
_print_statement.add(_assignment)


_root = Root()
_root.add(_print_statement)


test_evaluator = TestEvaluator(evaluator_id="TEST_EVALUATOR")


# @profile_callable(sort_by=SortBy.TIME)
def main():
	print()
	_root_result = test_evaluator.eval(_root)
	print(f"ROOT RESULT: {_root_result}")
	print(f"RESULT:")
	print(test_evaluator.get(_variable, "'FALSE'"))
	print()


if __name__ == "__main__":
	main()
