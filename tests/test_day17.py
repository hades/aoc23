from unittest import TestCase

from aoc23.day17 import Day17

INPUT='''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

class TestDay17(TestCase):
  def test_first_star(self):
    solver = Day17()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 102)

  def test_second_star(self):
    solver = Day17()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 94)

  def test_simple_example(self):
    solver = Day17()
    solver.presolve('''111111111111
999999999991
999999999991
999999999991
999999999991
''')
    self.assertEqual(solver.solve_second_star(), 71)

  def test_second_star_lower_bound_on_turn(self):
    solver = Day17()
    solver.presolve('''123456789999
999999999991
999999999991
999999999991
111111111111
''')
    self.assertEqual(solver.solve_second_star(), 49)

  def test_second_star_upper_bound_on_turn(self):
    solver = Day17()
    solver.presolve('''9999876543211111
9999999999911111
9999999999911111
9999999999911111
9999999999911111
''')
    self.assertEqual(solver.solve_second_star(), 103)

  def test_second_star_steps_before_stop(self):
    solver = Day17()
    solver.presolve('''111111111111
999999999991
999999999991
999999999991
999987654321
''')
    self.assertEqual(solver.solve_second_star(), 49)

  def test_loop_de_loop(self):
    solver = Day17()
    solver.presolve('''199999999999
191111199999
191919199999
191919199999
191919199999
111111199999
991999999999
991111111111
''')
    self.assertEqual(solver.solve_second_star(), 34)

# vim: ts=2:sw=2:et
