from unittest import TestCase

from aoc23.day09 import Day09

INPUT="""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

class TestDay09(TestCase):
  def test_first_star(self):
    solver = Day09()
    solver.presolve(INPUT)
    self.assertEqual(114, solver.solve_first_star())

  def test_second_star(self):
    solver = Day09()
    solver.presolve(INPUT)
    self.assertEqual(2, solver.solve_second_star())

# vim: ts=2:sw=2:et
