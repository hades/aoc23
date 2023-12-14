from .solver import Solver


class Day11(Solver):

  def __init__(self):
    super().__init__(11)
    self.galaxies: list = []
    self.blank_x: set[int] = set()
    self.blank_y: set[int] = set()

  def presolve(self, input: str):
    lines = input.rstrip().split('\n')
    self.galaxies = []
    max_x = 0
    max_y = 0
    for y, line in enumerate(lines):
      for x, c in enumerate(line):
        if c == '#':
          self.galaxies.append((x, y))
        max_x = max(max_x, x)
      max_y = max(max_y, y)
    self.blank_x = set(range(max_x + 1)) - {x for x, _ in self.galaxies}
    self.blank_y = set(range(max_y + 1)) - {y for _, y in self.galaxies}

  def solve(self, expansion_factor: int) -> int:
    galaxies = list(self.galaxies)
    total = 0
    for i in range(len(galaxies)):
      for j in range(i + 1, len(galaxies)):
        sx, sy = galaxies[i]
        dx, dy = galaxies[j]
        if sx > dx:
          sx, dx = dx, sx
        if sy > dy:
          sy, dy = dy, sy
        dist = sum((dx - sx, dy - sy,
            max(0, expansion_factor - 1) * len([x for x in self.blank_x if sx < x < dx]),
            max(0, expansion_factor - 1) * len([y for y in self.blank_y if sy < y < dy])))
        total += dist
    return total

  def solve_first_star(self):
    return self.solve(2)

  def solve_second_star(self):
    return self.solve(1_000_000)

# vim: ts=2:sw=2:et
