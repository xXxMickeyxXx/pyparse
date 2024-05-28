from ...errors import TimeOutError


class Tokenizer:

	def __init__(self, input=None):
		self._input = input
		self._pointer = 0
		self._tokens = []
		self._input_len = len(self._input) if self._input is not None else 0


	@property
	def can_consume(self):
		return self._pointer < self._input_len

	@property
	def tokens(self):
		return self._tokens

	@property
	def current_char(self):
		_input = self._input
		_pointer = self._pointer
		return _input[_pointer] if _input and self.can_consume else None

	def set_input(self, input):
		self._input = input
		self._input_len = len(input)

	def reset(self):
		self._pointer = 0
		self._tokens = []
		self._input = None
		self._input_len = 0

	def peek(self):
		if self.can_consume:
			_tmp_pointer = self._pointer + 1
			if (_tmp_pointer) < self._input_len:
				return self._input[_tmp_pointer]
		return None

	def advance(self):
		if self.can_consume:
			self._pointer += 1

	def consume(self):
		_current_char = self.current_char
		self.advance()
		return _current_char

	def consume_until(self, condition_callable, timeout=None):
		_is_expired = False
		_start_time = None
		_elapsed_time = None
		_tmp_word = ""
		while True:
			if timeout is not None:
				if _start_time is None:
					_start_time = time.time() if timeout is not None else None
				_elapsed_time = time.time() - _start_time
				if timeout - _elapsed_time <= 0:
					# TODO: create and raise custom error here
					_error_details = f"call to 'consume_until' has timed out..."
					raise TimeOutError(details=_error_details)
			if not condition_callable(self):
				_consume = self.consume()
				if _consume is None:
					break
				_tmp_word += _consume
				break
			_tmp_word += self.consume()
		if len(_tmp_word) > 0:
			return _tmp_word

	def expect(self, value, *, consume=False):
		_peek_val = self.peek()
		if _peek_val is not None and _peek_val == value:
			if consume:
				return self.consume()
			return True
		return False

	def add_token(self, token):
		self._tokens.append(token)

	def tokenize(self):
		raise NotImplementedError


if __name__ == "__main__":
	pass
