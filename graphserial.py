import serial
import matplotlib.pyplot as plt 
from liveplots import ScrollingLinePlot

SERIAL_PORT = 'COM3'

def basic_graph(ser):
    fig, axes = plt.subplots(nrows = 1, ncols = 1)
    graph = ScrollingLinePlot(axes, "Arduino Data", 0, 100, 25)

    plt.ion() #Make plot interactive
    while 1:
        try:
            line = ser.readline()
            data = int(line)
            graph.append_data(data)
            plt.show()
            plt.pause(0.2)
        except KeyboardInterrupt:
            return 1

def cleanup(ser):
    ser.flush()
    ser.close() 

try:
    arduino = serial.Serial(SERIAL_PORT, 9600)
except:
    print "Unable to open serial port [COM3]: Check that the Arduino is plugged in"
else:
    basic_graph(arduino)
    cleanup(arduino)
