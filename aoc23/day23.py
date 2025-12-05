from .solver import Solver


def _directions_from(char: str) -> list[tuple[int, int]]:
  if char == '.':
    return [(0, 1), (0, -1), (1, 0), (-1, 0)]
  if char == 'v':
    return [(1, 0)]
  if char == '^':
    return [(-1, 0)]
  if char == '<':
    return [(0, -1)]
  if char == '>':
    return [(0, 1)]
  raise ValueError(f'unknown char: {char}')

class Day23(Solver):
  lines: list[str]

  def __init__(self):
    super().__init__(23)

  def presolve(self, input: str):
    self.lines = input.splitlines()

  def _find_longest(self, current: tuple[int, int], visited: set[tuple[int, int]]) -> int|None:
    i, j = current
    if i == len(self.lines) - 1:
      return 0
    visited.add(current)
    options = []
    for di, dj in _directions_from(self.lines[i][j]):
      ni, nj = i + di, j + dj
      if ni < 0 or ni >= len(self.lines) or nj < 0 or nj >= len(self.lines[0]):
        continue
      if self.lines[ni][nj] == '#':
        continue
      if (ni, nj) in visited:
        continue
      result = self._find_longest((ni, nj), visited)
      if result is not None:
        options.append(result)
    visited.remove(current)
    if options:
      return max(options) + 1
    return None

  def solve_first_star(self) -> int:
    start_i = 0
    start_j = self.lines[0].find('.')
    result = self._find_longest((start_i, start_j), set())
    assert result
    return result

  def _find_longest_2(self, current: tuple[int, int],
                      connections: dict[tuple[int, int], list[tuple[int, int, int]]],
                      visited: set[tuple[int, int]]) -> int|None:
    i, j = current
    if i == len(self.lines) - 1:
      return 0
    visited.add(current)
    options = []
    for ni, nj, length in connections[(i, j)]:
      if (ni, nj) in visited:
        continue
      result = self._find_longest_2((ni, nj), connections, visited)
      if result is not None:
        options.append(result + length)
    visited.remove(current)
    if options:
      return max(options)
    return None

  def solve_second_star(self) -> int:
    start_i = 0
    start_j = self.lines[0].find('.')

    stack = [(start_i, start_j)]
    connections: dict[tuple[int, int], list[tuple[int, int, int]]] = {}
    visited = set()
    while stack:
      edge_i, edge_j = stack.pop()
      i, j = edge_i, edge_j
      path_length = 0
      options: list[tuple[int, int]] = []
      connections[(edge_i, edge_j)] = []
      while True:
        options = []
        path_length += 1
        visited.add((i, j))
        for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
          ni, nj = i + di, j + dj
          if ni < 0 or ni >= len(self.lines) or nj < 0 or nj >= len(self.lines[0]):
            continue
          if self.lines[ni][nj] == '#':
            continue
          if (ni, nj) in visited:
            continue
          options.append((ni, nj))
        if len(options) == 1:
          i, j = options[0]
        else:
          connections[(edge_i, edge_j)].append((i, j, path_length - 1))
          break
      connections[(i, j)] = [(ni, nj, 1) for ni, nj in options]
      stack.extend(options)

    connections_pairs = list(connections.items())
    for (i, j), connected_nodes in connections_pairs:
      for (ni, nj, d) in connected_nodes:
        if (ni, nj) not in connections:
          connections[(ni, nj)] = [(i, j, d)]
        elif (i, j, d) not in connections[(ni, nj)]:
          connections[(ni, nj)].append((i, j, d))

    result = self._find_longest_2((start_i, start_j), connections, set())
    assert result
    return result


# vim: ts=2:sw=2:et
