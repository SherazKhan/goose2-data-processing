import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, xLabel, yLabel, grid=True, lines=True):
        self.lines = lines
        self.grid = grid
        self.xLabel = xLabel
        self.yLabel = yLabel

        self.xList = []
        self.yList = []

        plt.ion()
        self.fig = plt.figure(1)

        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.grid(grid)
        self.ax1.set_xlabel(xLabel)
        self.ax1.set_ylabel(yLabel)

    def update(self, xValue, yValue):
        self.xList.append(xValue)
        self.yList.append(yValue)

    def plot(self):
        if not plt.fignum_exists(1):
            return

        self.ax1.clear()

        if self.lines:
            self.ax1.plot(self.xList, self.yList)
        else:
            self.ax1.plot(self.xList, self.yList, 'ro')

        self.ax1.grid(self.grid)
        self.ax1.set_xlabel(self.xLabel)
        self.ax1.set_ylabel(self.yLabel)

    @staticmethod
    def close():
        plt.close(1)
