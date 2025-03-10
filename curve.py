import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl import load_workbook
excel_file_path = '最小blk.xlsx'
sheetname='q=128&time'
np.set_printoptions(suppress=True)
# 使用pandas的read_excel函数读取Excel文件
# 如果Excel文件中有多个sheet，可以通过sheet_name参数指定要读取的sheet
df = pd.read_excel(excel_file_path, sheetname, header=0) 
data_array = np.array(df)
print(data_array)
x , y = data_array[:,12], data_array[:,14]
print(x,'\n',y)
coefficients = np.polyfit(x, y, 7)

# 创建多项式对象
polynomial = np.poly1d(coefficients)

# 打印多项式系数
print("Polynomial coefficients:", coefficients)

# 使用多项式对象生成一系列y值
y_fit = polynomial(x)

# 绘制原始数据点
plt.scatter(x, y, label='Data Points')

# 绘制拟合的多项式曲线
x_fit = np.linspace(min(x), max(x), 100)
y_fit = polynomial(x_fit)
plt.plot(x_fit, y_fit, label='Fitted Polynomial Curve', color='red')

# 添加图例
plt.legend()

# 显示图表
plt.show()
# 显示数据
# print(df)
# arrayx = np.zeros(90, dtype=int)
# print(df.columns)
# column_A=df['A']
# for x in range(1,91):
#     arrayx[x]=column_A[x]
# print(arrayx)