from abc import ABC, abstractmethod
from typing import List


class Component(ABC):

    def __init__(self, id: str | int):
        self._id = id

    @property
    def id(self) -> str | int:
        return self._id

    @id.setter
    def id(self, val: str | int) -> None:
        _error_details = f"unable to update 'id' attribute as it's bound to the lifetime of the object..."
        raise AttributeError(_error_details)

    @abstractmethod
    def get_size(self) -> int:
        raise NotImplementedError


class File(Component):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self.size = size

    @property
    def name(self):
        return self.id

    def get_size(self) -> int:
        return self.size


class Folder(Component):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.children: List["Folder", File] = []

    @property
    def name(self):
        return self.id

    def add(self, item: "Folder" | File) -> None:
        self.children.append(component)

    def remove(self, id):
        _len_children = len(self.children)
        for i in range(_len_children):
            if self.children[i].id == id:
                return self.children.pop(i)
        else:
            _error_details = f"unable to remove component bound to ID: {id} as it does not exists within this object..."
            raise ValueError(_error_details)    

    def get_size(self) -> int:
        total_size = 0
        stack = [self]

        while stack:
            current = stack.pop()
            if isinstance(current, File):
                total_size += current.get_size()
            elif isinstance(current, Folder):
                stack.extend(current.children)
        return total_size

    def display(self):

        for child in self.children:
            if isinstance(child, self.__class__):


def main():
    file1 = File(100)
    file2 = File(200)
    file3 = File(300)

    folder1 = Folder()
    folder1.add(file1)
    folder1.add(file2)

    folder2 = Folder()
    folder2.add(folder1)
    folder2.add(file3)

    # Getting sizes
    print(f"Size of file1: {file1.get_size()}")
    print(f"Size of folder1: {folder1.get_size()}")
    print(f"Size of folder2: {folder2.get_size()}")


if __name__ == "__main__":
    pass
