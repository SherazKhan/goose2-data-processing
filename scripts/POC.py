import sys
import os
sys.path.append(os.path.abspath("/Users/rosiezou/PycharmProjects/NoiseReduction/"))
import SVR as SVR
import NAV as NAV
import numpy as np
import timeit

start = timeit.default_timer()

JSONArray = []
## {"time":1009,"sensor":"gyro","data":[-1.54875,12.19750,11.36625]}
time = []
for i in range(100):
    time.append(i)

accelRawX = []
accelRawY = []
accelRawZ = []

for j in range(100):
    accelRawX.append(time[j] * 1)
    accelRawY.append(time[j] * 2)
    accelRawZ.append(time[j] * 3)
    accelRawX[j] += 0.001 * (np.random.uniform(1, 5))
    accelRawY[j] += 0.001 * (np.random.uniform(1, 5))
    accelRawZ[j] += 0.001 * (np.random.uniform(1, 5))


for k in range(100):
    JSONentry = {}
    JSONentry["time"] = time[k]
    JSONentry["sensor"] = "accelerometer"
    JSONentry["data"] = [accelRawX[k],accelRawY[k],accelRawZ[k]]
    JSONArray.append(JSONentry)

print(JSONArray)
accelArray = SVR.SVR_process_monotype(JSONArray)
NAV.calcLinearVelocityAlt(accelArray)
NAV.calcLinearDisplacementAlt(accelArray)

stop = timeit.default_timer()

print("Total processing time:")
print(stop - start)