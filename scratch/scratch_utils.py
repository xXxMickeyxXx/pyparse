from uuid import uuid1
from pathlib import Path

from pyprofiler import profile_callable, SortBy


def generate_id(*, prefix=None, suffix=None, uuid_factory=uuid1, uuid_type=None):
    uuid_obj = uuid_factory()

    if uuid_type is None:
        uuid_obj = str(uuid_obj)
        if prefix is not None:
            uuid_obj = str(prefix) + uuid_obj
        if suffix is not None:
            uuid_obj = uuid_obj + str(suffix)
    else:
        uuid_obj = uuid_type(uuid_obj)

    return uuid_obj


def copy_items(items, *, deepcopy=False):
    return [i.copy(deepcopy=deepcopy) for i in items]


def copy_item(item, *, deepcopy=False):
    return item.copy(deepcopy=deepcopy)


def read_source(source_file):
    _filepath = source_file.get()
    if not isinstance(_filepath, Path):
        _filepath = Path(_filepath)
    _file_data = ""
    with open(_filepath, "r") as in_file:
        _file_data = in_file.read()

    if not bool(_file_data):
        # TODO: create and raise custom error here
        _error_details = f"Error Reading Source File Contents -- unable to read data contained within file @: {filepath}"
        raise RuntimeError
    return [i for i in _file_data.split("\n") if i]


def countdown_helper(start, stop=1):
    _stack = [i for i in range(stop, start+1)]
    while _stack:
        _number = _stack.pop(-1)
        yield _number


if __name__ == "__main__":
    pass
