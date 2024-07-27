from pysynchrony import (
	PySynchronyEventLoop,
	PySynchronyPort,
	PySynchronyEvent
)

from .scratch_utils import generate_id


class ParserContext:

	def __init__(self, init_state=None, parser=None, context_id=None):
		self._context_id = context_id or generate_id()
		self._parser = parser
		self._event_loop = None
		self._channel = None
		self._port_mapping = {}
		self._command_mapping = {}
		self._executor = self._default_executor()

		self._state = init_state
		self._event = None

		self.initialize()

	@property
	def context_id(self):
		return self._context_id

	@property
	def event_loop(self):
		if self._event_loop is None:
			self._event_loop = self.event_loop_factory()
		return self._event_loop

	@property
	def parser(self):
		if self._parser is None:
			# TODO: create and raise custom error here
			_error_details = f"unable to access 'parser' attribute as one has yet to be associated with this instance of '{self.__class__.__name__}'..."
			raise AttributeError(_error_details)
		return self._parser

	@property
	def channel(self):
		if self._channel is None:
			self._channel = self.event_loop.channel(self.context_id)
		return self._channel

    def add_port(self, port, port_id=None, overwrite=False):
    	_port_id = port.port_id if hasattr(port, "port_id") else (port_id if port_id else generate_id())
    	if _port_id not in self._port_mapping or overwrite:
    		self._port_mapping.update({_port_id: port})

    def register_handler(self, port_id, handler, handler_id=None, overwrite=False):
    	_port = self._port_mapping


	def initialize(self):
		raise NotImplementedError

	def submit_command(self, command, command_id=None, execution_context=None):
		_command_id = command_id or generate_id()
		if _command_id not in self._command_mapping:
			self._command_mapping.update({_command_id: command})

	def schedule_command(self, command):
		_port = 


	def state(self):
		return self._state

	def event(self):
		_retval = None
		if self._event is not None:
			_retval = self._event
			self._event = None
		return _retval

	def set_state(self, state):
		self._state = state

	def set_event(self, event):
		if self._event is not None:
			# TODO: create and raise custom error here
			_error_details = f"unable to set event ID: {event.event_id} as event ID: {self._event.event_id} is awaiting further handling..."
			raise RuntimeError(_error_details)
		self._event = event

	def set_parser(self, parser):
		# TODO: create and raise custom error here indicating that only one parser
		# 		instance, and at most one time, can be set/bounded to the 'ParserContext'
		# 		instance/object, during it's lifetime (i.e. the 'ParserContext')
		if self._parser is not None:
			_error_details = f"unable to set parser as one has already been associated with this instance of '{self.__class__.__name__}'..."
			raise RuntimeError(_error_details)
		self._parser = parser

	def event_loop_factory(self):
		return PySynchronyEventLoop(loop_id=None)

	def register(self, signal_id, receiver=None, receiver_id=None):
		return self.channel.register(signal_id, receiver=receiver, receiver_id=receiver_id)

	def emit(self, event):
		# NOTE: event object's 'event_id' must match the signal ID that was registered
		# 		(possibly alongside the receiver)

		# TODO: either get rid of this method, and have emission of events be handled
		# 		using the concept of ports or revert back to passing an event object
		# 		(meaning) event receivers must be declared with the event parameter.
		# 		The other idea was to instead, pass the context over to the receiver,
		# 		have the context update a '_current_event' field (or something similar),
		# 		and since the context will go to the receiver, it can access the event
		# 		as needed. I'm leaning more towards using ports and have the event loop
		# 		handle resolving the/an event step (per execution cycle). I could also
		# 		make it so that the receiver gets the desired event, and the field/member
		# 		resets itself back to 'None', so that way it won't get emitted twice; should
		# 		a different/another component need to access that specific event, it will then
		# 		have to be propagated onward, from the receiver

		self.set_event(event)
		return self.channel.emit(event.event_id, self)

	@staticmethod
	def create_event(event_id, **data):
		return PySynchronyEvent(event_id, **data)

	@staticmethod
	def _default_executor(command, context):
		pass


if __name__ == "__main__":


	def parser_context_test_main():


		def _test_receiver_1(context):
			_new_event = context.event()
			print()
			print(f"NEW EVENT WITHIN TEST RECEIVER 1 ---> {_new_event}")
			print(f"HELLO, {_new_event.data('name', default='JOSEPHINA JOSINA').upper()}...HOW ARE YOU!?!")
			print(f"EVENT HAS CLEARED CONTEXT ---> {context._event is None}")


		def _test_receiver_2(context):
			_new_event = context.event()
			print()
			print(f"NEW EVENT WITHIN TEST RECEIVER 1 ---> {_new_event}")
			print(f"HELLO, {_new_event.data('swearing', default='SHITTTTTT').upper()}...HOW ARE YOU!?!")
			print(f"EVENT HAS CLEARED CONTEXT ---> {context._event is None}")


		_throwaway_obj = object()
		_test_parser_context = ParserContext(parser=_throwaway_obj)
		_test_parser_context.register("TEST_EVENT_1", _test_receiver_1)
		_test_parser_context.register("TEST_EVENT_2", _test_receiver_2)

		_event_1 = ParserContext.create_event("TEST_EVENT_1", name="MICHAEL MCKEVITT DRURY III", swearing="SHIT MC-MUFFIN!")
		_event_2 = ParserContext.create_event("TEST_EVENT_2", swearing="CUNT BAG MOTHER FUCKER", name="TILLY TILLERSON")

		print()
		print(f"EMITTING 'TEST_EVENT_1'...")
		_test_parser_context.emit(_event_1)
		print()

		print()
		print(f"EMITTING 'TEST_EVENT_2'...")
		_test_parser_context.emit(_event_2)
		print()


	parser_context_test_main()