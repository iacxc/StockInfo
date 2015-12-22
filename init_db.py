#!/usr/bin/python -O


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
    market_share integer Not Null)""")
code_infos = [
("000728",  196400),
("002055",   40300),
("002405",   66000),
("002415",  315500),
("300007",   18200),
("300024",   63400),
("300033",   26200),
("300059",  129100),
("300104",  109200),
("300214",   29300),
("300273",   51300),
("600388",  106900),
("600572",  119200),
("600830",   45400),
("600837",  809200),
("600895",  154900),
("601166", 1618000),
("601318", 1083300)]
cursor.executemany("insert into code values (?,?)", code_infos)

for code in (info[0] for info in code_infos):
    tablename = "T{0}".format(code)
    sqlstr = """CREATE TABLE IF NOT EXISTS {0} (
    date text not null primary key,
    fund_in real,
    fund_out real,
    fund_in2 real,
    fund_out2 real,
    price real default 1.0)""".format(tablename)

    if cleandb:
        print "Droping table", tablename
        cursor.execute("DROP TABLE IF EXISTS {0}".format(tablename))

    print "Creating table", tablename
    cursor.execute(sqlstr)

db.commit()

print "Initialization completed"
