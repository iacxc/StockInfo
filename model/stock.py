
from collections import namedtuple
import re
import requests


def get_history(code, startdate=None, enddate=None):
    """ get history data """
    url = "http://q.stock.sohu.com/hisHq.csv?code=cn_{0}".format(code)

    if enddate is None:
        import time
        enddate = time.strftime('%Y%m%d', time.localtime())

    if startdate is not None:
        url += "&start=" + startdate

    url += "&end=" + enddate

    if __debug__:
        print(url)

    resp = requests.get(url)
    RecordType = namedtuple("RecordType", ["date", "open", "close", 
                                           "inc", "inc_p", "low", "high", 
                                           "volume", "value", "exchange"])

    if resp.status_code == 200:
        result = resp.json()[0]
        if result["status"] == 0:
            return reversed([RecordType(*item) for item in result["hq"]])

    return []


def get_funds(codelist):
    """ get the funds in/out of a list of stocks, 资金流向 """
    prefix = lambda x: "ff_" + ("sh" if x.startswith("60") else "sz") + x
    url = "http://qt.gtimg.cn/q=" + ",".join(map(prefix, codelist))

    if __debug__:
        print(url)
    resp = requests.get(url)

    funds = {}
    for line in resp.text.split("\n"):
        if line.strip() == "":
            continue

        match = re.search(r"(.+)=\"(.+)\"", line)
        items = match.group(2).split("~")

        fund = {"big_in"   : float(items[1]),
                "big_out"  : float(items[2]),
                "big_net"  : float(items[3]),
                "big_per"  : float(items[4]),
                "small_in" : float(items[5]),
                "small_out": float(items[6]),
                "small_net": float(items[7]),
                "small_per": float(items[8]),
                "date"     : "{0}-{1}-{2}".format(items[13][0:4],
                                                  items[13][4:6],
                                                  items[13][6:8]),
               }
        funds[items[0][2:]] = fund

    return funds


def get_brief_data(codelist):
    """ get brief data"""
    prefix = lambda x: "s_" + ("sh" if x.startswith("60") else "sz") + x
    url = "http://qt.gtimg.cn/q=" + ",".join(map(prefix, codelist))

    if __debug__:
        print(url)
    resp = requests.get(url)

    datas = {}
    for code, line in zip(codelist, resp.text.split("\n")):
        if line.strip() == "":
            continue

        match = re.search(r"(.+)=\"(.+)\"", line)
        items = match.group(2).split("~")
        data = {"price"  : float(items[3]),
                "delta"  : float(items[4]),
                "percent": float(items[5]),
                "amount" : float(items[6]),
                "volume" : float(items[7]),
               }
        datas[code] = data

    return datas


def get_data(codelist):
    """ get the detail data of a list of stocks, 实时数据"""
    prefix = lambda x: ("sh" if x.startswith("60") else "sz") + x
    url = "http://qt.gtimg.cn/q=" + ",".join(map(prefix, codelist))

    if __debug__:
        print(url)
    resp = requests.get(url)

    datas = {}
    for code, line in zip(codelist, resp.text.split("\n")):
        if line.strip() == "":
            continue

        match = re.search(r"(.+)=\"(.+)\"", line)
        items = match.group(2).split("~")
        data = {"price"   : float(items[3]),
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
                "exchange": float(items[38]),
                "circu_value" : float(items[44]) * 1e4,
                "value"   : float(items[45]) * 1e4}
        datas[code] = data

    return datas


def get_url(code):
    """ get url """
    prefix = lambda x: ("sh" if x.startswith("60") else "sz") + x

    return "http://finance.sina.com.cn/realstock/company/{0}/nc.shtml".format(
        prefix(code)
    )


if __name__ == '__main__':
    print(list(get_history("600692", "20170101")))