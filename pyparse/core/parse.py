from abc import abstractmethod


class Parse:
	"""Encapsulates both the state and parse result object for a given input.
	The motive is as follows:
		
		1. Provides a sort of 'future' object, in the event that concurrency
		is added to this model
		
		2. Allows the parser implementation to switch parse contexts for different
		parses, at different times for whatever reason, making it so that you don't
		have to create and use multiple parser instances to achieve the desired
		result, which ideally reduces the memory footprint of this parsing system

		3. Gives the parsing implementation(s) the freedom to perform it's work in
		any way that it see's fit without being tied to object(s) that the client
		interacts with.

	The parser will always 

	"""

	__slots__ = ("_parse_id", "_input_counter", "_input")

	def __init__(self, parse_id=None):
		self._parse_id = parse_id
		self._input_counter = 0
		self._input = None
		self._output = None

	@property
	def parse_id(self):
		return self._parse_id

	@parse_id.setter
	def parse_id(self, val):
		# TODO: create and raise custom error here
		_error_details = f"unable to update 'parse_id' attribute; once the '{self.__class__.__name__}' instance is created and assigned the ID (via the value passed to the 'parse_id' parameter, upon instantiation), it remains as such for the duration of it's lifetime..."
		raise AttributeError(_error_details)

	@property
	def input(self):
		if self._input is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access 'input' as one has not yet been associated with this instance..."
			raise RuntimeError
		return self._input

	def bind(self, input):
		if self._input is not None:
			# TODO: create and raise custom error here
			_error_details = f"unable to bind an input to this object, as one has been binded previously..."
			raise RuntimeError(_error_details)
		self._input = input

	def get(self):
		# NOTE: should get the resulting output produced by the parser, either part of
		# 		or the whole, depending on parser implementation (need to ensure this
		# 		is consistent across different implementation boundries)
		raise NotImplementedError


if __name__ == "__main__":
	pass
