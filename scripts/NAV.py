# Script for navigation system with functions for position calculations
# Written by Rosie Zou, June 2017

import SVR as SVR
import math
import numpy as np
import matplotlib.pyplot as plt

## All functions take inputs in the following format:
#    [{"time":1009,"sensor":"gyro","data":[-1.54875,12.19750,11.36625]},
#     {"time":1009,"sensor":"gyro","data":[-1.54875,12.19750,11.36625]},...]
# (exactly the same format as the SVR.py output)

## All functions return dictionaries with 4 entries:
#     keys: x, y, z, time
#     values: arrays of time-series values

def calcLinearVelocityAlt(ACCELArray):
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

        xVel.append(0)
        yVel.append(0)
        zVel.append(0)
        count = 1
        while count < size:
            xVel.append((float)((x[count]-x[count-1])*(t[count] - t[count-1])))
            yVel.append((float)((y[count] - y[count - 1]) * (t[count] - t[count - 1])))
            zVel.append((float)((z[count] - z[count - 1]) * (t[count] - t[count - 1])))
            count += 1
        returnArray["time"] = t
        returnArray["xVelocity"] = xVel
        returnArray["yVelocity"] = yVel
        returnArray["zVelocity"] = zVel
        return returnArray

def outputRowPitchYaw(GYROArray):
    DataType = GYROArray[0]["sensor"]
    returnArray = {}
    if DataType != "gyro":
        return "Gyroscope readings required"
    else:
        size = len(GYROArray)
        row = []
        pitch = []
        yaw = []
        time = []
        for count in range(size):
            row.append((float)(GYROArray[count]["data"][0]/180))
            pitch.append((float)(GYROArray[count]["data"][1] / 180))
            yaw.append((float)(GYROArray[count]["data"][2] / 180))
            time.append((float)(GYROArray[count]["time"]))
        returnArray["time"] = time
        returnArray["row"] = row
        returnArray["pitch"] = pitch
        returnArray["yaw"] = yaw
        return returnArray

def calcAngularVelocity(ACCELArray, GYROArray):
    ## 3 feet tall, 2 feet wide (approximately)
    linVelocity = calcLinearVelocity(ACCELArray)
    rotation = outputRowPitchYaw(GYROArray)
    height = 0.4572
    width = 0.3048
    xVel = linVelocity["xVelocity"]
    yVel = linVelocity["yVelocity"]
    zVel = linVelocity["zVelocity"]
    xRot = rotation["row"]
    yRot = rotation["pitch"]
    zRot = rotation["yaw"]
    xAng = []
    yAng = []
    zAng = []
    xAng.append(0)
    yAng.append(0)
    zAng.append(0)
    count = 1
    size = len(xVel)
    returnArray = {}

    while count < size:
        xRad = (height * width) / math.sqrt(
            width * width * math.sin(xRot[count]) + height * height * math.sin(xRot[count]))
        yRad = (height * width) / math.sqrt(
            width * width * math.sin(yRot[count]) + height * height * math.sin(yRot[count]))
        zRad = (height * width) / math.sqrt(
            width * width * math.sin(zRot[count]) + height * height * math.sin(zRot[count]))
        xAng.append(xVel[count]/xRad)
        yAng.append(yVel[count]/yRad)
        zAng.append(zVel[count]/zRad)
        count += 1

    returnArray["time"] = GYROArray["time"]
    returnArray["xAngular"] = xAng
    returnArray["yAngular"] = yAng
    returnArray["zAngular"] = zAng
    return returnArray


def Optical(OptJSON):
    velocity = OptJSON["allData"]
    
    return


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