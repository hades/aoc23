from unittest import TestCase

from aoc23.day15 import Day15


class TestDay15(TestCase):
  def test_first_star(self):
    solver = Day15()
    solver.presolve('rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7')
    self.assertEqual(solver.solve_first_star(), 1320)

  def test_second_star(self):
    solver = Day15()
    solver.presolve('rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7')
    self.assertEqual(solver.solve_second_star(), 145)

# vim: ts=2:sw=2:et
