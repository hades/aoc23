import collections
import math

from .solver import Solver


class Day21(Solver):
  first_star_steps: int
  second_star_steps: int
  lines: list[str]

  def __init__(self):
    super().__init__(21)
    self.first_star_steps = 64
    self.second_star_steps = 26501365

  def presolve(self, input: str):
    self.lines = input.splitlines()

  def solve_first_star(self) -> int | str:
    positions = {(i, j) for i, line in enumerate(self.lines) for j, c in enumerate(line) if c == 'S'}
    for _ in range(self.first_star_steps):
      next_positions = set()
      for i, j in positions:
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
          if not 0 <= i + di < len(self.lines):
            continue
          if not 0 <= j + dj < len(self.lines[i]):
            continue
          if self.lines[i + di][j + dj] == '#':
            continue
          next_positions.add((i + di, j + dj))
      positions = next_positions
    return len(positions)

  def solve_second_star(self) -> int:
    initial_position = [(i, j) for i, line in enumerate(self.lines) for j, c in enumerate(line) if c == 'S'][0]
    for i, line in enumerate(self.lines):
      for j, c in enumerate(line):
        if (i == initial_position[0] or j == initial_position[1]) and c == '#':
          return self._second_star_general_method()
    if len(self.lines) != len(self.lines[0]):
      return self._second_star_general_method()
    return self._second_star_fast_method()

  def _second_star_general_method(self) -> int:
    size_i = len(self.lines)
    size_j = len(self.lines[0])
    odd_board_positions = len([(i, j) for i, line in enumerate(self.lines) for j, c in enumerate(line)
                               if c != '#' and (i + j) % 2])
    even_board_positions = len([(i, j) for i, line in enumerate(self.lines) for j, c in enumerate(line)
                               if c != '#' and (i + j) % 2 == 0])

    def _process_block(spillins: set[tuple[int, int, int]], initial_block_odd: int,
                       time_limit: int|None = None
    ) -> tuple[dict[tuple[int, int], dict[tuple[int, int], int]], list[int]]:
      positions = set()
      spills: dict[tuple[int, int], dict[tuple[int, int], int]] = collections.defaultdict(dict)
      counts = []
      while time_limit is None or len(counts) <= time_limit:
        for i, j, spill_timestamp in spillins:
          if spill_timestamp == len(counts):
            positions.add((i, j))
        counts.append(len(positions))
        is_odd = (len(counts) + initial_block_odd + 1) % 2
        pos_count = len(positions)
        if is_odd and pos_count == odd_board_positions or not is_odd and pos_count == even_board_positions:
          break
        next_positions = set()
        for i, j in positions:
          for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = i + di, j + dj
            if self.lines[ni % size_i][nj % size_j] == '#':
              continue
            bi, bj = ni // size_i, nj // size_j
            if bi != 0 or bj != 0:
              spills_on_side = spills[(bi, bj)]
              if (ni, nj) not in spills_on_side:
                spills_on_side[(ni, nj)] = len(counts)
            else:
              next_positions.add((ni, nj))
        positions = next_positions
      return spills, counts

    process_block_cache = {}
    def _process_block_cached(spillins: set[tuple[int, int, int]], initial_block_odd: int,
                              time_limit: int|None = None
                              ) -> tuple[dict[tuple[int, int], dict[tuple[int, int], int]], list[int]]:
      key = (tuple(sorted(spillins)), initial_block_odd)
      result = process_block_cache.get(key)
      if result is None:
        result = _process_block(spillins, initial_block_odd, time_limit)
        process_block_cache[key] = result
      return result

    positions = {(i, j) for i, line in enumerate(self.lines) for j, c in enumerate(line) if c == 'S'}
    initial_odd = sum(list(positions)[0]) % 2
    spills, counts = _process_block({(i, j, 0) for i, j in positions}, initial_odd)
    queue: dict[tuple[int, int], set[tuple[int, int, int]]] = collections.OrderedDict()
    for (bi, bj), spill_timestamps in spills.items():
      spillins = {(i % size_i, j % size_j, timestamp) for (i, j), timestamp in spill_timestamps.items()
                  if timestamp <= self.second_star_steps}
      if spillins:
        queue[(bi, bj)] = spillins
    semiprocessed_blocks = set()
    semiprocessed_block_positions = 0
    processed_blocks: dict[int, tuple[int, int]] = {}
    if len(counts) > self.second_star_steps:
      semiprocessed_blocks.add((0, 0))
      semiprocessed_block_positions += counts[self.second_star_steps]
    else:
      processed_blocks[0] = (0, 1)
    while queue:
      (bi, bj), spillins = queue.popitem(last=False)  # pytype: disable=wrong-keyword-args
      dt = min(timestamp for _, _, timestamp in spillins)
      corrected_spillins = {(i, j, timestamp - dt) for i, j, timestamp in spillins}
      spillouts, counts = _process_block_cached(
        corrected_spillins, (bi + bj + initial_odd + dt) % 2, self.second_star_steps - dt)
      for (dbi, dbj), spill_timestamps in spillouts.items():
        spillins = {(i % size_i, j % size_j, timestamp + dt) for (i, j), timestamp in spill_timestamps.items()
                    if timestamp + dt <= self.second_star_steps}
        if not spillins:
          continue
        nbi, nbj = bi + dbi, bj + dbj
        if (nbi, nbj) in semiprocessed_blocks:
          continue
        if nbi in processed_blocks and processed_blocks[nbi][0] <= nbj < processed_blocks[nbi][1]:
          continue
        if (nbi, nbj) in queue:
          queue[(nbi, nbj)].update(spillins)
        else:
          queue[(nbi, nbj)] = spillins
      if len(counts) + dt <= self.second_star_steps:
        if bi not in processed_blocks:
          processed_blocks[bi] = (bj, bj + 1)
        elif bj == processed_blocks[bi][0] - 1:
          processed_blocks[bi] = (bj, processed_blocks[bi][1])
        elif bj == processed_blocks[bi][1]:
          processed_blocks[bi] = (processed_blocks[bi][0], bj + 1)
        else:
          raise RuntimeError('merging block %s %s without a contiguous line', bi, bj)
      else:
        semiprocessed_blocks.add((bi, bj))
        semiprocessed_block_positions += counts[self.second_star_steps - dt]
    processed_positions = 0
    for bi, (bj_start, bj_stop) in processed_blocks.items():
      for bj in range(bj_start, bj_stop):
        is_odd = (bi + bj + self.second_star_steps + initial_odd) % 2
        if is_odd:
          processed_positions += odd_board_positions
        else:
          processed_positions += even_board_positions
    return semiprocessed_block_positions + processed_positions


  def _second_star_fast_method(self) -> int:
    positions = {(i, j) for i, line in enumerate(self.lines) for j, c in enumerate(line) if c == 'S'}
    modulus = self.second_star_steps % len(self.lines)
    points_to_extrapolate = (modulus, modulus + len(self.lines), modulus + len(self.lines) * 2)
    values = []
    for step_count in range(modulus + len(self.lines) * 2 + 1):
      if step_count in points_to_extrapolate:
        values.append(len(positions))
      next_positions = set()
      for i, j in positions:
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
          ni = i + di
          nj = j + dj
          if self.lines[ni % len(self.lines)][nj % len(self.lines)] == '#':
            continue
          next_positions.add((ni, nj))
      positions = next_positions
    a = (values[2] - values[1] *2 + values[0]) // 2
    b = values[1] - values[0] - 3 * a
    c = values[0] - b - a
    cycles = math.ceil(self.second_star_steps / len(self.lines))
    return a * cycles * cycles + b * cycles + c


# vim: ts=2:sw=2:et
