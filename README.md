Advent of Code 2023
===================

This package contains solutions to the Advent of Code 2023 edition:
https://adventofcode.com/2023/

Running
-------

```sh
$ day=1          # which challenge you want to solve
$ file=day01.in  # where the challenge input is stored
$ uv run --no-dev python -m aoc23 solve ${day} ${file}
```

Auto-downloading Problem Input
------------------------------

You can provide the `session` cookie instead of the input data file:

```sh
$ session=01234dead...beef
$ uv run --no-dev python -m aoc23 solve 13 --cookie=$session
```

Evaluation
----------

There is an option to run all of the solvers and show useful stats, such as
lines of code in the solution, and how long the solver took. Just provide all
of the input files, or a cookie:

```sh
$ session=01234dead...beef
$ uv run --no-dev python -m aoc23 evaluate *.txt
$ uv run --no-dev python -m aoc23 evaluate --cookie=$session
```

Developing
----------

Please install the pre-commit hooks to make sure your code passes my very high
quality standards. /s

```sh
$ uv run --all-groups pre-commit install
```

Add unit tests for all solutions and utility functions.
