import re
import unittest
from parsimonious.exceptions import IncompleteParseError
from parsimonious.exceptions import ParseError

from main import get_minutes_past_midnight
from main import is_valid_user_arguments
from main import get_time_or_minutes_past_midnight
from peg_time_parser import time_parser
from regex_time_parser import regex_time_parser
from regex_time_parser import get_value_from_search_groups
from regex_time_parser import cast_to_int
from regex_time_parser import replace_character_with_empty

class TestTimeParser(unittest.TestCase):
  def test_time_parser(self):
    self.assertEqual(time_parser('4'), (4, None, None))
    self.assertEqual(time_parser('7:38pm'), (7, 38, 'pm'))
    self.assertEqual(time_parser('23:42'), (23, 42, None))
    self.assertEqual(time_parser('3:16'), (3, 16, None))
    self.assertEqual(time_parser('3:16am'), (3, 16, 'am'))

  def test_time_parser_single_hour(self):
    for i in range(1, 23):
      self.assertEqual(time_parser(str(i)), (i, None, None))

  def test_time_parser_hour_and_minute(self):
    for i in range(1, 23):
      for j in range(1, 59):
        if j < 10:
          self.assertEqual(time_parser(f'{i}:0{j}'), (i, j, None))
        else:
          self.assertEqual(time_parser(f'{i}:{j}'), (i, j, None))

  def test_time_parser_single_hour_am_pm(self):
    for i in range(1, 12):
      self.assertEqual(time_parser(f'{i}am'), (i, None, 'am'))
      self.assertEqual(time_parser(f'{i}pm'), (i, None, 'pm'))

  def test_time_parser_hour_and_minute_am_pm(self):
    for i in range(1, 12):
      for j in range(1, 59):
        if j < 10:
          self.assertEqual(time_parser(f'{i}:0{j}am'), (i, j, 'am'))
          self.assertEqual(time_parser(f'{i}:0{j}pm'), (i, j, 'pm'))
        else:
          self.assertEqual(time_parser(f'{i}:{j}am'), (i, j, 'am'))
          self.assertEqual(time_parser(f'{i}:{j}pm'), (i, j, 'pm'))

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
    self.assertEqual(regex_time_parser('7:38pm'), (7, 38, 'pm'))
    self.assertEqual(regex_time_parser('23:42'), (23, 42, None))
    self.assertEqual(regex_time_parser('3:16'), (3, 16, None))
    self.assertEqual(regex_time_parser('3:16am'), (3, 16, 'am'))

  def test_get_value_from_search_groups_should_return_search_group(self):
    hour_pattern: str = '^(2[0-3])|([0-1]?[0-9])'
    minute_pattern: str = ':[0-5]?[0-9]'
    am_pm_pattern: str = 'am$|pm$'
    def get_mock_search_group(text: str, pattern: str):
      return re.search(pattern, text)
    self.assertEqual(get_value_from_search_groups(None, None, None), (None, None, None))
    self.assertEqual(get_value_from_search_groups(get_mock_search_group('4', hour_pattern), None, None), (4, None, None))
    self.assertEqual(get_value_from_search_groups(None, get_mock_search_group(':07', minute_pattern), None), (None, 7, None))
    self.assertEqual(get_value_from_search_groups(None, None, get_mock_search_group('pm', am_pm_pattern)), (None, None, 'pm'))
    self.assertEqual(get_value_from_search_groups(
      get_mock_search_group('4', hour_pattern),
      get_mock_search_group(':07', minute_pattern),
      get_mock_search_group('am', am_pm_pattern)),
      (4, 7, 'am'))

  def test_cast_to_int(self):
    self.assertEqual(cast_to_int('4'), 4)
    self.assertEqual(cast_to_int('7'), 7)
    self.assertEqual(cast_to_int('42'), 42)

  def test_replace_character_with_empty(self):
    self.assertEqual(replace_character_with_empty('4:', ':'), '4')
    self.assertEqual(replace_character_with_empty('7;', ';'), '7')
    self.assertEqual(replace_character_with_empty('42.', '.'), '42')
    self.assertEqual(replace_character_with_empty('11.', ':'), '11.')

  def test_all_user_arguments_are_provided(self):
    good_args1: list = ['main.py', '23:12', 'parsimonious', 'time']
    good_args2: list = ['main.py', '23:12', 'regex', 'minutes_past_midnight']
    bad_args1: list = ['main.py']
    bad_args2: list = ['main.py', '23:12', 'unknown_parser', 'unknown_something']
    bad_args3: list = ['main.py', '23:12', 'unknown_parser', 'time']
    self.assertEqual(is_valid_user_arguments(good_args1), True)
    self.assertEqual(is_valid_user_arguments(good_args2), True)
    self.assertEqual(is_valid_user_arguments(bad_args1), False)
    self.assertEqual(is_valid_user_arguments(bad_args2), False)
    self.assertEqual(is_valid_user_arguments(bad_args3), False)

  def test_hour_and_minute_regex(self):
    for i in range(0, 23):
      for j in range(0, 59):
        self.assertEqual(regex_time_parser(f'{i}:{j}'), (i, j, None))

  def test_single_hour_regex(self):
    for i in range(0, 23):
      self.assertEqual(regex_time_parser(f'{i}'), (i, None, None))

  def test_single_hour_am_regex(self):
    for i in range(1, 12):
      self.assertEqual(regex_time_parser(f'{i}am'), (i, None, 'am'))

  def test_get_single_hour_pm_regex(self):
    for i in range(1, 12):
      self.assertEqual(regex_time_parser(f'{i}pm'), (i, None, 'pm'))

  def test_hour_and_minute_am_regex(self):
    for i in range(1, 12):
      for j in range(0, 59):
        self.assertEqual(regex_time_parser(f'{i}:{j}am'), (i, j, 'am'))

  def test_hour_and_minute_pm_regex(self):
    for i in range(1, 12):
      for j in range(0, 59):
        self.assertEqual(regex_time_parser(f'{i}:{j}pm'), (i, j, 'pm'))

  def test_time_parser_should_not_parse_over_12_when_using_am_pm(self):
    with self.assertRaises(Exception) as context:
      regex_time_parser('13:00am')
    self.assertTrue('Invalid time.' in str(context.exception))

  def test_time_parser_rise_parse_error(self):
    with self.assertRaises(Exception) as context:
      regex_time_parser('lölölölöl')
    self.assertTrue('Invalid time.' in str(context.exception))

  def test_time_parser_rise_incomplete_parse_error(self):
    with self.assertRaises(Exception) as context:
      regex_time_parser('10010101')
    self.assertTrue('Invalid time.' in str(context.exception))

  def test_get_time_or_minutes_past_midnight(self):
    self.assertEqual(get_time_or_minutes_past_midnight('time', 4, 7, 'pm'), (4, 7, 'pm'))
    self.assertEqual(get_time_or_minutes_past_midnight('minutes_past_midnight', 4, 7, 'pm'), 4 * 60 + 7 + 12 * 60)

if __name__ == '__main__':
  unittest.main()