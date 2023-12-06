from unittest import TestCase

from aoc23 import util

class TestUpperBound(TestCase):
  def test_asserts_start_stop(self):
    with self.assertRaises(AssertionError):
      util.upper_bound(2, 1, lambda x: True)
    with self.assertRaises(AssertionError):
      util.upper_bound(1, 1, lambda x: True)

  def test_one_element(self):
    self.assertEqual(util.upper_bound(0, 1, lambda x: True), 1)
    self.assertEqual(util.upper_bound(0, 1, lambda x: False), 0)

  def test_two_elements(self):
    self.assertEqual(util.upper_bound(0, 2, lambda x: True), 2)
    self.assertEqual(util.upper_bound(0, 2, lambda x: x < 1), 1)
    self.assertEqual(util.upper_bound(0, 2, lambda x: False), 0)

  def test_three_elements(self):
    self.assertEqual(util.upper_bound(0, 3, lambda x: True), 3)
    self.assertEqual(util.upper_bound(0, 3, lambda x: x < 2), 2)
    self.assertEqual(util.upper_bound(0, 3, lambda x: x < 1), 1)
    self.assertEqual(util.upper_bound(0, 3, lambda x: False), 0)

  def test_four_elements(self):
    self.assertEqual(util.upper_bound(0, 4, lambda x: True), 4)
    self.assertEqual(util.upper_bound(0, 4, lambda x: x < 3), 3)
    self.assertEqual(util.upper_bound(0, 4, lambda x: x < 2), 2)
    self.assertEqual(util.upper_bound(0, 4, lambda x: x < 1), 1)
    self.assertEqual(util.upper_bound(0, 4, lambda x: False), 0)

# vim: ts=2:sw=2:et
