#!/usr/bin/python3

from datetime import datetime, timedelta
import tushare as ts


def get_stock_data(code):
    start_date = (datetime.today() - timedelta(days=180)).strftime('%Y-%m-%d')
    df = ts.get_hist_data(code, start=start_date)

    dl = len(df)
    h_high, h_low, l_high, l_low = [],[],[],[]
    cur_data = df.iloc[0]
    for i in range(1, dl):
        prev_data = df.iloc[i]
        h_high.append((cur_data.high - prev_data.high) / prev_data.high * 100)
        l_high.append((cur_data.low - prev_data.high) / prev_data.high * 100)
        h_low.append((cur_data.high - prev_data.low) / prev_data.low * 100)
        l_low.append((cur_data.low - prev_data.low) / prev_data.low * 100)
        cur_data = prev_data

    h_high.append(0)
    l_high.append(0)
    h_low.append(0)
    l_low.append(0)

    df['h_high'] = h_high
    df['l_high'] = l_high
    df['h_low'] = h_low
    df['l_low'] = l_low
    return df


def check_stock_data(code, percent=3):
    df = get_stock_data(code)

    dl = len(df)
    print('--- %s %d %% ---' % (code, percent))
    print('    Higher than high: %-.3f' % (len(df[df.h_high > percent]) / dl * 100))
    print('    Lower than high : %-.3f' % (len(df[df.l_high < -percent]) / dl * 100))
    print('    Higher than low : %-.3f' % (len(df[df.h_low > percent]) / dl * 100))
    print('    Lower than low  : %-.3f' % (len(df[df.l_low < -percent]) / dl * 100))


def predict_stock(codes, percent=3):
    df = ts.get_realtime_quotes(codes)
    fach = 1 + percent / 100
    facl = 1 - percent / 100
    for i in range(len(df)):
        data = df.iloc[i]
        print('%s:\t\t%5.2f -- %5.2f' % (data.code, 
                                    float(data.low) * facl, float(data.high) * fach))


if __name__ == '__main__':
    codes = (
        '000063', 
        '002405', 
        '300024', 
        '600388', 
        '600692',
        '600977', 
        '603885')
    predict_stock(codes)
