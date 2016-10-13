import matplotlib.pyplot as plt 

from arduinoserial import Arduino
from liveplots import ScrollingLinePlot

SERIAL_PORT = 'COM3'

def basic_graph(arduino):
    fig, axes = plt.subplots(nrows = 1, ncols = 1)
    graph = ScrollingLinePlot(axes, title="Arduino Data", ymin=0, ymax=100, width=50)

    plt.ion() #Make plot interactive
    while 1:
        try:
            data = arduino.read()
            for val in data:
                try:
                    graph.append_data(int(val))
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
        arduino.close()
