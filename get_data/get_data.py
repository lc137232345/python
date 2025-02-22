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
def MACD_Cross(data):
    """
    判断MACD金叉和死叉，并返回买入和卖出信号
    金叉：短期EMA上穿长期EMA，产生买入信号
    死叉：短期EMA下穿长期EMA，产生卖出信号
    """
    # 确保必要的列存在
    required_columns = {'EMA12', 'EMA26', 'DEA'}
    if not required_columns.issubset(data.columns):
        missing = required_columns - set(data.columns)
        raise ValueError(f"数据缺少必要的列: {missing}")
    
    # 计算MACD线和信号线
    data['MACD_Line'] = data['EMA12'] - data['EMA26']
    
    # 初始化信号列
    data['Signal'] = 0
    
    # 使用shift比较当前和前一时刻的MACD线和信号线
    data['Prev_MACD'] = data['MACD_Line'].shift(1)
    data['Prev_Signal'] = data['DEA'].shift(1)
    
    # 生成买入和卖出信号
    data.loc[(data['MACD_Line'] > data['DEA']) & (data['Prev_MACD'] <= data['Prev_Signal']), 'Signal'] = 1  # 买入信号
    data.loc[(data['MACD_Line'] < data['DEA']) & (data['Prev_MACD'] >= data['Prev_Signal']), 'Signal'] = -1  # 卖出信号
    
    # 删除辅助列
    data.drop(columns=['Prev_MACD', 'Prev_Signal'], inplace=True)
    
    return data
# 在deal_data函数中调用MACD_Cross
def deal_data(stock_code):
    data = get_data(stock_code)
    pa.set_ma(data)
    pa.set_MACD(data)
    pa.set_KDJ(data)
    pa.set_DDT(data)
    
    # 调用MACD金叉死叉判断函数
    data = MACD_Cross(data)
    
    save_data(data, stock_code)

# 示例调用
deal_data("000001")

deal_data("000001")