from unittest import TestCase

from aoc23.day16 import Day16

INPUT = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

class TestDay16(TestCase):
  def test_first_star(self):
    solver = Day16()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 46)

  def test_second_star(self):
    solver = Day16()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 46)

# vim: ts=2:sw=2:et
