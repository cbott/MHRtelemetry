#!/usr/bin/env python
#
# This is a wrapper on some matplotlib functions to allow easy creation
# of graphs that can have dynamic data in them
#
# Author: Colin Bott

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

def liveplot_init(rows, cols, title="LivePlot Window"):
    """ Initialize the Matplotlib window """
    global window_size

    fig = plt.figure(figsize=(12,6), facecolor=(0.7,0.7,0.7))
    fig.canvas.set_window_title(title)

    window_size = (rows, cols)

    plt.ion() #Make plot interactive

def liveplot_update(time=0.2):
    """ Show graphs with updated data and delay """
    plt.tight_layout() # really only needs to be called once
    plt.show()
    plt.pause(time)

class ScrollingLinePlot:
  """ Creates a line plot that shows a fixed number of
      data points at a time, scrolling right to left """
  def __init__(self, row, col, rowspan=1, colspan=1, title="Line Plot",
               ymin=0, ymax=100, width=100, ylabel="Data"):
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

  def update(self, val):
    """ Add data and update the graph """
    self.data.append(val) # deque automatically truncates to [width] values
    self.line.set_ydata(self.data)

class BarChart:
    """ Single bar in a plot that can show a
        changing height value """
    def __init__(self, row, col, rowspan=1, colspan=1, title="Bar Chart", ymin=0, ymax=100, ylabel="", color='r', show_axes=True):
        self.axis = plt.subplot2grid(window_size, (row,col),
                                 rowspan=rowspan, colspan=colspan)
        self.axis.set_title(title)
        self.axis.set_ylabel(ylabel)
        self.axis.xaxis.set_visible(False)
        self.axis.yaxis.set_visible(show_axes)
        self.axis.set_xlim(0, 10)
        self.axis.set_ylim(ymin, ymax)
        self.value = 0;
        self.bar = self.axis.bar(
            left = 0,
            height = self.value,
            width = 20,
            color = color)[0]
        self.color = color

    def update(self, val, color=None):
        self.value = val
        if color is not None:
            self.bar.set_color(color)
        self.bar.set_height(self.value)

class Dial:
    def __init__(self, row, col, rowspan=1, colspan=1,
                 title="Dial", ymin=0, ymax=100, ticks=9, color='r'):
        self.axis = plt.subplot2grid(window_size, (row,col),
                                 rowspan=rowspan, colspan=colspan, projection='polar')
        self.axis.set_ylim(0,1)
        self.axis.yaxis.set_visible(False)
        self.axis.grid(False) #remove radial grid lines
        self.axis.set_theta_offset(7*math.pi/6.0) #put zero on left side
        self.axis.set_theta_direction(-1); #make theta increase clockwise
        self.min = ymin
        self.max = ymax

        tick_num = ticks - 1
        tick_spacing = tick_num * 0.75
        self.axis.xaxis.set_major_locator(ticker.MultipleLocator(math.pi/tick_spacing))
        self.axis.set_xticklabels(['']+self._even_ticks(self.min, self.max, tick_num)+[''])#,minor=True)

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
    def __init__(self, row, col, rowspan=1, colspan=1, title="Text"):
        self.axis = plt.subplot2grid(window_size, (row,col),
                                 rowspan=rowspan, colspan=colspan)
        self.axis.set_title(title)
        self.axis.xaxis.set_visible(False)
        self.axis.yaxis.set_visible(False)
        #self.axis.axis('off')
        self.axis.spines['top'].set_visible(False)
        self.axis.spines['right'].set_visible(False)
        self.axis.spines['bottom'].set_visible(False)
        self.axis.spines['left'].set_visible(False)
        self.axis.set_ylim(0, 1)
        self.axis.set_xlim(0, 1)
        self.text = self.axis.text(0,1,"", fontsize=20, va='top', wrap=True)

    def update(self, text, color='k'):
        self.text.set_text(text)
        self.text.set_color(color)

def plot_example():
    """ Graph random data to show what the library can do """
    liveplot_init(2,2,"LivePlot Example")
    graph_a = ScrollingLinePlot(row=0, col=0, title="Graph A",
                                ymin=0, ymax=100, width=10)
    graph_b = BarChart(row=0, col=1, title="Graph B", ymin=0,
                       ymax=10, ylabel="Example value", color="#AA00AA")
    graph_c = Dial(row=1, col=0, title="Graph C", ymin=0, ymax=25)
    graph_d = Text(row=1, col=1, title="Graph D")
    
    for i in range(100):
        graph_a.update(random.randint(0,100))
        graph_b.update(i/3%10)
        graph_c.update((i%50)*(i%50<=25)+(50-i%50)*((i%50)>25))
        if(i%10 == 0):
            graph_d.update(i, 'r')
        else:
            graph_d.update(i)
        liveplot_update(0.1)
    plt.pause(-1)
    #plt.waitforbuttonpress(-1)
        
if __name__ == "__main__":
    plot_example()
