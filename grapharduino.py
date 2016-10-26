
from arduinoserial import Arduino
from liveplots import *

SERIAL_PORT = 'COM3'

def basic_graph(arduino):
    liveplot_init(2,3, "MHR Telemetry Data")

    rpm = Dial(row=0, col=0, title="Engine RPM", ymin=0, ymax=6000)
    temperature = ScrollingLinePlot(row=0, col=1, title="Engine Temp.",
                    ymin=0, ymax=250,width=25, ylabel="Degrees Celsius")
    speed = Dial(row=0, col=2, title="Speed (MPH)", ymin=0, ymax=100)
    error_state = Text(row=1, col=0, colspan=3, title="Error State")

    data = {"Speed":0, "RPM":0, "Temp":0, "Error":""}
    while 1:
        for val in arduino.read():
            try:
                vals = val.split(":")
                if vals[0] in data.keys():
                    data[vals[0]] = int(vals[1])
                else:
                    data["Error"] = val
            except (AttributeError, ValueError):
                print "Received unexpected data [",val,"]"
        rpm.update(data["RPM"])
        temperature.update(data["Temp"])
        speed.update(data["Speed"])
        error_state.update("Error State " + data["Error"])

        liveplot_update(0.2)

if __name__ == "__main__":
    arduino = Arduino(SERIAL_PORT)
    try:
        basic_graph(arduino)
    except Exception as e:
        # Close the serial port regardless of error condition
        print e
        arduino.close()
