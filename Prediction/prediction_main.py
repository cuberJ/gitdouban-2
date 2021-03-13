import lightgbm as lgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
from sklearn.model_selection import KFold

# kf = KFold(n_split=10)
rmse_score = []
train = pd.read_csv("../crawler/document/all_data.csv")
print(train.shape)
print(train.info)