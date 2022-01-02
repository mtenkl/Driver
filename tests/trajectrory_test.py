import unittest
import trajectory

class TestTrajectory(unittest.TestCase):


    def test_max_len(self):

        traj = trajectory.Trajectory(100, 0.1)

        for i in range(200):
            traj.add((i, i))

        self.assertEqual(len(traj), traj.MAX_LEN)


    def test_min_dist(self):

        traj = trajectory.Trajectory(10, 2)

        traj.add((0, 0))
        self.assertEqual(len(traj), 1)
        traj.add((0, 3))
        self.assertEqual(len(traj), 2)
        traj.add((0, 4))
        self.assertEqual(len(traj), 2)
        traj.add((0, 5))
        self.assertEqual(len(traj), 3)



if __name__ == "__main__":

    unittest.main()