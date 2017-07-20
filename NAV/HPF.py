import json
import SVR
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt

with open('HPFData.json') as data_file:
    HPF = json.load(data_file)

with open('NonHPFData.json') as data_file_2:
    NHPF = json.load(data_file_2)

HPFData = HPF["allData"]
NonHPFData = NHPF["allData"]

SVRNonHPFDataJSON = SVR.SVR_process_monotype(NHPF)
SVRNonHPFData = json.loads(SVRNonHPFDataJSON)
SVRNHPFData = SVRNonHPFData["allData"]

HPFtime = list(map(lambda x:x["time"], HPFData))
NHPFtime = list(map(lambda x:x["time"], NonHPFData))
SVRNHPFtime = list(map(lambda x:x["time"], SVRNHPFData))

HPFX = list(map(lambda x:x["data"][0], HPFData))
NHPFX = list(map(lambda x:x["data"][0], NonHPFData))
SVRNHPFX = list(map(lambda x:x["data"][0], SVRNHPFData))

HPFY = list(map(lambda x:x["data"][1], HPFData))
NHPFY = list(map(lambda x:x["data"][1], NonHPFData))
SVRNHPFY = list(map(lambda x:x["data"][1], SVRNHPFData))

HPFZ = list(map(lambda x:x["data"][2], HPFData))
NHPFZ = list(map(lambda x:x["data"][2], NonHPFData))
SVRNHPFZ = list(map(lambda x:x["data"][2], SVRNHPFData))

print(SVRNHPFX[100:150])

rawx, = plt.plot(NHPFtime[100:150], NHPFX[100:150], 'r--', label='raw x-axis data')
filteredx, = plt.plot(HPFtime[100:150], HPFX[100:150], 'r', label='filtered x-axis data')
rawy, = plt.plot(NHPFtime[100:150], NHPFY[100:150], 'bs', label='raw y-axis data')
filteredy, = plt.plot(HPFtime[100:150], HPFY[100:150], 'b', label='filtered y-axis data')
rawz, = plt.plot(NHPFtime[100:150], NHPFZ[100:150], 'g^', label='raw z-axis data')
filteredz, = plt.plot(HPFtime[100:150], HPFZ[100:150], 'g', label='filtered z-axis data')
plt.legend(handles=[rawx, filteredx, rawy, filteredy, rawz, filteredz])

plt.suptitle('selected visualization of angular velocity using built-in high-pass filter', fontsize=12, fontweight='bold')
plt.xlabel('time in ms')
plt.ylabel('angular velocity in deg/s')
plt.legend()
plt.show()


xrmse = sqrt(mean_squared_error(NHPFX[100:150], SVRNHPFX[100:150]))
yrmse = sqrt(mean_squared_error(NHPFY[100:150], SVRNHPFY[100:150]))
zrmse = sqrt(mean_squared_error(NHPFZ[100:150], SVRNHPFZ[100:150]))

HPFxrmse = sqrt(mean_squared_error(NHPFX[100:150], HPFX[100:150]))
HPFyrmse = sqrt(mean_squared_error(NHPFY[100:150], HPFY[100:150]))
HPFzrmse = sqrt(mean_squared_error(NHPFZ[100:150], HPFZ[100:150]))

print("the root mean squared error for x, y, and z directional angular velocity is",xrmse, yrmse, "and", zrmse, "for support vector regression filter")
print("the root mean squared error for x, y, and z directional angular velocity is",HPFxrmse, HPFyrmse, "and", HPFzrmse, "for built-in high-pass filter")