import pandas as pd
import numpy as np
import yfinance as yf
import vectorbt as vbt

# 参数设置
symbol = '600519.SS'  # 贵州茅台
start_date = '2020-01-01'
end_date = '2025-01-01'
initial_capital = 100000  # 初始资金

# 获取数据
data = yf.download(symbol, start=start_date, end=end_date)
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

# 计算技术指标
def calculate_features(df):
    # 双均线系统
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    
    # MACD指标
    df['EMA12'] = df['Close'].ewm(span=12).mean()
    df['EMA26'] = df['Close'].ewm(span=26).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9).mean()
    
    # 动量因子
    df['Momentum'] = df['Close'].pct_change(periods=5)
    return df.dropna()

data = calculate_features(data)

# 生成交易信号
def generate_signals(df):
    # 金叉买入信号
    df['Buy_Signal'] = (df['MA5'] > df['MA20']) & (df['MACD'] > df['Signal'])
    
    # 死叉卖出信号
    df['Sell_Signal'] = (df['MA5'] < df['MA20']) | (df['Close'] < df['MA20']*0.97)  # 3%止损
    
    return df

data = generate_signals(data)

# 回测策略
portfolio = vbt.Portfolio.from_signals(
    close=data['Close'],
    entries=data['Buy_Signal'],
    exits=data['Sell_Signal'],
    init_cash=initial_capital,
    fees=0.001,        # 交易佣金0.1%
    slippage=0.002     # 滑点0.2%
)

# 输出结果
print("策略总收益率:", portfolio.total_return())
print("年化收益率:", portfolio.annualized_return())
print("最大回撤:", portfolio.max_drawdown())

# 可视化
portfolio.plot().show()