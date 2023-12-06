from unittest import TestCase

from aoc23.day01 import Day01

INPUT="""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

INPUT_SECOND="""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

class TestDay01(TestCase):
  def test_basic_first_star(self):
    solver = Day01()
    solver.presolve(INPUT)
    self.assertEqual(142, solver.solve_first_star())
    self.assertEqual(142, solver.solve_second_star())

  def test_basic_second_star(self):
    solver = Day01()
    solver.presolve(INPUT_SECOND)
    self.assertEqual(281, solver.solve_second_star())

  def test_overlapping(self):
    solver = Day01()
    solver.presolve("35zrgthreetwonesz")
    self.assertEqual(31, solver.solve_second_star())

# vim: ts=2:sw=2:et
