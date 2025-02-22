"""_summary_
    同花顺的函数公式
Returns:
    _type_: _description_
"""


from MyTT import *

def get_top_and_down_count(result_tmp):
    CLOSE = result_tmp['close']
    OPEN = result_tmp['open']
    HIGH = result_tmp['high']
    LOW = result_tmp['low']  # 基础数据定义

    VAR1 = 1
    # VAR2 = 1/WINNER(CLOSE)
    VAR3 = MA(CLOSE, 13)
    #VAR4 = 100 - ABS((CLOSE - VAR3) / VAR3 * 100)
    VAR5 = LLV(LOW, 75)
    VAR6 = HHV(HIGH, 75)
    VAR7 = (VAR6 - VAR5) / 100
    VAR8 = (SMA((CLOSE - VAR5) / VAR7, 20, 1))
    VAR9 = (SMA((OPEN - VAR5) / VAR7, 20, 1))
    VARA = 3 * VAR8 - 2 * SMA(VAR8, 15, 1)
    VARB = 3 * VAR9 - 2 * SMA(VAR9, 15, 1)
    #VARC = 100 - VARB

    duzhan_tmp = (100 - VARA) * VAR1

    return duzhan_tmp



# 曲线平滑处理，第一个参数为数据信号，第二个参数为滑动平均的大小。
def np_move_avg(a, n, mode="same"):
    return np.convolve(a, np.ones((n,)) / n, mode=mode)


# 定义计算离散点导数的函数
def cal_deriv(x, y):  # x, y的类型均为列表
    diff_x = []  # 用来存储x列表中的两数之差
    for i, j in zip(x[0::], x[1::]):
        diff_x.append(j - i)

    diff_y = []  # 用来存储y列表中的两数之差
    for i, j in zip(y[0::], y[1::]):
        diff_y.append(j - i)

    slopes = []  # 用来存储斜率
    for i in range(len(diff_y)):
        slopes.append(diff_y[i] / diff_x[i])

    deriv = []  # 用来存储一阶导数
    for i, j in zip(slopes[0::], slopes[1::]):
        deriv.append((0.5 * (i + j)))  # 根据离散点导数的定义，计算并存储结果
    deriv.insert(0, slopes[0])  # (左)端点的导数即为与其最近点的斜率
    deriv.append(slopes[-1])  # (右)端点的导数即为与其最近点的斜率

    return deriv  # 返回存储一阶导数结果的列表  


def remove_nan(in_data):
    result = np.nan_to_num(in_data)
    result = [i for i in result if i != 0]
    return result


def cal_deriv_after_average(in_data):
    # 生成x轴的临时变量
    x_list = list(range(1, in_data.size + 1))
    # 计算平滑后的导数
    y_list = cal_deriv(x_list, np_move_avg(in_data, 20))
    # 平滑导数图像
    y_list = np_move_avg(y_list, 20)
    return y_list