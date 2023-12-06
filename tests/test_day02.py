from unittest import TestCase

from aoc23.day02 import Day02

INPUT="""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

class TestDay02(TestCase):
  def test_basic_first_star(self):
    solver = Day02()
    solver.presolve(INPUT)
    self.assertEqual(8, solver.solve_first_star())

  def test_basic_second_star(self):
    solver = Day02()
    solver.presolve(INPUT)
    self.assertEqual(2286, solver.solve_second_star())

# vim: ts=2:sw=2:et
