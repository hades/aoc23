import collections
import math
import re

from .solver import Solver


class Day20(Solver):
  modules: dict[str, tuple[str, list[str]]]
  conjunction_inputs: dict[str, set[str]]

  def __init__(self):
    super().__init__(20)

  def presolve(self, input: str):
    self.modules = {}
    self.conjunction_inputs = collections.defaultdict(set)
    for line in input.splitlines():
      m = re.fullmatch(r'(\W?)(\w+) -> (.*)', line)
      assert m
      kind, name, destinations = m.groups()
      self.modules[name] = (kind, destinations.split(', '))
    for source, (_, destinations) in self.modules.items():
      for destination, (kind, _) in ((d, self.modules[d]) for d in destinations if d in self.modules):
        if kind == '&':
          self.conjunction_inputs[destination].add(source)

  def _press_button(self, flip_flops_on: set[str],
                    conjunction_high_pulses: dict[str, set[str]]) -> tuple[list[str], list[str]]:
    low_pulses: list[str] = []
    high_pulses: list[str] = []
    pulse: list[tuple[str, str, int]] = [('', 'broadcaster', 0)]
    while pulse:
      origin, source, value = pulse.pop(0)
      if value == 0:
        low_pulses.append(source)
      else:
        high_pulses.append(source)
      if source not in self.modules:
        continue
      kind, destinations = self.modules[source]
      if source == 'broadcaster':
        for d in destinations:
          pulse.append((source, d, value))
      elif kind == '%' and value == 0:
        if source in flip_flops_on:
          flip_flops_on.remove(source)
          for d in destinations:
            pulse.append((source, d, 0))
        else:
          flip_flops_on.add(source)
          for d in destinations:
            pulse.append((source, d, 1))
      elif kind == '&':
        if value:
          conjunction_high_pulses[source].add(origin)
        elif origin in conjunction_high_pulses[source]:
          conjunction_high_pulses[source].remove(origin)
        if conjunction_high_pulses[source] == self.conjunction_inputs[source]:
          for d in destinations:
            pulse.append((source, d, 0))
        else:
          for d in destinations:
            pulse.append((source, d, 1))
    return low_pulses, high_pulses


  def solve_first_star(self) -> int:
    flip_flops_on: set[str] = set()
    conjunction_high_pulses: dict[str, set[str]] = collections.defaultdict(set)
    low_pulse_count = 0
    high_pulse_count = 0
    for _ in range(1000):
      low, high = self._press_button(flip_flops_on, conjunction_high_pulses)
      low_pulse_count += len(low)
      high_pulse_count += len(high)
    return low_pulse_count* high_pulse_count

  def solve_second_star(self) -> int:
    flip_flops_on: set[str] = set()
    conjunction_high_pulses: dict[str, set[str]] = collections.defaultdict(set)
    button_count = 0
    rx_upstream = [module for module, (_, destinations) in self.modules.items() if 'rx' in destinations]
    if len(rx_upstream) != 1:
      rx_upstream = []
    else:
      rx_upstream = [module for module, (_, destinations) in self.modules.items() if rx_upstream[0] in destinations]
    rx_upstream_periods: list[int|None] = [None] * len(rx_upstream)
    low_pulses: list[str] = []
    while 'rx' not in low_pulses and (not rx_upstream or not all(rx_upstream_periods)):
      button_count += 1
      low_pulses, _ = self._press_button(flip_flops_on, conjunction_high_pulses)
      for module, periods in zip(rx_upstream, rx_upstream_periods, strict=True):
        if periods is not None:
          continue
        if module in low_pulses:
          rx_upstream_periods[rx_upstream.index(module)] = button_count
    if 'rx' in low_pulses:
      return button_count
    return math.lcm(*[x or 0 for x in rx_upstream_periods])

# vim: ts=2:sw=2:et
