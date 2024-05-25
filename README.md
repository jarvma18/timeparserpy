# timeparserpy
This is small project where is minimal implementation of time specification parsing.

## To do
* Design a BNF grammar to parse a time specification (4pm, 7:38pm, 23:42, 3:16, 3:16am) √
* Implement a parser for the BNF grammar using PEG parser generator (output should be an integer containing the number of minutes past midnight) √
* Implement the time parser using regular expressions

## How to run
```
# Run tests
python3 -m unittest test.py

# Run program
python3 main.py <time> <parser>

# Examples
python3 main.py 20:10 regex
python3 main.py 20 regex
python3 main.py 8pm regex
python3 main.py 20:10 parser
python3 main.py 20 parser
python3 main.py 8pm parser
```
