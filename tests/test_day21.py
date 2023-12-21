from unittest import TestCase

from aoc23.day21 import Day21

INPUT='''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
'''

INPUT2='''...........
......##.#.
.###..#..#.
..#.#...#..
....#.#....
.....S.....
.##......#.
.......##..
.##.#.####.
.##...#.##.
...........
'''


class TestDay21(TestCase):
  def test_first_star(self):
    solver = Day21()
    solver.first_star_steps = 6
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 16)


  def test_second_star_6(self):
    solver = Day21()
    solver.second_star_steps = 6
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 16)

  def test_second_star_10(self):
    solver = Day21()
    solver.second_star_steps = 10
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 50)

  def test_second_star_50(self):
    solver = Day21()
    solver.second_star_steps = 50
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 1594)

  def test_second_star_100(self):
    solver = Day21()
    solver.second_star_steps = 100
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 6536)

  def test_second_star_500(self):
    solver = Day21()
    solver.second_star_steps = 500
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 167004)

  def test_second_star_1000(self):
    solver = Day21()
    solver.second_star_steps = 1000
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 668697)

  def test_second_star_5000(self):
    solver = Day21()
    solver.second_star_steps = 5000
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 16733044)

  def test_second_star_6_fast(self):
    solver = Day21()
    solver.second_star_steps = 6
    solver.presolve(INPUT2)
    self.assertEqual(solver.solve_second_star(), 36)

  def test_second_star_10_fast(self):
    solver = Day21()
    solver.second_star_steps = 10
    solver.presolve(INPUT2)
    self.assertEqual(solver.solve_second_star(), 90)

  def test_second_star_50_fast(self):
    solver = Day21()
    solver.second_star_steps = 50
    solver.presolve(INPUT2)
    self.assertEqual(solver.solve_second_star(), 1940)

  def test_second_star_100_fast(self):
    solver = Day21()
    solver.second_star_steps = 100
    solver.presolve(INPUT2)
    self.assertEqual(solver.solve_second_star(), 7645)

  def test_second_star_500_fast(self):
    solver = Day21()
    solver.second_star_steps = 500
    solver.presolve(INPUT2)
    self.assertEqual(solver.solve_second_star(), 188756)

  def test_second_star_1000_fast(self):
    solver = Day21()
    solver.second_star_steps = 1000
    solver.presolve(INPUT2)
    self.assertEqual(solver.solve_second_star(), 753480)

  def test_second_star_5000_fast(self):
    solver = Day21()
    solver.second_star_steps = 5000
    solver.presolve(INPUT2)
    self.assertEqual(solver.solve_second_star(), 18807440)

# vim: ts=2:sw=2:et
