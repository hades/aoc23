import dataclasses
import functools

from .solver import Solver


class MatchState:
  pass

@dataclasses.dataclass
class NotMatching(MatchState):
  pass

@dataclasses.dataclass
class Matching(MatchState):
  current_length: int
  desired_length: int

@functools.cache
def _match_one_template(template: str, groups: tuple[int, ...]) -> int:
  if not groups:
    if '#' in template:
      return 0
    else:
      return 1
  state: MatchState = NotMatching()
  remaining_groups: list[int] = list(groups)
  options_in_other_branches: int = 0
  for i in range(len(template)):
    match (state, template[i]):
      case (NotMatching(), '.'):
        pass
      case (NotMatching(), '?'):
        options_in_other_branches += _match_one_template(template[i+1:], tuple(remaining_groups))
        if not remaining_groups:
          return options_in_other_branches
        group, *remaining_groups = remaining_groups
        state = Matching(1, group)
      case (NotMatching(), '#'):
        if not remaining_groups:
          return options_in_other_branches
        group, *remaining_groups = remaining_groups
        state = Matching(1, group)
      case (Matching(current_length, desired_length), '.') if current_length == desired_length:
        state = NotMatching()
      case (Matching(current_length, desired_length), '.') if current_length < desired_length:
        return options_in_other_branches
      case (Matching(current_length, desired_length), '?') if current_length == desired_length:
        state = NotMatching()
      case (Matching(current_length, desired_length), '?') if current_length < desired_length:
        state = Matching(current_length + 1, desired_length)
      case (Matching(current_length, desired_length), '#') if current_length < desired_length:
        state = Matching(current_length + 1, desired_length)
      case (Matching(current_length, desired_length), '#') if current_length == desired_length:
        return options_in_other_branches
      case _:
        raise RuntimeError(f'unexpected {state=} with {template=} position {i} and {remaining_groups=}')
  match state, remaining_groups:
    case NotMatching(), []:
      return options_in_other_branches + 1
    case Matching(current, desired), [] if current == desired:
      return options_in_other_branches + 1
    case (NotMatching(), _) | (Matching(_, _), _):
      return options_in_other_branches
  raise RuntimeError(f'unexpected {state=} with {template=} at end of template and {remaining_groups=}')


def _unfold(template: str, groups: tuple[int, ...]) -> tuple[str, tuple[int, ...]]:
  return '?'.join([template] * 5), groups * 5


class Day12(Solver):

  def __init__(self):
    super().__init__(12)
    self.input: list[tuple[str, tuple[int, ...]]] = []

  def presolve(self, input: str):
    lines = input.rstrip().split('\n')
    for line in lines:
      template, groups = line.split(' ')
      self.input.append((template, tuple(int(group) for group in groups.split(','))))

  def solve_first_star(self) -> int:
    return sum(_match_one_template(template, groups) for template, groups in self.input)

  def solve_second_star(self) -> int:
    return sum(_match_one_template(*_unfold(template, groups)) for template, groups in self.input)

  def flush_caches(self):
    _match_one_template.cache_clear()

# vim: ts=2:sw=2:et
