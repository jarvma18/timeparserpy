import sys

from peg_time_parser import time_parser
from regex_time_parser import regex_time_parser

def get_minutes_past_midnight(hour: int, minute: int, am_pm: str) -> int:
  result: int = None
  if type(hour) == int:
    result = hour * 60
    if am_pm == 'pm':
      result += 12 * 60
    if type(minute) == int:
      result += minute
  return result

def is_valid_user_arguments(args: list) -> bool:
  result = True
  if len(args) > 3:
    if args[2] != 'regex' and args[2] != 'parsimonious':
      result = False
      return result
    if args[3] != 'time' and args[3] != 'minutes_past_midnight':
      result = False
  else:
    result = False
  return result

def get_time_or_minutes_past_midnight(time_or_minutes_past_midnight: str, hour: int, minute: int, am_pm: str):
  if time_or_minutes_past_midnight == 'time':
    print('Returning time.')
    return hour, minute, am_pm
  elif time_or_minutes_past_midnight == 'minutes_past_midnight':
    print('Returning minutes past midnight.')
    return get_minutes_past_midnight(hour, minute, am_pm)

def parse_time_and_return_minutes_past_midnight(parser, time, time_or_minutes_past_midnight) -> int:
  if parser == 'regex':
    print('Using regex parser.')
    hour, minute, am_pm = regex_time_parser(time)
    return get_time_or_minutes_past_midnight(time_or_minutes_past_midnight, hour, minute, am_pm)
  elif parser == 'parsimonious':
    print('Using parsimonious parser.')
    hour, minute, am_pm = time_parser(time)
    return get_time_or_minutes_past_midnight(time_or_minutes_past_midnight, hour, minute, am_pm)

def main():
  if is_valid_user_arguments(sys.argv):
    time: str = sys.argv[1]
    parser: str = sys.argv[2]
    time_or_minutes_past_midnight: str = sys.argv[3]
    result = parse_time_and_return_minutes_past_midnight(parser, time, time_or_minutes_past_midnight)
    print(result)
  else:
    print('Please provide a time and parser: <time> <parser>')

if __name__ == "__main__":
  main()