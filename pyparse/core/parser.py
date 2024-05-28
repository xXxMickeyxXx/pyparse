class Parser:

	# TODO: determine the usage and/or inlusion of a static parsing table; the option
	#       to use one should at the very least be there. Perhaps in one of the 
	#       implementations, that become the input into the 'Parser' constructor (or
	#       the abstract class related to the bridge pattern)

	def __init__(self, parser_imp=None):
		self._parser_imp = parser_imp

	def set_parser(self, parser_imp):
		self._parser_imp = parser_imp

	def parse(self, input):
		return self._parser_imp.parse(input)


if __name__ == "__main__":
	pass
