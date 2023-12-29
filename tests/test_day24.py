from unittest import TestCase

from aoc23.day24 import Day24

INPUT='''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''

class TestDay24(TestCase):
  def test_first_star(self):
    solver = Day24()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 0)

  def test_second_star(self):
    solver = Day24()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 47)

# vim: ts=2:sw=2:et
