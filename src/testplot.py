import matplotlib.pyplot as plt
import numpy as np
import pickle

fig, ax = plt.subplots(1, 1)

x = np.arange(-np.pi, np.pi, 0.01)
y = np.tan(x)
ax.plot(x, y)

pickle.dump((fig, ax), open("myplot.pkl", "wb"))

plt.show()