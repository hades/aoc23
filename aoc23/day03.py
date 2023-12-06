import collections
import re

from .solver import Solver

class Day03(Solver):
  def __init__(self):
    super().__init__(3)
    self.lines = []

  def presolve(self, input: str):
    self.lines = input.rstrip().split('\n')

  def solve_first_star(self):
    adjacent_to_symbols = set()
    for i, line in enumerate(self.lines):
      for j, sym in enumerate(line):
        if sym in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'):
          continue
        for di in (-1, 0, 1):
          for dj in (-1, 0, 1):
            adjacent_to_symbols.add((i + di, j + dj))
    numbers = []
    for i, line in enumerate(self. lines):
      for number_match in re.finditer(r'\d+', line):
        is_adjacent_to_symbol = False
        for j in range(number_match.start(), number_match.end()):
          if (i, j) in adjacent_to_symbols:
            is_adjacent_to_symbol = True
        if is_adjacent_to_symbol:
          numbers.append(int(number_match.group()))
    return sum(numbers)

  def solve_second_star(self):
    gear_numbers = collections.defaultdict(list)
    adjacent_to_gears = {}
    for i, line in enumerate(self.lines):
      for j, sym in enumerate(line):
        if sym == '*':
          for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
              adjacent_to_gears[(i + di, j + dj)] = (i, j)
    for i, line in enumerate(self. lines):
      for number_match in re.finditer(r'\d+', line):
        adjacent_to_gear = None
        for j in range(number_match.start(), number_match.end()):
          if (i, j) in adjacent_to_gears:
            adjacent_to_gear = adjacent_to_gears[(i, j)]
        if adjacent_to_gear:
          gear_numbers[adjacent_to_gear].append(int(number_match.group()))
    ratios = []
    for gear_numbers in gear_numbers.values():
      match gear_numbers:
        case [a, b]:
          ratios.append(a * b)
    return sum(ratios)


# vim: ts=2:sw=2:et
