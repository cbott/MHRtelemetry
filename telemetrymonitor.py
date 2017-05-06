#!/usr/bin/env python
#grapharduino.py
from arduinoserial import Arduino
from liveplots import *
import sys
from time import strftime

def basic_graph(arduino, log):
    SIZE = 1 #Expected packet length
    liveplot_init(2,1, "Basic Telemetry Data")

    speedometer = Dial(row=0, col=0, title="Car Speed (MPH)", ymin=0, ymax=90, ticks=10)
    readout = Text(row=1, col=0, title="")
    topspeed = -100

    data = [ 0 for i in range(SIZE) ];
    while 1:
        for val in arduino.read():
            try:
                vals = val.split()
                data = map(float, vals)
                print(data)
            except (AttributeError, ValueError):
                print "Received unexpected data [",val,"]"
        if len(data) == SIZE:
            log.write(strftime("[%H:%M:%S] ") + str(data) + "\n")
            mph = data[0]
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
    #11# [Accel Pedal Error] boolean 
    #12# [Brake Pedal Percentage] 0-100
    #13# [Brake Pedal Error] boolean
    #14# [Low Voltage Battery SOC] 0-120 /10
    SIZE = 15
    liveplot_init(3,5, "MHR17 Telemetry System")
    engine_t = ScrollingLinePlot(row=0, col=3, title="Engine Temp.", ymin=0, ymax=255, width=25, ylabel="deg F")
    l_bat_t = ScrollingLinePlot(row=1, col=0, title="Left Battery Temp.", ymin=0, ymax=255, width=25, ylabel="deg F")
    r_bat_t = ScrollingLinePlot(row=2, col=0, title="Right Battery Temp.", ymin=0, ymax=255, width=25, ylabel="deg F")

    l_bat_soc = BarChart(row=0, col=0, title="Left Accumulator SOC", ymin=0, ymax=100, ylabel="%")
    r_bat_soc = BarChart(row=0, col=1, title="Right Accumulator SOC", ymin=0, ymax=100, ylabel="%")
    lv_soc = BarChart(row=0, col=2, title="LV Battery Voltage", ymin=0, ymax=13, ylabel="V")

    rpm = Dial(row=0, col=4, title="Engine RPM (x1000)", ymin=0, ymax=15, ticks=16)

    l_motor_t = ScrollingLinePlot(row=1, col=1, title="Left In-Hub Temp.", ymin=0, ymax=255, width=25, ylabel="deg F")
    r_motor_t = ScrollingLinePlot(row=2, col=1, title="Right In-Hub Temp.", ymin=0, ymax=255, width=25, ylabel="deg F")

    l_mc_t = ScrollingLinePlot(row=1, col=2, title="Left Motor Controller Temp.", ymin=0, ymax=255, width=25, ylabel="deg F")
    r_mc_t = ScrollingLinePlot(row=2, col=2, title="Right Motor Controller Temp.", ymin=0, ymax=255, width=25, ylabel="deg F")

    accel = BarChart(row=1, col=3, title="Accel Pedal %", ymin=0, ymax=100, ylabel="%")
    accel_err = BarChart(row=1, col=4, title="Accel Pedal Error", ymin=0, ymax=1, ylabel="", show_axes=False)
    
    brake = BarChart(row=2, col=3, title="Brake Pedal %", ymin=0, ymax=100, ylabel="%")
    brake_err = BarChart(row=2, col=4, title="Brake Pedal Error", ymin=0, ymax=1, ylabel="", show_axes=False)

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
            rpm.update(data[5]/10.0)
            l_motor_t.update(data[6])
            r_motor_t.update(data[7])
            l_mc_t.update(data[8])
            r_mc_t.update(data[9])
            accel.update(data[10])
            accel_err.update(1,color = 'r' if data[11] else 'g')
            brake.update(data[12])
            brake_err.update(1,color = 'r' if data[13] else 'g')
            lv_soc.update(data[14]/10.0)
        liveplot_update(0.1)

if __name__ == "__main__":
    serial_port = ""
    log_file = "TelemetryData.txt"

    if len(sys.argv) == 2:
        serial_port = sys.argv[1]
    elif len(sys.argv) == 3:
        serial_port = sys.argv[1]
        log_file = sys.argv[2]
    else:
        print("Incorrect Argument Format\nUsage: python grapharduino.py serial_port [log file]")
        sys.exit()
    arduino = Arduino(serial_port)
    log = open(log_file, 'a')
    log.write(strftime(">> BEGIN LOG << %m/%d/%y at %I:%M %p\n"))
    try:
        car_monitor(arduino, log)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
    finally:
        #run cleanup procedures when application closes
        arduino.close()
        log.close()
