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
    market_share integer Not Null,
    name text not null)""")
code_infos = [
("000728",  196400, u"国元证券"),
("002055",   40300, u"德润电子"),
("002405",   66000, u"四维图新"),
("002415",  315500, u"海康威视"),
("002615",   10300, u"哈 尔 斯"),
("002666",   22700, u"德联集团"),
("300007",   18200, u"汉威电子"),
("300024",   63400, u"机 器 人"),
("300033",   26200, u"同 花 顺"),
("300059",  129100, u"东方财富"),
("300104",  109200, u"乐 视 网"),
("300149",   35600, u"量子高科"),
("300214",   29300, u"日科化学"),
("300273",   51300, u"和佳股份"),
("600388",  106900, u"龙净环保"),
("600572",  119200, u"康 恩 贝"),
("600830",   45400, u"香溢融通"),
("600837",  809200, u"海通证券"),
("600895",  154900, u"张江高科"),
("601166", 1618000, u"兴业银行"),
("601318", 1083300, u"中国平安")]
cursor.executemany("insert into code values (?,?,?)", code_infos)

for code in (info[0] for info in code_infos):
    tablename = "T{0}".format(code)
    sqlstr = """CREATE TABLE IF NOT EXISTS {0} (
    date text not null primary key,
    fund_in real,
    fund_out real,
    fund_net real,
    fund_per real,
    price real default 1.0)""".format(tablename)

    if cleandb:
        print "Droping table", tablename
        cursor.execute("DROP TABLE IF EXISTS {0}".format(tablename))

    print "Creating table", tablename
    cursor.execute(sqlstr)

db.commit()

print "Initialization completed"
