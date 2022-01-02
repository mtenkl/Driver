import collections
import numpy as np



class Trajectory(object):

    def __init__(self, max_len:int, min_dist:float) -> None:
        
        self.MAX_LEN = max_len
        self.MIN_DIST = min_dist

        self.buffer = collections.deque(maxlen=self.MAX_LEN)
        self.last = None

    def add(self, position: tuple):
        
        if len(self.buffer) > 0:
            if np.linalg.norm(self.last-np.array(position)) >= self.MIN_DIST:
                self.last = position
                self.buffer.append(position)
        else:
            self.buffer.append(position)
            self.last = np.array(position)

    def pop(self):
        return self.buffer.pop()

    def __len__(self):
        return len(self.buffer)

