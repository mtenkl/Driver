import imp
import unittest
import pid
import numpy as np
from matplotlib import pyplot as plt

class Steering():


    def __init__(self) -> None:
        self.steering_angle = 0


    def steer(self, steering_speed, dt):

        self.steering_angle += steering_speed * dt
        return self.steering_angle

class TestPID(unittest.TestCase):


    def test_pid(self):

        steering = Steering()
        controller = pid.PID(10,10,0,0, 100)

        time = np.linspace(0,10,100)

        x = list()
        y = list()
        z = list()
        s = 0
        target = 20

        for t in time:
            
            o = controller.output(s, target, 0.1)
            s = steering.steer(o, 0.1)

            x.append(t)
            y.append(o)
            z.append(s)

        plt.plot(x,y, "b")
        plt.plot(x,z,"r")
        plt.show()