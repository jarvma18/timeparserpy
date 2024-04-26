import unittest

from main import time_parser

class TestTimeParser(unittest.TestCase):
  def test_time_parser(self):
    self.assertEqual(time_parser('4'), 16 * 60)
    self.assertEqual(time_parser('7:38pm'), 19 * 60 + 38)
    self.assertEqual(time_parser('23:42'), 23 * 60 + 42)
    self.assertEqual(time_parser('3:16'), 3 * 60 + 16)
    self.assertEqual(time_parser('3:16am'), 3 * 60 + 16)

if __name__ == '__main__':
  unittest.main()