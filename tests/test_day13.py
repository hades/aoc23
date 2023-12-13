from unittest import TestCase

from aoc23.day13 import Day13

INPUT='''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''


class TestDay13(TestCase):
  def test_first_star(self):
    solver = Day13()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 405)

  def test_second_star(self):
    solver = Day13()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 400)

# vim: ts=2:sw=2:et
