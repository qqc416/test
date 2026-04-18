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

