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
("000728",  u"国元证券"),
("002055",  u"德润电子"),
("002405",  u"四维图新"),
("002415",  u"海康威视"),
("002615",  u"哈 尔 斯"),
("002666",  u"德联集团"),
("300007",  u"汉威电子"),
("300024",  u"机 器 人"),
("300033",  u"同 花 顺"),
("300059",  u"东方财富"),
("300100",  u"双林股份"),
("300104",  u"乐 视 网"),
("300149",  u"量子高科"),
("300214",  u"日科化学"),
("300273",  u"和佳股份"),
("300251",  u"光线传媒"),
("600388",  u"龙净环保"),
("600572",  u"康 恩 贝"),
("600830",  u"香溢融通"),
("600837",  u"海通证券"),
("600895",  u"张江高科"),
("601166",  u"兴业银行"),
("601318",  u"中国平安")]
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
