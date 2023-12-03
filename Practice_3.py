import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('Practice/4/6.txt', header=None)
df.columns = ['Nums']

df.describe()


def interval(df):
    height = df.Nums
    m = round(1 + np.log2(len(height)))
    h = (np.max(height) - np.min(height)) / m
    interval = [np.min(height) - 0.01]
    for k in range(1, m + 2):
        interval = np.append(interval, interval[k - 1] + h)
    interval_1 = interval[1::]
    interval_2 = interval[:-1]
    height = sorted(height)
    abs_freq_var = [0] * (m + 1)
    i = 0
    for k in range(len(height)):
        for j in range(len(interval_1)):
            if (height[k] > interval_2[j] and height[k] < interval_1[j]):
                abs_freq_var[j] += 1

    var_series_2 = pd.DataFrame([interval_2, interval_1])
    rel_freq_var = np.array(abs_freq_var) / len(df)
    var_series_2 = var_series_2.T
    var_series_2.columns = ['left', 'right']
    var_series_2 = var_series_2.join(
        [pd.Series(abs_freq_var, name='abs_freq').T, pd.Series(rel_freq_var, name='rel_freq').T])
    return var_series_2, interval_1, interval_2, h


var, int1, int2, h = interval(df)

var

interval_hist = list(map(str, np.array([x for x in zip(int2.round(2), int1.round(2))])))
interval_hist = [x.replace(']', '') for x in interval_hist]
interval_hist = [x.replace('[', '') for x in interval_hist]

plt.figure(figsize=(12, 6))
plt.bar(int1, var['rel_freq'], width=h, edgecolor='r', tick_label=interval_hist)


def chi2_pearson_norm(df1, df2):
    mean = df1.Nums.describe()['mean']
    std = df1.Nums.describe()['std']
    df2['Pi'] = (stats.norm.cdf((df2['right'] - mean) / std) - 0.5 - (
                stats.norm.cdf((df2['left'] - mean) / std) - 0.5)) * len(df)
    chi2 = (((df2['abs_freq'] - df2['Pi']) ** 2) / df2['Pi']).sum()
    if chi2 < stats.chi2.ppf(0.95, len(df2) - 3):
        return 'norm', df2, chi2, stats.chi2.ppf(0.95, len(df2) - 3)
    else:
        return 'not norm'


def chi2_pearson_exp(df1, df2):
    mean = df1.Nums.describe()['mean']
    lambda_ = 1 / mean
    df2['Pi'] = (np.exp((-1) * lambda_ * df2['left']) - np.exp((-1) * lambda_ * df2['right'])) * len(df1)
    chi2 = (((df2['abs_freq'] - df2['Pi']) ** 2) / abs(df2['Pi'])).sum()
    if chi2 < stats.chi2.ppf(0.95, len(df2) - 2):
        return 'exp', df2, chi2, stats.chi2.ppf(0.95, len(df2) - 2)
    else:
        return 'not exp'


chi2_pearson_exp(df, var)

chi2_pearson_norm(df, var)

var_new = var[var['abs_freq'] != 0]

anamorf = pd.DataFrame(np.log(var_new['rel_freq']))

anamorf['mean_int'] = ((var['right'] + var['left']) / 2)
anamorf['x'] = (anamorf['mean_int'] - df['Nums'].mean()) ** 2
anamorf

X = np.array(anamorf['x'])
y = np.array(anamorf['rel_freq'])
X_1 = np.array(anamorf['mean_int'])

X_new = np.c_[X, np.ones(np.shape(X)[0])]
X_new_1 = np.c_[X_1, np.ones(np.shape(X_1)[0])]

from sklearn.metrics import r2_score

W_1 = np.linalg.inv(X_new.T @ X_new) @ X_new.T @ y
W_2 = np.linalg.inv(X_new_1.T @ X_new_1) @ X_new_1.T @ y

fig, ax = plt.subplots()
plt.figure(figsize=(5, 5))
ax.grid()
ax.scatter(X_1, y)
ax.plot(X_1, X_new_1 @ W_2, color='r')
ax.set_xlabel("X")
ax.set_ylabel("ln(w)")
ax.set_title(f'Анаморфоза для показательного распределения; R2 = {r2_score(y, X_new_1 @ W_2).round(3)}')
plt.show()

fig, ax = plt.subplots()
plt.figure(figsize=(5, 5))
ax.grid()
ax.scatter(X, y)
ax.plot(X, X_new @ W_1, color='r')
ax.set_xlabel("X")
ax.set_ylabel("ln(w)")
ax.set_title(f'Анаморфоза для нормального распределения; R2 = {r2_score(y, X_new @ W_1).round(3)}')
plt.show()

W_1[1]

print("std =", np.sqrt(-1 / (2 * W_1[0])))

print("lambda =", -1 / W_2[0])
