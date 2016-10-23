#
# This is a wrapper on some matplotlib functions to allow easy creation
# of graphs that can have dynamic data in them
#

from collections import deque
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import mplDeprecation
import matplotlib.ticker as ticker

import math
import random

# matplotlib will throw a deprecation warning when using 
# plt.pause() or plt.waitforbuttonpress(), this prevents
# the warning from being printed to terminal
import warnings
warnings.filterwarnings("ignore", category=mplDeprecation)

class ScrollingLinePlot:
  """ Creates a line plot that shows a fixed number of
      data points at a time, scrolling right to left """
  def __init__(self, row, col, window_size, rowspan=1, colspan=1, title="Line Plot", ymin=0, ymax=100, width=100, ylabel="Data"):
    self.axis = plt.subplot2grid(window_size, (row,col),
                                 rowspan=rowspan, colspan=colspan)
    self.axis.set_title(title)
    self.axis.set_xlabel("Time")
    self.axis.set_ylabel(ylabel)

    # set x/y window range, prevents auto-scaling
    self.axis.set_xlim(-width,0)
    self.axis.set_ylim(ymin, ymax)

    self.data = deque([0]*(width+1), maxlen = width+1)
    self.line = self.axis.plot(self.data)[0]
    self.line.set_data(range(-len(self.data)+1,1), self.data)

  def append_data(self, val):
    """ Add data and update the graph """
    self.data.append(val) # deque automatically truncates to [width] values
    self.line.set_ydata(self.data)

class BarChart:
    """ Single bar in a plot that can show a
        changing height value """
    def __init__(self, row, col, window_size, rowspan=1, colspan=1, title="Bar Chart", ymin=0, ymax=100, ylabel="", color='r'):
        self.axis = plt.subplot2grid(window_size, (row,col),
                                 rowspan=rowspan, colspan=colspan)
        self.axis.set_title(title)
        self.axis.set_ylabel(ylabel)
        self.axis.xaxis.set_visible(False)
        self.axis.set_xlim(0, 10)
        self.axis.set_ylim(ymin, ymax)
        self.value = 0;
        self.bar = self.axis.bar(
            left = 1,
            height = self.value,
            width = 8,
            color = color)[0]

    def update(self, val):
        self.value = val
        self.bar.set_height(self.value)

class Dial:
    def __init__(self, row, col, window_size, rowspan=1, colspan=1, title="Dial", ymin=0, ymax=100, color='r'):
        self.axis = plt.subplot2grid(window_size, (row,col),
                                 rowspan=rowspan, colspan=colspan, projection='polar')
        self.axis.set_ylim(0,1)
        self.axis.yaxis.set_visible(False)
        self.axis.grid(False) #remove radial grid lines
        self.axis.set_theta_offset(7*math.pi/6.0) #put zero on left side
        self.axis.set_theta_direction(-1); #make theta increase clockwise
        self.min = ymin
        self.max = ymax
        self.axis.xaxis.set_major_locator(ticker.MultipleLocator(math.pi/9))
        self.axis.set_xticklabels(['']+self._even_ticks(self.min, self.max, 12)+[''])#,minor=True)

        self.axis.set_title(title)

        self.value = 0
        self.line = self.axis.plot((0,self.value), (0,1), c=color, linewidth=3)[0]

    def _even_ticks(self, low, up, leng):
        step = ((up-low) * 1.0 / leng)
        return [int(round(low+i*step,0)) for i in range(leng+1)]

    def update(self, val):
        self.value = float(val)
        theta = (self.value/(self.max-self.min))*4*math.pi/3.0
        self.line.set_data((0,theta), (0,1))

class Text:
    def __init__(self, row, col, window_size, rowspan=1, colspan=1, title="Text"):
        self.axis = plt.subplot2grid(window_size, (row,col),
                                 rowspan=rowspan, colspan=colspan)
        self.axis.xaxis.set_visible(False)
        self.axis.yaxis.set_visible(False)
        #self.axis.axis('off')
        self.axis.spines['top'].set_visible(False)
        self.axis.spines['right'].set_visible(False)
        self.axis.spines['bottom'].set_visible(False)
        self.axis.spines['left'].set_visible(False)
        self.axis.set_ylim(0, 4)
        self.axis.set_xlim(0, 10)
        self.text = self.axis.text(0,3,"Hello", fontsize=20)

    def update(self, text):
        self.text.set_text(text)

def plot_example():
    """ Graph random data to show what the library can do """
    fig = plt.figure()
    fig.canvas.set_window_title("Example Plot")
    dim = (2,2) # The window will have 2 rows and 2 columns of axes
    graph_a = ScrollingLinePlot(row=0, col=0, window_size=dim,
                                title="Graph A", ymin=0, ymax=100, width=10)
    graph_b = BarChart(row=0, col=1, window_size=dim, title="Graph B", 
                       ymin=0, ymax=10, ylabel="Example value", color="#AA00AA")
    graph_c = Dial(row=1, col=0, window_size=dim, title="Graph C", ymin=0, ymax=25)
    graph_d = Text(row=1, col=1, window_size=dim, title="Graph D")
    plt.tight_layout()
    plt.ion() #Make plot interactive
    for i in range(100):
        graph_a.append_data(random.randint(0,100))
        graph_b.update(i/3%10)
        graph_c.update((i%50)*(i%50<=25)+(50-i%50)*((i%50)>25))
        graph_d.update(i)
        plt.show()
        plt.pause(0.1)
    plt.pause(-1)
    #plt.waitforbuttonpress(-1)
        
if __name__ == "__main__":
    plot_example()
