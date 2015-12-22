#!/usr/bin/python -O


import sqlite3
import DBUtils

#init
#create table code (code text not null primary key);
#

conn = sqlite3.connect(DBUtils.DBFILE)

codes = DBUtils.get_codes(conn)
cursor = conn.cursor()
for code in codes:
    tablename = "T{0}".format(code)
    sqlstr = """CREATE TABLE IF NOT EXISTS {0} (
    date integer not null,
    fund real,
    source text default 'dzh',
    primary key (date, source))""".format(tablename)

    print "Creating table", tablename
    cursor.execute(sqlstr)

print "Initialization completed"
