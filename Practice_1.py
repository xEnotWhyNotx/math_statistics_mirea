# '''
# №1 Первичная обработка данных
# '''
#
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat
import math as m

# ЦЕЛОЧИСЛЕННЫЕ ДАННЫЕ (числа от 0 до 8)
X = [7, 5, 0, 5, 4, 4, 2, 0, 2, 5]
n = len(X)

setX = list(set(X))
countsX = []
for i in range(len(setX)):
    countsX.append(X.count(setX[i]))
W = [round(x / n, 3) for x in countsX]

print(f"Вар-ый ряд:     {sorted(X)}")
print(f"Ста-ий. ряд:    {setX}")
print(f"Абс-ые частоты: {countsX}")
print(f"Отн-ые частоты: {W}")


print("*график*")
plt.plot(setX, W)
plt.scatter(setX, W)
plt.xlabel("Xi")
plt.ylabel("Wi")
plt.grid()
plt.show()


print("*график*")


def F(setX, countsX):
    n = sum(countsX)
    F = []
    for i in range(len(setX) + 1):
        F.append(sum(countsX[:i]) / n)
    return F


F = F(setX, countsX)
setXX = sorted(setX + setX)
setXX.insert(0, setX[0] - 10000)
setXX.append(setX[-1] + 10000)
coordsX = []
i = 0
j = 1

while j <= len(F) + len(setX):
    if setXX[i] != setXX[j]:
        coordsX.append([setXX[i], setXX[j]])
    i += 1
    j += 1
coordsF = [[fx, fx] for fx in F]

for i in range(len(coordsF)):
    plt.plot(coordsX[i], coordsF[i], color='blue')
    plt.xlim(setX[0] - 0.5, setX[-1] + 0.5)

dotsX = [x[1] for x in coordsX]
dotsF = [fx[1] for fx in coordsF]
plt.scatter(dotsX, dotsF, color='blue', marker='x')
plt.grid()
plt.show()


sumX = 0
for i in range(n):
    sumX += X[i]
xV = sumX / n
sumDiff = 0
for i in range(n):
    sumDiff += (X[i] - xV) ** 2
dV = sumDiff / n
sigmaV = dV ** (0.5)
median = stat.median(sorted(X))
Vx = sigmaV / xV
print(f"Выборочное среднее:               {round(xV, 3)}")
print(f"Выборочная дисперсия:             {round(dV, 3)}")
print(f"Выборочне стандартное отклонение: {round(sigmaV, 3)}")
print(f"Выборочная медиана:               {median}")
print(f"Коэффициент вариации:             {round(Vx, 3)}")


# ВЕЩЕСТВЕННЫЕ ДАННЫЕ (рост)
X = [178.0, 182.0, 175.0, 176.0, 183.4, 176.0, 186.0, 190.0, 190.0, 185.0]
print(sorted(X))
n = len(X)
m = round(1 + m.log(n, 2))


h = (max(X) - min(X)) / m
S = [min(X) - h / 2]
for i in range(m + 1):
    S.append(S[i] + h)
I = []
i = 0
j = 1
while j < len(S):
    I.append([S[i], S[j]])
    i += 1
    j += 1
countsI = [0] * len(I)
sortX = sorted(X)
for i in range(len(I)):
    for j in range(len(X)):
        if (I[i][0] <= X[j]) and (X[j] <= I[i][1]):
            countsI[i] += 1
W = [round(ci / n, 3) for ci in countsI]
print(f"Число интервалов: {m}")
print("Интервальный ряд:")
print(f"ni {countsI}")
print(f"wi {W}")


print("*график*")
plt.hist(X, bins=S, edgecolor='black')
plt.xlabel("Выборка")
plt.ylabel("Частоты")
plt.show()


print("*график*")


def F(S, countsI):
    n = sum(countsI)
    F = []
    for i in range(len(S)):
        F.append(sum(countsI[:i]) / n)
    return F


F = F(S, countsI)
print(F)
coordsX = S
coordsX.insert(0, 0)
coordsX.append(300)
coordsF = F
coordsF.insert(0, coordsF[0])
coordsF.append(coordsF[-1])
# plt.plot(S, F)
#plt.xlim(S[1] - 0.5, S[-2] + 0.5)
for i in range(len(coordsF)):
    plt.plot(coordsX[i], coordsF[i], color='blue')
    plt.xlim(S[1] - 0.5, S[-2] + 0.5)
plt.scatter(coordsX, coordsF, color='blue', marker='x')
plt.grid()
plt.show()


sumX = 0
for i in range(n):
    sumX += X[i]
xV = sumX / n
sumDiff = 0
for i in range(n):
    sumDiff += (X[i] - xV) ** 2
dV = sumDiff / n
sigmaV = dV ** (0.5)
median = stat.median(sorted(X))
Vx = sigmaV / xV
print(f"Выборочное среднее:               {round(xV, 3)}")
print(f"Выборочная дисперсия:             {round(dV, 3)}")
print(f"Выборочне стандартное отклонение: {round(sigmaV, 3)}")
print(f"Выборочная медиана:               {median}")
print(f"Коэффициент вариации:             {round(Vx, 3)}")
