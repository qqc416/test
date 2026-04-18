# -*- coding: utf-8 -*-
#引入该任务所需的标准库
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings#由于seaborn版本兼容性问题，将加入忽略警告信息
warnings.filterwarnings('ignore')
# 解决中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#任务1：数据预处理 
print("任务1：数据预处理 ")
df = pd.read_csv('ICData.csv')

# 自动识别数据中的时间列
time_col = None
for col in df.columns:
    if '时间' in col:
        time_col = col
        break
#将字符串转化为pandas的datetime格式
df['交易时间'] = pd.to_datetime(df[time_col])
df['hour'] = df['交易时间'].dt.hour#提取小时数，生成hour列

# 计算搭乘站点数
df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])
before = df.shape[0]#删除站数为0的异常值
df = df[df['ride_stops'] != 0]
print(f"删除ride_stops=0异常值：{before - df.shape[0]} 条")

# 输出缺失值
print("缺失值：")
print(df.isnull().sum())
