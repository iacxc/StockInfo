# -*- coding:utf8 -*-
"""
   db repository using SQLAlchemy ORM
"""

from __future__ import print_function

from sqlalchemy import create_engine, Column, Float, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.exc


DBPATH = "stock_fund.db"


def utf8(astr):
    """ convert to utf8 """
    return unicode(astr, "utf-8")

Base = declarative_base()

class Code(Base):
    """ class Code """
    __tablename__ = "code"

    code = Column(String, nullable=False, primary_key=True)
    name = Column(UnicodeText, nullable=False)

    def __repr__(self):
        return u"<{0}: {1}>".format(self.code, self.name)


class Funds(Base):
    """ class Funds """
    __tablename__ = "funds"

    code = Column("code", String, nullable=False, primary_key=True)
    date = Column("date", String, nullable=False, primary_key=True)
    fund_in = Column("fund_in", Float)
    fund_out = Column("fund_out", Float)
    fund_net = Column("fund_net", Float)
    fund_per = Column("fund_per", Float)
    value = Column("value", Float, default=1.0)
    inc_p = Column("inc_p", Float)
    exchange = Column("exchange", Float)

    @property
    def percent(self):
        """ percent """
        return self.fund_net / self.value

    def __repr__(self):
        return "<{0}: {1}>".format(self.code, self.date)


class Repository(object):
    """ the repository """
    def __init__(self, db_path=DBPATH):
        self.engine = create_engine("sqlite:///{0}".format(db_path),
                                    convert_unicode=True,
                                    echo=True)
        self.session = sessionmaker(bind=self.engine)()

    def init(self, clean_db=False):
        """ init """
        Code.__table__.drop(bind=self.engine, checkfirst=True)
        if clean_db:
            Funds.__table__.drop(bind=self.engine, checkfirst=True)

        print("Creating tables")
        Base.metadata.create_all(bind=self.engine)

        with file("static/codeinfo.txt") as f:
            for line in f:
                code, name = line.strip().split(",")
                self.session.add(Code(code=code, name=utf8(name)))

        self.session.commit()

    def get_codes(self):
        """ get_codes """
        return self.session.query(Code.code, Code.name).all()

    def add_stockdata(self, code, date_str, fund, stock_data):
        """ get_codes """
        try:
            self.session.query(Funds).filter_by(code=code, date=date_str).one()
            self.session.query(Funds)\
                .filter(Funds.code == code, Funds.date == date_str)\
                .update({"fund_in": fund["big_in"],
                         "fund_out": fund["big_out"],
                         "fund_net": fund["big_net"],
                         "fund_per": fund["big_per"],
                         "value": stock_data[code]["circu_value"],
                         "inc_p": stock_data[code]["percent"],
                         "exchange": stock_data[code]["exchange"]})
        except sqlalchemy.orm.exc.NoResultFound:
            self.session.add(Funds(code=code,
                                   date=date_str,
                                   fund_in=fund["big_in"],
                                   fund_out=fund["big_out"],
                                   fund_net=fund["big_net"],
                                   fund_per=fund["big_per"],
                                   value=stock_data[code]["circu_value"],
                                   inc_p=stock_data[code]["percent"],
                                   exchange=stock_data[code]["exchange"]))
 
        self.session.commit()

    def get_stockdata(self, code, limit):
        """ get_codes """
        return (self.session.query(Funds)
                .filter_by(code=code)
                .order_by(Funds.date.desc())
                .limit(limit)
                .from_self()
                .order_by(Funds.date)
                .all())
