"""Provides base class for the solvers."""

_all_solvers: dict[int, "Solver"] = {}

class Solver:
  def __init__(self, day):
    _all_solvers[day] = self

  def presolve(self, input: str):
    raise NotImplementedError()

  def solve_first_star(self) -> int:
    raise NotImplementedError()

  def solve_second_star(self) -> int:
    raise NotImplementedError()

  def flush_caches(self):
    pass

def get_solver_for_day(d: int) -> Solver:
  if d not in _all_solvers:
    raise ValueError(f"solver does not exist for day {d}")
  return _all_solvers[d]

# vim: ts=2:sw=2:et
