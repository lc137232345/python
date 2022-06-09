import matplotlib.pyplot as plt

#创建画布
plt.figure(figsize=(20,8),dpi=100)

#绘制图像
x=[1,2,3]
y=[4,5,6]
z=[7,8,9]

plt.grid(True,linestyle='--',alpha=0.5)

plt.legend()

plt.plot(x,y,z)
#显示
plt.show()