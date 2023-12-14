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
    for y in range(self.data.shape[1]):
      self.data[:, y] = _tilt(self.data[:, y].tolist())
    return sum((self.data.shape[0] - x) * (self.data[x] == 2).sum() for x in range(self.data.shape[0]))

  def solve_second_star(self) -> int:
    seen = {}
    order = []
    for i in range(1_000_000_000):
      order += [self.data.copy()]
      s = self.data.tobytes()
      if s in seen:
        loop_size = i - seen[s]
        remainder = (1_000_000_000 - i) % loop_size
        self.data = order[seen[s] + remainder]
        break
      seen[s] = i
      for y in range(self.data.shape[1]):
        self.data[:, y] = _tilt(self.data[:, y].tolist())
      for x in range(self.data.shape[0]):
        self.data[x, :] = _tilt(self.data[x, :].tolist())
      for y in range(self.data.shape[1]):
        self.data[:, y] = _tilt(self.data[:, y].tolist(), reverse=True)
      for x in range(self.data.shape[0]):
        self.data[x, :] = _tilt(self.data[x, :].tolist(), reverse=True)
    return sum((self.data.shape[0] - x) * (self.data[x] == 2).sum() for x in range(self.data.shape[0]))

# vim: ts=2:sw=2:et
