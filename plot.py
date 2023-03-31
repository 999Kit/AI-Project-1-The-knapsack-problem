import numpy as np
import matplotlib.pyplot as plt
import collections

plt.rcParams["figure.autolayout"] = True

x = np.loadtxt("data.bin")
y = np.array([i for i in range(len(x))])
plt.subplot(1, 2, 1)
plt.plot(x, 'r.')
# x.sort()
frequency = dict(collections.Counter(x))
names = list(frequency.keys())
names.sort()
values = [frequency[i] for i in names]
plt.subplot(1, 2, 2)
# plt.bar(range(len(frequency)), values, tick_label=names)
# x.sort()
plt.plot(names, values)
plt.show()