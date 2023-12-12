from unittest import TestCase

from aoc23.day12 import Day12, _match_one_template

INPUT = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

class TestDay12(TestCase):
  def test_one_template(self):
    self.assertEqual((_match_one_template('???.###', (1, 1, 3))), 1)
    self.assertEqual((_match_one_template('.??..??...?##.', (1, 1, 3))), 4)
    self.assertEqual((_match_one_template('?#?#?#?#?#?#?#?', (1, 3, 1, 6))), 1)
    self.assertEqual((_match_one_template('????.#...#...', (4, 1, 1))), 1)
    self.assertEqual((_match_one_template('????.######..#####.', (1, 6, 5))), 4)
    self.assertEqual((_match_one_template('?###????????', (3, 2, 1))), 10)
    self.assertEqual((_match_one_template('???#?.???????.?', (3, 1, 1, 1, 1))), 22)
    self.assertEqual((_match_one_template('????.#????#?????#??#', (1, 2, 1, 1, 7))), 5)
    self.assertEqual((_match_one_template('?#???#??.#.?..', (5, 1))), 1)

  def test_first_star(self):
    solver = Day12()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_first_star(), 21)

  def test_second_star(self):
    solver = Day12()
    solver.presolve(INPUT)
    self.assertEqual(solver.solve_second_star(), 525152)


# vim: ts=2:sw=2:et
