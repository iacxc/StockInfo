#!/usr/bin/python -O


from datetime import date
import DBUtils
import StockUtil

datestr = date.today().strftime('%Y-%m-%d')

db = DBUtils.get_db()
cursor = db.cursor()

codelist = list(DBUtils.get_codes(db))
funds = StockUtil.get_funds(codelist)
stock_data = StockUtil.get_data(codelist)

for code in codelist:
    if code in funds:
        if __debug__:
            print "Processing" , code, "..."
        fund = funds[code]

        if fund["date"] != datestr:
            continue

        sqlstr = "insert into funds({0}) values (?,?,?,?,?,?,?)".format(
                      "code, date, fund_in, fund_out, fund_net, fund_per, value")
        cursor.execute(sqlstr, (code, datestr, fund["big_in"], fund["big_out"],
                                         fund["big_net"], fund["big_per"],
                                         stock_data[code]['circu_value']))

    db.commit()
