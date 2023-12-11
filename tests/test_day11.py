from unittest import TestCase

from aoc23.day11 import Day11

INPUT="""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

class TestDay11(TestCase):
  def test_first_star(self):
    solver = Day11()
    solver.presolve(INPUT)
    self.assertEqual(374, solver.solve_first_star())

  def test_second_star(self):
    solver = Day11()
    solver.presolve(INPUT)
    self.assertEqual(1030, solver.solve(10))
    self.assertEqual(8410, solver.solve(100))
    self.assertEqual(82000210, solver.solve_second_star())

# vim: ts=2:sw=2:et
