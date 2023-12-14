from unittest import TestCase

from aoc23.day14 import Day14

INPUT="""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

class TestDay14(TestCase):
  def test_first_star(self):
    solver = Day14()
    solver.presolve(INPUT)
    self.assertEqual(136, solver.solve_first_star())

  def test_second_star(self):
    solver = Day14()
    solver.presolve(INPUT)
    self.assertEqual(64, solver.solve_second_star())

# vim: ts=2:sw=2:et
