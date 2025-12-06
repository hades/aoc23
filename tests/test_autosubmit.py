import functools
import tempfile
import unittest

import responses

from aoc23 import autosubmit


def temp_autosubmit_results(f):
  @functools.wraps(f)
  def wrapper(*args, **kwargs):
    with tempfile.NamedTemporaryFile() as file:
      autosubmit._RESULT_STORE_FILE = file.name
      return f(*args, **kwargs)
  return wrapper


class TestAutosubmit(unittest.TestCase):
  @temp_autosubmit_results
  @responses.activate
  def test_accepted_result(self):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s the right answer</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.ACCEPTED)

  @temp_autosubmit_results
  @responses.activate
  def test_rejected_result(self):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED)

  @temp_autosubmit_results
  @responses.activate
  def test_rejected_too_low(self):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer - your answer is too low.</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED_TOO_LOW)

  @temp_autosubmit_results
  @responses.activate
  def test_rejected_too_high(self):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer - your answer is too high.</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED_TOO_HIGH)

  @temp_autosubmit_results
  @responses.activate
  def test_does_not_resubmit_accepted_result(self):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s the right answer</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.ACCEPTED)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body=AssertionError('should not be called'))
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.ACCEPTED)

  @temp_autosubmit_results
  @responses.activate
  def test_does_not_resubmit_rejected_result(self):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body=AssertionError('should not be called'))
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED)

  @temp_autosubmit_results
  @responses.activate
  def test_multiple_rejected_results(self):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer</p></html>', status=200)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer</p></html>', status=200)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '41', 'cookie'), autosubmit.Result.REJECTED)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED)
    self.assertEqual(autosubmit.submit(7, 1, '43', 'cookie'), autosubmit.Result.REJECTED)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body=AssertionError('should not be called'))
    self.assertEqual(autosubmit.submit(7, 1, '41', 'cookie'), autosubmit.Result.REJECTED)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED)
    self.assertEqual(autosubmit.submit(7, 1, '43', 'cookie'), autosubmit.Result.REJECTED)

  @temp_autosubmit_results
  @responses.activate
  def test_checks_upper_bound(self):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer - your answer is too high.</p></html>', status=200)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer - your answer is too high.</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED_TOO_HIGH)
    self.assertEqual(autosubmit.submit(7, 1, '40', 'cookie'), autosubmit.Result.REJECTED_TOO_HIGH)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body=AssertionError('should not be called'))
    self.assertEqual(autosubmit.submit(7, 1, '50', 'cookie'), autosubmit.Result.REJECTED_TOO_HIGH)

  @temp_autosubmit_results
  @responses.activate
  def test_checks_lower_bound(self):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer - your answer is too low.</p></html>', status=200)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer - your answer is too low.</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED_TOO_LOW)
    self.assertEqual(autosubmit.submit(7, 1, '44', 'cookie'), autosubmit.Result.REJECTED_TOO_LOW)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body=AssertionError('should not be called'))
    self.assertEqual(autosubmit.submit(7, 1, '30', 'cookie'), autosubmit.Result.REJECTED_TOO_LOW)

  @temp_autosubmit_results
  @responses.activate
  @unittest.mock.patch('time.sleep')
  def test_waits_when_timed_out(self, mock_sleep: unittest.mock.MagicMock):
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>You gave an answer too recently. You have 5m 31s left to wait"</p></html>',
                   status=200)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s not the right answer</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '42', 'cookie'), autosubmit.Result.REJECTED)
    mock_sleep.assert_called_once_with(331)
    mock_sleep.reset_mock()
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>You gave an answer too recently. You have 57s left to wait"</p></html>', status=200)
    responses.post('https://adventofcode.com/2023/day/7/answer',
                   body='<html><p>That\'s the right answer</p></html>', status=200)
    self.assertEqual(autosubmit.submit(7, 1, '41', 'cookie'), autosubmit.Result.ACCEPTED)
    mock_sleep.assert_called_with(57)

# vim: ts=2:sw=2:et
