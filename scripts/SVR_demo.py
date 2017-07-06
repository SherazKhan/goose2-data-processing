# Curve Smoothing with Support Vector Regression using Radial Basis Function (RBF) kernel
# SVR(kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1)
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import timeit

start = timeit.default_timer()


# Generate sample data
X = np.sort(5 * np.random.rand(40, 1), axis=0)
print(X)
y = np.sin(X).ravel()
print(y)

# Add noise to targets
y[::5] += 3 * (0.5 - np.random.rand(8))
print(len(y))
# Fit regression model
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1, verbose=False)
y_rbf = svr_rbf.fit(X, y).predict(X)

# look at the results
lw = 2
plt.scatter(X, y, color='darkorange', label='data')
plt.hold('on')
plt.plot(X, y_rbf, color='navy', lw=lw, label='RBF model')
# plt.plot(X, y_lin, color='c', lw=lw, label='Linear model')
# plt.plot(X, y_poly, color='cornflowerblue', lw=lw, label='Polynomial model')
plt.xlabel('data')
plt.ylabel('target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()

# Total running time of the script: (0 minutes 0.769 seconds)

stop = timeit.default_timer()

print(stop - start)