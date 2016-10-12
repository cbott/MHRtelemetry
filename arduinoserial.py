import serial

class Arduino:
    def __init__(self, port, baudrate = 9600):
        self.port = port
        self.baudrate = baudrate
        self._connect()

        self.buffer = ""

    def _connect(self):
        """ Connect to serial port """
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
        except:
            self.ser = None
            print "Unable to open serial port [%s]: Check that the Arduino is plugged in"%self.port

    def is_open(self):
        return self.ser is not None

    def read(self, sep = '\n'):
        """ return a list of all data in the serial buffer, split at 'sep' """
        if self.is_open():
            self.buffer += self.ser.read(self.ser.in_waiting)
            lines = self.buffer.split(sep)
            self.buffer = lines[-1] #may be incomplete data, keep in buffer
            return lines[:-1] # return all guaranteed complete data

        return [10]

    def close(self):
        if self.is_open():
            print "Closing Serial Connection %s..."%self.port
            self.ser.flush()
            self.ser.close() 
            self.ser = None
        else:
            print "No open serial connection"