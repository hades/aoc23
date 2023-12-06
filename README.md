Advent of Code 2023
===================

This package contains solutions to the Advent of Code 2023 edition:
https://adventofcode.com/2023/

Running
-------

```sh
$ day=1          # which challenge you want to solve
$ file=day01.in  # where the challenge input is stored
$ poetry install --without=dev
$ poetry run python -m aoc23 solve ${day} ${file}
```

Developing
----------

Please install the pre-commit hooks to make sure your code passes my very high
quality standards. /s

```sh
$ poetry install --with=dev
$ poetry run pre-commit install
```

Add unit tests for all solutions and utility functions.
