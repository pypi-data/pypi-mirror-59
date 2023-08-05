"""
=============================
VFI Decision Regions
=============================

In this plot we can compare the decision regions among a VFI classifier against a CART, a Kernel SV model and a 3NN classifier.
"""

print(__doc__)

from itertools import product

import numpy as np
import matplotlib.pyplot as plt

import vfi
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier

# Loading some example data
iris = datasets.load_iris()
X = iris.data[:, [0, 2]]
y = iris.target

# Training classifiers
vfi = vfi.VFI()
clf1 = DecisionTreeClassifier(random_state=0)
clf2 = KNeighborsClassifier(n_neighbors=3)
clf3 = GaussianNB()


clf1.fit(X, y)
clf2.fit(X, y)
clf3.fit(X, y)
vfi.fit(X, y)

# Plotting decision regions
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))

f, axarr = plt.subplots(2, 2, sharex="col", sharey="row", figsize=(10, 8))

for idx, clf, tt in zip(
    product([0, 1], [0, 1]),
    [vfi, clf1, clf2, clf3],
    ["VFI", "Decision Tree", "KNN (k=3)", "Naive Bayes"],
):

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    axarr[idx[0], idx[1]].contourf(xx, yy, Z, alpha=0.4)
    axarr[idx[0], idx[1]].scatter(X[:, 0], X[:, 1], c=y, s=20, edgecolor="k")
    axarr[idx[0], idx[1]].set_title(tt)

plt.show()
