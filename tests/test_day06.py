from unittest import TestCase

from aoc23.day06 import Day06

INPUT="""Time:      7  15   30
Distance:  9  40  200
"""

class TestDay06(TestCase):
  def test_part1(self):
    solver = Day06()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 288)

  def test_part2(self):
    solver = Day06()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 71503)

# vim: ts=2:sw=2:et
