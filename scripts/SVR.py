# Curve Smoothing with Support Vector Regression using Radial Basis Function (RBF) kernel
# Written by Rosie Zou, June 2017

# syntax for calling the support vector regression function
#     SVR(kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001,
#         C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1)

# Sample data input format:
# {"time":1009,"sensor":"gyro","data":[-1.54875,12.19750,11.36625]}
import numpy as np
from sklearn.svm import SVR
import timeit
import json
import matplotlib.pyplot as plt

start = timeit.default_timer()


def SVR_process_monotype(JSONArray):
    DataType = JSONArray[0]["sensor"]
    size = len(JSONArray)
    x = []
    y = []
    z = []
    t = []
    for count in range(size):
        x.append(JSONArray[count]["data"][0])
        y.append(JSONArray[count]["data"][1])
        z.append(JSONArray[count]["data"][2])
        t.append([JSONArray[count]["time"]])

    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1, verbose=False)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    x_rbf = svr_rbf.fit(t, x).predict(t)
    y_rbf = svr_rbf.fit(t, y).predict(t)
    z_rbf = svr_rbf.fit(t, z).predict(t)
    returnJSONArray = []
    count = 0
    while count < size:
        returnJSONArray.append({"time": t[count][0], "sensor": DataType, "data": [x_rbf[count], y_rbf[count], z_rbf[count]]})
        count += 1

    # red for x, blue for y and green for z
    plt.plot(t, x_rbf, 'r', t, y_rbf, 'b', t, z_rbf, 'g', t, x, 'r--', t, y, 'bs', t, z, 'g^', lw = 2)
    plt.show()

    return returnJSONArray

stop = timeit.default_timer()

print(stop - start)


## DEMO

DemoData = []
for i in range(50):
    i += 1
    DemoData.append({"time": i, "sensor": "gyro", "data": [np.random.uniform(0, i), np.random.chisquare(i), np.random.binomial(50, (float)(i/(i+1)))]})

SVR_process_monotype(DemoData)
