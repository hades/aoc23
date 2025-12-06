import datetime
import inspect
import logging
import sys
import timeit
import zoneinfo

import requests
from cleo.application import Application
from cleo.commands.command import Command
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option

from .autosubmit import submit
from .solver import get_solver_for_day


class CleoHandler(logging.Handler):
  def __init__(self, io):
    super().__init__()
    self.io = io
    self.setFormatter(logging.Formatter("<info>%(funcName)s:%(lineno)s: %(message)s"))

  def emit(self, record):
    self.io.write_line(self.format(record))

def get_problem_input(file: str|None, day: int, cookie: str|None) -> str:
  if file:
    with open(file, encoding='utf-8') as f:
      return f.read()
  if cookie:
    url = f'https://adventofcode.com/2023/day/{day}/input'
    r = requests.get(url, cookies={'session': cookie})
    r.raise_for_status()
    return r.text
  raise RuntimeError('No input file or cookie provided')

class SolveCommand(Command):
  name = "solve"
  arguments = [
    Argument("day", description="Which day (1 to 25) you want to solve"),
    Argument("input_file", description="Where the problem input data is stored", required=False),
  ]
  options = [
    Option("debug", description="Enables debug output", flag=True),
    Option("submit", description="Automatically submit the answer", flag=True),
    Option("cookie", description="Session cookie for downloading input data", flag=False),
    Option("second_only", description="Enables debug output", flag=True),
  ]

  def _setup_debug_logging(self):
    handler = CleoHandler(self.io)
    handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("debug logging enabled")

  def handle(self):
    if self.option('debug'):
      self._setup_debug_logging()
    day = int(self.argument('day'))
    self.line(f'<info>Solving day {day} challenge</info>')
    solver = get_solver_for_day(day)
    with self.spin('reading file', 'reading file complete'):
      input = get_problem_input(self.argument('input_file'), day, self.option('cookie'))
    with self.spin('parsing and pre-solving', 'presolving complete'):
      solver.presolve(input)
    if not self.option('second_only'):
      with self.spin('solving (first star)', 'solved (first star)'):
        solution = solver.solve_first_star()
      self.line(f'Answer (first star): <comment>{solution}</>')
      if self.option('submit'):
        with self.spin('submitting first star answer', 'first star answer submitted'):
          submit_result = submit(day, 1, str(solution), self.option('cookie'))
        self.line(f'Submit result (first star): <comment>{submit_result.name}</>')
    with self.spin('solving (second star)', 'solved (second star)'):
      solution = solver.solve_second_star()
    self.line(f'Answer (second star): <comment>{solution}</>')
    if self.option('submit'):
      with self.spin('submitting second star answer', 'second star answer submitted'):
        submit_result = submit(day, 2, str(solution), self.option('cookie'))
      self.line(f'Submit result (second star): <comment>{submit_result.name}</>')

class EvaluateCommand(Command):
  name = "evaluate"
  arguments = [
    Argument("input_files", description="Where the problem input data is stored (1 file per day)",
             required=False, is_list=True),
  ]
  options = [
    Option("cookie", description="Session cookie for downloading input data",
           flag=False),
    Option("repeats_for_timing", description="How many times to solve the problem for timing purposes",
           flag=False, default=3),
  ]

  def __solve_both_for_day(self, day: int, input: str):
    solver = get_solver_for_day(day)
    solver.flush_caches()
    solver.presolve(input)
    solver.solve_first_star()
    solver.solve_second_star()

  def handle(self) -> int:
    days = min(25, (datetime.datetime.now(tz=zoneinfo.ZoneInfo('America/New_York')).date() -
                    datetime.date(2023, 12, 1)).days + 1)
    repeats = int(self.option('repeats_for_timing'))
    times: list[float] = []
    linecounts: list[int] = []
    if len(self.argument('input_files')) != days and not self.option('cookie'):
      self.line_error(f'Either provide {days} input files (one for each day) or a session cookie')
      return 1
    for day in range(1, days + 1):
      with self.spin(f'retrieving input data for day {day}', f'input data for day {day} retrieved'):
        input = get_problem_input(self.argument('input_files')[day - 1] if self.argument('input_files') else None,
                                  day, self.option('cookie'))
      with self.spin(f'solving {repeats} times', 'solved'):
        times.append(min(timeit.repeat(
          lambda: self.__solve_both_for_day(day, input),  # noqa: B023
          repeat=repeats, number=1)))
      mod = inspect.getmodule(type(get_solver_for_day(day)))
      if mod is None:
        raise RuntimeError(f"unable to inspect.getmodule for solver for day {day}")
      linecounts.append(len(inspect.getsource(mod).splitlines()))
    self.table().set_headers(['Day', 'Time (s)', 'Lines', 'line-seconds']).add_rows([
      [f'{day:2d}', f'{time:5.3f}', f'{linecount:4d}', f'{time * linecount:6.3f}']
      for day, time, linecount in zip(range(1, days + 1), times, linecounts, strict=True)]).render()
    return 0


app = Application()
app.add(SolveCommand())
app.add(EvaluateCommand())

sys.setrecursionlimit(10000)
app.run()

# vim: ts=2:sw=2:et
