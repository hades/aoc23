import functools
import operator
import re

import portion as P  # noqa: N812

from .solver import Solver


def isize(i: P.Interval):
  return sum(i_part.upper - i_part.lower - int(i_part.left == P.OPEN) + int(i_part.right == P.CLOSED)
             for i_part in i)

class Day19(Solver):
  workflows: dict[str, list[str|tuple[str, str, int, str]]]
  parts: list[dict[str, int]]

  def __init__(self):
    super().__init__(19)

  def presolve(self, input: str):
    lines = input.splitlines()
    self.workflows = {}
    while lines:
      line = lines.pop(0)
      if not line:
        break
      name, program = line.split('{')
      instructions = program[:-1].split(',')
      self.workflows[name] = []
      for item in instructions:
        match_condition = re.fullmatch(r'(\w+)([<>])(\d+):(\w+)', item)
        if match_condition:
          category, op, threshold, goto = match_condition.groups()
          self.workflows[name].append((category, op, int(threshold), goto))
        else:
          self.workflows[name].append(item)
    self.parts = []
    while lines:
      items = lines.pop(0)[1:-1].split(',')
      part = {}
      for category, value in (i.split('=') for i in items):
        part[category] = int(value)
      self.parts.append(part)

  def solve_first_star(self):
    return sum(sum(part.values()) for part in self.parts if
               self._count_options('in', 0, {c: P.singleton(v) for c, v in part.items()}) > 0)

  def solve_second_star(self):
    return self._count_options('in', 0, {c: P.closed(1, 4000) for c in self.parts[0].keys()})

  def _count_options(self, workflow_name: str, workflow_index: int, ranges: dict[str, P.Interval]) -> int:
    if workflow_name == 'A':
      return functools.reduce(operator.mul, (isize(r) for r in ranges.values()), 1)
    if workflow_name == 'R':
      return 0
    if any(isize(r) == 0 for r in ranges.values()):
      return 0
    match self.workflows[workflow_name][workflow_index]:
      # Types ignored in the lines below should be correct because of match arms.
      # Why mypy does not recognize that is a mystery.
      case (category, '>', threshold, goto):
        new_ranges_true = {c: r & P.open(threshold, P.inf) if c == category else r for c, r in ranges.items()}
        new_ranges_false = {c: r & P.openclosed(-P.inf, threshold) if c == category else r for c, r in ranges.items()}
        return (self._count_options(goto, 0, new_ranges_true) + # type: ignore[arg-type]
                self._count_options(workflow_name, workflow_index + 1, new_ranges_false))
      case (category, '<', threshold, goto):
        new_ranges_true = {c: r & P.open(-P.inf, threshold) if c == category else r for c, r in ranges.items()}
        new_ranges_false = {c: r & P.closedopen(threshold, P.inf) if c == category else r for c, r in ranges.items()}
        return (self._count_options(goto, 0, new_ranges_true) + # type: ignore[arg-type]
                self._count_options(workflow_name, workflow_index + 1, new_ranges_false))
      case next_workflow:
        return self._count_options(next_workflow, 0, ranges) # type: ignore[arg-type]

# vim: ts=2:sw=2:et
