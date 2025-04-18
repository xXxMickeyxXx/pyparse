from abc import ABC, abstractmethod
from collections import deque


from ...utils import generate_id


class NodeTraveler(ABC):

	def __init__(self, traveler_id=None):
		self._traveler_id = traveler_id or generate_id()

	@property
	def traveler_id(self):
		return self._traveler_id

	@abstractmethod
	def traverse(self, node):
		raise NotImplementedError


class BFSNodeTreeTraveler(NodeTraveler):

	def traverse(self, node):
		_queue = deque([node])
		while _queue:
			_next_node = _queue.popleft()
			print(f"NodeID: {_next_node.node_id}")
			if _next_node.is_leaf:
				continue
			_queue.extend(_next_node.branches())
		return


class DFSNodeTreeTraveler(NodeTraveler):

	def traverse(self, node):
		print(f"NodeID: {node.node_id}")
		_has_data = node.has_data
		print(f"DOES NODE ID: {node.node_id} HAVE DATA ---> {_has_data}")
		if _has_data:
			print(f"NODE DATA ---> {node.data}")
		if not node.is_leaf:
			for _node in node.branches():
				_node.traverse(self)
		return


class Node(ABC):

	def __init__(self, node_id):
		self._node_id = node_id
		self._root_node = None
		self._branches = []

	@property
	def node_id(self):
		return self._node_id

	@property
	def is_leaf(self):
		return True if not self._branches and self.root is not None else False

	@property
	def is_root(self):
		return True if self.root is None else False

	@property
	def has_root(self):
		return True if (self._root_node is None or not bool(self._root_node)) else False

	@property
	def has_branch(self):
		if self.is_leaf:
			_error_details = f"a node designated as a leaf is unable to have branches and/or perform any branch related operations...."
			raise TypeError(_error_details)
		return len(self._branches) > 0		

	@property
	def root(self):
		return self._root_node

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return f"{self.__class__.__name__}(node_id={self.node_id})"

	def branches(self):
		if self._branches:
			return (i for i in self._branches)
		return ()

	def prune(self):
		self.root.remove(self.node_id)
		self.set_root(None)

	def set_root(self, root_node):
		self._root_node = root_node

	def add(self, node):
		if node.root is not None:
			# TODO: create and raise custom error here
			_error_details = f"unable to add node to branch as node already belongs to a different root (node ID: {node.root.node_id})..."
			raise RuntimeError(_error_details)
		self._branches.append(node)
		node.set_root(self)

	def remove(self, node_id):
		if self.is_leaf:
			_error_details = f"unable to perform any branch related operations as node ID: {self.node_id} has been designated as a leaf node..."
			raise TypeError(_error_details)
		_nodes_len = len(self._branches)
		_counter = 0
		while _counter < _nodes_len:
			_current_node = self._branches[_counter]
			if _current_node.node_id == node_id:
				_node = self._branches.pop(_counter)
				_node.set_root(None)
				return _node
			_counter += 1
		_error_details = f"invalid 'node_id' as this instance of '{self.__class__.__name__}' has not sub-node associated with node ID: {node_id}..."
		raise ValueError(_error_details)

	def select(self, node_id=None, node_ids=None):
		# NOTE: all node ID's passed to the 'node_ids' argument must exist in order
		# 		for this function to return selected node grouping else a custom
		# 		error will occurr
		if self.is_leaf:
			_error_details = f"unable to perform any branch related operations as node ID: {self.node_id} has been designated as a leaf node..."
			raise TypeError(_error_details)		
		if node_id is not None:
			for _node in self._branches:
				if _node.node_id == node_id:
					return _node
		elif isinstance(node_ids, (list, tuple, set)):
			_node_is_len = len(node_ids)
			if _node_is_len <= 1:
				_error_details = f"in order to return multiple nodes contained within the branch or branches, the 'node_ids' parameter must receive an argument which is of a list, tuple or set type, containing 2 OR MORE desired node ID's (NOTE: calling this method with 'node_ids' will either return all of the requested nodes or an error will occur should, for instance, invalid node ID('s) were included in the method call)...if only one node is desired for selection, call 'select' using only the 'node_id' parameter..."
				raise RuntimeError(_error_details)
			_invalid_nodes = [i for i in self._branches if i not in node_ids]
			if len(_invalid_nodes) <= 0:
				return tuple([i for i in self._branches if i in node_ids])
			else:
				# TODO: create and raise custom error here
				_invalid_nodes_len = len(_invalid_nodes)
				if _invalid_nodes_len == 1:
					_invalid_ids_4_err_details = _invalid_nodes[0]
				elif _invalid_nodes_len >= 2:
					_invalid_ids_4_err_details = ', '.join(_invalid_nodes[:-1]) + f"and {_invalid_nodes[-1]}"
				_error_details = f"an error occurred attempting to select the following invalid node ID('s): {_invalid_ids_4_err_details}; please update 'node_ids' argument, making sure to correctly specifcy which group of node's should return upon calling the method in this way..."
				raise ValueError(_error_details)
		else:
			if not any([node_id, node_ids]):
				# TODO: create and raise custom error here
				_error_details_ = f"'select' method must receive either a 'node_id' argument, returning the requested node by itself if it exists, or a 'node_ids' argument, which must be a list, tuple or set of 2 or more node ID's (which then returns a tuple of nodes found)..."
			elif all([node_id, node_ids]):
				_error_details_ = f"'select' method must only receive an argument for one parameter, either the 'node_id' or the 'node_ids'; please ensure only one argument is passed to this method and try again..."
			else:
				_error_details_ = f"an error has occurred when calling 'select' method of node ID: {self.node_id}; pleas review source in order to begin resolving this issue..."
			raise RuntimeError(_error_details_)

	def traverse(self, node_traveler):
		return node_traveler.traverse(self)


if __name__ == "__main__":
	# NOTE: pushing textual output further down in the terminal display as running
	# 		this module using the '-m' switch is stating that running it this way
	# 		may be unpredictable
	for _ in range(3):
		print()


	class DataNode(Node):

		def __init__(self, data=None, node_id=generate_id()):
			super().__init__(node_id)
			self._data = data
			self._data_set = self._data is not None or bool(self._data)

		@property
		def data(self):
			if (self._data is None or not bool(self._data)) and not self._data_set:
				# TODO: create and raise custom error here
				_error_details = f"unable to retrieve data on this node (ID: {self.node_id}) as it's data field has not yet been set; set field by calling node's 'set_data' method and try again..."
				raise AttributeError(_error_details)
			return self._data

		@property
		def has_data(self):
			return self._data_set and (self._data is not None or bool(self._data))

		def set_data(self, data):
			if not self._data_set and (self._data is None or not bool(self._data)):
				self._data = data
				self._data_set = True
				return None
			# TODO: create and raise custom error here
			_error_details = f"unable to set data on this node (ID: {self.node_id}) as previous data occupies the data field; remove it by calling node's 'reset' method, and try again..."

		def reset(self):
			self._data = None
			self._data_set = False



	_root_node = DataNode(data="DEXTER", node_id="[TEST_ROOT_NODE]")
	_non_leaf_node_1 = DataNode(data="Violet", node_id=f"[{'non_leaf_node_1'.upper()}]")
	_non_leaf_node_2 = DataNode(data="Theo", node_id=f"[{'non_leaf_node_2'.upper()}]")
	_non_leaf_node_3 = DataNode(data="Penny", node_id=f"[{'non_leaf_node_3'.upper()}]")

	_leaf_node_1 = DataNode(data="Mickey", node_id=f"[{'leaf_node_1'.upper()}]")
	_leaf_node_2 = DataNode(data="Sarah", node_id=f"[{'leaf_node_2'.upper()}]")
	_leaf_node_3 = DataNode(data="Katie", node_id=f"[{'leaf_node_3'.upper()}]")
	_leaf_node_4 = DataNode(data="Sam", node_id=f"[{'leaf_node_4'.upper()}]")
	_leaf_node_5 = DataNode(data="Dad", node_id=f"[{'leaf_node_5'.upper()}]")
	_leaf_node_6 = DataNode(data="Mom", node_id=f"[{'leaf_node_6'.upper()}]")
	
	_non_leaf_node_7 = DataNode(data="non_leaf_node_7", node_id=f"[{'non_leaf_node_7'.upper()}]")

	_non_leaf_node_7.add(_leaf_node_4)
	_non_leaf_node_7.add(_leaf_node_5)

	_root_node.add(_non_leaf_node_1)
	_root_node.add(_non_leaf_node_2)
	_root_node.add(_non_leaf_node_3)
	_root_node.add(_leaf_node_1)
	_root_node.add(_non_leaf_node_7)

	_non_leaf_node_1.add(_leaf_node_2)
	_non_leaf_node_1.add(_leaf_node_3)
	_non_leaf_node_3.add(_leaf_node_6)


	_bfs_search = BFSNodeTreeTraveler()
	val_1 = _root_node.traverse(_bfs_search)
	print()
	print()
	_dfs_search = DFSNodeTreeTraveler()
	val_2 = _root_node.traverse(_dfs_search)

	print()
	print(val_1)
	print()
	print()
	print(val_2)
	print()
