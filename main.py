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

def time_parser(time: str):
  print(grammar.parse(time))
  return

def main():
  time_parser('15')

if __name__ == "__main__":
  main()