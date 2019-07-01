import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


X, Y = np.meshgrid(np.arange(0,200,1), np.arange(0,200,1))

# get 2D z data
Z = np.loadtxt("a.csv", delimiter=",")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z)

plt.show()