__author__ = 'masslab'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import LinearLocator
import matplotlib.dates as m_dates


datetime_fmt = m_dates.DateFormatter('%b %d, %H:%M')

class EnvironmentPlot(FigureCanvasQTAgg):
    """ Formats matplotlib figure for environmental data """
    def __init__(self):
        self.counter = 0
        self.fig = plt.figure(facecolor='white')
        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312, sharex=self.ax1)
        self.ax3 = self.fig.add_subplot(313, sharex=self.ax1)

        self.ax1.margins(0.05)
        self.ax1.set_ylabel(u'Temperature [\N{DEGREE SIGN}C]', fontsize=12)
        self.ax1.xaxis.set_major_locator(LinearLocator(numticks=0))
        self.ax1.tick_params(labelbottom='off')

        self.ax2.margins(0.05)
        self.ax2.set_ylabel(u'Pressure [Pa]', fontsize=12)
        self.ax2.xaxis.set_major_locator(LinearLocator(numticks=0))
        self.ax2.xaxis.set_tick_params(labelbottom='off')

        self.ax3.margins(0.05)
        self.ax3.set_ylabel(u'Humidity [%rh]', fontsize=12)
        self.ax3.xaxis.set_major_locator(LinearLocator(numticks=5))
        self.ax3.xaxis.set_tick_params(labelbottom='off')

        plt.setp(self.ax1.get_yticklabels(), fontsize=10)
        plt.setp(self.ax2.get_yticklabels(), fontsize=10)
        plt.setp(self.ax3.get_yticklabels(), fontsize=10)

        FigureCanvasQTAgg.__init__(self, self.fig)

    def add_point(self, t, p, h):
        now = datetime.now()
        self.ax1.plot(now, t, 'r.')
        self.ax2.plot(now, p, 'g.')
        self.ax3.plot(now, h, 'b.')
        if self.counter > 0:
            self.ax3.xaxis.set_major_formatter(datetime_fmt)
            self.ax3.xaxis.set_tick_params(labelbottom='on')
            plt.setp(self.ax3.get_xticklabels(), rotation=15, fontsize=10)
        self.draw()
        self.counter += 1

    def add_vertical(self):
        self.ax1.axvline(datetime.now(), linestyle='--', linewidth=1.5)
        self.ax2.axvline(datetime.now(), linestyle='--', linewidth=1.5)
        self.ax3.axvline(datetime.now(), linestyle='--', linewidth=1.5)
        self.draw()

