from unittest import TestCase

from aoc23.day20 import Day20

INPUT='''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

INPUT_SECOND='''%bit00 -> bit01, checker0
%bit01 -> bit02
%bit02 -> checker0
%bit10 -> checker1, bit11
%bit11 -> bit12
%bit12 -> checker1
%bit20 -> checker2, bit21
%bit21 -> bit22
%bit22 -> checker2
%bit30 -> bit31, checker3
%bit31 -> bit32, checker3
%bit32 -> checker3
&checker0 -> result0, bit00, bit01, bit02
&checker1 -> result1, bit10, bit12
&checker2 -> result2, bit20, bit21
&checker3 -> result3, bit30
&result0 -> acc
&result1 -> acc
&result2 -> acc
&result3 -> acc
&acc -> rx
broadcaster -> bit00, bit10, bit20, bit30
'''

class TestDay20(TestCase):
  def test_first_star(self):
    solver = Day20()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 32000000)

  def test_second_star(self):
    solver = Day20()
    solver.presolve(INPUT_SECOND)
    self.assertEqual(solver.solve_second_star(), 35)

# vim: ts=2:sw=2:et
