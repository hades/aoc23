from unittest import TestCase

from aoc23.day03 import Day03

INPUT="""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

class TestDay03(TestCase):
  def test_basic_first_star(self):
    solver = Day03()
    solver.presolve(INPUT)
    self.assertEqual(4361, solver.solve_first_star())

  def test_basic_second_star(self):
    solver = Day03()
    solver.presolve(INPUT)
    self.assertEqual(467835, solver.solve_second_star())

# vim: ts=2:sw=2:et
