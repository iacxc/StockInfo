#!/usr/bin/python -O
# -*- coding: utf-8 -*-

import DBUtils
import sys

if len(sys.argv) > 1 and sys.argv[1] == "clean":
    cleandb = True
else:
    cleandb = False


db = DBUtils.get_db()

cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS code")
cursor.execute("""CREATE TABLE code (
    code text Not Null Primary Key,
    name text not null)""")
code_infos = [
("002405",  u"四维图新"),
("002631",  u"德尔未来"),
("300024",  u"机 器 人"),
("300033",  u"同 花 顺"),
("300059",  u"东方财富"),
("300131",  u"英唐智控"),
("600388",  u"龙净环保"),
("600692",  u"亚通股份"),
("600977",  u"中国电影"),
("603885",  u"吉祥航空"),
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
    print "Droping table"
    cursor.execute("DROP TABLE IF EXISTS funds")

print "Creating table"
cursor.execute(sqlstr)

db.commit()

print "Initialization completed"
