# Script for navigation system with functions for position calculations
# Written by Rosie Zou, June 2017

import numpy as np
from sklearn.svm import SVR
import timeit
import matplotlib.pyplot as plt
import sys
import json

start = timeit.default_timer()


def SVR_process_monotype(JSONArray):
    DataType = JSONArray["allData"][0]["sensor"]
    size = len(JSONArray["allData"])
    x = []
    y = []
    z = []
    t = []
    for count in range(size):
        x.append(JSONArray["allData"][count]["data"][0])
        y.append(JSONArray["allData"][count]["data"][1])
        z.append(JSONArray["allData"][count]["data"][2])
        t.append([JSONArray["allData"][count]["time"]])

    svr_rbf = SVR(kernel='rbf', C=1.45e2, gamma=0.2, verbose=False)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    x_rbf = svr_rbf.fit(t, x).predict(t)
    y_rbf = svr_rbf.fit(t, y).predict(t)
    z_rbf = svr_rbf.fit(t, z).predict(t)
    returnJSONArray = {}
    returnJSONArray["allData"] = []
    count = 0
    while count < size:
        returnJSONArray["allData"].append({"time": t[count][0], "sensor": DataType, "data": [x_rbf[count], y_rbf[count], z_rbf[count]]})
        count += 1
    returnJSONObject = json.dumps(returnJSONArray)
    print(returnJSONObject)
    sys.stdout.flush()
    return returnJSONObject


def SVR_process_monotypeAlt(JSONArray):
    DataType = JSONArray[0]["val"]["sensor"]
    size = len(JSONArray)
    x = []
    y = []
    z = []
    t = []
    for count in range(size):
        x.append(JSONArray[count]['val']["data"][0])
        y.append(JSONArray[count]['val']["data"][1])
        z.append(JSONArray[count]['val']["data"][2])
        t.append([JSONArray[count]['val']["time"]])

    svr_rbf = SVR(kernel='rbf', C=0.2e2, gamma=0.2, verbose=False)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    x_rbf = svr_rbf.fit(t, x).predict(t)
    y_rbf = svr_rbf.fit(t, y).predict(t)
    z_rbf = svr_rbf.fit(t, z).predict(t)
    returnJSONArray = {}
    returnJSONArray["allData"] = []
    count = 0
    while count < size:
        returnJSONArray["allData"].append({"time": t[count][0], "sensor": DataType, "data": [x_rbf[count], y_rbf[count], z_rbf[count]]})
        count += 1

    # red for x, blue for y and green for z
    # plt.plot(t, x_rbf, 'r', t, y_rbf, 'b', t, z_rbf, 'g', t, x, 'r--', t, y, 'bs', t, z, 'g^', lw = 2)
    # plt.show()
    returnJSONObject = json.dumps(returnJSONArray)
    print(returnJSONObject)
    sys.stdout.flush()
    return returnJSONObject

def calcLinearVelocity(ACCELArray):
    DataType = ACCELArray["allData"][0]["sensor"]
    returnArray = {}
    if DataType != "accel":
        return "Accelerometer readings required"
    else:
        size = len(ACCELArray["allData"])
        print(size)
        x = []
        y = []
        z = []
        t = []
        xVel = []
        yVel = []
        zVel = []
        for count in range(size):
            x.append(ACCELArray["allData"][count]["data"][0]*9.80665)
            y.append(ACCELArray["allData"][count]["data"][1]*9.80665)
            z.append(ACCELArray["allData"][count]["data"][2]*9.80665)
            t.append((float)(ACCELArray["allData"][count]["time"]/1000))

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
        # plt.plot(t[:300], zVel[:300], 'g')
        # plt.suptitle('selected visualization of vertical vibration', fontsize=12, fontweight='bold')
        # plt.xlabel('time in s')
        # plt.ylabel('velocity in m/s')
        # plt.show()
        print(returnArray)
        sys.stdout.flush()
        return returnArray

def calcLinearDisplacement(ACCELArray):
    DataType = ACCELArray["allData"][0]["sensor"]
    returnArray = {}
    if DataType != "accel":
        return "Accelerometer readings required"
    else:
        velocity = calcLinearVelocity(ACCELArray)
        size = len(velocity["time"])
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
        # print(len(zDisp))
        # plt.plot(time[:300], zDisp[:300], 'g-')
        # plt.suptitle('selected visualization of vertical vibration', fontsize=12, fontweight='bold')
        # plt.xlabel('time in s')
        # plt.ylabel('displacement in m')
        # plt.show()
        # print(returnArray)
        # sys.stdout.flush()
        return returnArray

def outputRowPitchYaw(ACCELArray, MAGArray):
    DataType = ACCELArray["allData"][0]["sensor"]
    returnArray = {}
    if DataType != "accel":
        return "Accelerometer readings required"
    elif MAGArray["allData"][0]["sensor"] != "mag":
        return "Magnetometer readings required"
    else:
        size = len(ACCELArray)
        row = []
        pitch = []
        yaw = []
        time = []
        for count in range(size):
            r = (float)(ACCELArray[count]["data"][3]/180)
            p = (float)(ACCELArray[count]["data"][4]/180)
            xm = MAGArray[count]["data"][0]
            ym = MAGArray[count]["data"][1]
            zm = MAGArray[count]["data"][2]
            row.append(r)
            pitch.append(p)
            yaw.append(calcYaw(r, p, xm, ym, zm))
            time.append((float)(ACCELArray[count]["time"]))
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


# yaw = atan2( (-ymag*cos(Roll) + zmag*sin(Roll) ) , (xmag*cos(Pitch) + ymag*sin(Pitch)*sin(Roll)+ zmag*sin(Pitch)*cos(Roll)) )
def calcYaw(roll, pitch, xmag, ymag, zmag):
    arg1 = -1 * ymag * np.cos(roll) + zmag * np.sin(roll)
    arg2 = xmag * np.cos(pitch) + ymag * np.sin(pitch) * np.sin*(roll) + zmag * np.sin(pitch) * np.cos(roll)
    return np.arctan2(arg1, arg2)


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


stop = timeit.default_timer()
#
# class SimpleEcho(WebSocket):
#
#     def handleMessage(self):
#         # echo message back to client
#         self.sendMessage(self.data)
#
#     def handleConnected(self):
#         print(self.address, 'connected')
#
#     def handleClose(self):
#         print(self.address, 'closed')
#
# server = SimpleWebSocketServer('', 8000, SimpleEcho)
# server.serveforever()

print(stop - start)

# longitude acceleration +-2g
# lateral acceleration +- 1g
# vertical acceleration +- 1g
