import networkx as nx

from .solver import Solver


class Day25(Solver):

  def __init__(self):
    super().__init__(25)

  def presolve(self, input: str):
    self.graph = nx.Graph()
    for line in input.splitlines():
      from_, to_line = line.split(': ')
      for to in to_line.split(' '):
        self.graph.add_edge(from_, to)

  def solve_first_star(self) -> int | str:
    cut_value, partition = nx.algorithms.stoer_wagner(self.graph)
    return len(partition[0]) * len(partition[1])

# vim: ts=2:sw=2:et
