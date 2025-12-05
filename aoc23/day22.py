import collections

from aoc23.util import assert_full_match

from .solver import Solver


def _trace_brick(x0, y0, x1, y1):
  if x0 == x1:
    y0, y1 = min(y0, y1), max(y0, y1)
    for y in range(y0, y1 + 1):
      yield (x0, y)
  elif y0 == y1:
    x0, x1 = min(x0, x1), max(x0, x1)
    for x in range(x0, x1 + 1):
      yield (x, y0)
  else:
    raise ValueError(f'not a brick: {x0}, {y0}, {x1}, {y1}')

class Day22(Solver):
  can_be_deleted: set[int]
  support_map: dict[int, list[int]]
  brick_count: int

  def __init__(self):
    super().__init__(22)

  def presolve(self, input: str):
    lines = input.splitlines()
    bricks = []
    for line in lines:
      x0, y0, z0, x1, y1, z1 = assert_full_match(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', line).groups()
      bricks.append(((int(x0), int(y0), int(z0)), (int(x1), int(y1), int(z1))))
    self.brick_count = len(bricks)
    bricks.sort(key=lambda brick: min(brick[0][2], brick[1][2]))
    self.can_be_deleted = set()
    topmost_brick_per_position: dict[tuple[int, int], tuple[int, int]] = {}
    self.support_map = {}
    for brick_id, ((x0, y0, z0), (x1, y1, z1)) in enumerate(bricks):
      support_brick_ids = set()
      support_brick_z = 0
      for (x, y) in _trace_brick(x0, y0, x1, y1):
        potential_support = topmost_brick_per_position.get((x, y))
        if not potential_support:
          continue
        if potential_support[0] > support_brick_z:
          support_brick_z = potential_support[0]
          support_brick_ids = {potential_support[1]}
        elif potential_support[0] == support_brick_z:
          support_brick_ids.add(potential_support[1])
      self.support_map[brick_id] = list(support_brick_ids)
      if len(support_brick_ids) == 1:
        self.can_be_deleted.discard(support_brick_ids.pop())
      for (x, y) in _trace_brick(x0, y0, x1, y1):
        topmost_brick_per_position[(x, y)] = (support_brick_z + 1 + z1 - z0, brick_id)
      self.can_be_deleted.add(brick_id)


  def solve_first_star(self) -> int:
    return len(self.can_be_deleted)

  def solve_second_star(self) -> int:
    reverse_support_map = collections.defaultdict(set)
    for brick_id, support_brick_ids in self.support_map.items():
      for support_brick_id in support_brick_ids:
        reverse_support_map[support_brick_id].add(brick_id)
    total = 0
    for brick_id in range(self.brick_count):
      all_destroyed_bricks: set[int] = set()
      queue = [brick_id]
      while queue:
        destroy_brick_id = queue.pop(0)
        for potential_destroyed_brick in reverse_support_map[destroy_brick_id]:
          if potential_destroyed_brick in all_destroyed_bricks:
            continue
          remaining_supports = set(self.support_map[potential_destroyed_brick])
          remaining_supports -= (all_destroyed_bricks | {destroy_brick_id})
          if not remaining_supports:
            queue.append(potential_destroyed_brick)
        all_destroyed_bricks.add(destroy_brick_id)
      total += len(all_destroyed_bricks) - 1
    return total


# vim: ts=2:sw=2:et
