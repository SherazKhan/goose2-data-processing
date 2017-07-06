# Script for navigation system with functions for position calculations
# Written by Rosie Zou, June 2017

import SVR as SVR
import numpy as np
import matplotlib.pyplot as plt

## All functions take inputs in the following format:
#    [{"time":1009,"sensor":"gyro","data":[-1.54875,12.19750,11.36625]},
#     {"time":1009,"sensor":"gyro","data":[-1.54875,12.19750,11.36625]},...]
# (exactly the same format as the SVR.py output)

## All functions return dictionaries with 4 entries:
#     keys: x, y, z, time
#     values: arrays of time-series values

def calcLinearVelocity(ACCELArray):
    DataType = ACCELArray[0]["sensor"]
    returnArray = {}
    if DataType != "accelerometer":
        return "Accelerometer readings required"
    else:
        size = len(ACCELArray)
        x = []
        y = []
        z = []
        t = []
        xVel = []
        yVel = []
        zVel = []
        for count in range(size):
            x.append(ACCELArray[count]["data"][0]*9.80665)
            y.append(ACCELArray[count]["data"][1]*9.80665)
            z.append(ACCELArray[count]["data"][2]*9.80665)
            t.append(ACCELArray[count]["time"])

        LowerBound = 0
        UpperBound = LowerBound + 2
        while UpperBound < size:
            xVel.append(np.trapz(t[LowerBound:UpperBound], x[LowerBound:UpperBound]))
            yVel.append(np.trapz(t[LowerBound:UpperBound], y[LowerBound:UpperBound]))
            zVel.append(np.trapz(t[LowerBound:UpperBound], z[LowerBound:UpperBound]))
            LowerBound += 1
            UpperBound = LowerBound + 2
        print(len(xVel))
        plt.plot(t[2:], xVel, 'r', t[2:], yVel, 'b', t[2:], zVel, 'g', lw=2)
        plt.show()

        returnArray["time"] = t
        returnArray["xVelocity"] = xVel
        returnArray["yVelocity"] = yVel
        returnArray["zVelocity"] = zVel

    print(returnArray)
    return returnArray

## AngularVelocity = LinearVelocity/AngleInRPM(Radian)
##     x/y/z gyro data in +/- 245 degrees
def calcAngularVelocity(ACCELArray, GYROArray):
    velocities = calcLinearVelocity(ACCELArray)
    xVel = velocities["xVelocity"]
    yVel = velocities["yVelocity"]
    zVel = velocities["zVelocity"]
    returnArray = {}
    if (GYROArray[0]["sensor"] != "gyro"):
        return "Gyroscope data needed"
    else:
        size = len(GYROArray)
        x = []
        y = []
        z = []
        t = []
        for count in range(size):
            x.append(GYROArray[count]["data"][0])
            y.append(GYROArray[count]["data"][1])
            z.append(GYROArray[count]["data"][2])
            t.append(GYROArray[count]["time"])

        map(lambda x: (float)(x / 180), x)
        map(lambda x: (float)(x / 180), y)
        map(lambda x: (float)(x / 180), z)

        for i in range(size):
            xVel[i] = (float)(xVel[i]/x[i])
            yVel[i] = (float)(yVel[i]/y[i])
            zVel[i] = (float)(zVel[i]/z[i])

        returnArray["time"] = t
        returnArray["xAngVelocity"] = xVel
        returnArray["yAngVelocity"] = yVel
        returnArray["zAngVelocity"] = zVel
        plt.plot(t[2:], xVel, 'r', t[2:], yVel, 'b', t[2:], zVel, 'g', lw=2)
        plt.show()
        print(returnArray)
        return returnArray
    # loop through the velocity arrays and divide by radian

#
# longitude acceleration +-2g
# lateral acceleration +- 1g
# vertical acceleration +- 1g
#
def calcLinearDisplacement(ACCELArray):
    velocities = calcLinearVelocity(ACCELArray)
    xVel = velocities["xVelocity"]
    yVel = velocities["yVelocity"]
    zVel = velocities["zVelocity"]
    times = velocities["time"]
    xDisp = []
    yDisp = []
    zDisp = []
    retval = {}
    size = len(xVel)
    LowerBound = 0
    UpperBound = LowerBound + 2
    while UpperBound < size:
        xDisp.append(np.trapz(times[LowerBound:UpperBound], xVel[LowerBound:UpperBound]))
        yDisp.append(np.trapz(times[LowerBound:UpperBound], yVel[LowerBound:UpperBound]))
        zDisp.append(np.trapz(times[LowerBound:UpperBound], zVel[LowerBound:UpperBound]))
        LowerBound += 1
        UpperBound = LowerBound + 2
    plt.plot(times[4:], xDisp, 'r', times[4:], yDisp, 'b', times[4:], zDisp, 'g', lw=2)
    plt.show()

    retval["xDisplacement"] = xDisp
    retval["yDisplacement"] = yDisp
    retval["zDisplacement"] = zDisp
    retval["times"] = times
    return retval

def calcAngularDisplacement(ACCELArray, GYROArray):
    displacement = calcLinearDisplacement(ACCELArray)
    xDisp = displacement["xDisplacement"]
    yDisp = displacement["yDisplacement"]
    zDisp = displacement["zDisplacement"]
    returnArray = {}
    if (GYROArray[0]["sensor"] != "gyro"):
        return "Gyroscope data needed"
    else:
        size = len(GYROArray)
        x = []
        y = []
        z = []
        t = []
        for count in range(size):
            x.append(GYROArray[count]["data"][0])
            y.append(GYROArray[count]["data"][1])
            z.append(GYROArray[count]["data"][2])
            t.append(GYROArray[count]["time"])

        map(lambda x: (float)(x / 180), x)
        map(lambda x: (float)(x / 180), y)
        map(lambda x: (float)(x / 180), z)

        for i in range(size):
            xDisp[i] = (float)(xDisp[i]/x[i])
            yDisp[i] = (float)(yDisp[i]/y[i])
            zDisp[i] = (float)(zDisp[i]/z[i])

        returnArray["time"] = t
        returnArray["xAngDisplacement"] = xDisp
        returnArray["yAngDisplacement"] = yDisp
        returnArray["zAngDisplacement"] = zDisp

        print(returnArray)
        return returnArray


def Optical(arrData):
    count = len(arrData)
    Displacement = []
    Time = []
    Velocity = []
    for i in range(count):
        Displacement.append(arrData["data"][0])
        Time.append(arrData["time"])
        if i == 0:
            Velocity.append(0)
        else:
            Velocity.append((float)((Displacement[i]-Displacement[i-1])/(Time[i]-Time[i-1])))
    return



# DemoData = []
# for i in range(50):
#     i += 1
#     DemoData.append({"time": i, "sensor": "accelerometer", "data": [np.random.uniform(0, i), np.random.chisquare(i), np.random.binomial(50, (float)(i/(i+1)))]})
# #
# # DemoData2 = []
# # for i in range(50):
# #     i += 1
# #     DemoData.append({"time": i, "sensor": "gyro", "data": [np.random.uniform(0, i), np.random.chisquare(i), np.random.binomial(50, (float)(i/(i+1)))]})
# #
#
# calcLinearDisplacement(SVR.SVR_process_monotype(DemoData))

# calcAngularVelocity(SVR.SVR_process_monotype(DemoData), SVR.SVR_process_monotype(DemoData2))