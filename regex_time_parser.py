import re

def cast_to_int(value: str) -> int:
  return int(value)

def replace_character_with_empty(value: str, character: str) -> str:
  return value.replace(character, '')

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

def regex_time_parser(text) -> int:
  hour_pattern = '^((2[0-3])|([0-1]?[0-9]))(:|am|pm|$)'
  minute_pattern = ':[0-5]?[0-9]'
  am_pm_pattern = 'am$|pm$'
  hour_search = re.search(hour_pattern, text)
  minute_search = re.search(minute_pattern, text)
  am_pm_search = re.search(am_pm_pattern, text)
  hour, minute, am_pm = get_value_from_search_groups(hour_search, minute_search, am_pm_search)
  if hour == None:
    raise Exception('Invalid time.')
  if hour > 12 and (am_pm == 'pm' or am_pm == 'am'):
    raise Exception('Invalid time.')
  return (hour, minute, am_pm)