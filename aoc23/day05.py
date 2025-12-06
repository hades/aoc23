import portion as P  # noqa: N812

from .solver import Solver

_maps = [
  'seed-to-soil',
  'soil-to-fertilizer',
  'fertilizer-to-water',
  'water-to-light',
  'light-to-temperature',
  'temperature-to-humidity',
  'humidity-to-location',
]

def group_lines_in_maps(lines):
  group: list[str] = []
  for line in lines:
    if not line:
      yield group
      group = []
      continue
    group.append(line)
  yield group

class Day05(Solver):
  def __init__(self):
    super().__init__(5)
    self.seeds = []
    self.mappings = {}

  def presolve(self, input: str):
    lines = input.rstrip().split('\n')
    self.seeds = list(map(int, lines[0].split(' ')[1:]))
    self.mappings = {}
    for mapping in group_lines_in_maps(lines[2:]):
      mapping_name = mapping[0].split(' ')[0]
      mapping_ranges = (tuple(map(int, rng.split(' '))) for rng in mapping[1:])
      self.mappings[mapping_name] = list(mapping_ranges)


  def solve_first_star(self):
    locations = []
    for seed in self.seeds:
      location = seed
      for mapping in map(self.mappings.get, _maps):
        assert mapping
        for dest, source, length in mapping:
          if 0 <= location - source < length:
            location = dest + (location - source)
            break
      locations.append(location)
    return min(locations)


  def solve_second_star(self):
    current_set = P.empty()
    for i in range(0, len(self.seeds), 2):
      current_set = current_set | P.closedopen(self.seeds[i], self.seeds[i] + self.seeds[i + 1])
    for mapping in map(self.mappings.get, _maps):
      assert mapping
      unmapped = current_set
      next_set = P.empty()
      for dest, source, length in mapping:
        delta = dest - source
        source_range = P.closedopen(source, source + length)
        mappable = unmapped & source_range
        mapped_to_destination = mappable.apply(
            lambda x: (x.left, x.lower + delta, x.upper + delta, x.right))  # noqa: B023
        next_set = next_set | mapped_to_destination
        unmapped = unmapped - source_range
      current_set = next_set | unmapped
    return next(P.iterate(current_set, step=1))

# vim: ts=2:sw=2:et
