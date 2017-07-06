import json


class ColorParser:
    def __init__(self):
        self.lastTime = 0
        self.intervalDistance = 18  # constant
        self.lastColorValue = 0
        self.totalDistance = 0
        self.currVelocity = 0
        self.avgVelocity = 0
        self.totalTime = 0
        self.intervalTime = 0
        self.firstParse = True
        self.newDataParsed = False
        self.jsonDict = {}

    @staticmethod
    def _sameOrangeColor(prevValue, currValue):
        if (prevValue == 0 or prevValue == 1) and currValue == prevValue:
            return True
        else:
            return False

    # calculates physical attributes based on data point provided
    def parse(self, data):
        try:
            if data['sensor'] == 'color':
                currTime = data['time']
                currColorValue = data['data'][0]

                # only calculate once for orange patch
                if (currColorValue == 0 or currColorValue == 1) \
                        and not self._sameOrangeColor(self.lastColorValue, currColorValue):
                    if not self.firstParse:
                        self.intervalTime = currTime - self.lastTime

                        # calculate velocity and other attributes
                        self.currVelocity = self.intervalDistance / self.intervalTime
                        self.totalDistance += self.intervalDistance
                        self.totalTime += self.intervalTime
                        self.avgVelocity = self.totalDistance / self.totalTime
                    else:
                        self.firstParse = False

                    self.lastTime = currTime
                    self.lastColorValue = currColorValue
                    self.newDataParsed = True
                else:
                    self.lastColorValue = currColorValue
                    self.newDataParsed = False
        except:
            return

    # build the json object so that it can be written
    def build(self, unitVel='m/s', unitDist='m', unitTime='s'):
        if self.jsonDict == {}:
            self.jsonDict = {"allData": []}

        data = {'intVel': self.getCurrIntervalVelocity(unitVel), 'avgVel': self.getAvgVelocity(unitVel),
                'intTime': self.getCurrIntervalTime(unitTime), 'totalTime': self.getTotalTime(unitTime),
                'intDistance': self.getCurrIntervalDistance(unitDist),
                'totalDistance': self.getTotalDistance(unitDist)}

        self.jsonDict['allData'].append(data)

    # write the json object to the file
    def write(self, file):
        file.write(json.dumps(self.jsonDict))

    # returns velocity between recent orange blocks. Supports cm/ms, m/s and cm/s
    def getCurrIntervalVelocity(self, unit='m/s'):
        if unit == 'm/s':
            return self.currVelocity * 10
        elif unit == 'cm/s':
            return self.currVelocity / 100
        else:
            return self.currVelocity

    # returns time passed between recent orange blocks. Supports ms and s
    def getCurrIntervalTime(self, unit='s'):
        if unit == 's':
            return self.intervalTime / 1000
        else:
            return self.intervalTime

    # returns distance between two orange blocks. Supports cm and m. This is a constant
    def getCurrIntervalDistance(self, unit='m'):
        if unit == 'm':
            return self.intervalDistance / 100
        else:
            return self.intervalDistance

    # returns total distance that a pod has covered based on orange stripes distance. Supports cm and m
    def getTotalDistance(self, unit='m'):
        if unit == 'm':
            return self.totalDistance / 100
        else:
            return self.totalDistance

    # returns total time that has been passed while the pod is moving. Supports ms and s
    def getTotalTime(self, unit='s'):
        if unit == 's':
            return self.totalTime / 1000
        else:
            return self.totalTime

    # returns the average velocity of the pod. Supports cm/ms, m/s and cm/s
    def getAvgVelocity(self, unit='m/s'):
        if unit == 'm/s':
            return self.avgVelocity * 10
        elif unit == 'cm/s':
            return self.avgVelocity / 100
        else:
            return self.avgVelocity

    # returns true or false based on if new data was processed or not on the previous call to parse
    def newDataParsed(self):
        return self.newDataParsed
