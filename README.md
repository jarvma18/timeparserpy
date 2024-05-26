# timeparserpy
This is small project where is minimal implementation of time specification parsing.

## To do
* Design a BNF grammar to parse a time specification (4pm, 7:38pm, 23:42, 3:16, 3:16am) √
* Implement a parser for the BNF grammar using PEG parser generator (output should be an integer containing the number of minutes past midnight) √
* Implement the time parser using regular expressions √

## How to run
```
# Run tests
python3 -m unittest test.py

# Run program
python3 main.py <time> <parser> <time_or_minutes_past_midnight>

# Examples

# Hour, minutes, am or pm
python3 main.py 20:10 regex time
python3 main.py 20 regex time
python3 main.py 8pm regex time
python3 main.py 8:10pm regex time
python3 main.py 20:10 parsimonious time
python3 main.py 20 parsimonious time
python3 main.py 8pm parsimonious time
python3 main.py 8:10pm parsimonious time

# Minutes past midnight
python3 main.py 20:10 regex minutes_past_midnight
python3 main.py 20 regex minutes_past_midnight
python3 main.py 8pm regex minutes_past_midnight
python3 main.py 8:10pm regex minutes_past_midnight
python3 main.py 20:10 parsimonious minutes_past_midnight
python3 main.py 20 parsimonious minutes_past_midnight
python3 main.py 8pm parsimonious minutes_past_midnight
python3 main.py 8:10pm parsimonious minutes_past_midnight
```
