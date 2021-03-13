import lightgbm as lgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
import time
from sklearn.model_selection import KFold

kf = KFold(n_splits=10)
rmse_scores = []
train = pd.read_csv("../crawler/document/all_data.csv")
for i in train.columns:
    if i in ['isChinese', 'ID', 'datetime', 'name']:
        train[i] = train[i].astype('object')
number_columns = [col for col in train.columns if train[col].dtype != 'object']
category_columns = [col for col in train.columns if train[col].dtype == 'object']
print(number_columns)
print(category_columns)

# use proportion between firstweek and firstday to fix the NULL in csv
for row in train.iterrows():
    row = row[1]
    print(row['firstweekbox'])
    if np.isnan(row['firstweekbox']):
        row['firstweekbox'] = row['allbox'] / 4
        print('--------------------')
    if np.isnan(row['firstdaybox']):
        row['firstdaybox'] = row['firstweekbox'] / 8

'''
for i, col in zip(range(len(number_columns)), number_columns):
    print(col)
    sns.distplot(train[col], ax=axes[i])
    plt.tight_layout()
plt.show()
'''
# create divide pots graph to show the relation between aspects and allbox
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(20, 18))
axes = axes.flatten()
for i, col in zip(range(len(number_columns)), number_columns):
    print(col)
    if i == 0:
        continue
    else:
        sns.scatterplot(x=col, y='allbox', data=train, ax=axes[i-1])
        plt.tight_layout()
plt.show()
'''
plt.figure(figsize=(16, 8)) # 画布大小
plt.title("allbox with firstweekbox")
#sns.scatterplot(x='YearBuilt', y='SalePrice', data=train) # 写法一
sns.scatterplot(train.firstweekbox, train.allbox) # 写法二
plt.show()
'''

# train the lightGBM-Model to predict the data
X = train.drop(columns=['ID', 'allbox', 'datetime', 'name'], axis=1).values  # 说明：ID, name, datetime不是特征，box是标签，需要屏蔽
y = train['allbox'].values  # 标签allbox

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)  # 验证集占比20%，打乱顺序
for train_indices, test_indices in kf.split(X):
    X_train, X_test = X[train_indices], X[test_indices]
    y_train, y_test = y[train_indices], y[test_indices]
    # 初始化模型
    LGBR = lgb.LGBMRegressor() # 基模型
    # 训练/fit拟合
    LGBR.fit(X_train, y_train)
    # 预测
    y_pred = LGBR.predict(X_test)
    # 评估
    rmse = mean_absolute_error(y_test, y_pred)
    # 累计结果
    rmse_scores.append(rmse)

print("rmse scores : ", rmse_scores)
print(f'average rmse scores : {np.mean(rmse_scores)}')