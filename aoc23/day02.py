import collections

from .solver import Solver


class Day02(Solver):
  def __init__(self):
    super().__init__(2)
    self.games = []

  def presolve(self, input: str):
    lines = input.rstrip().split('\n')
    for line in lines:
      draws = line.split(': ')[1].split('; ')
      draws2 = [draw.split(', ') for draw in draws]
      self.games.append(draws2)

  def solve_first_star(self):
    game_id = 0
    total = 0
    for game in self.games:
      game_id += 1
      is_good = True
      for draw in game:
        for item in draw:
          count, colour = item.split(' ')
          if (colour == 'red' and int(count) > 12 or
                colour == 'blue' and int(count) > 14 or
                colour == 'green' and int(count) > 13):
            is_good = False
      if is_good:
        total += game_id
    return total

  def solve_second_star(self):
    total = 0
    for game in self.games:
      minimums: dict[str, int] = collections.defaultdict(lambda: 0)
      for draw in game:
        for item in draw:
          count, colour = item.split(' ')
          minimums[colour] = max(minimums[colour], int(count))
      power = minimums['red'] * minimums['blue'] * minimums['green']
      total += power
    return total

# vim: ts=2:sw=2:et
