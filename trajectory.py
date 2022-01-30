import collections
import numpy as np
import math



class Node():

    def __init__(self, x:int, y:int, theta:float=None) -> None:
        self._x = x
        self._y = y
        self._theta = theta

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def theta(self):
        return self._theta

    def distance(self, position):

        return math.hypot(self._x - position.x, self._y - position.y)




class Trajectory(object):

    def __init__(self, max_len:int, min_dist:float = None) -> None:
        
        self.MAX_LEN = max_len
        self.MIN_DIST = min_dist

        self._buffer = collections.deque(maxlen=self.MAX_LEN)
        self._last = None

    def add(self, position: Node):
        """
        Add new position to buffer.
        @position: Dictionary containing x, y, theta
        """
        
        if len(self._buffer) > 0:
            if self.MIN_DIST is not None:
                if self._last.distance(position) >= self.MIN_DIST:
                    self._last = position
                    self._buffer.append(position)
            else:
                self._buffer.append(position)
        else:
            self._buffer.append(position)
            self._last = position


    def pop(self):
        return self._buffer.pop()

    def __len__(self):
        return len(self._buffer)

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self) -> Node:

        if self._n < len(self._buffer):
            result = self._buffer[self._n]
            self._n += 1
            return result
        else:
            raise StopIteration