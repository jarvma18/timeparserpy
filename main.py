from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(
  """
  time = (hour ":" minute am_pm) / (hour am_pm) / (hour  ":" minute) / hour
  hour = (digit_2 digit_0_4) / (digit_0_1 digit) / digit
  minute = digit_0_5 digit
  digit = ~"[0-9]"
  digit_0_1 = ~"[0-1]"
  digit_2 = "2"
  digit_0_4 = ~"[0-4]"
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
    print(node.text)
    print('visittime', visited_children)
    visited_children = visited_children[0]
    if type(visited_children) == int:
      self.hour = visited_children
      return
    if len(visited_children) > 0:
      self.hour = visited_children[0]
    if len(visited_children) > 2:
      self.minute = visited_children[2]
    if len(visited_children) > 3:
      self.am_pm = visited_children[3]

  def visit_hour(self, node, visited_children):
    print('visithour', visited_children)
    return int(node.text)

  def visit_minute(self, node, visited_children):
    print('visitmin', visited_children)
    return int(node.text)

  def visit_am_pm(self, node, visited_children):
    return node.text

  def visit_digit(self, node, visited_children):
    return node.text

  def visit_digit_0_to_3(self, node, visited_children):
    return node.text

  def generic_visit(self, node, visited_children):
    return visited_children or node

  def parse(self):
    tree = grammar.parse(self.text)
    print(tree)
    self.visit(tree)
    return self.hour, self.minute, self.am_pm

def time_parser(text):
  parser = TimeParser(text)
  minutesPastMidnight: int = None
  hour, minute, am_pm = parser.parse()
  print('hour', hour)
  print('minute', minute)
  print('am_pm', am_pm)
  if type(hour) == int:
    if type(am_pm) == str and am_pm == 'pm':
      minutesPastMidnight = (hour + 12) * 60
    else:
      minutesPastMidnight = hour * 60
  if type(minute) == int:
    minutesPastMidnight += minute
  return minutesPastMidnight

def main():
  time_parser('15')

if __name__ == "__main__":
  main()