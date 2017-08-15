import serial
import time
import matplotlib.pyplot as plt
import numpy as np

plt.ion()

x = list()
y = list()
t = 1
hour_list = list()
plt.figure()
while True:
    hora = time.strftime("%H:%M:%S", time.localtime())
    hour_list.append(hora)
    x.append(t)
    y.append(t)
    t = t + 1
    plt.xticks(x, hour_list)
    plt.scatter(x, y)
    plt.pause(1)