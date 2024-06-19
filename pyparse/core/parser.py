class Parser:

	# TODO: add higher level operations that are contained in any/all parser types

	# TODO: determine the usage and/or inlusion of a static parsing table; the option
	#       to use one should at the very least be there. Perhaps in one of the 
	#       implementations, that become the input into the 'Parser' constructor (or
	#       the abstract class related to the bridge pattern)

	def __init__(self, parser=None):
		self._parser = parser

	def set(self, parser):
		self._parser = parser

	def parse(self, input):
		return self._parser.parse(input)


if __name__ == "__main__":
	pass
