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

def time_parser(text: str) -> int:
  parser = TimeParser(text)
  hour, minute, am_pm = parser.parse()
  return get_minutes_past_midnight(hour, minute, am_pm)

def get_value_from_search_groups(hour, minute, am_pm) -> tuple:
  if hour != None:
    hour = hour.group(0)
    hour = replace_character_with_empty(hour, ':')
    hour = replace_character_with_empty(hour, 'am')
    hour = replace_character_with_empty(hour, 'pm')
    hour = cast_to_int(hour)
  if minute != None:
    minute = minute.group(0)
    minute = replace_character_with_empty(minute, ':')
    minute = cast_to_int(minute)
  if am_pm != None:
    am_pm = am_pm.group(0)
    am_pm = replace_character_with_empty(am_pm, ':')
  return hour, minute, am_pm

def cast_to_int(value: str) -> int:
  return int(value)

def replace_character_with_empty(value: str, character: str) -> str:
  return value.replace(character, '')

def regex_time_parser(text) -> int:
  hour_pattern = '^((2[0-3])|([0-1]?[0-9]))(:|am|pm|$)'
  minute_pattern = ':[0-5]?[0-9]'
  am_pm_pattern = 'am$|pm$'
  hour_search = re.search(hour_pattern, text)
  minute_search = re.search(minute_pattern, text)
  am_pm_search = re.search(am_pm_pattern, text)
  hour, minute, am_pm = get_value_from_search_groups(hour_search, minute_search, am_pm_search)
  print(text, hour, minute, am_pm)
  if hour == None:
    raise Exception('Invalid time.')
  if hour > 12 and (am_pm == 'pm' or am_pm == 'am'):
    raise Exception('Invalid time.')
  return (hour, minute, am_pm)

def is_valid_user_arguments(args: list) -> bool:
  if len(args) > 2:
    if args[2] == 'regex' or args[2] == 'parsimonious':
      return True
    return False
  else:
    return False

def parse_time_and_return_minutes_past_midnight(parser, time) -> int:
  if parser == 'regex':
    print('Using regex parser.')
    hour, minute, am_pm = regex_time_parser(time)
    return get_minutes_past_midnight(hour, minute, am_pm)
  elif parser == 'parsimonious':
    print('Using parsimonious parser.')
    return time_parser(time)

def main():
  if is_valid_user_arguments(sys.argv):
    time: str = sys.argv[1]
    parser: str = sys.argv[2]
    minutes_past_midnight = parse_time_and_return_minutes_past_midnight(parser, time)
    print(f'Time: {time} is {minutes_past_midnight} minutes past midnight.')
  else:
    print('Please provide a time and parser: <time> <parser>')

if __name__ == "__main__":
  main()