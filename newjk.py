from operator import imod
from statistics import mode
from xml.dom.expatbuilder import parseString
import jqdatasdk as jq
import pandas as pd
import numpy as np
import datetime as dt
import matpl as pl
import param as par

jq.auth('18892136693', '2226612.LIchen')

close_data = jq.get_price("516160.XSHG", count = 200, end_date='2023-04-24', frequency='5m', fq='pre',fields=['open', 'close','high','low'])


par.set_ma(close_data)
par.set_DDT(close_data)

close=close_data.dropna()

par.set_Derivative(close)

x=list(range(1,close['DDT'].size+1))
y=list(close['DDT'])
pl.plot_dingditu(x,y)

x=list(range(1,close['Derivative'].size+1))
y=list(close['Derivative'])
pl.plot_dingditu(x,y)

#close.to_csv('./data/'+'516160.csv')