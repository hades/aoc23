import collections

from aoc23.util import assert_full_match

from .solver import Solver


def _hash(string: str) -> int:
  result = 0
  for c in string:
    result = (result + ord(c)) * 17 % 256
  return result

class Day15(Solver):
  input: list[str]

  def __init__(self):
    super().__init__(15)

  def presolve(self, input: str):
    self.input = input.rstrip().split(',')

  def solve_first_star(self) -> int:
    return sum(_hash(string) for string in self.input)

  def solve_second_star(self) -> int:
    boxes: list[collections.OrderedDict[str, str]] = [collections.OrderedDict() for _ in range(256)]
    for instruction in self.input:
      label, op, value = assert_full_match(r'([a-z]+)([=-])(\d*)', instruction).groups()
      box = boxes[_hash(label)]
      match op:
        case '-':
          if label in box:
            del box[label]
        case '=':
          box[label] = value
    return sum((1 + box_idx) * (1 + lens_idx) * int(value)
                for box_idx, box in enumerate(boxes)
                for lens_idx, (_, value) in enumerate(box.items()))

# vim: ts=2:sw=2:et
