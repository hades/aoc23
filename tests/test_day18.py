from unittest import TestCase

from aoc23.day18 import Day18

INPUT='''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''


class TestDay18(TestCase):
  def test_first_star(self):
    solver = Day18()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 62)

  def test_second_star(self):
    solver = Day18()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 952408144115)

  def test_second_star_simple(self):
    solver = Day18()
    solver.presolve('''_ _ (#000020)
_ _ (#000021)
_ _ (#000022)
_ _ (#000013)''')
    self.assertEqual(solver.solve_second_star(), 9)

# vim: ts=2:sw=2:et
