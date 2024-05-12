import unittest
from parsimonious.exceptions import IncompleteParseError

from main import time_parser

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

  def test_time_parser_should_not_parse_over_12_when_using_am_pm(self):
    with self.assertRaises(IncompleteParseError):
      time_parser('13:00am')

  def test_time_parser_invalid(self):
    with self.assertRaises(IncompleteParseError):
      time_parser('10010101')

if __name__ == '__main__':
  unittest.main()