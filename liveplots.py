#
# This is a wrapper on some matplotlib functions to allow easy creation
# of graphs that can have dynamic data in them
#

from collections import deque
import matplotlib.pyplot as plt 
import random

class ScrollingLinePlot:
  """ Creates a line plot that shows a fixed number of
      data points at a time, scrolling right to left """
  def __init__(self, axis, title, ymin=0, ymax=100, width=100, ylabel="Data"):
    self.axis = axis
    self.axis.set_title(title)
    self.axis.set_xlabel("Time")
    self.axis.set_ylabel(ylabel)

    # set x/y window range, prevents auto-scaling
    self.axis.set_xlim(-width,0)
    self.axis.set_ylim(ymin, ymax)

    self.data = deque([0]*width, maxlen = width)
    self.line = self.axis.plot(self.data)[0]
    self.line.set_data(range(-len(self.data)+1,1), self.data)

  def append_data(self, val):
    """ Add data and update the graph """
    self.data.append(val) # deque automatically truncates to [width] values
    self.line.set_ydata(self.data)

class BarChart:
    """ Single bar in a plot that can show a
        changing height value """
    def __init__(self, axis, title, ymin=0, ymax=100, ylabel="", color='r'):
        self.axis = axis
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

def line_plot_example():
    """ Graph random data to show what the library can do """
    fig, axes = plt.subplots(nrows = 1, ncols = 2)
    fig.canvas.set_window_title("Example Plot")
    graph_a = ScrollingLinePlot(axes[0], "Graph A", 0, 100, 10)
    graph_b = BarChart(axes[1], "Graph B", ymin=0, ymax=10, 
                       ylabel="Example value", color="#FF9000")

    plt.ion() #Make plot interactive
    for i in range(100):
        graph_a.append_data(random.randint(0,100))
        graph_b.update(i/3%10)
        plt.show()
        plt.pause(0.1)
        
if __name__ == "__main__":
    line_plot_example()
