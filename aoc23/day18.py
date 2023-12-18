from .solver import Solver


class Day18(Solver):

  def __init__(self):
    super().__init__(18)

  def presolve(self, input: str):
    self.lines = input.splitlines()

  def solve_first_star(self):
    commands = []
    for line in self.lines:
      direction, distance, *_ = line.split(' ')
      commands.append((direction, int(distance)))
    return self._solve(commands)

  def solve_second_star(self):
    commands = []
    for line in self.lines:
      _, _, command = line.split(' ')
      distance = int(command[2:-2], 16)
      direction = ('R', 'D', 'L', 'U')[int(command[-2])]
      commands.append((direction, distance))
    return self._solve(commands)

  def _solve(self, commands: list[tuple[str, int]]):
    points: list[tuple[int, int]] = [(0, 0)]
    perimeter_integer_points = 1
    x, y = 0, 0
    for direction, distance in commands:
      dx, dy = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}[direction]
      x, y = x + dx * distance, y + dy * distance
      perimeter_integer_points += distance
      points.append((x, y))
    last_x, last_y = points[-1]
    perimeter_integer_points += abs(last_x) + abs(last_y) - 1
    area_x2 = sum((points[i][1] + points[(i+1) % len(points)][1]) *
                  (points[i][0] - points[(i+1) % len(points)][0])
                  for i in range(len(points)))
    interior_integer_points = (area_x2 - perimeter_integer_points) // 2 + 1
    return interior_integer_points + perimeter_integer_points

# vim: ts=2:sw=2:et
