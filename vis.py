import json
import matplotlib.pyplot as plt
import scipy.optimize as opt
import numpy as np
import statistics
import math

def exponential_fit(x, a, b, c):
  return a * np.exp(-b * x) + c

with open('data.json') as file:
  data = json.load(file)

x = []
y = []
y_mean = []

for idx,key in enumerate(data):
  x.append(int(key))
  cur_y = list(map(float, data[key]))
  y.append(cur_y)
  y_mean.append(statistics.mean(cur_y))

plt.plot(x, y, color='gray', marker='o', markersize=1, linewidth=0)
plt.plot(x, y_mean, 'r_', markersize=5)
plt.title('RSA Key Generation Runtime')
plt.xlabel('Key Size [bits]')
plt.ylabel('Generation Time [seconds]')
plt.savefig('plot.png', dpi=125)
