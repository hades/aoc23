import re
from collections.abc import Callable


def upper_bound(start: int, stop: int, predicate: Callable[[int], bool]) -> int:
  """Find the smallest integer in [start, stop) for which the predicate is
   false, or stop if the predicate is always true.

   The predicate must be monotonic, i.e. predicate(x + 1) implies predicate(x).
   """
  assert start < stop
  if not predicate(start):
    return start
  if predicate(stop - 1):
    return stop
  while start + 1 < stop:
    mid = (start + stop) // 2
    if predicate(mid):
      start = mid
    else:
      stop = mid
  return stop

def assert_full_match(pattern: str, string: str) -> re.Match:
  """Matches the pattern against the string and raises an exception if the
   pattern does not match the string."""
  m = re.fullmatch(pattern, string)
  if not m:
    raise RuntimeError(f'pattern {pattern} does not match {string}')
  return m

# vim: ts=2:sw=2:et
