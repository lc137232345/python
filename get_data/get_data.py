# 确保安装tushare库
# 可以在命令行中运行以下命令来安装或升级tushare
# python -m pip install --upgrade pip

import tushare as ts
import pandas as pd
import datetime as dat
import param as pa





# 设置Tushare的API Token
ts.set_token('b6fc04bc3a1161c3e5649e5c462b134f956a00d00b334553e8719bcd')

# 初始化Pro接口
pro = ts.pro_api()

# 获取股票数据，例如获取贵州茅台（600519.SH）的日线数据
def get_trade_day(stock_code, temp_start_date, temp_end_date):
    #date =str(dat.datetime.now().date()).replace('-', '')
    df = pro.daily(ts_code=stock_code, start_date=temp_start_date, end_date=temp_end_date)
    stock_code_name = stock_code[:6]
    df.to_csv('./data/'+stock_code_name+'.csv')


def get_data(stock_code):
    df=pd.read_csv('./data/'+stock_code+'.csv')
    df.drop(labels='Unnamed: 0', axis=1, inplace=True)
    df = df.sort_values(by='trade_date')
    return df

def save_data(df,stock_code):
    # 更改名字
    df.to_csv('./data/'+stock_code+'11.csv')

def deal_data(stock_code):
    data = get_data(stock_code)
    pa.set_ma(data)
    pa.set_MACD(data)
    pa.set_KDJ(data)
    pa.set_DDT(data)
    save_data(data,stock_code)

deal_data("000001")