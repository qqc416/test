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
#  任务2：时间分布 
print("\n 任务2：时间分布 ")
df_up = df[df['刷卡类型'] == 0].copy()#只筛选上车刷卡记录
hours = np.array(df_up['hour'])#转化为numpy数组

morning = np.sum(hours < 7)#使用布尔索引统计各时段刷卡量
night = np.sum(hours >= 22)
total = len(hours)#计算总量
#输出结果与占比
print(f"早峰前：{morning}，占比：{morning/total:.1%}")
print(f"深夜：{night}，占比：{night/total:.1%}")

# 绘图
hour_cnt = df_up['hour'].value_counts().sort_index()
plt.figure(figsize=(12,5))
c = ['#ff6666' if h<7 or h>=22 else '#3399ff' for h in hour_cnt.index]
plt.bar(hour_cnt.index, hour_cnt.values, color=c)
plt.title('24小时刷卡量分布')
plt.xlabel('小时')
plt.ylabel('次数')
plt.xticks(range(0,24,2))
plt.grid(alpha=0.3)
plt.savefig('hour_distribution.png', dpi=150)
plt.close()
# 任务3：线路站点分析 
print("\n 任务3：线路站点分析")
#定义函数，计算标准差
def analyze_route_stops(df, route_col='线路号', stops_col='ride_stops'):
    res = df.groupby(route_col)[stops_col].agg(['mean','std']).reset_index()#分组计算均值，标准差
    res.columns = ['线路号','mean_stops','std_stops']#对各列进行命名
    return res.sort_values('mean_stops', ascending=False)##降序排序

route_df = analyze_route_stops(df)
print(route_df.head(10))

# 水平条形图
top15 = route_df.head(15)
plt.figure(figsize=(10,6))
plt.barh(top15['线路号'].astype(str), top15['mean_stops'], color='#5599cc')
plt.title('Top15线路平均搭乘站点数')
plt.xlabel('平均站点数')
plt.ylabel('线路号')
plt.tight_layout()
plt.savefig('route_stops.png', dpi=150)
plt.close()

# 任务4：高峰小时系数 
print("\n任务4：高峰小时系数 ")
hourly = df_up.groupby('hour').size()#按小时统计上车辆
peak_h = hourly.idxmax()#高峰小时
peak_n = hourly.max()#高峰小时刷卡量
print(f"高峰小时：{peak_h}:00-{peak_h+1}:00，共{peak_n}次")

peak_df = df_up[df_up['hour'] == peak_h].copy()#筛选数据
peak_df['min'] = peak_df['交易时间'].dt.minute#提取分钟数，用于分窗统计

# 5min
peak_df['bin5'] = peak_df['min'] // 5
max5 = peak_df['bin5'].value_counts().max()
phf5 = peak_n / (12 * max5)

# 15min
peak_df['bin15'] = peak_df['min'] // 15
max15 = peak_df['bin15'].value_counts().max()
phf15 = peak_n / (4 * max15)

print(f"PHF5 = {phf5:.4f}")
print(f"PHF15 = {phf15:.4f}")

# 任务5：驾驶员文件导出 
print("\n任务5：线路驾驶员文件 ")
out_dir = '线路驾驶员信息'#创建文件
os.makedirs(out_dir, exist_ok=True)

routes = df[(df['线路号']>=1101)&(df['线路号']<=1120)]['线路号'].unique)#筛选路线1101-1120
#遍历所有路线，生成txt文件
for r in sorted(routes):
    sub = df[df['线路号']==r]#提取当前路线数据
    pairs = sub[['车辆编号','驾驶员编号']].drop_duplicates()
    with open(f'{out_dir}/{r}.txt','w',encoding='utf-8') as f:#写入文件
        f.write(f'线路号: {r}\n车辆编号\t驾驶员编号\n')
        for _,row in pairs.iterrows():
            f.write(f"{row['车辆编号']}\t{row['驾驶员编号']}\n")
    print(f'已生成：{r}.txt')

