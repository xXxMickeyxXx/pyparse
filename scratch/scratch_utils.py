from uuid import uuid1


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


class CircularBuffer:

    def __init__(self, max_size):
        self.max_size = max_size
        self.buffer = [None] * max_size
        self.head = 0
        self.tail = 0
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.max_size

    def enqueue(self, item):
        if self.is_full():
            # TODO: create and raise custom error here
            raise IndexError("Buffer is full")
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % self.max_size
        self.size += 1

    def dequeue(self, default=None):
        if self.is_empty():
            return default
        item = self.buffer[self.head]
        self.head = (self.head + 1) % self.max_size
        self.size -= 1
        return item

    def peek(self):
        if self.is_empty():
            # TODO: create and raise custom error here
            raise IndexError("Buffer is empty")
        return self.buffer[self.head]

    def clear(self):
        self.head = 0
        self.tail = 0
        self.size = 0
        self.buffer = [None] * self.max_size


if __name__ == "__main__":
    pass
