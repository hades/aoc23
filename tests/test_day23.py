from unittest import TestCase

from aoc23.day23 import Day23

INPUT='''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
'''

class TestDay23(TestCase):
  def test_first_star(self):
    solver = Day23()
    solver.presolve(INPUT)
    self.assertEqual(94, solver.solve_first_star())

  def test_second_star(self):
    solver = Day23()
    solver.presolve(INPUT)
    self.assertEqual(154, solver.solve_second_star())

# vim: ts=2:sw=2:et
