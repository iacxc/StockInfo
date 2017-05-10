
from __future__ import print_function

import requests
import re
from collections import namedtuple


def get_history(code, fromdate=None, todate=None):
    """ get history data from yahoo"""
    url = "http://table.finance.yahoo.com/table.csv?s={0}.{1}".format(
        code, "ss" if code.startswith("60") else "sz")

    if fromdate is not None:
        url += "&a={0}&b={1}&c={2}".format(fromdate.month-1,
                                           fromdate.day, fromdate.year)
    if todate is not None:
        url += "&d={0}&e={1}&f={2}".format(todate.month-1,
                                           todate.day, todate.year)

    if __debug__:
        print(url)
    resp = requests.get(url)
    RecordType = namedtuple("RecordType", ["date", "open", "high", "low",
                                           "close", "volume", "adj_close"])

    datas = []
    if resp.status_code == 200:
        for line in resp.text.split("\n")[1:]:
            if line.strip() == "": continue

            datas.append(RecordType(*line.split(",")))

    return reversed(datas)


def get_funds(codelist):
    """ get the funds in/out of a list of stocks """
    prefix = lambda x: "ff_" + ("sh" if x.startswith("60") else "sz") + x
    url = "http://qt.gtimg.cn/q=" + ",".join(map(prefix, codelist))

    if __debug__:
        print(url)
    resp = requests.get(url)

    funds = {}
    for code, line in zip(codelist, resp.text.split("\n")):
        if len(line.strip()) == 0: continue

        m = re.search(r"(.+)=\"(.+)\"", line)
        items = m.group(2).split("~")

        fund = {"big_in"    : float(items[1]),
                "big_out"   : float(items[2]),
                "big_net"   : float(items[3]),
                "big_per"   : float(items[4]),
                "small_in"  : float(items[5]),
                "small_out" : float(items[6]),
                "small_net" : float(items[7]),
                "small_per" : float(items[8]),
                "date"      : "{0}-{1}-{2}".format(items[13][0:4],
                                                   items[13][4:6],
                                                   items[13][6:8]),
                }
        funds[items[0][2:]] = fund

    return funds


def get_brief_data(codelist):
    prefix = lambda x: "s_" + ("sh" if x.startswith("60") else "sz") + x
    url = "http://qt.gtimg.cn/q=" + ",".join(map(prefix, codelist))

    if __debug__:
        print(url)
    resp = requests.get(url)

    datas = {}
    for code, line in zip(codelist, resp.text.split("\n")):
        if len(line.strip()) == 0: continue

        m = re.search(r"(.+)=\"(.+)\"", line)
        items = m.group(2).split("~")
        data = {"price"   : float(items[3]),
                "delta"   : float(items[4]),
                "percent" : float(items[5]),
                "amount"  : float(items[6]),
                "volume"  : float(items[7]),
                }
        datas[code] = data

    return datas


def get_data(codelist):
    """ get the detail data of a list of stocks"""
    prefix = lambda x: ("sh" if x.startswith("60") else "sz") + x
    url = "http://qt.gtimg.cn/q=" + ",".join(map(prefix, codelist))

    if __debug__:
        print(url)
    resp = requests.get(url)

    datas = {}
    for code, line in zip(codelist, resp.text.split("\n")):
        if len(line.strip()) == 0: continue

        m = re.search(r"(.+)=\"(.+)\"", line)
        items = m.group(2).split("~")
        data = { "price"   : float(items[3]),
                 "last"    : float(items[4]),
                 "open"    : float(items[5]),
                 "buy"     : float(items[9]),
                 "buy2"    : float(items[11]),
                 "buy3"    : float(items[13]),
                 "sell"    : float(items[19]),
                 "sell2"   : float(items[21]),
                 "sell3"   : float(items[23]),
                 "delta"   : float(items[31]),
                 "percent" : float(items[32]),
                 "high"    : float(items[33]),
                 "low"     : float(items[34]),
                 "volume"  : float(items[36]),
                 "amount"  : float(items[37]),
                 "circu_value" : float(items[44]) * 1e4,
                 "value"   : float(items[45]) * 1e4 }
        datas[code] = data

    return datas


def get_url(code):
    prefix = lambda x: ("sh" if x.startswith("60") else "sz") + x

    return "http://finance.sina.com.cn/realstock/company/{0}/nc.shtml".format(
        prefix(code)
    )
