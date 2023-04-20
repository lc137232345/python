from operator import imod
from statistics import mode
from xml.dom.expatbuilder import parseString
import jqdatasdk as jq
import pandas as pd
import numpy as np
import datetime as dt
import math
from MyTT import *

jq.auth('18892136693', '2226612.LIchen')


def get_top_and_down_count(result_tmp):
    CLOSE = result_tmp['close']
    OPEN = result_tmp['open']
    HIGH = result_tmp['high']
    LOW = result_tmp['low']  # 基础数据定义

    VAR1 = 1
    # VAR2 = 1/WINNER(CLOSE)
    VAR3 = MA(CLOSE, 13)
    VAR4 = 100 - ABS((CLOSE - VAR3) / VAR3 * 100)
    VAR5 = LLV(LOW, 75)
    VAR6 = HHV(HIGH, 75)
    VAR7 = (VAR6 - VAR5) / 100
    VAR8 = (SMA((CLOSE - VAR5) / VAR7, 20, 1))
    VAR9 = (SMA((OPEN - VAR5) / VAR7, 20, 1))
    VARA = 3 * VAR8 - 2 * SMA(VAR8, 15, 1)
    VARB = 3 * VAR9 - 2 * SMA(VAR9, 15, 1)
    VARC = 100 - VARB

    duzhan_tmp = (100 - VARA) * VAR1

    return duzhan_tmp

# 获得股票数据源
def get_stock_price_csv(stock_code_list, start_date, end_date):
    for stock_code in stock_code_list:
        df = jq.get_price(stock_code, start_date=start_date, end_date=end_date,
                          frequency='daily', fields=['open', 'close', 'high', 'low', 'volume', 'money'])

        # 整理数据
        df.to_csv('temp.csv')
        df = pd.read_csv('temp.csv')
        df.rename(columns={'Unnamed: 0': "trade_date"}, inplace=True)

        # 整理数据
        df.to_csv('temp.csv')  # 这里随意取名，这个csv会存在当前.py文件的同一目录下，可以查看具体数据
        # 后面这个parse_dates参数的作用是将trade_date那一列的日期数据从xxxxxxxx（float型）改成xxxx-xx-xx（日期型）形式
        df = pd.read_csv('temp.csv', parse_dates=[
            'trade_date'], index_col=['trade_date'])
        df.drop(labels='Unnamed: 0', axis=1, inplace=True)

        df = df.sort_values(by='trade_date')
        # 计算MA5
        df.insert(loc=0, column='ts_code', value=stock_code)
        df.loc[:, "MA5"] = round(df['close'].rolling(5).mean(), 2)  # 添加5均的价格
        df.loc[:, "MA10"] = round(
            df['close'].rolling(10).mean(), 2)  # 添加10均的价格
        df.loc[:, "MA20"] = round(
            df['close'].rolling(20).mean(), 2)  # 添加20均的价格
        df.loc[:, "MA30"] = round(
            df['close'].rolling(30).mean(), 2)  # 添加30均的价格

        df = df.sort_values(by='trade_date', ascending=False)
        # 更改名字
        stock_code_name = stock_code[:-5]
        df.to_csv('./data/MA5_modle/jq_all_stock_data/'+stock_code_name+'.csv')

# 计算首板5均买入的胜率


def camulate_stock_data(stock_code_list, camulate_day):

    # 读取要写入的文件
    result = pd.read_csv('templete.csv')
    for stock_code in stock_code_list:

        # 读取股票的本地数据源
        df = pd.read_csv(stock_code+'.csv', parse_dates=[
            'trade_date'], index_col=['trade_date'])

        dd = dt.datetime.strptime(camulate_day, '%Y-%m-%d').date()
        camulate_day_one_day = str(dd+dt.timedelta(days=-1))
        camulate_day_two_day = str(dd+dt.timedelta(days=-2))

        tp_ts_code = df.loc[camulate_day, 'ts_code']
        tp_last_MA5 = df.loc[camulate_day_two_day, 'MA5']
        tp_today_MA5 = df.loc[camulate_day_one_day, 'MA5']
        tp_tomory_MA5 = df.loc[camulate_day, 'MA5']
        tp_tomory_low_price = df.loc[camulate_day, 'low']
        tp_tomory_close_price = df.loc[camulate_day, 'close']

        ts_code = tp_ts_code[camulate_day]
        last_MA5 = tp_last_MA5[camulate_day_two_day]
        today_MA5 = tp_today_MA5[camulate_day_one_day]
        tomory_MA5 = tp_tomory_MA5[camulate_day]
        low_price = tp_tomory_low_price[camulate_day]
        close_price = tp_tomory_close_price[camulate_day]

        # 目标买入价位
        target_price = round((today_MA5+2*(today_MA5-last_MA5))*0.993, 2)

        # 目标买入价位与最低点差值
        diff_value = '{:.2%}'.format(
            ((target_price-low_price)/target_price))

        # 计算买入后的收益率
        if(target_price > tp_tomory_low_price[camulate_day]):
            get = '{:.2%}'.format((close_price-target_price)/target_price)
        else:
            get = 0

        result.loc[len(result)] = {'ts_code': ts_code, 'last_MA5': last_MA5, 'today_MA5': today_MA5, 'tomory_MA5': tomory_MA5,
                                   'low_price': low_price, 'close': close_price, 'target_price': target_price, "diff_value": diff_value, 'get': get}

    # 写入文件
    result.to_csv('./data/首板5均模型/首板涨停板数据/'+camulate_day+'.csv')


# 计算主升趋势10均买入的胜率
def camulate_stock_data_at_MA10(stock_code_list):

    # 读取要写入的文件
    result = pd.read_csv('templete.csv')
    for stock_code in stock_code_list:

        # 读取股票的本地数据源
        df = pd.read_csv('./data/MA5_modle/jq_all_stock_data/'+stock_code+'.csv', parse_dates=[
            'trade_date'])
        for i in range(1, len(df) - 1):
            one_day_MA5 = df.loc[i+1, 'MA5']
            one_day_MA10 = df.loc[i+1, 'MA10']
            one_day_MA20 = df.loc[i+1, 'MA20']
            one_day_MA30 = df.loc[i+1, 'MA30']
            one_day_low = df.loc[i+1, 'low']
            if(math.isnan(one_day_MA30)):  # 判断30日均线不存在，停止遍历
                break
            else:
                if(one_day_MA5 > one_day_MA10*1.02 and one_day_MA10 > one_day_MA20*1.02):  # 满足均线主升要求

                    trade_date = df.loc[i, 'trade_date']
                    ts_code = df.loc[i, 'ts_code']
                    today_low = df.loc[i, 'low']

                    tomorrow_open = df.loc[i-1, 'open']
                    tomorrow_high = df.loc[i-1, 'high']
                    tomorrow_low = df.loc[i-1, 'low']
                    tomorrow_close = df.loc[i-1, 'close']

                    two_day_MA10 = df.loc[i+2, 'MA10']  # 计算当日的10均价格
                    # 目标买入价位
                    target_price = round(
                        one_day_MA10+(one_day_MA10-two_day_MA10)*1.002, 2)

                    # 目标买入价位与最低点差值
                    diff_value = '{:.2%}'.format(
                        ((target_price-today_low)/target_price))

                    # 计算买入后，明日的日线后的收益率
                    if(target_price > today_low):
                        get_close = '{:.2%}'.format(
                            (tomorrow_close-target_price)/target_price)
                        get_high = '{:.2%}'.format(
                            (tomorrow_high-target_price)/target_price)
                        get_open = '{:.2%}'.format(
                            (tomorrow_open-target_price)/target_price)
                    else:
                        get_close = 0

                    result.loc[len(result)] = {'trade_date': trade_date, 'ts_code': ts_code,
                                               'two_day_MA10': two_day_MA10, 'one_day_MA10': one_day_MA10,
                                               'tomorrow_low': tomorrow_low,
                                               'tomorrow_open': tomorrow_open, 'tomorrow_high': tomorrow_high,
                                               'target_price': target_price, "diff_value": diff_value,
                                               'get_close': get_close, "get_high": get_high, "get_open": get_open}

            # 写入文件
        result.to_csv('./data/MA10_modle/'+stock_code+'.csv')
        result.drop(result.index, inplace=True)


#stock_code = pd.read_csv('./data/主板名称.csv')
#stock_code_list = stock_code['ts_code'].str[:6].to_list()
# 切割数据
#stock_code_list = stock_code_list.str[:6].to_list()

#get_stock_price_csv('000001', '2017-01-01', '2022-05-29')

# camulate_stock_data(stock_code_list, '2022-05-25')

#camulate_stock_data_at_MA10(stock_code_list)
close_data=jq.get_price('000001.XSHE', count = 1000, end_date='2023-04-20', frequency='15m', fq='pre',fields=['open', 'close','high','low'])

duzhan = get_top_and_down_count(close_data)

for dz in duzhan:
    print(dz)

print("hello world")
