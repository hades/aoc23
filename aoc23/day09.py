from .solver import Solver
class Day09(Solver):

  def __init__(self):
    super().__init__(9)
    self.numbers: list[list[int]] = []

  def presolve(self, input: str):
    lines = input.rstrip().split('\n')
    self.numbers = [[int(n) for n in line.split(' ')] for line in lines]
    for line in self.numbers:
      stack = [line]
      while not all(x == 0 for x in stack[-1]):
        diff = [stack[-1][i+1] - stack[-1][i] for i in range(len(stack[-1]) - 1)]
        stack.append(diff)
      stack.reverse()
      stack[0].append(0)
      stack[0].insert(0, 0)
      for i in range(1, len(stack)):
        stack[i].append(stack[i-1][-1] + stack[i][-1])
        stack[i].insert(0, stack[i][0] - stack[i-1][0])

  def solve_first_star(self) -> int:
    return sum(line[-1] for line in self.numbers)

  def solve_second_star(self) -> int:
    return sum(line[0] for line in self.numbers)

# vim: ts=2:sw=2:et
