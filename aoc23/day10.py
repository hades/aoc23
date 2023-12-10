from .solver import Solver

_EXITS_MAP = {
  '|': ((0, -1), (0, 1)),
  '-': ((-1, 0), (1, 0)),
  'L': ((1, 0), (0, -1)),
  'J': ((-1, 0), (0, -1)),
  '7': ((-1, 0), (0, 1)),
  'F': ((1, 0), (0, 1)),
  '.': (),
  'S': (),
}

class Day10(Solver):

  def __init__(self):
    super().__init__(10)
    self.maze: dict[tuple[int, int], str] = {}
    self.start: tuple[int, int] = (0, 0)
    self.dists: dict[tuple[int, int], int] = {}

  def _pipe_has_exit(self, x: int, y: int, di: int, dj: int, inverse: bool = False) -> bool:
    if inverse:
      di, dj = -di, -dj
    return (di, dj) in _EXITS_MAP[self.maze[(x, y)]]

  def presolve(self, input: str):
    self.maze: dict[tuple[int, int], str] = {}
    self.start: tuple[int, int] = (0, 0)
    for y, line in enumerate(input.rstrip().split('\n')):
      for x, c in enumerate(line):
        self.maze[(x, y)] = c
        if c == 'S':
          self.start = (x, y)
    next_pos: list[tuple[int, int]] = []
    directions_from_start = []
    for di, dj in ((0, -1), (1, 0), (0, 1), (-1, 0)):
      x, y = self.start[0] + di, self.start[1] + dj
      if (x, y) not in self.maze:
        continue
      if not self._pipe_has_exit(x, y, di, dj, inverse=True):
        continue
      next_pos.append((x, y))
      directions_from_start.append((di, dj))
    self.maze[self.start] = [c for c, dmap in _EXITS_MAP.items()
                              if set(directions_from_start) == set(dmap)][0]
    dists: dict[tuple[int, int], int] = {}
    cur_dist = 0
    while True:
      cur_dist += 1
      new_next_pos = []
      for x, y in next_pos:
        if (x, y) in dists:
          continue
        dists[(x, y)] = cur_dist
        for di, dj in ((0, -1), (1, 0), (0, 1), (-1, 0)):
          nx, ny = x + di, y + dj
          if (nx, ny) not in self.maze:
            continue
          if not self._pipe_has_exit(x, y, di, dj):
            continue
          new_next_pos.append((nx, ny))
      if not new_next_pos:
        break
      next_pos = new_next_pos
    self.dists = dists

  def solve_first_star(self) -> int:
    return max(self.dists.values())

  def solve_second_star(self) -> int:
    area = 0
    for y in range(max(y for _, y in self.dists.keys()) + 1):
      internal = False
      previous_wall = False
      wall_start_symbol = None
      for x in range(max(x for x, _ in self.dists.keys()) + 1):
        is_wall = (x, y) == self.start or (x, y) in self.dists
        wall_continues = is_wall
        pipe_type = self.maze[(x, y)]
        if is_wall and pipe_type == '|':
          internal = not internal
          wall_continues = False
        elif is_wall and not previous_wall and pipe_type in 'FL':
          wall_start_symbol = pipe_type
        elif is_wall and not previous_wall:
          raise RuntimeError(f'expecting wall F or L at {x}, {y}, got {pipe_type}')
        elif is_wall and previous_wall and pipe_type == 'J':
          wall_continues = False
          if wall_start_symbol == 'F':
            internal = not internal
        elif is_wall and previous_wall and pipe_type == '7':
          wall_continues = False
          if wall_start_symbol == 'L':
            internal = not internal
        elif not is_wall and previous_wall:
          raise RuntimeError(f'expecting wall J or 7 at {x}, {y}, got {pipe_type}')
        if internal and not is_wall:
          area += 1
        previous_wall = wall_continues
    return area

# vim: ts=2:sw=2:et
