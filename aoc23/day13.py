from .solver import Solver


def is_mirrored_x(pattern: set[tuple[int, int]], max_x: int, max_y: int,
                  x_mirror: int, desired_errors: int = 0) -> bool:
  min_x = max(0, 2 * x_mirror - max_x)
  max_x = min(max_x, 2 * x_mirror)
  errors = 0
  for y in range(max_y):
    for x in range(min_x, x_mirror):
      mirrored = 2 * x_mirror - x - 1
      if (x, y) in pattern and (mirrored, y) not in pattern:
        errors += 1
      if (x, y) not in pattern and (mirrored, y) in pattern:
        errors += 1
      if errors > desired_errors:
        return False
  return errors == desired_errors

def is_mirrored_y(pattern: set[tuple[int, int]], max_x: int, max_y: int,
                  y_mirror: int, desired_errors: int = 0) -> bool:
  min_y = max(0, 2 * y_mirror - max_y)
  max_y = min(max_y, 2 * y_mirror)
  errors = 0
  for x in range(max_x):
    for y in range(min_y, y_mirror):
      mirrored = 2 * y_mirror - y - 1
      if (x, y) in pattern and (x, mirrored) not in pattern:
        errors += 1
      if (x, y) not in pattern and (x, mirrored) in pattern:
        errors += 1
      if errors > desired_errors:
        return False
  return errors == desired_errors

def find_mirror_axis(pattern: set[tuple[int, int]], max_x: int, max_y: int,
                     desired_errors: int = 0) -> tuple[None, int]|tuple[int, None]:
  for possible_x_mirror in range(1, max_x):
    if is_mirrored_x(pattern, max_x, max_y, possible_x_mirror, desired_errors):
      return possible_x_mirror, None
  for possible_y_mirror in range(1, max_y):
    if is_mirrored_y(pattern, max_x, max_y, possible_y_mirror, desired_errors):
      return None, possible_y_mirror
  raise RuntimeError('No mirror axis found')

class Day13(Solver):

  def __init__(self):
    super().__init__(13)
    self.patterns: list[set[tuple[int, int]]] = []
    self.dimensions: list[tuple[int, int]] = []

  def presolve(self, input: str):
    patterns = input.rstrip().split('\n\n')
    for pattern in patterns:
      lines = pattern.splitlines()
      points: set[tuple[int, int]] = set()
      max_x = 0
      max_y = 0
      for y, line in enumerate(lines):
        max_y = max(max_y, y)
        for x, char in enumerate(line):
          max_x = max(max_x, x)
          if char == '#':
            points.add((x, y))
      self.patterns.append(points)
      self.dimensions.append((max_x + 1, max_y + 1))

  def solve_first_star(self) -> int:
    sum = 0
    for pattern, (max_x, max_y) in zip(self.patterns, self.dimensions, strict=True):
      mirror_x, mirror_y = find_mirror_axis(pattern, max_x, max_y)
      sum += (mirror_x or 0) + (mirror_y or 0) * 100
    return sum

  def solve_second_star(self) -> int:
    sum = 0
    for pattern, (max_x, max_y) in zip(self.patterns, self.dimensions, strict=True):
      mirror_x, mirror_y = find_mirror_axis(pattern, max_x, max_y, 1)
      sum += (mirror_x or 0) + (mirror_y or 0) * 100
    return sum

# vim: ts=2:sw=2:et
