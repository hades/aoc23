from unittest import TestCase

from aoc23.day25 import Day25

INPUT='''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
'''

class TestDay25(TestCase):
  def test_first_star(self):
    solver = Day25()
    solver.presolve(INPUT)
    self.assertEqual(54, solver.solve_first_star())

# vim: ts=2:sw=2:et
