import random
from collections import deque
import time
import hashlib
from enum import IntEnum, StrEnum, auto

from pyprofiler import profile_callable, SortBy
from pyevent import PyChannels, PyChannel, PySignal
from .scratch_utils import generate_id


class TraversalStrategy(IntEnum):

	DFS = 1
	BFS = 2


def trampoline(component, stack):
	pass


class VisitorChannel:

	def __init__(self, visitor_id=None):
		self._visitor_id = visitor_id or generate_id()
		self._channel = PyChannel(channel_id=self._visitor_id)

	@property
	def visitor_id(self):
		return self._visitor_id

	@property
	def channel(self):
		return self._channel

	def __getattr__(self, attr_name):
		return getattr(self.channel, attr_name)


class Component:

	_channel = PyChannel()

	def __init__(self, data, component_id=None):
		self._data = data
		self._component_id = component_id or generate_id()
		self._root = None
		self._locked = False
		self._index = None
		self._hash = None
		self._signal = None

	@property
	def data(self):
		return self._data

	@property
	def component_id(self):
		return self._component_id

	@property
	def root(self):
		return self._root

	@property
	def index(self):
		# TODO: create and raise custom error here if index isn't set
		return self._index

	@property
	def hash(self):
		if self._hash is None:
			self._calculate_hash()
		return self._hash

	@property
	def is_composite(self):
		return False

	@property
	def channel(self):
		return self._channel

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return f"{self.component_id}"

	def __enter__(self):
		self.unlock()
		return self

	def __exit__(self, err_type, err_value, err_tb):
		self.lock()

	def register(self, event_id, receiver, receiver_id=None, overwrite=False):
		_event_signal = self.channel.signal(signal_id=event_id)
		_event_signal.register(receiver, receiver_id=receiver_id, overwrite=overwrite)

	def execute(self, event_id, event=None):
		_event_signal = self.channel.signal(signal_id=event_id)
		if event is not None:
			_event = event
		else:
			_event = self
		return _event_signal.emit(_event)

	def _calculate_hash(self):
		component_id_bytes = str(self._component_id).encode('utf-8')
		hash_object = hashlib.sha256(component_id_bytes)
		self._hash = hash_object.hexdigest()

	def __eq__(self, other):
		return self.component_id == other.component_id

	def set_data(self, data):
		if not self._locked:
			self._data = data
		# TODO: create and raise custom error for the locking mechanism

	def set_root(self, root):
		if not self._locked and self._root is None:
			self._root = root

	def reset_root(self):
		self._root = None
		self._index = None

	def lock(self):
		self._locked = True

	def unlock(self):
		self._locked = False

	def set_index(self, index):
		if not self._locked:
			self._index = index
		# TODO: create and raise custom error for the locking mechanism

	def copy(self):
		raise NotImplementedError


class Components(Component):

	def __init__(self, data, component_id=None):
		super().__init__(data, component_id=component_id)
		self._components = []
		self._next_index = 0
		self._update_indices()

	@property
	def components(self):
		return self._components

	@property
	def is_composite(self):
		return True

	def __len__(self):
		return len(self._components)

	# @property
	# def mapping(self):
	# 	return {component.component_id: component for component in self._components}

	def add(self, component):
		if component not in self._components:
			with component:
				component.set_root(self)
				component.set_index(self._next_index)
			self._components.append(component)
			self._next_index += 1

	def remove(self, component_id):
		i = 0
		while i < len(self):
			if self._components[i].component_id == component_id:
				_comopnent = self._components.pop(i)
				_comopnent.reset_root()
				self._update_indices()
				return _comopnent
			i += 1
		return None

	def select(self, component_id, *, tstrategy=1):
		for comp in self.traverse(tstrategy):
			if comp.component_id == component_id:
				return comp
		return None

	def _update_indices(self):
		self._next_index = 0
		for component in self._components:
			with component:
				component.set_index(self._next_index)
			self._next_index += 1

	# def component_hashes(self):
	# 	hash_map = {}
	# 	for component in self._components:
	# 		hash_map[component.component_id] = component
	# 		if isinstance(component, Components):
	# 			hash_map.update(component.component_hashes())
	# 	return hash_map

	def traverse(self, tstrategy):
		return tstrategy(self)


TEST_LIST = []


def test_event_receiver(test_id):
	def _test_handle_comp(comp):
		print()
		print(f"SEARCHING FOR TEST ID: {test_id} IN ROOT...")
		comp = comp.select(test_id, tstrategy=1)
		_found = f"ID: {comp.component_id}\nDATA: {comp.data}\nHASH: {comp.hash}\nINDEX: {comp.index}"
		TEST_LIST.append(_found)
		print(_found)
		print()
	return _test_handle_comp


class Root(Components):

	def __init__(self, data, component_id=None):
		super().__init__(data, component_id=component_id)
		self._tstrategy_mapping = {1: self._traverse_depth_first, 2: self._traverse_breadth_first}

	def traverse(self, tstrategy):
		if tstrategy not in [i for i in TraversalStrategy]:
			_error_details = f"unable to traverse structure with traversal strategy input ---> {tstrategy}; argument must be a value from the following set: {[i for i in self._tstrategy_mapping.keys()]}..."
			raise ValueError(_error_details)

		_traversal_strat_callable = self._tstrategy_mapping[tstrategy]
		# return _traversal_strat_callable(self)
		return super().traverse(_traversal_strat_callable)

	@staticmethod
	def _traverse_depth_first(comp):
		def dfs(component):
			if component != comp:
				yield component
			if isinstance(component, Components):
				for child in component.components:
					yield from dfs(child)
		return dfs(comp)

	@staticmethod
	def _traverse_breadth_first(comp):
		def bfs(component):
			queue = deque([component])
			while queue:
				current = queue.popleft()
				if current != comp:
					yield current
				if isinstance(current, Components):
					for child in current.components:
						queue.append(child)
		
		return bfs(comp)


def test_main_1(tstrategy=1):
	from .utils import apply_color, bold_text, underline_text, center_text


	RANGE = 10
	POSSIBLE_TEST_DATA_VALS_4_LEAVES = [i for i in range(1, 50)]
	POSSIBLE_TEST_DATA_VALS_4_COMPOSITES = [i for i in range(51, 100)]

	_test_leaf_data_1 = random.choice(POSSIBLE_TEST_DATA_VALS_4_LEAVES)
	_test_leaf_data_2 = random.choice(POSSIBLE_TEST_DATA_VALS_4_LEAVES)
	_test_leaf_data_3 = random.choice(POSSIBLE_TEST_DATA_VALS_4_LEAVES)
	_test_leaf_data_4 = random.choice(POSSIBLE_TEST_DATA_VALS_4_LEAVES)
	_test_leaf_data_5 = random.choice(POSSIBLE_TEST_DATA_VALS_4_LEAVES)


	_test_composite_data_1 = random.choice(POSSIBLE_TEST_DATA_VALS_4_COMPOSITES)
	_test_composite_data_2 = random.choice(POSSIBLE_TEST_DATA_VALS_4_COMPOSITES)
	_test_composite_data_3 = random.choice(POSSIBLE_TEST_DATA_VALS_4_COMPOSITES)
	_test_composite_data_4 = random.choice(POSSIBLE_TEST_DATA_VALS_4_COMPOSITES)
	_test_composite_data_5 = random.choice(POSSIBLE_TEST_DATA_VALS_4_COMPOSITES)


	ROOT_ID = bold_text(apply_color(165, f"ROOT"))

	_temp_comps = []
	for i in range(1, RANGE + 1):
		CHILD_1_ID = apply_color(163, "CHILD_1")
		LEAF_1_ID = apply_color(161, f"LEAF_{i}")
		_LEAF_1_ID = f"{CHILD_1_ID}.{LEAF_1_ID}"
		_child_1_leaf = Component(_test_leaf_data_1, component_id=_LEAF_1_ID)
		_temp_comps.append(_child_1_leaf)
	_child_1 = Components(_test_composite_data_1, component_id=f"{ROOT_ID}.{CHILD_1_ID}")
	for i in _temp_comps:
		_child_1.add(i)
	_temp_comps = []

	LEAF_2_ID = apply_color(161, "LEAF_2")
	CHILD_2_ID = apply_color(163, "CHILD_2")
	_LEAF_2_ID = f"{CHILD_2_ID}.{LEAF_2_ID}"
	_child_2_leaf = Component(_test_leaf_data_2, component_id=_LEAF_2_ID)
	_child_2 = Components(_test_composite_data_2, component_id=f"{ROOT_ID}.{CHILD_2_ID}")
	_child_2.add(_child_2_leaf)

	LEAF_3_ID = apply_color(161, "LEAF_3")
	CHILD_3_ID = apply_color(163, "CHILD_3")
	_LEAF_3_ID = f"{CHILD_3_ID}.{LEAF_3_ID}"
	_child_3_leaf = Component(_test_leaf_data_3, component_id=_LEAF_3_ID)
	_child_3 = Components(_test_composite_data_3, component_id=f"{ROOT_ID}.{CHILD_3_ID}")
	_child_3.add(_child_3_leaf)

	LEAF_4_ID = apply_color(161, "LEAF_4")
	CHILD_4_ID = apply_color(163, "CHILD_4")
	_LEAF_4_ID = f"{CHILD_4_ID}.{LEAF_4_ID}"
	_child_4_leaf = Component(_test_leaf_data_4, component_id=_LEAF_4_ID)
	_child_4 = Components(_test_composite_data_4, component_id=f"{ROOT_ID}.{CHILD_4_ID}")
	_child_4.add(_child_4_leaf)

	LEAF_5_ID = apply_color(161, "LEAF_5")
	CHILD_5_ID = apply_color(163, "CHILD_5")
	_LEAF_5_ID = f"{CHILD_5_ID}.{LEAF_5_ID}"
	_child_5_leaf = Component(_test_leaf_data_5, component_id=_LEAF_5_ID)
	_child_5 = Components(_test_composite_data_5, component_id=f"{ROOT_ID}.{CHILD_5_ID}")
	_child_5.add(_child_5_leaf)



	_test_components_list = iter([_child_1, _child_2, _child_3, _child_4, _child_5])
	root = Root(100, component_id=ROOT_ID)

	for child in _test_components_list:
		root.add(child)

	print()
	print(root)
	for i in root.traverse(tstrategy):
		if i.is_composite:
			print(f"\t{i}")
		elif not i.is_composite:
			print(f"\t\t{i}")
	print()


	CHILD_1_ID = apply_color(163, "CHILD_1")
	# LEAF_1_ID = apply_color(161, f"LEAF_{int(RANGE / 2)}")
	LEAF_1_ID = apply_color(161, f"LEAF_{random.choice([i for i in range(1, 10)])}")
	test_id = f"{CHILD_1_ID}.{LEAF_1_ID}"
	_event_receiver = test_event_receiver(test_id)
	root.register("TEST_EVENT_IN_ORIGINAL_FUNCTION", _event_receiver)
	root.execute("TEST_EVENT_IN_ORIGINAL_FUNCTION")
	_test_id_comp = TEST_LIST.pop(0) if TEST_LIST else None
	print(f"COMPONENT ---> {_test_id_comp}")


def test_main_2(tstrategy=1):

	def _test_leaf_visitor_channel_closure(component):
		print(f"HELLO MOTO!!!!")
		print(f"COMPONENT ID: {component.component_id} ---> GOODBYE MOTO!!!!")
		print()

	def _test_leaf_receiver_closure(component):
		print(f"COMPONENT ID: {component.component_id} ---> GOODBYE MOTO!!!!")
		print(f"HEY HEY HEY HELLO MOTO!!!!")
		print()


	def _test_leaf_receiver_closure_2(component):
		print(f"COMPONENT ID: {component.component_id} ---> GOODBYE MOTO!!!!")
		print()


	VISITOR_ID = "TEST_VISITOR_CHANNEL"
	ROOT_ID = "[ROOT]"
	TEST_EVENT_ID = "TEST_EVENT_ID"
	TOTAL_LEAVES = 100000
	TOTAL_COMPOSITES = 34905
	# TEST_COMOPNENT_ID = f"test_leaf_{int((TOTAL_LEAVES + 1 if not TOTAL_LEAVES % 2 == 0 else TOTAL_LEAVES) / 2)}"
	TEST_COMOPNENT_ID = f"test_leaf_3"

	visitor_channel = VisitorChannel(visitor_id=VISITOR_ID)
	component_leaves = [Component(i, component_id=f"test_leaf_{i}") for i in range (1, TOTAL_LEAVES + 1)]
	composite_leaves = [Components(i, component_id=f"TEST_COMPOSITE_{i}") for i in range (1, TOTAL_COMPOSITES + 1)]

	count = 0
	_composites = []
	_component_leaves = component_leaves[:]
	while _component_leaves and count < len(composite_leaves):
		_next_comp_leaf_1 = _component_leaves.pop(0)
		if _next_comp_leaf_1.component_id == TEST_COMOPNENT_ID:
			_next_comp_leaf_1.register(f"{TEST_EVENT_ID}_2", _test_leaf_visitor_channel_closure)
		_next_comp_leaf_2 = _component_leaves.pop(1)
		if _next_comp_leaf_2.component_id == TEST_COMOPNENT_ID:
			_next_comp_leaf_2.register(f"{TEST_EVENT_ID}_3", _test_leaf_receiver_closure)
		_next_composite_leaf = composite_leaves.pop(composite_leaves.index(random.choice(composite_leaves)))
		_next_composite_leaf.add(_next_comp_leaf_1)
		_next_composite_leaf.add(_next_comp_leaf_2)
		_composites.append(_next_composite_leaf)
		count += 1

	# _test_component_leaf_half_of_total = component_leaves.pop(component_leaves.index("test_leaf_50"))
	root = Root(100, component_id=ROOT_ID)
	for comp in _composites:
		root.add(comp)

	# visitor_channel.register("test_leaf_1", _test_leaf_visitor_channel_closure)
	# print(_test_component_leaf_half_of_total)
	root.register(TEST_EVENT_ID, _test_leaf_receiver_closure)
	root.register(f"{TEST_EVENT_ID}_1", _test_leaf_receiver_closure_2)
	root.register(f"{TEST_EVENT_ID}_2", _test_leaf_receiver_closure_2)

	def _runtime_1():
		# print(root)
		for i in root.traverse(tstrategy):
			if i.is_composite:
				print(f"\t{i}")
			elif not i.is_composite:
				print(f"\t\t{i}")


	def _runtime_2():
		print(root)
		_test_component_leaf = [i for i in component_leaves if i.component_id == TEST_COMOPNENT_ID]
		if _test_component_leaf and isinstance(_test_component_leaf, list):
			_test_component_leaf = _test_component_leaf.pop(0)
			# print(f"EXECUTING COMPONENT ID: {TEST_COMOPNENT_ID}:")
			_test_component_leaf.execute(TEST_EVENT_ID)
			# _test_component_leaf.execute(f"{TEST_EVENT_ID}_1")
			# _test_component_leaf.execute(f"{TEST_EVENT_ID}_2")
			# _test_component_leaf.execute(f"{TEST_EVENT_ID}_3")
		print()
		# print(f"EXECUTING ROOT COMPONENT")
		# print(f"EXECUTING EVENT --->", end=" ")
		# print(root.execute(f"{TEST_EVENT_ID}_1"))
		# root.execute(f"{TEST_EVENT_ID}_2")
		# root.execute(f"{TEST_EVENT_ID}_3")


	print()
	# _runtime_1()
	_runtime_2()
	print()


# @profile_callable(sort_by=SortBy.TIME)
def main():
	TRAVERSAL_STRATEGY = TraversalStrategy.BFS

	MAX = 100
	_counter = 1
	_use = TRAVERSAL_STRATEGY
	while _counter <= MAX:
		print(f"TRAVERSAL STRATEGY ---> {_use}")
		test_main_1(tstrategy=_use)
		test_main_2(tstrategy=_use)
		_use ^= 3
		_counter += 1
	print(flush=True)


if __name__ == "__main__":
	main()
