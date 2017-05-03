#!/usr/bin/python -O

<<<<<<< HEAD
from __future__ import print_function

=======
>>>>>>> cecb4acef63c2f52f2f72167d8130349fca0467d
from datetime import date
import sys

from model import Repository
from model import stock

if len(sys.argv) == 1:
    date_str = date.today().strftime('%Y-%m-%d')
else:
    date_str = sys.argv[1]

repository = Repository()

<<<<<<< HEAD
code_list = repository.get_codes()
=======
code_list = list(repository.get_codes())
>>>>>>> cecb4acef63c2f52f2f72167d8130349fca0467d
funds = stock.get_funds(code_list)
stock_data = stock.get_data(code_list)

for code in code_list:
    if code in funds:
        if __debug__:
            print("Processing", code, "...")
        fund = funds[code]

        if fund["date"] != date_str:
            continue

        repository.add_stockdata(code, date_str, fund, stock_data)

