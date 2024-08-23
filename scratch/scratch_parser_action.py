import pysynchrony
from .scratch_cons import PyParseEventID


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


if __name__ == "__main__":
	pass
