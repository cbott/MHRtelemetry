import matplotlib.pyplot as plt 

from arduinoserial import Arduino
from liveplots import ScrollingLinePlot, BarChart

SERIAL_PORT = 'COM3'

def basic_graph(arduino):
    fig, axes = plt.subplots(nrows = 1, ncols = 2)
    fig.canvas.set_window_title("Example Plot")
    graph = ScrollingLinePlot(axes[0], title="Arduino Data", ymin=0, ymax=100, width=50)
    bar = BarChart(axes[1], title="Arduino Data 2", ymin=0, ymax=10)

    plt.ion() #Make plot interactive
    while 1:
        try:
            data = arduino.read()
            for val in data:
                try:
                    vals = val.split(":")
                    graph.append_data(int(vals[0]))
                    bar.update(int(vals[1]))
                except ValueError:
                    print "Received unexpected data [",val,"]"
        except KeyboardInterrupt:
            arduino.close()
            return 1

        plt.show()
        plt.pause(0.2)

if __name__ == "__main__":
    arduino = Arduino(SERIAL_PORT)
    try:
        basic_graph(arduino)
    except Exception as e:
        # Close the serial port regardless of error condition
        print e
        arduino.close()
