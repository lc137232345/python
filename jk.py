from operator import imod
from statistics import mode
import jqdatasdk as jq
import pandas as pd
import numpy as np
import datetime as dt

jq.auth('17802925769', '2226612.LIchen')


#获得股票数据源
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
        #更改名字
        stock_code_name=stock_code[:-5]
        df.to_csv('./data/MA5_modle/jq_all_stock_data/'+stock_code_name+'.csv')

#计算首板5均买入的胜率
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



stock_code =pd.read_csv('./data/主板名称.csv')
stock_code_list=stock_code['ts_code'].to_list()

get_stock_price_csv(stock_code_list, '2017-01-01', '2022-05-29')

#camulate_stock_data(stock_code_list, '2022-05-25')
