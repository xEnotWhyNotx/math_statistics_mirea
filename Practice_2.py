import pandas as pd
import numpy as np
from scipy.stats import t
from scipy.stats import chi2
import warnings

warnings.filterwarnings('ignore')

df_1 = pd.read_csv('Practice/4/1.txt', sep=' ', header=None)
df_2 = pd.read_csv('2.txt', sep=' ', header=None)
df_3 = pd.read_csv('Practice/4/3.txt', sep=' ', header=None)
df_4 = pd.read_csv('Practice/4/4.txt', sep=' ', header=None)


"""
Точечная оценка - число, с помощью кот. оцениваем соотв. парам. ген. совокупности.
Несмещенная - мат. ожидание оценки параметра == истинное значение параметра.
Состоятельность - при увелич. объема выборки оценка сход. к истинному знач. параметра.
Эффективность - наилучшая из всех возможных оценок. Т.е. минимальная дисперсия.
"""

def interval(df):
    # Получаем описание мат. ожидания и стандартного отклонения
    res = df.describe().T.loc[:, ['mean', 'std']]
    print(res)
    # Находим границы доверительного интервала мат. ожидания по правилу нормального
    # распределения, используя таблицу критических значений функции Лапласа
    interval_laplass = np.array(
        [res['mean'] - 1.96 * res['std'] / np.sqrt(len(df)), res['mean'] + 1.96 * res['std'] / np.sqrt(len(df))])
    # По правилу t-распределения Стьюдента
    interval_t = np.array([res['mean'] - t.ppf(0.95, len(df) - 1) * res['std'] / np.sqrt(len(df)),
                           res['mean'] + t.ppf(0.95, len(df) - 1) * res['std'] / np.sqrt(len(df))])
    print("t: ", t.ppf(0.95, len(df) - 1))
    print("𝜒^2: ", chi2.ppf(1 - 0.025, len(df) - 1))
    print("𝜒^2: ",chi2.ppf(0.025, len(df) - 1))
    # Найти границы доверительного интервала для среднеквадратического отклонения
    # по оценке 𝜒**2 -распределения при значении уверенности 𝛾 = 0.95
    interval_std = np.array([res['std'] * np.sqrt(len(df - 1)) / np.sqrt(chi2.ppf(1 - 0.025, len(df) - 1)),
                             res['std'] * np.sqrt(len(df - 1)) / np.sqrt(chi2.ppf(0.025, len(df) - 1))])
    interval_laplass, interval_t, interval_std = [float(x) for x in interval_laplass], [float(x) for x in interval_t], [
        float(x) for x in interval_std]
    return (pd.DataFrame([interval_laplass, interval_t, interval_std], columns=['Левая граница', 'Правая граница'],
                         index=['interval_mean_laplass', 'interval_mean_t', 'interval_std']))


print(interval(df_1), "\n" * 3)
print(interval(df_2), "\n" * 3)
print(interval(df_3), "\n" * 3)
print(interval(df_4))
