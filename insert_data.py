#!/usr/bin/python -O

import sys
import DBUtils
from datetime import date

if len(sys.argv) < 2:
    sys.exit(1)

fname = sys.argv[1]
_, datestr = fname.split('.')

db = DBUtils.get_db()
cursor = db.cursor()

with file(fname) as f:
    stock_data = [line.split() for line in f]
    codelist = ['sh' + data[0] if data[0].startswith('6')
                               else 'sz' + data[0]
                    for data in stock_data]
    stock_info = DBUtils.get_stockinfo(codelist)
    for data in stock_data:
        sqlstr = "insert into {0} values (?,?,?,?,?,?)".format("T" + data[0])
        price = stock_info[data[0]]['curr']
        cursor.execute(sqlstr, (datestr, data[1], data[2],
                                data[3], data[4], price))

    db.commit()


