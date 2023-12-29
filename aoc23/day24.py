import numpy as np
import z3

from aoc23.util import assert_full_match

from .solver import Solver


class Day24(Solver):

  def __init__(self):
    super().__init__(24)
    self.test_area = [200000000000000, 400000000000000]

  def presolve(self, input: str):
    self.stones = []
    for line in input.splitlines():
      (x, y, z, vx, vy, vz) = assert_full_match(
        r'([0-9-]+), +([0-9-]+), +([0-9-]+) +@ +([0-9-]+), +([0-9-]+), +([0-9-]+)', line).groups()
      self.stones.append((int(x), int(y), int(z), int(vx), int(vy), int(vz)))

  def solve_first_star(self) -> int | str:
    count = 0
    for i, stone_a in enumerate(self.stones):
      for stone_b in self.stones[i+1:]:
        matrix = np.array([[stone_a[3], -stone_b[3]],
                          [stone_a[4], -stone_b[4]],])
        rhs = np.array([[stone_b[0] - stone_a[0]], [stone_b[1] - stone_a[1]]])
        try:
          x = np.linalg.solve(matrix, rhs)
          if not (x > 0).all():
            continue
          intersection_x = stone_a[0] + stone_a[3] * x[0, 0]
          intersection_y = stone_a[1] + stone_a[4] * x[0, 0]
          if (self.test_area[0] <= intersection_x <= self.test_area[1]
              and self.test_area[0] <= intersection_y <= self.test_area[1]):
            count += 1
        except np.linalg.LinAlgError:
          continue
    return count

  def solve_second_star(self) -> int | str:
    x0 = z3.Int('x0')
    y0 = z3.Int('y0')
    z0 = z3.Int('z0')
    vx0 = z3.Int('vx0')
    vy0 = z3.Int('vy0')
    vz0 = z3.Int('vz0')
    t1 = z3.Int('t1')
    t2 = z3.Int('t2')
    t3 = z3.Int('t3')
    solver = z3.Solver()
    solver.add(x0 + vx0 * t1 == self.stones[0][0] + self.stones[0][3] * t1)
    solver.add(y0 + vy0 * t1 == self.stones[0][1] + self.stones[0][4] * t1)
    solver.add(z0 + vz0 * t1 == self.stones[0][2] + self.stones[0][5] * t1)
    solver.add(x0 + vx0 * t2 == self.stones[1][0] + self.stones[1][3] * t2)
    solver.add(y0 + vy0 * t2 == self.stones[1][1] + self.stones[1][4] * t2)
    solver.add(z0 + vz0 * t2 == self.stones[1][2] + self.stones[1][5] * t2)
    solver.add(x0 + vx0 * t3 == self.stones[2][0] + self.stones[2][3] * t3)
    solver.add(y0 + vy0 * t3 == self.stones[2][1] + self.stones[2][4] * t3)
    solver.add(z0 + vz0 * t3 == self.stones[2][2] + self.stones[2][5] * t3)
    assert solver.check() == z3.sat
    model = solver.model()
    return sum([model[x0].as_long(), model[y0].as_long(), model[z0].as_long()])

# vim: ts=2:sw=2:et
