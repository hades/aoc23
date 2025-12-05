# type: ignore

import enum
import logging
import pathlib
import re
import time

import requests
import tomlkit

LOG = logging.getLogger('aoc23.autosubmit')
_RESULT_STORE_FILE = "results.toml"

class Result(enum.Enum):
  ACCEPTED = 0
  REJECTED = 1
  REJECTED_TOO_LOW = 2
  REJECTED_TOO_HIGH = 3

def _submit_to_server(day: int, part: int, answer: str, cookie: str) -> Result:
  url = f'https://adventofcode.com/2023/day/{day}/answer'
  data = {'level': part, 'answer': answer}
  headers = {'Cookie': f'session={cookie}'}
  request = requests.post(url, data=data, headers=headers)
  request.raise_for_status()
  text = request.text
  if "You gave an answer too recently" in text:
    try:
      [(minutes, seconds)] = re.findall(r"You have (?:(\d+)m )?(\d+)s left to wait", text)
      LOG.info("waiting for %s minutes and %s seconds", minutes, seconds)
      time.sleep(int(minutes or 0) * 60 + int(seconds))
      return _submit_to_server(day, part, answer, cookie)
    except ValueError as e:
      LOG.error("failed to parse timeout message %s", text)
      raise RuntimeError from e
  if "That's the right answer" in text:
    return Result.ACCEPTED
  if "your answer is too high" in text:
    return Result.REJECTED_TOO_HIGH
  if "your answer is too low" in text:
    return Result.REJECTED_TOO_LOW
  return Result.REJECTED

def _write_initial_result_store(file_path: pathlib.Path):
  store = tomlkit.document()
  store.add(tomlkit.comment("This file contains the previously submitted results for AoC 2023."))
  store.add(tomlkit.nl())
  if not file_path.exists():
    with file_path.open('w') as f:
      f.write(tomlkit.dumps(store))

def submit(day: int, part: int, answer: str, cookie: str) -> Result:
  file_path = pathlib.Path(_RESULT_STORE_FILE)
  if not file_path.exists():
    _write_initial_result_store(file_path)
  with file_path.open() as f:
    results = tomlkit.parse(f.read())
  key = f"day{day}.part{part}"
  if key not in results:
    results[key] = tomlkit.table()
  if 'accepted' in results[key]:
    logging.debug("answer %s for %s.%s is already accepted", results[key]['accepted'], day, part)
    return Result.ACCEPTED if answer == results[key]['accepted'] else Result.REJECTED
  if 'upper_bound' in results[key]:
    if int(answer) >= results[key]['upper_bound']:
      logging.debug("answer %s for %s.%s is not lower than a previously rejected answer %s",
                    answer, day, part, results[key]['upper_bound'])
      return Result.REJECTED_TOO_HIGH
  if 'lower_bound' in results[key]:
    if int(answer) <= results[key]['lower_bound']:
      logging.debug("answer %s for %s.%s is not higher than a previously rejected answer %s",
                    answer, day, part, results[key]['lower_bound'])
      return Result.REJECTED_TOO_LOW
  if answer in results[key].get('rejected', []):
    logging.debug("answer %s for %s.%s is already rejected", answer, day, part)
    return Result.REJECTED
  result = _submit_to_server(day, part, answer, cookie)
  if result == Result.ACCEPTED:
    results[key]['accepted'] = answer
  if result == Result.REJECTED_TOO_HIGH:
    upper_bound = int(answer)
    if 'upper_bound' in results[key]:
      upper_bound = min(upper_bound, results[key]['upper_bound'])
    results[key]['upper_bound'] = int(answer)
  if result == Result.REJECTED_TOO_LOW:
    lower_bound = int(answer)
    if 'lower_bound' in results[key]:
      lower_bound = max(lower_bound, results[key]['lower_bound'])
    results[key]['lower_bound'] = int(answer)
  if result == Result.REJECTED:
    if 'rejected' not in results[key]:
      results[key]['rejected'] = []
    results[key]['rejected'].append(answer)
  with file_path.open('w') as f:
    f.write(tomlkit.dumps(results))
  return result

# vim: ts=2:sw=2:et
