import fun as ths

def set_ma(close_data):
    close_data.loc[:, "MA5"] = round(close_data['close'].rolling(5).mean(), 3)  # 添加5均的价格
    close_data.loc[:, "MA10"] = round(
        close_data['close'].rolling(10).mean(), 3)  # 添加10均的价格
    close_data.loc[:, "MA20"] = round(
        close_data['close'].rolling(20).mean(), 3)  # 添加20均的价格
    close_data.loc[:, "MA30"] = round(
        close_data['close'].rolling(30).mean(), 3)  # 添加30均的价格

def set_DDT(close_data):
    close_data.loc[:,"DDT"] = ths.get_top_and_down_count(close_data)


def set_Derivative(close_data):
    close_data.loc[:,"Derivative"] = ths.cal_deriv_after_average(close_data['DDT'])
