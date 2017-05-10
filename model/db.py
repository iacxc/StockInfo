
# -*- coding: utf-8 -*-
from __future__ import print_function

from collections import namedtuple
import sqlite3

DBFILE = "stock_fund.db"

RowType = namedtuple("RowType", ["code", "date", "fund_in", "fund_out",
                                 "fund_net", "fund_per", "percent", "inc_p"])


def debug(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        if __debug__:
            print(result)
        return result

    return wrapper


class Field(object):
    def __init__(self, name_, type_, isnull_=True, default_=None,
                 isprimarykey_=False):
        self.name = name_
        self.type = type_
        self.isnull = isnull_
        self.default = default_
        self.isprimarykey = isprimarykey_

    @debug
    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(
            self.name,
            self.type,
            "" if self.isnull else "Not Null",
            "" if self.default is None else "Default {0}".format(self.default),
            "Primary Key" if self.isprimarykey else ""
        ).strip()


class Table(object):
    def __init__(self, name_, fields_=None, primarykey_=None):
        self.name = name_
        if fields_ is None:
            self.fields = []
        else:
            self.fields = fields_

        if primarykey_ is None:
            self.primary_key = None
        else:
            self.primary_key = "Primary Key({0})".format(primarykey_)

    def add_field(self, field):
        self.fields.append(field)

    @debug
    def drop(self, ifexists=True):
        return "DROP TABLE {0} {1}".format("IF EXISTS" if ifexists else "",
                                           self.name)

    @debug
    def create(self, ifnotexists=True):
        if self.primary_key is None:
            fields = ", ".join(map(str, self.fields))
        else:
            fields = ", ".join(map(str, self.fields) + [self.primary_key])

        return "CREATE TABLE {0} {1} ({2})".format("IF NOT EXISTS" if ifnotexists else "",
                                                    self.name, fields)

    @debug
    def insert(self, fields=None):
        if fields is None:
            fields = [f.name for f in self.fields]

        value_params = ["?"] * len(fields)
        return "INSERT INTO {0} ({1}) VALUES({2})".format(self.name,
                                                          ",".join(fields),
                                                          ",".join(value_params))
    @debug
    def update(self, fields, where):
        set_str = ",".join(["{0}=?".format(f) for f in fields])
        return "UPDATE {0} SET {1} WHERE {2}".format(self.name, set_str, where)

t_code = Table("code",
               [Field("code", "text", False, isprimarykey_=True),
                Field("name", "text", False)])

t_funds = Table("funds",
                [Field("code", "text", False),
                 Field("date", "text", False),
                 Field("fund_in", "real"),
                 Field("fund_out", "real"),
                 Field("fund_net", "real"),
                 Field("fund_per", "real"),
                 Field("value", "real", default_=1.0),
                 Field("inc_p", "real")],
                primarykey_="code, date")


class Repository(object):
    def __init__(self, db_file=DBFILE):
        self._db = sqlite3.connect(db_file)

    def init(self, clean_db=False):

        cursor = self._db.cursor()
        print("Creating table code")
        cursor.execute(t_code.drop())
        cursor.execute(t_code.create())
        code_infos = [
            ("000615", u"京汉股份"),
            ("000651", u"格力电器"),
            ("000856", u"冀东装备"),
            ("002158", u"汉钟精机"),
            ("002405", u"四维图新"),
            ("002457", u"青龙管业"),
            ("002631", u"德尔未来"),
            ("300024", u"机 器 人"),
            ("300033", u"同 花 顺"),
            ("300059", u"东方财富"),
            ("300131", u"英唐智控"),
            ("300157", u"恒泰艾普"),
            ("600388", u"龙净环保"),
            ("600692", u"亚通股份"),
            ("600977", u"中国电影"),
            ("603288", u"海天味业"),
            ("603616", u"韩建河山"),
            ("603885", u"吉祥航空"),
            ("603886", u"元祖股份"),
        ]
        cursor.executemany(t_code.insert(["code", "name"]), code_infos)

        if clean_db:
            print("Dropping table")
            cursor.execute(t_funds.drop())

        print("Creating table funds")
        cursor.execute(t_funds.create())

        self.commit()

    def commit(self):
        self._db.commit()

    def get_codes(self):
        cursor = self._db.cursor()
        cursor.execute("SELECT code,name FROM code")

        return cursor.fetchall()

    def add_stockdata(self, code, date_str, fund, stock_data):
        cursor = self._db.cursor()
        try:
            cursor.execute(t_funds.insert(),
                           (code,
                            date_str,
                            fund["big_in"],
                            fund["big_out"],
                            fund["big_net"],
                            fund["big_per"],
                            stock_data[code]["circu_value"],
                            stock_data[code]["percent"]))
        except sqlite3.IntegrityError:
            cursor.execute(
                t_funds.update(
                    ["fund_in", "fund_out", "fund_net", "fund_per", "value", "inc_p"],
                    "code='{0}' AND date='{1}'".format(code, date_str)),
                (fund["big_in"], fund["big_out"], fund["big_net"], fund["big_per"],
                 stock_data[code]["circu_value"], stock_data[code]["percent"])
            )

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

