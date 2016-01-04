
# -*- coding: utf-8 -*-

import sqlite3


DBFILE = "stock_fund.db"


def get_db(dbfile=DBFILE):
    return sqlite3.connect(dbfile)


def get_codes(db):
    cursor = db.cursor()
    cursor.execute("SELECT code FROM code")

    return (row[0] for row in cursor.fetchall())



