#!/usr/bin/env python
#grapharduino.py
from arduinoserial import Arduino
from liveplots import *
from time import strftime

SIZE = 4 #Expected packet length

SERIAL_PORT = 'COM12'
LOG_FILE = "TelemetryData.txt"

def basic_graph(arduino, log):
    liveplot_init(2,1, "MHR Telemetry Data")

    speedometer = Dial(row=0, col=0, title="Car Speed (MPH)", ymin=0, ymax=80, ticks=9)
    readout = Text(row=1, col=0, title="")
    topspeed = -100

    data = [ 0 for i in range(SIZE) ];
    while 1:
        for val in arduino.read():
            try:
                vals = val.split()
                data = map(int, vals)
                print(data)
            except (AttributeError, ValueError):
                print "Received unexpected data [",val,"]"
        if len(data) == SIZE:
            log.write(strftime("[%H:%M:%S] ") + str(data) + "\n")
            mph = data[0]/2.0
            speedometer.update(mph)
            topspeed = max(topspeed, mph)
            readout.update("Current Speed: "+str(mph)+" MPH\nTop Speed:       "+str(topspeed)+" MPH")
        liveplot_update(0.1)
    
    # rpm = Dial(row=0, col=0, title="Engine RPM", ymin=0, ymax=6000)
    # temperature = ScrollingLinePlot(row=0, col=1, title="Engine Temp.",
    #                 ymin=0, ymax=250,width=25, ylabel="Degrees Celsius")
    # speed = Dial(row=0, col=2, title="Speed (MPH)", ymin=0, ymax=100)
    # error_state = Text(row=1, col=0, colspan=3, title="Error State")

    # data = {"Speed":0, "RPM":0, "Temp":0, "Error":""}
    # while 1:
    #     for val in arduino.read():
    #         try:
    #             vals = val.split(":")
    #             if vals[0] in data.keys():
    #                 data[vals[0]] = int(vals[1])
    #             else:
    #                 data["Error"] = val
    #         except (AttributeError, ValueError):
    #             print "Received unexpected data [",val,"]"
    #     rpm.update(data["RPM"])
    #     temperature.update(data["Temp"])
    #     speed.update(data["Speed"])
    #     error_state.update("Error State " + data["Error"])

    #     log.write(strftime("[%H:%M:%S] ") + str(data) + "\n")

    #     liveplot_update(0.2)

if __name__ == "__main__":
    arduino = Arduino(SERIAL_PORT)
    log = open(LOG_FILE, 'a')
    log.write(strftime(">> BEGIN LOG << %m/%d/%y at %I:%M %p\n"))
    try:
        basic_graph(arduino, log)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
    finally:
        #run cleanup procedures when application closes
        arduino.close()
        log.close()
