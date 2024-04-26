from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

class TimeParser(NodeVisitor):
  def visit_time_specification(self, node, visited_children):
    if len(visited_children) == 1:
      return visited_children[0]
    elif len(visited_children) == 2:
      return visited_children[0] + visited_children[1]
    elif len(visited_children) == 3:
      return visited_children[0] * 60 + visited_children[2]
    else:
      return visited_children[0] * 60 + visited_children[2]

  def visit_hour(self, node, visited_children):
    if len(visited_children) == 1:
      return visited_children[0]
    elif len(visited_children) == 2:
      return visited_children[0] * 10 + visited_children[1]
    else:
      return visited_children[0] * 100 + visited_children[1] * 10 + visited_children[2]

  def visit_minute(self, node, visited_children):
    if len(visited_children) == 1:
      return visited_children[0]
    else:
      return visited_children[0] * 10 + visited_children[1]

  def visit_am_pm(self, node, visited_children):
    return 0 if visited_children[0] == "am" else 12

  def visit_digit(self, node, visited_children):
    return int(node.text)

  def visit_digit_0_to_1(self, node, visited_children):
    return int(node.text)

  def visit_digit_0_to_3(self, node, visited_children):
    return int(node.text)

  def visit_digit_0_to_5(self, node, visited_children):
    return int(node.text)

def time_parser(time_specification):
  grammar = Grammar(r"""
    time_specification = hour / (hour am_pm) / (hour ":" minute) / (hour ":" minute am_pm)
    hour = (digit_0_to_1 digit digit) / ("2" digit_0_to_3) / digit
    minute = (digit_0_to_5 digit) / digit
    am_pm = "am" / "pm"
    digit = "0" / "1" / "2" / "3" / "4" / "5" / "6" / "7" / "8" / "9"
    digit_0_to_1 = "0" / "1"
    digit_0_to_3 = "0" / "1" / "2" / "3"
    digit_0_to_5 = "0" / "1" / "2" / "3" / "4" / "5"
  """)
  tree = grammar.parse(time_specification)
  visited_children = TimeParser().visit(tree)
  minutes_past_midnight = visited_children[0] * 60 + visited_children[1]
  return minutes_past_midnight