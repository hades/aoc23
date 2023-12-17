import collections
import dataclasses
import heapq

import numpy as np

from .solver import Solver


@dataclasses.dataclass(order=True)
class QueueEntry:
  price: int
  x: int
  y: int
  momentum_x: int
  momentum_y: int
  deleted: bool


class Day17(Solver):
  lines: list[str]
  sx: int
  sy: int
  lower_bounds: np.ndarray

  def __init__(self):
    super().__init__(17)

  def presolve(self, input: str):
    self.lines = input.splitlines()
    self.sx = len(self.lines[0])
    self.sy = len(self.lines)
    start = (self.sx - 1, self.sy - 1)
    self.lower_bounds = np.zeros((self.sx, self.sy)) + np.inf
    self.lower_bounds[start] = 0
    queue: list[QueueEntry] = [QueueEntry(0, self.sx - 1, self.sy - 1, 0, 0, False)]
    queue_entries: dict[tuple[int, int], QueueEntry] = {start: queue[0]}
    while queue:
      cur_price, x, y, _, _, deleted = dataclasses.astuple(heapq.heappop(queue))
      if deleted:
        continue
      del queue_entries[(x, y)]
      self.lower_bounds[x, y] = cur_price
      price = cur_price + int(self.lines[y][x])
      for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nx, ny = x + dx, y + dy
        if not (0 <= nx < self.sx) or not (0 <= ny < self.sy):
          continue
        if price < self.lower_bounds[nx, ny]:
          self.lower_bounds[nx, ny] = price
          if (nx, ny) in queue_entries:
            queue_entries[(nx, ny)].deleted = True
          queue_entries[(nx, ny)] = QueueEntry(price, nx, ny, 0, 0, False)
          heapq.heappush(queue, queue_entries[(nx, ny)])

  def _solve(self, maximum_run: int, minimum_run_to_turn: int):
    came_from: dict[tuple[int, int, int, int], tuple[int, int, int, int]] = {}
    start = (0, 0, 0, 0)
    queue: list[QueueEntry] = [QueueEntry(self.lower_bounds[0, 0], *start, False)]
    queue_entries: dict[tuple[int, int, int, int], QueueEntry] = {start: queue[0]}
    route: list[tuple[int, int]] = []
    prices: dict[tuple[int, int, int, int], float] = collections.defaultdict(lambda: np.inf)
    prices[start] = 0
    while queue:
      _, current_x, current_y, momentum_x, momentum_y, deleted = dataclasses.astuple(heapq.heappop(queue))
      cur_price = prices[(current_x, current_y, momentum_x, momentum_y)]
      if deleted:
        continue
      if ((current_x, current_y) == (self.sx - 1, self.sy - 1) and
          (momentum_x >= minimum_run_to_turn or momentum_y >= minimum_run_to_turn)):
        previous = came_from.get((current_x, current_y, momentum_x, momentum_y))
        route.append((current_x, current_y))
        while previous:
          x, y, *_ = previous
          if x != 0 or y != 0:
            route.append((x, y))
          previous = came_from.get(previous)
        break
      for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        dot_product = dx * momentum_x + dy * momentum_y
        if dot_product < 0 or dot_product >= maximum_run:
          continue
        if ((momentum_x or momentum_y) and dot_product == 0 and
            abs(momentum_x) < minimum_run_to_turn and abs(momentum_y) < minimum_run_to_turn):
          continue
        new_x, new_y = current_x + dx, current_y + dy
        if not (0 <= new_x < self.sx) or not (0 <= new_y < self.sy):
          continue
        new_momentum_x, new_momentum_y = (dx, dy) if dot_product == 0 else (momentum_x + dx, momentum_y + dy)
        new_position = (new_x, new_y, new_momentum_x, new_momentum_y)
        potential_new_price = cur_price + int(self.lines[new_y][new_x])
        if potential_new_price < prices[new_position]:
          queue_entry = queue_entries.get(new_position)
          if queue_entry:
            queue_entry.deleted = True
          queue_entries[new_position] = QueueEntry(potential_new_price + self.lower_bounds[new_x, new_y],
                                                   *new_position, False)
          came_from[new_position] = (current_x, current_y, momentum_x, momentum_y)
          prices[new_position] = potential_new_price
          heapq.heappush(queue, queue_entries[new_position])
    return sum(int(self.lines[y][x]) for x, y in route)

  def solve_first_star(self) -> int:
    return self._solve(3, 0)

  def solve_second_star(self) -> int:
    return self._solve(10, 4)

# vim: ts=2:sw=2:et
