from .solver import Solver


def _trace_beam(data: list[str], initial_beam_head: tuple[int, int, int, int]):
  wx = len(data[0])
  wy = len(data)
  beam_heads = [initial_beam_head]
  seen_beam_heads = set()
  while beam_heads:
    next_beam_heads = []
    for x, y, dx, dy in beam_heads:
      seen_beam_heads.add((x, y, dx, dy))
      nx, ny = (x + dx), (y + dy)
      if nx < 0 or nx >= wx or ny < 0 or ny >= wy:
        continue
      obj = data[ny][nx]
      if obj == '|' and dx != 0:
        next_beam_heads.append((nx, ny, 0, 1))
        next_beam_heads.append((nx, ny, 0, -1))
      elif obj == '-' and dy != 0:
        next_beam_heads.append((nx, ny, 1, 0))
        next_beam_heads.append((nx, ny, -1, 0))
      elif obj == '/':
        next_beam_heads.append((nx, ny, -dy, -dx))
      elif obj == '\\':
        next_beam_heads.append((nx, ny, dy, dx))
      else:
        next_beam_heads.append((nx, ny, dx, dy))
    beam_heads = [x for x in next_beam_heads if x not in seen_beam_heads]
  energized = {(x, y) for x, y, _, _ in seen_beam_heads}
  return len(energized) - 1


class Day16(Solver):

  def __init__(self):
    super().__init__(16)

  def presolve(self, input: str):
    data = input.splitlines()
    self.possible_energized_cells = (
      [_trace_beam(data, (-1, y, 1, 0)) for y in range(len(data))] +
      [_trace_beam(data, (x, -1, 0, 1)) for x in range(len(data[0]))] +
      [_trace_beam(data, (len(data[0]), y, -1, 0)) for y in range(len(data))] +
      [_trace_beam(data, (x, len(data), 0, -1)) for x in range(len(data[0]))])


  def solve_first_star(self) -> int:
    return self.possible_energized_cells[0]

  def solve_second_star(self) -> int:
    return max(self.possible_energized_cells)


# vim: ts=2:sw=2:et
