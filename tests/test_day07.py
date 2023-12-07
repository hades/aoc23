from unittest import TestCase

from aoc23.day07 import Day07

INPUT="""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

class TestDay07(TestCase):
  def test_first_star(self):
    solver = Day07()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 6440)

  def test_second_star(self):
    solver = Day07()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 5905)

# vim: ts=2:sw=2:et
