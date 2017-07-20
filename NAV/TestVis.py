import json
import ast
import NAV
import matplotlib.pyplot as plt

with open('10_6_2017_15_55_55_22.json') as data_file:
    set1 = json.load(data_file)

count = 0
arrLen = len(set1)
set1DictList = []

while count < arrLen:
    listEntry = {}
    listEntry["val"] = ast.literal_eval(set1[count]["val"])
    set1DictList.append(listEntry)
    count += 1
set1ProcessedJSON = NAV.SVR_process_monotypeAlt(set1DictList)

## [{'val': {'sensor': 'accel', 'time': 1726, 'data': [0.037271, 0.295118, 0.99674, -89.999428, 9.539576e-06, 188.580017]}}, ...]
rawTime = list(map(lambda x:x["val"]["time"], set1DictList))
rawDataX = list(map(lambda x:x["val"]["data"][0], set1DictList))
rawDataY = list(map(lambda x:x["val"]["data"][1], set1DictList))
rawDataZ = list(map(lambda x:x["val"]["data"][2]*-1, set1DictList))

processed = json.loads(set1ProcessedJSON)
processedData = processed["allData"]
processedTime = list(map(lambda x:x["time"], processedData))
processedX = list(map(lambda x:x["data"][0], processedData))
processedY = list(map(lambda x:x["data"][1], processedData))
processedZ = list(map(lambda x:x["data"][2]*-1, processedData))

# velocity1ProcessedJSON = NAV.calcLinearVelocity(processed)
displacementProcessedJSON = NAV.calcLinearDisplacement(processed)
print(displacementProcessedJSON)
# raw, = plt.plot(rawTime[:300], rawDataZ[:300], 'g^', label='raw data')
# filtered, = plt.plot(rawTime[:300], processedZ[:300], 'g', label='filtered data')
# plt.legend(handles=[raw, filtered])
#
# plt.suptitle('selected visualization of vertical vibration', fontsize=12, fontweight='bold')
# plt.xlabel('time in ms')
# plt.ylabel('acceleration in g')
# plt.legend()
# plt.show()