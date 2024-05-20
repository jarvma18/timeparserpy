import unittest
from parsimonious.exceptions import IncompleteParseError
from parsimonious.exceptions import ParseError

from main import time_parser
from main import get_minutes_past_midnight
from main import regex_time_parser

class TestTimeParser(unittest.TestCase):
  def test_time_parser(self):
    self.assertEqual(time_parser('4'), 4 * 60)
    self.assertEqual(time_parser('7:38pm'), 19 * 60 + 38)
    self.assertEqual(time_parser('23:42'), 23 * 60 + 42)
    self.assertEqual(time_parser('3:16'), 3 * 60 + 16)
    self.assertEqual(time_parser('3:16am'), 3 * 60 + 16)

  def test_time_parser_single_hour(self):
    for i in range(1, 23):
      self.assertEqual(time_parser(str(i)), i * 60)

  def test_time_parser_hour_and_minute(self):
    for i in range(1, 23):
      for j in range(1, 59):
        if j < 10:
          self.assertEqual(time_parser(f'{i}:0{j}'), i * 60 + j)
        else:
          self.assertEqual(time_parser(f'{i}:{j}'), i * 60 + j)

  def test_time_parser_single_hour_am_pm(self):
    for i in range(1, 12):
      self.assertEqual(time_parser(f'{i}am'), i * 60)
      self.assertEqual(time_parser(f'{i}pm'), i * 60 + 12 * 60)

  def test_time_parser_hour_and_minute_am_pm(self):
    for i in range(1, 12):
      for j in range(1, 59):
        if j < 10:
          self.assertEqual(time_parser(f'{i}:0{j}am'), i * 60 + j)
          self.assertEqual(time_parser(f'{i}:0{j}pm'), i * 60 + j + 12 * 60)
        else:
          self.assertEqual(time_parser(f'{i}:{j}am'), i * 60 + j)
          self.assertEqual(time_parser(f'{i}:{j}pm'), i * 60 + j + 12 * 60)

  def test_time_parser_should_not_parse_over_12_when_using_am_pm(self):
    with self.assertRaises(IncompleteParseError):
      time_parser('13:00am')

  def test_time_parser_rise_parse_error(self):
    with self.assertRaises(ParseError):
      time_parser('lölölölöl')

  def test_time_parser_raisa_incomplete_parse_error(self):
    with self.assertRaises(IncompleteParseError):
      time_parser('10010101')

  def test_get_minutes_past_midnight(self):
    for i in range(0, 23):
      for j in range(0, 59):
        self.assertEqual(get_minutes_past_midnight(i, j, ''), i * 60 + j)

  def test_get_minutes_past_midnight_single_hour(self):
    for i in range(0, 23):
      self.assertEqual(get_minutes_past_midnight(i, None, None), i * 60)

  def test_get_minutes_past_midnight_single_hour_am(self):
    for i in range(1, 12):
      self.assertEqual(get_minutes_past_midnight(i, None, 'am'), i * 60)

  def test_get_minutes_past_midnight_single_hour_pm(self):
    for i in range(1, 12):
      self.assertEqual(get_minutes_past_midnight(i, None, 'pm'), i * 60 + 12 * 60)

  def test_get_minutes_past_midnight_am(self):
    for i in range(1, 12):
      for j in range(0, 59):
        self.assertEqual(get_minutes_past_midnight(i, j, 'am'), i * 60 + j)

  def test_get_minutes_past_midnight_pm(self):
    for i in range(1, 12):
      for j in range(0, 59):
        self.assertEqual(get_minutes_past_midnight(i, j, 'pm'), i * 60 + j + 12 * 60)

  def test_get_minutes_past_midnight_should_return_none(self):
    self.assertEqual(get_minutes_past_midnight(None, None, None), None)

  def test_regex_parser_should_return_tuple(self):
    self.assertEqual(regex_time_parser('4'), (4, None, None))
    self.assertEqual(regex_time_parser('7:38pm'), (19, 38, 'pm'))
    self.assertEqual(regex_time_parser('23:42'), (23, 42, None))
    self.assertEqual(regex_time_parser('3:16'), (3, 16, None))
    self.assertEqual(regex_time_parser('3:16am'), (3, 16, 'am'))

if __name__ == '__main__':
  unittest.main()