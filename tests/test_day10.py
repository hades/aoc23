from unittest import TestCase

from aoc23.day10 import Day10

INPUT1=""".....
.S-7.
.|.|.
.L-J.
....."""

INPUT2="""-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

INPUT3="""7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

INPUT4="""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

INPUT5=""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

class TestDay10(TestCase):
  def test_input_1(self):
    solver = Day10()
    solver.presolve(INPUT1)
    self.assertEqual(4, solver.solve_first_star())
    self.assertEqual(1, solver.solve_second_star())

  def test_input_2(self):
    solver = Day10()
    solver.presolve(INPUT2)
    self.assertEqual(4, solver.solve_first_star())
    self.assertEqual(1, solver.solve_second_star())

  def test_input_3(self):
    solver = Day10()
    solver.presolve(INPUT3)
    self.assertEqual(8, solver.solve_first_star())
    self.assertEqual(1, solver.solve_second_star())

  def test_input_4(self):
    solver = Day10()
    solver.presolve(INPUT4)
    self.assertEqual(23, solver.solve_first_star())
    self.assertEqual(4, solver.solve_second_star())

  def test_input_5(self):
    solver = Day10()
    solver.presolve(INPUT5)
    self.assertEqual(70, solver.solve_first_star())
    self.assertEqual(8, solver.solve_second_star())

# vim: ts=2:sw=2:et
