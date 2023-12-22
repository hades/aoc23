from unittest import TestCase

from aoc23.day22 import Day22

INPUT='''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''

class TestDay22(TestCase):
  def test_first_star(self):
    solver = Day22()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 5)

  def test_second_star(self):
    solver = Day22()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 7)


# vim: ts=2:sw=2:et
