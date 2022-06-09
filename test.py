from ctypes import sizeof
from pickle import TRUE
import tushare as ts
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as mp
import matplotlib.dates as md
import mplfinance as mpf
import datetime as dat
from pathlib import Path
import os

# 设置接口
# 手动给我的token加密
ts.set_token('b6fc04bc3a1161c3e5649e5c462b134f956a00d00b334553e8719bcd')
# 在tushare pro注册后可在个人中心找到token，复制过来就好
pro = ts.pro_api()


def get_limit_up_data(date_list):
    for date in date_list:
        #读取数据
        df = pro.daily(trade_date=date)
        #保存数据
        df.to_csv('./data/'+date+'.csv')
        #清理数据
        df = pd.read_csv('./data/'+date+'.csv')
        limit_up = df[((df['pct_chg'] >= 9.8) & (df['pct_chg'] <= 10.1))]
        #保存
        limit_up.to_csv('./data/limit_up/limit_up_'+date+'.csv')

def get_limit_up_now_day():
    date=str(dat.datetime.now().date()).replace('-', '')
    #读取数据
    df = pro.daily(trade_date=date)
    #保存数据
    df.to_csv('./data/'+date+'.csv')
    #清理数据
    df = pd.read_csv('./data/'+date+'.csv')
    limit_up = df[((df['pct_chg'] >= 9.8) & (df['pct_chg'] <= 10.1))]
    #保存
    limit_up.to_csv('./data/limit_up/limit_up_'+date+'.csv')

def get_trade_day():
    date =str(dat.datetime.now().date()).replace('-', '')
    df = pro.daily(ts_code='000001.SZ', start_date='20220101', end_date=date)
    df.to_csv('./data/temp_date.csv')
    df=pd.read_csv('./data/temp_date.csv')
    data=df["trade_date"].astype(str).tolist()
    print(data)
    return data

def read_all_file_name():
    file_path = './data/limit_up/data/'
    file_name = os.listdir(file_path)
    return file_name

#统计每一天的首板
def camculate_limit_up_day():
    file_name_list =read_all_file_name()
    file_name_list.sort(reverse=True)
    for i in range(len(file_name_list)-1):
        camculate_day=file_name_list[i]
        camculate_last_day=file_name_list[i+1]
        camculate_data=pd.read_csv('./data/limit_up/data/'+camculate_day)
        camculate_last_data=pd.read_csv('./data/limit_up/data/'+camculate_last_day)
        same_diif_df=pd.merge(camculate_data,camculate_last_data,on=['ts_code'])
        set_diff_df=camculate_data.append(same_diif_df)
        set_diff_df=set_diff_df.drop_duplicates(subset=['ts_code'],keep=False)
        set_diff_df.to_csv('./data/limit_up/首板/'+'首板_'+camculate_day)


#date=get_trade_day()
#get_limit_up_data('20211230')
camculate_limit_up_day()