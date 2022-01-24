# python -m unittest scanner-tests.py

import unittest

from solutions import Scanner


class TestScannerMethods(unittest.TestCase):

    def test_all_zeros(self):
        s = Scanner(123, [(0, 0, 0)])
        expected_pts = [(0, 0, 0)]
        for o in s.orientations:
            for rotated_pt in o:
                self.assertIn(rotated_pt, expected_pts)

    def test_two_zeros(self):
        s = Scanner(123, [(1, 0, 0)])
        expected_pts = [
            (1, 0, 0),  (0, 0, 1), (-1, 0, 0), (0, 0, -1),
            (0, 1, 0),  (0, 1, 0), (0, 1, 0), (0, 1, 0),
            (0, 0, 1),  (1, 0, 0), (-1, 0, 0), (0, 0, -1),
            (-1, 0, 0), (0, 0, 1), (1, 0, 0), (0, 0, -1), 
            (0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0), 
            (0, 0, -1), (-1, 0, 0), (0, 0, 1), (1, 0, 0)
        ]
        for o in s.orientations:
            for rotated_pt in o:
                self.assertIn(rotated_pt, expected_pts)

    def test_one_zero(self):
        s = Scanner(123, [(1, 10, 0)])
        expected_pts = [
            (1, 10, 0),   (-1, 10, 0),  (0, 10, 1),   (0, 10, -1),
            (-10, 1, 0),  (10, 1, 0),   (0, 1, -10),  (0, 1, 10),
            (-1, -10, 0), (1, -10, 0),  (0, -10, -1), (0, -10, 1),
            (10, -1, 0),  (-10, -1, 0), (0, -1, 10),  (0, -1, -10), 
            (1, 0, -10),  (-1, 0, 10),  (10, 0, 1),   (-10, 0, -1), 
            (1, 0, 10),   (-1, 0, -10), (-10, 0, 1),  (10, 0, -1)  # negate x & z, flip & negate x, flip & negate z
        ]
        for o in s.orientations:
            for rotated_pt in o:
                self.assertIn(rotated_pt, expected_pts)
    
    def test_no_zeros(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
