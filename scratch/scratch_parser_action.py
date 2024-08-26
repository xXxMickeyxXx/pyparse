from abc import ABC, abstractmethod

import pysynchrony

from .scratch_parser_command import ParserCommand
from .scratch_cons import (
	PyParseEventID,
	ParserActionType
)


_EXIT_OK_ = set()


def sleeper(count):
	yield Sleep(count)


def countdown(length=5, rate=1, step=1):
	_EXIT_OK_.add(True)

	print(f"PROGRAM WILL EXIT IN...")
	for i in range(1, length+1)[::-1]:
		_time_unit = "SECOND...." if i == 1 else "SECONDS..."
		print(f"{i} {_time_unit}")
		yield Sleep(rate)
	print(f"EXITING PROGRAM...")
	_new_task = yield CreateTask(lambda name: print(f"HELLO {name}!!!"), "MICKEY MOUSE")
	yield pysynchrony.AwaitTask(_new_task)
	yield pysynchrony.EmitEvent(PyParseEventID.ON_QUIT)
	return 10


def close_at_finish(rate=.5):
	_task_id = yield pysynchrony.GetTaskID()
	yield pysynchrony.Sleep(rate)
	_remaining_tasks = yield pysynchrony.RemainingTasks()
	if (_task_id in _remaining_tasks and len(_task_id) <= 1) and len(_EXIT_OK_) >= 1:
		yield pysynchrony.EmitEvent(PyParseEventID.ON_QUIT)
		return
	yield pysynchrony.CreateTask(close_at_finish, rate=rate)


class ParserActionCommand(ParserCommand):

	def __init__(self, action_type, command_id=None):
		super().__init__(command_id=command_id)
		self._action_type = action_type
		if action_type not in [i for i in ParserActionType]:
			_error_details = f"unable to instantiate command ID: {self.command_id} of command class: {self.__class__.__name__} as '{action_type}' is not a valid 'action_type':..."
			raise TypeError(_error_details)

	@abstractmethod
	def execute(self):
		raise NotImplementedError


if __name__ == "__main__":
	pass
