#!/usr/bin/python -O


from datetime import date
import DBUtils
import StockUtil

datestr = date.today().strftime('%Y-%m-%d')

db = DBUtils.get_db()
cursor = db.cursor()

codelist = [info[0] for info in DBUtils.get_codeinfo(db)]
funds = StockUtil.get_funds(codelist)
stock_data = StockUtil.get_brief_data(codelist)

for code in codelist:
    if code in funds:
        if __debug__:
            print "Processing" , code, "..."
        fund = funds[code]

        if fund["date"] != datestr:
            continue

        sqlstr = "insert into {0}({1}) values (?,?,?,?,?,?)".format(
                      "T" + code,
                      "date, fund_in, fund_out, fund_net, fund_per, price")
        cursor.execute(sqlstr, (datestr, fund["big_in"], fund["big_out"],
                                         fund["big_net"], fund["big_per"],
                                         stock_data[code]['price']))

    db.commit()
