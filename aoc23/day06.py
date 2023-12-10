import re
from functools import reduce
from operator import mul

from .solver import Solver
from .util import upper_bound


def travel_distance(hold: int, limit: int) -> int:
  dist = hold * (limit - hold)
  return dist

def ways_to_win(time: int, record: int) -> int:
  definitely_winning_hold = time // 2
  assert travel_distance(definitely_winning_hold, time) > record
  minimum_hold_to_win = upper_bound(
      1, definitely_winning_hold, lambda hold: travel_distance(hold, time) <= record)
  minimum_hold_to_lose = upper_bound(
      definitely_winning_hold, time, lambda hold: travel_distance(hold, time) > record)
  return minimum_hold_to_lose - minimum_hold_to_win

class Day06(Solver):

  def __init__(self):
    super().__init__(6)
    self.times = []
    self.distances = []

  def presolve(self, input: str):
    times, distances = input.rstrip().split('\n')
    self.times = [int(time) for time in re.split(r'\s+', times)[1:]]
    self.distances = [int(distance) for distance in re.split(r'\s+', distances)[1:]]

  def solve_first_star(self):
    ways= []
    for time, record in zip(self.times, self.distances, strict=True):
      ways.append(ways_to_win(time, record))
    return reduce(mul, ways)

  def solve_second_star(self):
    time = int(''.join(map(str, self.times)))
    distance = int(''.join(map(str, self.distances)))
    return ways_to_win(time, distance)

# vim: ts=2:sw=2:et
