import copy


class MarkerSymbol:

	# NOTE: implementing this class in order to ensure that the marker symbol logic
	# 		that exists within other implementations (such as'GrammarRule') aren't
	# 		messed up when the same symbol is used within the grammar itself

	__slots__ = ("_char",)

	def __init__(self, char: str):
		self._char = char

	@property
	def char(self):
		return self._char

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return self.char

	def __eq__(self, other):
		return isinstance(self, type(other)) and (self.char == other.char)

	def __hash__(self):
		return hash(self.char)

	def copy(self, *, deepcopy=False):
		_cls_type = type(self)
		return self._deepcopy(_cls_type) if deepcopy else self._copy(_cls_type)

	def _copy(self, cls_type):
		return cls_type(copy.copy(self.char))

	def _deepcopy(self, cls_type):
		return cls_type(copy.deepcopy(self.char))


if __name__ == "__main__":
	pass
