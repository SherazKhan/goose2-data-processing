import json

import serial


class Reader:
    # this supports both Serial reading and file reading. It has the ability to display logs to
    # console by passing True for showLogs Param
    # 1) To use Serial reading, just give first 2 params values
    # 2) To use File reading, give whatever for first 3 params and give a file name for the 4th param
    def __init__(self, port, baud, showLogs=False, fileName=None):
        self.showLogs = showLogs
        self.jsonDict = {}

        # we will use file reading
        if fileName is not None:
            try:
                self.useFile = True
                self.counter = 0

                with open(fileName) as json_data:
                    self.jsonData = json.load(json_data)

                for key in self.jsonData:
                    self.content = self.jsonData[key]

                self.fileLength = len(self.content)
            except:
                if showLogs:
                    print("Stuff went wrong")
        else:
            # for Serial reading
            self.useFile = False
            self.ser = serial.Serial(port, baud, timeout=1)
            self.port = port
            self.baud = baud

    # build a json object that will be written
    def build(self, data):
        if self.jsonDict == {}:
            self.jsonDict = {"allData": []}

        if data is None:
            return

        self.jsonDict['allData'].append(data)

    # write the json object that has been created
    def write(self, file=None):
        try:
            file.write(json.dumps(self.jsonDict))

            if self.showLogs:
                print("Write Successful: ")
        except:
            if self.showLogs:
                print("Error detected!")

    # returns JSON dict for the line read
    def readJSON(self):
        try:
            if self.useFile:
                data = self.content[self.counter]
                print(data)
                self.counter += 1
                return data
            else:
                dict = json.loads(str(self.ser.readline(), 'utf-8').rstrip())
                return dict
        except:
            return None

    # checks if there is eof always check this before reading
    def eof(self):
        if not self.useFile:
            return False

        if self.counter >= self.fileLength:
            return True
        else:
            return False
