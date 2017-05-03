
# -*- coding: utf-8 -*-
<<<<<<< HEAD
from __future__ import print_function
=======
>>>>>>> cecb4acef63c2f52f2f72167d8130349fca0467d

from collections import namedtuple
import sqlite3

DBFILE = "stock_fund.db"

RowType = namedtuple("RowType", ["code", "date", "fund_in", "fund_out",
                                 "fund_net", "fund_per", "percent", "inc_p"])

class Repository(object):
    def __init__(self, db_file=DBFILE):
        self._db = sqlite3.connect(db_file)

    def init(self, cleandb=False):
        cursor = self._db.cursor()
        cursor.execute("DROP TABLE IF EXISTS code")
        cursor.execute("""CREATE TABLE code (
code text Not Null Primary Key,
name text not null)""")
        code_infos = [
            ("000615", u"京汉股份"),
            ("000856", u"冀东装备"),
            ("002405", u"四维图新"),
<<<<<<< HEAD
            ("002457", u"青龙管业"),
=======
            ("002457", u"青龙管业：w"),
>>>>>>> cecb4acef63c2f52f2f72167d8130349fca0467d
            ("002631", u"德尔未来"),
            ("300024", u"机 器 人"),
            ("300033", u"同 花 顺"),
            ("300059", u"东方财富"),
            ("300131", u"英唐智控"),
            ("600388", u"龙净环保"),
            ("600692", u"亚通股份"),
            ("600977", u"中国电影"),
            ("603885", u"吉祥航空"),
        ]
        cursor.executemany("insert into code values (?,?)", code_infos)

        sqlstr = """CREATE TABLE IF NOT EXISTS funds (
    code text not null,
    date text not null,
    fund_in real,
    fund_out real,
    fund_net real,
    fund_per real,
    value real default 1.0,
    inc_p real,
    primary key (code, date))"""

        if cleandb:
<<<<<<< HEAD
            print("Dropping table")
            cursor.execute("DROP TABLE IF EXISTS funds")

        print("Creating table")
=======
            print "Dropping table"
            cursor.execute("DROP TABLE IF EXISTS funds")

        print "Creating table"
>>>>>>> cecb4acef63c2f52f2f72167d8130349fca0467d
        cursor.execute(sqlstr)

        self._db.commit()

    def get_codes(self):
        cursor = self._db.cursor()
<<<<<<< HEAD
        cursor.execute("SELECT code,name FROM code")

        return [(row[0], row[1]) for row in cursor.fetchall()]
=======
        cursor.execute("SELECT code FROM code")

        return (row[0] for row in cursor.fetchall())
>>>>>>> cecb4acef63c2f52f2f72167d8130349fca0467d

    def add_stockdata(self, code, date_str, fund, stock_data):
        cursor = self._db.cursor()
        sql_str = "insert into funds({0}) values (?,?,?,?,?,?,?,?)".format(
                  "code, date, fund_in, fund_out, fund_net, fund_per, value, inc_p")
<<<<<<< HEAD
        if __debug__:
            print(sql_str)
=======
>>>>>>> cecb4acef63c2f52f2f72167d8130349fca0467d
        cursor.execute(sql_str, (code, date_str, fund["big_in"], fund["big_out"],
                                 fund["big_net"], fund["big_per"],
                                 stock_data[code]['circu_value'],
                                 stock_data[code]['percent']))
<<<<<<< HEAD
        self._db.commit()
=======
>>>>>>> cecb4acef63c2f52f2f72167d8130349fca0467d

    def get_stockdata(self, code, limit):
        query_str = """SELECT * FROM
    (SELECT code, date, fund_in, fund_out, fund_net, fund_per,
            fund_net / value as percent, inc_p
     FROM funds
     WHERE code = ?
     ORDER BY date DESC LIMIT {1})
ORDER BY date""".format(",".join(RowType._fields), limit)
        cursor = self._db.cursor()
        cursor.execute(query_str, (code,))

        return [RowType(*row) for row in cursor.fetchall()]

