# -*- coding:utf8 -*-
"""
   db repository using SQLAlchemy core module
"""

from __future__ import print_function

from collections import namedtuple

from sqlalchemy import create_engine, MetaData, Table, Column, \
                       Float, String, UnicodeText
import sqlalchemy.exc
from sqlalchemy.sql import text


DBPATH = "stock_fund.db"
RowType = namedtuple("RowType", ["code", "date", "fund_in", "fund_out",
                                 "fund_net", "fund_per", "percent", "inc_p"])


class Repository(object):
    """ the repository """
    def __init__(self, db_path=DBPATH):
        self.engine = create_engine("sqlite:///{0}".format(db_path),
                                    convert_unicode=True,
                                    echo=True)
        self.engine.raw_connection().connection.text_factory = str

        self.meta = MetaData(self.engine)

        self.t_code = Table("code", self.meta,
                            Column("code", String, nullable=False,primary_key=True),
                            Column("name", UnicodeText, nullable=False))

        self.t_funds = Table("funds", self.meta,
                             Column("code", String, nullable=False, primary_key=True),
                             Column("date", String, nullable=False, primary_key=True),
                             Column("fund_in", Float),
                             Column("fund_out", Float),
                             Column("fund_net", Float),
                             Column("fund_per", Float),
                             Column("value", Float, default=1.0),
                             Column("inc_p", Float))

    def init(self, clean_db=False):
        """ init """
        print("Creating table code")
        self.t_code.drop(checkfirst=True)
        self.t_code.create()

        conn = self.engine.connect()

        code_infos = []
        with file("static/codeinfo.txt") as f:
            for line in f:
                code, name = line.strip().split(",")
                code_infos.append({"code": code, "name": unicode(name, "utf-8")})

        conn.execute(self.t_code.insert(), code_infos)

        print("Creating table funds")
        self.t_funds.create(checkfirst=True)

    def get_codes(self):
        """ get code """
        return self.t_code.select().execute().fetchall()

    def add_stockdata(self, code, date_str, fund, stock_data):
        """ add stockdata """
        try:
            insert_ = self.t_funds.insert()
            insert_.execute({"code": code,
                             "date": date_str,
                             "fund_in": fund["big_in"],
                             "fund_out": fund["big_out"],
                             "fund_net": fund["big_net"],
                             "fund_per": fund["big_per"],
                             "value": stock_data[code]["circu_value"],
                             "inc_p": stock_data[code]["percent"]})
        except sqlalchemy.exc.IntegrityError:
            update_ = self.t_funds.update().\
                          where(self.t_funds.c.code == code, self.t_funds.c.date == date_str).\
                          values(
                {"fund_in": fund["big_in"],
                 "fund_out": fund["big_out"],
                 "fund_net": fund["big_net"],
                 "fund_per": fund["big_per"],
                 "value": stock_data[code]["circu_value"],
                 "inc_p": stock_data[code]["percent"]})
            update_.execute()

    def get_stockdata(self, code, limit):
        """ get stockdata """
        query_str = text("""SELECT * FROM
    (SELECT code, date, fund_in, fund_out, fund_net, fund_per,
            fund_net / value as percent, inc_p
     FROM funds
     WHERE code = :code
     ORDER BY date DESC LIMIT {0})
ORDER BY date""".format(limit))
        conn = self.engine.connect()

        return [RowType(*row) for row in conn.execute(query_str, code=code).fetchall()]
