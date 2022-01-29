import numpy as np

class PID():


    def __init__(self, kp, ki, kd, clip_min=None, clip_max=None) -> None:
        pass

        self.KP = kp
        self.KI = ki
        self.KD = kd

        self.clip_max = clip_max
        self.clip_min = clip_min

        self._output = 0

    def output(self, current:float, target:float, dt: float) -> float:

        error = target - current

        p = self.KP * error
        i = self.KI * error * dt
        d = self.KD * error / dt

        self._output = np.clip(p + i + d, self.clip_min, self.clip_max)

        return self._output
