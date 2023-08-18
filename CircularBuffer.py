
class CircularBuffer:

    def __init__(self, dimension: int):
        self._buffer = bytearray(dimension)
        self._head = 0
        self._tail = 0
        self._size = 0

    def isFull(self) -> bool:
        return self._size == len(self._buffer)

    def isEmpty(self) -> bool:
        return self._size == 0

    def push(self, element: int):
        self._buffer[self._tail] = element
        if not self.isFull():
            self._size += 1
        self._tail = (self._tail + 1) % len(self._buffer)
        if self._size == len(self._buffer):
            self._head = self._tail

    def pop(self) -> (int, None):
        if self.isEmpty():
            return None
        element = self._buffer[self._head]
        self._head = (self._head + 1) % len(self._buffer)
        self._size -= 1
        return element

    def top(self):
        if self.isEmpty():
            return None
        return self._buffer[self._head]

    def insert(self, to_be_copied: [int]):
        copy_index = 0
        if len(self._buffer) < len(to_be_copied):
            copy_index = len(to_be_copied) - len(self._buffer)

        for i in range(copy_index, len(to_be_copied)):
            self.push(to_be_copied[i])

    def getSize(self):
        return self._size

    def __getitem__(self, index):
        return self._buffer[(self._head+index) % len(self._buffer)]

    def ptr(self):
        return self._buffer


if __name__ == "__main__":

    cb = CircularBuffer(3)
    print(cb.isEmpty())
    cb.push(10)
    cb.push(20)
    cb.push(30)
    print(cb.isFull())
    print(cb[1])
    print(cb.top())
    cb.pop()
    print(cb.ptr())
    print(cb.isFull())
    print(cb.isEmpty())
