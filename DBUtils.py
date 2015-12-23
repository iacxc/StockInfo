
# -*- coding: utf-8 -*-

import sqlite3


DBFILE = "stock_fund.db"


def get_db():
    return sqlite3.connect(DBFILE)


def get_codeinfo(db):
    cursor = db.cursor()
    cursor.execute("SELECT code, market_share FROM code")

    return cursor.fetchall()



