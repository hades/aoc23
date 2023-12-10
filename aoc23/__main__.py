import logging

from cleo.application import Application
from cleo.commands.command import Command
from cleo.io.inputs.argument import Argument
from cleo.io.inputs.option import Option

from .solver import get_solver_for_day


class CleoHandler(logging.Handler):
  def __init__(self, io):
    super().__init__()
    self.io = io
    self.setFormatter(logging.Formatter("<info>%(funcName)s:%(lineno)s: %(message)s"))

  def emit(self, record):
    self.io.write_line(self.format(record))


class SolveCommand(Command):
  name = "solve"
  arguments = [
    Argument("day", description="Which day (1 to 25) you want to solve"),
    Argument("input_file", description="Where the problem input data is stored"),
  ]
  options = [
    Option("debug", description="Enables debug output", flag=True),
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
    file = self.argument('input_file')
    self.line(f'<info>Solving day {day} challenge</info>')
    solver = get_solver_for_day(day)
    with self.spin('reading file', 'reading file complete'):
      with open(file, encoding='utf-8') as f:
        input = f.read()
    with self.spin('parsing and pre-solving', 'presolving complete'):
      solver.presolve(input)
    with self.spin('solving', 'solved'):
      solution = solver.solve_first_star()
    self.line(f'Answer (first star): <comment>{solution}</>')
    with self.spin('solving', 'solved'):
      solution = solver.solve_second_star()
    self.line(f'Answer (second star): <comment>{solution}</>')


app = Application()
app.add(SolveCommand())

app.run()

# vim: ts=2:sw=2:et
