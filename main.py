from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

class TimeParser(NodeVisitor):
  def visit_time_specification(self, node, visited_children):
    print(node, visited_children)
    if len(visited_children) == 0:
      return None
    if len(visited_children) == 1:
      return visited_children[0]
    if len(visited_children) == 2:
      return visited_children[0] * 60 + visited_children[1]
    return visited_children

  def visit_hour(self, node, visited_children):
    print(node, visited_children)
    return int(node.text)

  def visit_minute(self, node, visited_children):
    print(node, visited_children)
    return int(node.text)

  def visit_am_pm(self, node, visited_children):
    print(node, visited_children)
    return node.text

  def generic_visit(self, node, visited_children):
    print(node, visited_children)
    return None

def time_parser(time_specification):
  grammar = Grammar(r"""
    time_specification = hour / (hour ":" minute) / (hour ":" minute am_pm)
    hour = (digit_0_to_1 digit) / ("2" digit_0_to_3) / digit
    minute = (digit_0_to_5 digit) / digit
    am_pm = "am" / "pm"
    digit = "0" / "1" / "2" / "3" / "4" / "5" / "6" / "7" / "8" / "9"
    digit_0_to_1 = "0" / "1"
    digit_0_to_3 = "0" / "1" / "2" / "3"
    digit_0_to_5 = "0" / "1" / "2" / "3" / "4" / "5"
  """)
  tree = grammar.parse(time_specification)
  visited_children = TimeParser().visit(tree)
  print(visited_children)
  minutes_past_midnight = visited_children * 60
  return minutes_past_midnight