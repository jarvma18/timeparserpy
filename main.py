import sys

from peg_time_parser import time_parser
from regex_time_parser import regex_time_parser

def get_minutes_past_midnight(hour: int, minute: int, am_pm: str) -> int:
  minutes_past_midnight: int = None
  if type(hour) == int:
    minutes_past_midnight = hour * 60
    if am_pm == 'pm':
      minutes_past_midnight += 12 * 60
    if type(minute) == int:
      minutes_past_midnight += minute
  return minutes_past_midnight

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
    hour, minute, am_pm = time_parser(time)
    return get_minutes_past_midnight(hour, minute, am_pm)

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