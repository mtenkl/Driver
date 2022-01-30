import unittest
import trajectory
from trajectory import Node
import numpy as np
from matplotlib import pyplot as plt

class TestTrajectory(unittest.TestCase):


    def test_max_len(self):

        traj = trajectory.Trajectory(100, 0.1)

        for i in range(200):
            traj.add(Node(i, i))

        self.assertEqual(len(traj), traj.MAX_LEN)


    def test_min_dist(self):

        traj = trajectory.Trajectory(10, 2)

        traj.add(Node(0, 0))
        self.assertEqual(len(traj), 1)
        traj.add(Node(0, 3))
        self.assertEqual(len(traj), 2)
        traj.add(Node(0, 4))
        self.assertEqual(len(traj), 2)
        traj.add(Node(0, 5))
        self.assertEqual(len(traj), 3)

    def test_trajectory(self):

        traj = trajectory.Trajectory(200)

        x = np.linspace(0, 50, 1000)
        y = np.sin(x)
        theta = np.cos(x)

        for _x, _y, _theta in zip(x, y, theta):
            traj.add(Node(_x, _y, _theta))

        t_x = list()
        t_y = list()
        while len(traj) > 0:
            p = traj.pop()
            t_x.append(p.x)
            t_y.append(p.y)
        
        plt.plot(t_x, t_y, "o")
        plt.plot(x,y,"r--")
        plt.show()

    def test_iteration(self):

        traj = trajectory.Trajectory(200)

        x = np.linspace(0, 50, 100)
        y = np.sin(x)
        theta = np.cos(x)

        for _x, _y, _theta in zip(x, y, theta):
            traj.add(Node(_x, _y, _theta))

        t_x = list()
        t_y = list()       

        for node in traj:
            t_x.append(node.x)            
            t_y.append(node.y)

        self.assertEqual(len(t_x), len(traj._buffer))

        plt.plot(t_x, t_y, "o")
        plt.plot(x,y,"r--")
        plt.show()

if __name__ == "__main__":

    unittest.main()