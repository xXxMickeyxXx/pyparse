from ...library import PySynchronyEventLoop
from ...errors import TimeOutError


class Tokenizer:

	def __init__(self, input=None):
		self._input = input
		self._pointer = 0
		self._tokens = []
		self._input_len = len(self._input) if self._input is not None else 0
		self._event_loop = PySynchronyEventLoop(loop_id=None)


	@property
	def can_consume(self):
		return self._input is not None and self._pointer < self._input_len

	@property
	def current_char(self):
		_input = self._input
		_pointer = self._pointer
		return _input[_pointer] if _input and self.can_consume else None

	def on_loop(self, handler, handler_id=None):
		self._event_loop.on_loop(handler, handler_id=handler_id)

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

	def push_token(self, token, ):
		# TODO: consider adding the 'block=False, timeout=None' params, like how the
		# 		built-in 'Queue' object does it
		self._tokens.append(token)

	def tokens(self):
		return self._tokens

	def pop_token(self, idx=-1):
		return self._tokens.pop(idx)

	def token_at(self, index):
		if index >= self._input_len:
			# TODO: create and raise custom error here
			_error_details = f"unable to access token at index: {index} as it exceeds the bounds of tokens container..."
			raise IndexError(_error_details)
		return self._tokens[index]

	def token_range(self, *slice_args):
		_slicer = slice(*slice_args)
		return self._tokens[_slicer]

	def quit(self):
		self._event_loop.quit()

	def tokenize(self):
		self._event_loop.run()
		return self.tokens()


if __name__ == "__main__":
	pass
