class Node:

	def __init__(self, node_id, nodes=None):
		self._node_id = node_id

	@property
	def node_id(self):
		return sef._node_id


class Nodes(Node):

	def __init__(self, node_id, nodes=None):
		super().__init__(node_id)
		self._nodes = nodes or []

	def add(self, node):
		self._nodes.append(node)

	def remove(self, node_id):
		_nodes_len = len(self._nodes)
		_counter = 0
		while _counter < _nodes_len:
			_current_node = self._nodes[_counter]
			if _current_node.node_id == node_id:
				return self._nodes.pop(_counter)
			_counter += 1
		_error_details = f"invalid 'node_id'; a node associated with ID: {node_id};"


if __name__ == "__main__":
	pass
