from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = r"""
time_specification = hour ":" minute am_pm
hour = digit_0_to_1 digit / digit
minute = digit_0_to_5 digit / digit
am_pm = "am" / "pm"
digit = "0" / "1" / "2" / "3" / "4" / "5" / "6" / "7" / "8" / "9"
digit_0_to_1 = "0" / "1"
digit_0_to_5 = "0" / "1" / "2" / "3" / "4" / "5"
"""

class TimeParser(NodeVisitor):
  def __init__(self, text):
    self.text = text
    self.hour = None
    self.minute = None
    self.am_pm = None

  def visit_time_specification(self, node, visited_children):
    self.hour = visited_children[0]
    self.minute = visited_children[2]
    self.am_pm = visited_children[3]

  def visit_hour(self, node, visited_children):
    return int(node.text)

  def visit_minute(self, node, visited_children):
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
    grammarOfGrammar = Grammar(grammar)
    tree = grammarOfGrammar.parse(self.text)
    self.visit(tree)
    return self.hour, self.minute, self.am_pm

def time_parser(text):
  parser = TimeParser(text)
  hour, minute, am_pm = parser.parse()
  if am_pm == 'pm':
    hour += 12
  return hour * 60 + minute