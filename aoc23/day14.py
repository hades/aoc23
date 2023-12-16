import numpy as np

from .solver import Solver


def _tilt(row: list[int], reverse: bool = False) -> list[int]:
  res = row[::-1] if reverse else row[:]
  rock_x = 0
  for x, item in enumerate(res):
    if item == 1:
      rock_x = x + 1
    if item == 2:
      if rock_x < x:
        res[rock_x] = 2
        res[x] = 0
      rock_x += 1
  return res[::-1] if reverse else res

class Day14(Solver):
  data: np.ndarray

  def __init__(self):
    super().__init__(14)

  def presolve(self, input: str):
    lines = input.splitlines()
    self.data = np.zeros((len(lines), len(lines[0])), dtype=np.int8)
    for x, line in enumerate(lines):
      for y, char in enumerate(line):
        if char == '#':
          self.data[x, y] = 1
        elif char == 'O':
          self.data[x, y] = 2

  def solve_first_star(self) -> int:
    data = self.data.copy()
    for y in range(data.shape[1]):
      data[:, y] = _tilt(data[:, y].tolist())
    return sum((data.shape[0] - x) * (data[x] == 2).sum() for x in range(data.shape[0]))

  def solve_second_star(self) -> int:
    data = self.data.copy()
    seen = {}
    order = []
    for i in range(1_000_000_000):
      order += [data.copy()]
      s = data.tobytes()
      if s in seen:
        loop_size = i - seen[s]
        remainder = (1_000_000_000 - i) % loop_size
        data = order[seen[s] + remainder]
        break
      seen[s] = i
      for _ in range(4):
        for y in range(data.shape[1]):
          data[:, y] = _tilt(data[:, y].tolist())
        data = np.rot90(data, axes=(1, 0))
    return sum((data.shape[0] - x) * (data[x] == 2).sum() for x in range(data.shape[0]))

# vim: ts=2:sw=2:et
