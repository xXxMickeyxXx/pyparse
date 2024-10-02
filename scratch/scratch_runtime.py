"""
	_____QUICK-NOTES_____

		A.) 

"""


from .scratch_runtime_init import parse_main


def main():
	print()
	parse_main()
	print()


if __name__ == "__main__":
    pass


# from pyprofiler import profile_callable, SortBy


# class State:
# 	def __init__(self, production, dot_position, start_position):
# 		self.production = production  # production is a tuple (LHS, RHS) like ("E", ["E", "*", "B"])
# 		self.dot_position = dot_position  # position of the dot (•) in the RHS
# 		self.start_position = start_position  # start position of this state in the input

# 	def next_symbol(self):
# 		"""Return the symbol after the dot if there is one."""
# 		if self.dot_position < len(self.production[1]):
# 			return self.production[1][self.dot_position]
# 		return None

# 	def is_complete(self):
# 		"""Check if this state is complete (dot has reached the end)."""
# 		return self.dot_position == len(self.production[1])

# 	def __repr__(self):
# 		lhs, rhs = self.production
# 		rhs = list(rhs)  # Make sure it's mutable for displaying
# 		rhs.insert(self.dot_position, "•")
# 		return f"{lhs} -> {' '.join(rhs)}, [{self.start_position}]"

# 	def __eq__(self, other):
# 		return self.production == other.production and self.dot_position == other.dot_position and self.start_position == other.start_position


# class EarleyParser:
# 	def __init__(self, grammar):
# 		self.grammar = grammar  # grammar is a dict like {"E": [["E", "*", "B"], ["E", "+", "B"], ["B"]], "B": [["0"], ["1"]]}
# 		self.chart = []  # chart will store sets of states at each position in the input

# 	def predict(self, state, position):
# 		"""Predict new states for non-terminals."""
# 		non_terminal = state.next_symbol()
# 		if non_terminal and non_terminal in self.grammar:
# 			for production in self.grammar[non_terminal]:
# 				print(f"PRODUCTION:")
# 				print(f"\t{production}")
# 				print()
# 				new_state = State((non_terminal, production), 0, position)
# 				print(f"NEW STATE:")
# 				print(new_state)
# 				if new_state not in self.chart[position]:
# 					print(f"ADDING TO CHART @ POSITION ---> {position}")
# 					self.chart[position].append(new_state)
# 				print()

# 	def scan(self, state, position, token):
# 		"""Scan terminal symbols (consume tokens from input)."""
# 		if state.next_symbol() == token:
# 			new_state = State(state.production, state.dot_position + 1, state.start_position)
# 			self.chart[position + 1].append(new_state)

# 	def complete(self, state, position):
# 		"""Complete a state and propagate it to earlier states."""
# 		if state.is_complete():
# 			start_position = state.start_position
# 			for prev_state in self.chart[start_position]:
# 				if prev_state.next_symbol() == state.production[0]:
# 					new_state = State(prev_state.production, prev_state.dot_position + 1, prev_state.start_position)
# 					self.chart[position].append(new_state)

# 	def parse(self, tokens):
# 		"""Parse a sequence of tokens."""
# 		# Initialize the chart
# 		self.chart = [[] for _ in range(len(tokens) + 1)]
# 		self.chart[0].append(State(("S'", ["E"]), 0, 0))  # Add the start production S' -> E

# 		for i in range(len(tokens) + 1):
# 			for state in self.chart[i]:
# 				if not state.is_complete():
# 					if state.next_symbol() in self.grammar:
# 						self.predict(state, i)
# 					elif i < len(tokens):
# 						self.scan(state, i, tokens[i])
# 				else:
# 					self.complete(state, i)

# 		# Check if the final state (S' -> E•) is in the last chart set
# 		final_state = State(("S'", ["E"]), 1, 0)
# 		return final_state in self.chart[len(tokens)]


# @profile_callable(sort_by=SortBy.TIME)
# def main():
# 	# Example grammar definition
# 	grammar = {
# 		"E": [["E", "*", "B"], ["E", "/", "B"], ["E", "+", "B"], ["E", "-", "B"], ["B"]],
# 		"B": [["number"], ["C"]],
# 		"C": [["(", "E", ")"]],
# 		"number": [["NUMBER"]]
# 	}




# 	# Example input
# 	input_tokens_1 = ["(", "(", "1", "/", "1", "*", "21", "+", "100021", "*", "(", "123", ")", "+", "1024", ")", "+", "(", "3", "*", "2", ")", "-", "1", ")", "+"]
# 	input_tokens_2 = input_tokens_1.copy()
# 	for i in range(3):
# 		input_tokens_1.extend(input_tokens_2)

# 	input_tokens_1.pop(-1)

# 	for i in range(len(input_tokens_1)):
# 		_token = input_tokens_1[i]
# 		if _token.isdigit():
# 			input_tokens_1[i] = "NUMBER"
# 	print(f"INPUT TOKENS:")
# 	print()
# 	for i in input_tokens_1:
# 		print(i)
# 	print()
# 	print()

# 	# Run the Earley parser
# 	parser = EarleyParser(grammar)
# 	if parser.parse(input_tokens_1):
# 		print("The input is accepted by the grammar.")
# 	else:
# 		print("The input is not accepted by the grammar.")

# 	print()

# 	for i in parser.chart:
# 		print(i)
# 	print()
# 	print()
