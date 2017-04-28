#!/usr/bin/env python
#grapharduino.py
from arduinoserial import Arduino
from liveplots import *
from time import strftime

SIZE = 13 #Expected packet length

SERIAL_PORT = 'COM8'
LOG_FILE = "TelemetryData.txt"

def basic_graph(arduino, log):
    liveplot_init(2,1, "Basic Telemetry Data")

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
    
def car_monitor(arduino, log):
    ####### Data Format
    ## Byte array
    #0# [Engine Temp] 0-255
    #1# [Left EV Battery Temp] 0-255
    #2# [Right EV Battery Temp] 0-255
    #3# [Left Accumulator SOC] 0-100
    #4# [Right Accumulator SOC] 0-100
    #5# [RPM] 0-150 x100
    #6# [Left In-Hub Motor Temp] 0-255
    #7# [Right In-Hub Motor Temp] 0-255
    #8# [Left Motor Controller Temp] 0-255
    #9# [Right Motor Controller Temp] 0-255
    #10# [Accel Pedal Percentage] 0-100
    #11# [Brake Pedal Percentage] 0-100
    #12# [Accel Pedal Error, Brake Pedal Error] boolean
    liveplot_init(3,4, "MHR17 Telemetry System")
    engine_t = ScrollingLinePlot(row=0, col=0, title="Engine Temp.", ymin=0, ymax=255, width=25)
    l_bat_t = ScrollingLinePlot(row=1, col=0, title="Left Battery Temp.", ymin=0, ymax=255, width=25)
    r_bat_t = ScrollingLinePlot(row=2, col=0, title="Right Battery Temp.", ymin=0, ymax=255, width=25)

    l_bat_soc = BarChart(row=0, col=1, title="Engine Temp.", ymin=0, ymax=100, ylabel="%")
    r_bat_soc = BarChart(row=0, col=2, title="Engine Temp.", ymin=0, ymax=100, ylabel="%")

    rpm = Dial(row=0, col=3, title="Engine RPM (x100)", ymin=0, ymax=150, ticks=8)

    l_motor_t = ScrollingLinePlot(row=1, col=1, title="Left In-Hub Temp.", ymin=0, ymax=255, width=25)
    r_motor_t = ScrollingLinePlot(row=2, col=1, title="Right In-Hub Temp.", ymin=0, ymax=255, width=25)

    l_mc_t = ScrollingLinePlot(row=1, col=2, title="Left Motor Controller Temp.", ymin=0, ymax=255, width=25)
    r_mc_t = ScrollingLinePlot(row=2, col=2, title="Right Motor Controller Temp.", ymin=0, ymax=255, width=25)

    accel = BarChart(row=1, col=3, title="Accel Pedal %", ymin=0, ymax=100, ylabel="%")
    brake = BarChart(row=2, col=3, title="Brake Pedal %", ymin=0, ymax=100, ylabel="%")

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
            engine_t.update(data[0])
            l_bat_t.update(data[1])
            r_bat_t.update(data[2])
            l_bat_soc.update(data[3])
            r_bat_soc.update(data[4])
            rpm.update(data[5])
            l_motor_t.update(data[6])
            r_motor_t.update(data[7])
            l_mc_t.update(data[8])
            r_mc_t.update(data[9])
            accel.update(data[10])
            brake.update(data[11])
        liveplot_update(0.1)

if __name__ == "__main__":
    arduino = Arduino(SERIAL_PORT)
    log = open(LOG_FILE, 'a')
    log.write(strftime(">> BEGIN LOG << %m/%d/%y at %I:%M %p\n"))
    try:
        car_monitor(arduino, log)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
    finally:
        #run cleanup procedures when application closes
        arduino.close()
        log.close()
