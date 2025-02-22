import matplotlib.pyplot as plt

def plot_dingditu(x, y):
    #创建画布
    plt.figure(figsize=(200,8),dpi=100)
    plt.grid(True,linestyle='--',alpha=0.5)
    plt.legend()
    plt.plot(x,y)
    #显示
    plt.show()