from unittest import TestCase

from aoc23.day08 import Day08

INPUT1 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

INPUT2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

class TestDay08(TestCase):
  def test_first_star(self):
    solver = Day08()
    solver.presolve(INPUT1)
    self.assertEqual(6, solver.solve_first_star())

  def test_second_star(self):
    solver = Day08()
    solver.presolve(INPUT2)
    self.assertEqual(6, solver.solve_second_star())

# vim: ts=2:sw=2:et
