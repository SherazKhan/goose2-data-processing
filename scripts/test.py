import random
import time as t
## subroutine for simulation using a uniform PRNG
def generateMockData(a, b, iters, array):
    count = 0
    while (count < iters):
        array.append(random.uniform(a, b))
        count += 1
    return array

mockX = []
mockY = []
mockZ = []
mockX = generateMockData(0, 1, 1000, mockX)
mockY = generateMockData(2, 3, 1000, mockY)
mockZ = generateMockData(1, 2, 1000, mockZ)


mockJSONArray = []

f = open('FakeData.tsv', 'w')
f.write("Time X Y Z\n")
for i in range(1000):
    time = t.clock()
    f.write(str(time) + ' ' + str(mockX[i]) + ' ' + str(mockY[i]) + ' ' + str(mockZ[i]) + '\n')

# processedData = {}
# processedData = denoise.processMonotype(denoise.parseMonotype(mockJSONArray))
# print(processedData)
#
# for j in range(3):
#     plt.plot(processedData["Gyro"][j])
