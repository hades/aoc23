import itertools
import math
import re

from .solver import Solver

class Day08(Solver):

  def __init__(self):
    super().__init__(8)
    self.instructions: str = ''
    self.nodes: dict[str, tuple[str, str]] = {}

  def presolve(self, input: str):
    lines = input.rstrip().split('\n')
    self.instructions = lines[0]
    for line in lines[2:]:
      g = re.fullmatch(r'(\w+) = \((\w+), (\w+)\)', line)
      assert g, f"line {line} doesn't match expected format"
      target, left, right = g.groups()
      self.nodes[target] = (left, right)

  def solve_first_star(self) -> int:
    instructions = itertools.cycle(self.instructions)
    cur = 'AAA'
    counter = 0
    while cur != 'ZZZ':
      instruction = next(instructions)
      if instruction == 'L':
        cur = self.nodes[cur][0]
      elif instruction == 'R':
        cur = self.nodes[cur][1]
      else:
        raise RuntimeError(f'Unexpected instruction: {instruction}')
      counter += 1
    return counter

  def solve_second_star(self) -> int:
    start_nodes: list[str] = [node for node in self.nodes if node.endswith('A')]
    end_nodes: set[str] = set(node for node in self.nodes if node.endswith('Z'))
    loop_offsets: dict[str, int] = {}
    loop_sizes: dict[str, int] = {}
    destination_offset_in_loops: dict[str, list[int]] = {}
    for node in start_nodes:
      cur = node
      path: list[tuple[int, str]] = [(0, cur)]
      for instruction_offset, instruction in itertools.cycle(enumerate(self.instructions)):
        next_node = self.nodes[cur][0] if instruction == 'L' else self.nodes[cur][1]
        next_state = ((instruction_offset + 1) % len(self.instructions), next_node)
        if next_state in path:
          loop_offsets[node] = path.index(next_state)
          loop_sizes[node] = len(path) - loop_offsets[node]
          destination_offset_in_loops[node] = [i for i, [_, n] in enumerate(path) if n in end_nodes]
          break
        path.append(next_state)
        cur = next_node
    return math.lcm(*loop_sizes.values())

# vim: ts=2:sw=2:et
