import json
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from color.ColorParser import ColorParser
from shared.Plotter import Plotter
from shared.Reader import Reader


class Window:
    def __init__(self, runSpeed, parserFileName=None, readerFileName=None):
        if parserFileName is not None:
            # file to write velocity and time data
            self.parserFile = open(parserFileName, 'w')
            self.parserWrite = True
        else:
            self.parserWrite = False

        if readerFileName is not None:
            # file to write read data
            self.readerFile = open(readerFileName, 'w')
            self.readerWrite = True
        else:
            self.readerWrite = False

        self.interactive = False
        self.readerCreated = False

        self.plotter = Plotter("Time", "Interval Velocity")

        self.cp = ColorParser()
        self.master = Tk()
        self.run = False
        self.sr = None
        self.runSpeed = runSpeed

        self.master.after(self.runSpeed, self.actions)

        # make window non resizable and set the background color
        self.master.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TButton", background="#64b3d9", font=("Segoe UI", 12))

        self.frame = ttk.Frame(self.master)
        self.frame.pack()

        # button to run and stop the program
        self.btn = ttk.Button(self.frame, text="Run")
        self.btn.grid(row=2, column=0, rowspan=5, padx=10, pady=10)
        self.btn.config(command=self.buttonHandler)
        self.btn['state'] = 'disabled'

        # button to interactively use matplot
        self.matBtn = ttk.Button(self.frame, text="Interactive")
        self.matBtn.grid(row=2, column=1, rowspan=5, padx=10, pady=10)
        self.matBtn.config(command=self.interactiveBtnHandler)

        # button to close everything
        self.closeBtn = ttk.Button(self.frame, text="Close")
        self.closeBtn.grid(row=2, column=2, rowspan=5, padx=10, pady=10)
        self.closeBtn.config(command=self.closeBtnHandler)

        # button to use serial
        self.serialBtn = ttk.Button(self.frame, text="Serial")
        self.serialBtn.grid(row=2, column=3, rowspan=5, padx=10, pady=10)
        self.serialBtn.config(command=self.serialBtnHandler)

        # button to use file
        self.fileBtn = ttk.Button(self.frame, text="File")
        self.fileBtn.grid(row=2, column=4, rowspan=5, padx=10, pady=10)
        self.fileBtn.config(command=self.fileBtnHandler)

        # label to show status
        self.statusLabel = ttk.Label(self.frame, text='Program is stopped')
        self.statusLabel.grid(row=2, column=5, padx=10, pady=10)

        # label for current speed
        ttk.Label(self.frame, text='Interval Speed').grid(row=0, column=0, padx=10, pady=10)
        self.intervalSpeedLabel = ttk.Label(self.frame, text='0 m/s')
        self.intervalSpeedLabel.grid(row=1, column=0, padx=10)

        # label for average speed
        ttk.Label(self.frame, text='Average Speed').grid(row=0, column=1, padx=10)
        self.avgSpeedLabel = ttk.Label(self.frame, text='0 m/s')
        self.avgSpeedLabel.grid(row=1, column=1, padx=10)

        # label for current time
        ttk.Label(self.frame, text='Interval Time').grid(row=0, column=2, padx=10)
        self.intervalTimeLabel = ttk.Label(self.frame, text='0 s')
        self.intervalTimeLabel.grid(row=1, column=2, padx=10)

        # label for total time
        ttk.Label(self.frame, text='Total Time').grid(row=0, column=3, padx=10)
        self.totalTimeLabel = ttk.Label(self.frame, text='0 s')
        self.totalTimeLabel.grid(row=1, column=3, padx=10)

        # label for current distance
        ttk.Label(self.frame, text='Interval Distance').grid(row=0, column=4, padx=10)
        self.intervalDistanceLabel = ttk.Label(self.frame, text='0 m')
        self.intervalDistanceLabel.grid(row=1, column=4, padx=10)

        # label for total distance
        ttk.Label(self.frame, text='Total Distance').grid(row=0, column=5, padx=10)
        self.totalDistanceLabel = ttk.Label(self.frame, text='0 m')
        self.totalDistanceLabel.grid(row=1, column=5, padx=10)

        self.master.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.master.mainloop()

    def buttonHandler(self):
        if self.btn['text'] == 'Stop':
            self.statusLabel['text'] = 'Program Stopped'
            self.btn['text'] = 'Run'
            self.run = False
        else:
            self.statusLabel['text'] = 'Reading Data'
            self.btn['text'] = 'Stop'
            self.run = True

    def interactiveBtnHandler(self):
        if self.matBtn['text'] == 'Interactive':
            self.matBtn['text'] = 'Stop Interaction'
            self.interactive = True
        else:
            self.matBtn['text'] = 'Interactive'
            self.interactive = False

    def closeBtnHandler(self):
        if self.parserWrite:
            # write to file
            self.cp.write(self.parserFile)
            self.parserFile.close()

        if self.readerWrite:
            # write to file
            self.sr.write(self.readerFile)
            self.readerFile.close()

        self.plotter.close()
        self.master.destroy()
        exit(0)

    def doneSerialBtnHandler(self):
        com = self.e1.get()
        bitRate = int(self.e2.get())
        self.root.destroy()

        self.sr = Reader(com, bitRate, False)
        self.readerCreated = True

    def serialBtnHandler(self):
        if not self.readerCreated:
            self.root = Tk()
            Label(self.root, text="Port Address: ").grid(row=0)
            Label(self.root, text="Bit Rate:").grid(row=1)

            self.e1 = Entry(self.root)
            self.e2 = Entry(self.root)

            self.e1.insert(10, "COM10")
            self.e2.insert(10, "115200")

            self.e1.grid(row=0, column=1)
            self.e2.grid(row=1, column=1)

            Button(self.root, text='Quit', command=self.root.quit).grid(row=3, column=0, sticky=W, pady=4)
            Button(self.root, text='Done', command=self.doneSerialBtnHandler).grid(row=3, column=1, sticky=W, pady=4)

        self.btn['state'] = 'enabled'
        self.serialBtn['state'] = 'disabled'
        self.fileBtn['state'] = 'disabled'

    def fileBtnHandler(self):
        if not self.readerCreated:
            fileName = askopenfilename()
            self.sr = Reader('COM11', 115200, False, fileName)
            self.readerCreated = True

        self.btn['state'] = 'enabled'
        self.serialBtn['state'] = 'disabled'
        self.fileBtn['state'] = 'disabled'

    def onClosing(self):
        self.closeBtnHandler()

    def actions(self):
        if self.run:
            data = self.sr.readJSON()

            if self.readerWrite:
                # build json from what is being read
                self.sr.build(data)

            if self.sr.eof():
                self.run = False
                self.statusLabel['text'] = "Nothing to read anymore :("
                self.plotter.plot()
            else:
                self.cp.parse(data)

                if self.cp.newDataParsed:
                    # store values
                    intVel = self.cp.getCurrIntervalVelocity('m/s')
                    intTime = self.cp.getCurrIntervalTime('s')
                    avgVel = self.cp.getAvgVelocity('m/s')
                    totalTime = self.cp.getTotalTime('s')
                    totalDistance = self.cp.getTotalDistance('m')
                    intDistance = self.cp.getCurrIntervalDistance('m')

                    # update screen labels
                    self.intervalSpeedLabel['text'] = "{0:.2f} m/s".format(intVel)
                    self.avgSpeedLabel['text'] = "{0:.2f} m/s".format(avgVel)
                    self.intervalTimeLabel['text'] = "{0:.2f} s".format(intTime)
                    self.totalTimeLabel['text'] = "{0:.2f} s".format(totalTime)
                    self.intervalDistanceLabel['text'] = "{0:.2f} m".format(intDistance)
                    self.totalDistanceLabel['text'] = "{0:.2f} m".format(totalDistance)

                    # update the plot
                    self.plotter.update(totalTime, intVel)

                    if self.parserWrite:
                        # build json string to write
                        self.cp.build()

                    if self.interactive:
                        self.plotter.plot()

        self.master.after(self.runSpeed, self.actions)
