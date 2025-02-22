import fun as ths
import numpy as np
import pandas as pd

def calculate_moving_average(data, window):
    """
    计算移动平均并四舍五入到3位小数
    :param data: DataFrame，包含收盘价数据
    :param window: int，移动平均的窗口大小
    :return: DataFrame，添加了新的移动平均列
    """
    ma_name = f"MA{window}"  # 根据窗口大小生成列名
    data[ma_name] = round(data['close'].rolling(window).mean(), 3)
    return data

def set_ma(close_data):
    """
    设置多个移动平均线
    :param close_data: DataFrame，包含收盘价数据
    :return: DataFrame，添加了多个移动平均线列
    """
    # 定义移动平均的窗口大小列表
    windows = [5, 10, 20, 30]
    
    # 循环计算每个移动平均线
    for window in windows:
        close_data = calculate_moving_average(close_data, window)
    
    return close_data

# 使用示例
# 假设df是包含收盘价数据的DataFrame
# df = set_ma(df)

def set_MACD(df):
        # MACD指标
    df['EMA12'] = round(df['close'].ewm(span=12).mean(),3)
    df['EMA26'] = round(df['close'].ewm(span=26).mean(),3)
    df['MACD'] = round(df['EMA12'] - df['EMA26'],3)
    df['Signal'] = round(df['MACD'].ewm(span=9).mean(),3)


def set_KDJ(df):
    # 计算最高价、最低价和收盘价的差值
    df['High_Low'] = round((df['high'] - df['low']), 3)
    
    # 计算最高价、最低价和收盘价的差值的9天内的最高值和最低值
    df['High_Low_9'] = round(df['High_Low'].rolling(window=9).max(), 3)
    df['Close_Low_9'] = round(df['close'].rolling(window=9).min(), 3)
    
    # 初始化 K 和 D 列
    df['K'] = 50  # 初始值可以根据需要调整
    df['D'] = 50  # 初始值可以根据需要调整
    
    # 计算 high_low_diff 列
    df['high_low_diff'] = df['High_Low_9'] - df['Close_Low_9']
    
    # 计算 K 值的矢量化操作
    df['K'] = 2/3 * df['K'] + 1/3 * (df['close'] - df['Close_Low_9']) / df['high_low_diff']

    # 处理除数为零的情况
    df['K'] = np.where(df['high_low_diff'] != 0, df['K'], np.nan)
   
    # 计算 D 值
    df['D'] = 2/3 * df['D'].shift(1) + 1/3 * df['K']
    
    # 计算 J 值
    df['J'] = 3 * df['K'] - 2 * df['D']
    
    # 重置 KDJ 的初始值（如果需要）
    df[['K', 'D', 'J']] = df[['K', 'D', 'J']].fillna(0)
    
    # 仅保留最近的 KDJ 值，并四舍五入到小数点后三位
    df[['K', 'D', 'J']] = df[['K', 'D', 'J']].apply(lambda x: round(x, 3))
    
    # 删除辅助列
    df.drop(columns=['High_Low', 'high_low_diff'], inplace=True)
    
    return df


 
#该函数进行设置顶底图参数
def set_DDT(close_data):
    # 使用列表推导式计算 DDT 并四舍五入
    close_data['DDT'] = [round(x, 3) for x in ths.get_top_and_down_count(close_data)]

def set_Derivative(close_data):
    close_data.loc[:,"Derivative"] = ths.cal_deriv_after_average(close_data['DDT'])
