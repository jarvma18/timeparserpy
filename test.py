import unittest

from main import time_parser

class TestTimeParser(unittest.TestCase):
  def test_time_parser(self):
    self.assertEqual(time_parser('12:00:00'), 720)
    self.assertEqual(time_parser('00:00:00'), 0)
    self.assertEqual(time_parser('23:59:59'), 1439)
    self.assertEqual(time_parser('01:00:00'), 60)
    self.assertEqual(time_parser('00:01:00'), 1)
    self.assertEqual(time_parser('00:00:01'), 0)

if __name__ == '__main__':
  unittest.main()