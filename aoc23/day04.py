import collections
import re

from .solver import Solver

class Day04(Solver):
  def __init__(self):
    super().__init__(4)
    self.cards = []

  def presolve(self, input: str):
    lines = input.rstrip().split('\n')
    self.cards = []
    for line in lines:
      left, right = re.split(r' +\| +', re.split(': +', line)[1])
      left, right = map(int, re.split(' +', left)), map(int, re.split(' +', right))
      self.cards.append((list(left), list(right)))

  def solve_first_star(self):
    points = 0
    for winning, having in self.cards:
      matches = len(set(winning) & set(having))
      if not matches:
        continue
      points += 1 << (matches - 1)
    return points

  def solve_second_star(self):
    factors = collections.defaultdict(lambda: 1)
    count = 0
    for i, (winning, having) in enumerate(self.cards):
      count += factors[i]
      matches = len(set(winning) & set(having))
      if not matches:
        continue
      for j in range(i + 1, i + 1 + matches):
        factors[j] = factors[j] + factors[i]
    return count

# vim: ts=2:sw=2:et
