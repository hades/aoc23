import re

from .solver import Solver


class Day01(Solver):
  def __init__(self):
    super().__init__(1)
    self.lines = []

  def presolve(self, input: str):
    self.lines = input.rstrip().split('\n')

  def solve_first_star(self):
    numbers = []
    for line in self.lines:
      digits = [ch for ch in line if ch.isdigit()]
      numbers.append(int(digits[0] + digits[-1]))
    return sum(numbers)

  def solve_second_star(self):
    numbers = []
    digit_map = {
      "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
      "six": 6, "seven": 7, "eight": 8, "nine": 9, "zero": 0,
      }
    for i in range(10):
      digit_map[str(i)] = i
    for line in self.lines:
      digits = [digit_map[digit] for digit in re.findall(
          "(?=(one|two|three|four|five|six|seven|eight|nine|[0-9]))", line)]
      numbers.append(digits[0]*10 + digits[-1])
    return sum(numbers)

# vim: ts=2:sw=2:et
