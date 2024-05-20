import sys
import re
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(
  """
  time = (hour_am_pm ":" minute am_pm) / (hour_am_pm am_pm) / (hour  ":" minute) / hour
  hour = (digit_2 digit_0_3) / (digit_0_1 digit) / digit
  hour_am_pm = (digit_1 digit_0_2) / (digit_0 digit) / digit
  minute = digit_0_5 digit
  digit = ~"[0-9]"
  digit_0 = "0"
  digit_1 = "1"
  digit_0_1 = ~"[0-1]"
  digit_0_2 = ~"[0-2]"
  digit_2 = "2"
  digit_0_3 = ~"[0-3]"
  digit_0_5 = ~"[0-5]"
  am_pm = "am" / "pm"
  """
)

class TimeParser(NodeVisitor):
  def __init__(self, text):
    self.text = text
    self.hour = None
    self.minute = None
    self.am_pm = None

  def visit_time(self, node, visited_children):
    visited_children = visited_children[0]
    if type(visited_children) == int:
      self.hour = visited_children
      return
    if len(visited_children) > 0:
      self.hour = visited_children[0]
    if len(visited_children) == 2:
      self.am_pm = visited_children[1]
    if len(visited_children) > 2:
      self.minute = visited_children[2]
    if len(visited_children) > 3:
      self.am_pm = visited_children[3]

  def visit_hour(self, node, visited_children) -> int:
    return int(node.text)

  def visit_hour_am_pm(self, node, visited_children) -> int:
    return int(node.text)

  def visit_minute(self, node, visited_children) -> int:
    return int(node.text)

  def visit_am_pm(self, node, visited_children) -> list:
    return node.text

  def visit_digit(self, node, visited_children) -> list:
    return node.text

  def visit_digit_0_to_3(self, node, visited_children) -> list:
    return node.text

  def visit_digit_0_to_1(self, node, visited_children) -> list:
    return node.text

  def visit_digit_2(self, node, visited_children) -> list:
    return node.text

  def visit_digit_0_to_5(self, node, visited_children) -> list:
    return node.text

  def generic_visit(self, node, visited_children) -> list:
    return visited_children or node

  def parse(self) -> tuple:
    tree = grammar.parse(self.text)
    self.visit(tree)
    return self.hour, self.minute, self.am_pm

def get_minutes_past_midnight(hour: int, minute: int, am_pm: str) -> int:
  minutes_past_midnight: int = None
  if type(hour) == int:
    minutes_past_midnight = hour * 60
    if am_pm == 'pm':
      minutes_past_midnight += 12 * 60
    if type(minute) == int:
      minutes_past_midnight += minute
  return minutes_past_midnight

def time_parser(text) -> int:
  parser = TimeParser(text)
  hour, minute, am_pm = parser.parse()
  return get_minutes_past_midnight(hour, minute, am_pm)

def regex_time_parser(text) -> int:
  hour_pattern = r'([0-1]?[0-9]|2[0-3])'
  minute_pattern = r'([0-5]?[0-9])'
  am_pm_pattern = r'(am|pm)'
  hour_match = rf'({hour_pattern})'
  minute_match = rf'({minute_pattern})'
  am_pm_match = rf'({am_pm_pattern})'
  # continue here..
  return None

def main():
  if len(sys.argv) > 1:
    time: str = sys.argv[1]
    parser: str = sys.argv[2]
    if parser == 'regex':
      print('Using regex parser.')
    else:
      print('Using parsimonious parser.')
      minutes_past_midnight: int = time_parser(time)
    print(f'Time: {time} is {minutes_past_midnight} minutes past midnight.')
  else:
    print('Please provide a time to parse.')

if __name__ == "__main__":
  main()