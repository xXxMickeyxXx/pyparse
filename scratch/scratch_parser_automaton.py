class ParserAutomaton:
	
	def __init__(self, parser=None):
		self._parser = parser

	@property
	def parser(self):
		if self._parser is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access 'parser' field as one has not yet been associated with instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._parser

	def set_parser(self, parser):
		if self._parser is None:
			self._parser = parser

	def reset(self):
		self._parser = None


if __name__ == "__main__":
    pass
