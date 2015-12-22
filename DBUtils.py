
# -*- coding: utf-8 -*-

import sqlite3


DBFILE = "stock_fund.db"


def get_db():
    return sqlite3.connect(DBFILE)


def get_codeinfo(db):
    cursor = db.cursor()
    cursor.execute("SELECT code, market_share FROM code")

    return cursor.fetchall()


def get_stockinfo(codelist):
    import requests
    url = "http://hq.sinajs.cn/list=%s" % ",".join(codelist)

    if __debug__: print url
    resp = requests.get(url)

    import re
    infos = {}
    for code, line in zip(codelist, resp.text.split("\n")):
        if len(line.strip()) == 0:
            continue

        m = re.search(r"(.+)=\"(.+)\"", line)
        items = m.group(2).split(",")
        info = {
             "curr"   : float(items[3]),
             "last"   : float(items[2]),
             "open"   : float(items[1]),
             "delta"  : float(items[3]) - float(items[2]),
             "low"    : float(items[5]),
             "high"   : float(items[4]),
             "buy"    : float(items[6]),
             "sell"   : float(items[7]),
             "volumn" : int(float(items[8]) / 100),
             "amount" : int(float(items[9]) / 10000) }

        infos[code[2:]] = info

    return infos

