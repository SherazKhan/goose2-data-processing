# Script for navigation system with functions for position calculations
# Written by Rosie Zou, June 2017

import matplotlib.pyplot as plt
import sys

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

        xVel.append(0)
        yVel.append(0)
        zVel.append(0)
        count = 1
        while count < size:
            xVel.append((float)((x[count] - x[count - 1]) * (t[count] - t[count - 1])))
            yVel.append((float)((y[count] - y[count - 1]) * (t[count] - t[count - 1])))
            zVel.append((float)((z[count] - z[count - 1]) * (t[count] - t[count - 1])))
            count += 1
        returnArray["time"] = t
        returnArray["xVelocity"] = xVel
        returnArray["yVelocity"] = yVel
        returnArray["zVelocity"] = zVel
        plt.plot(t, xVel, 'r', t, yVel, 'b', t, zVel, 'g')
        plt.show()
        print(returnArray)
        sys.stdout.flush()

def calcLinearDisplacement(ACCELArray):
    DataType = ACCELArray[0]["sensor"]
    returnArray = {}
    if DataType != "accelerometer":
        return "Accelerometer readings required"
    else:
        velocity = calcLinearVelocity(ACCELArray)
        size = len(ACCELArray)
        xVel = velocity["xVelocity"]
        yVel = velocity["yVelocity"]
        zVel = velocity["zVelocity"]
        time = velocity["time"]
        xDisp = []
        yDisp = []
        zDisp = []

        xDisp.append(0)
        yDisp.append(0)
        zDisp.append(0)
        count = 1
        while count < size:
            xDisp.append((float)((xVel[count]-xVel[count-1])*(time[count] - time[count-1])) + xDisp[count-1])
            yDisp.append((float)((yVel[count]-yVel[count-1])*(time[count] - time[count-1])) + yDisp[count-1])
            zDisp.append((float)((zVel[count]-zVel[count-1])*(time[count] - time[count-1])) + zDisp[count-1])
            count += 1
        returnArray["time"] = time
        returnArray["xDisplacement"] = xDisp
        returnArray["yDisplacement"] = yDisp
        returnArray["zDisplacement"] = zDisp
        plt.plot(time, xDisp, 'r--', time, yDisp, 'b^', time, zDisp, 'g-')
        plt.show()
        print(returnArray)
        sys.stdout.flush()

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
            row.append((float)(GYROArray[count]["data"][3]/180))
            pitch.append((float)(GYROArray[count]["data"][4] / 180))
            yaw.append((float)(GYROArray[count]["data"][5] / 180))
            time.append((float)(GYROArray[count]["time"]))
        returnArray["time"] = time
        returnArray["row"] = row
        returnArray["pitch"] = pitch
        returnArray["yaw"] = yaw
        print(returnArray)
        sys.stdout.flush()

def calcAngularVelocity(GYROArray):
    xAng = []
    yAng = []
    zAng = []
    time = []
    returnArray = {}
    if GYROArray[0]["sensor"] != "gyro":
        return "Gyroscope readings required"
    else:
        size = len(GYROArray)
        for count in range(size):
            xAng.append((float)(GYROArray[count]["data"][0] / 180))
            yAng.append((float)(GYROArray[count]["data"][1] / 180))
            zAng.append((float)(GYROArray[count]["data"][2] / 180))
            time.append((float)(GYROArray[count]["time"]))
        returnArray["time"] = time
        returnArray["xAngular"] = xAng
        returnArray["yAngular"] = yAng
        returnArray["zAngular"] = zAng
    print(returnArray)
    sys.stdout.flush()


def Optical(OptJSON):
    data = OptJSON["allData"]
    time = []
    timeCumulative = []
    displacement = []
    displacementCumulative = []
    velocity = []
    timeCumulative.append(0)
    time.append(data[0]["intTime"])
    displacement.append(0)
    displacementCumulative.append(0)
    velocity.append(0)
    size = len(data)
    count = 1
    while count < size:
        time.append(data[count]["intTime"])
        timeCumulative.append(time[count] + time[count-1])
        displacement.append(displacement[count-1] + 30.58158984)
        displacementCumulative.append(displacement[count] + displacement[count-1])
        velocity.append((displacement[count]-displacement[count-1])/(time[count]))
        count += 1
    returnArray = {}
    returnArray["time"] = timeCumulative
    returnArray["displacement"] = displacement
    returnArray["velocity"] = velocity
    print(returnArray)
    sys.stdout.flush()

#
# longitude acceleration +-2g
# lateral acceleration +- 1g
# vertical acceleration +- 1g
