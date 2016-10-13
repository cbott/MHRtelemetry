import serial

class Arduino:
    """ Wrapper on Serial port to allow easy data reading from and arduino """
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
            print "Unable to open serial port [%s]: \
                   Check that the Arduino is plugged in"%self.port

    def is_open(self):
        return self.ser is not None

    def read(self, sep = '\n'):
        """ return a list of all data in the serial buffer, split at 'sep' """
        if self.is_open():
            # read in all available bytes
            self.buffer += self.ser.read(self.ser.in_waiting)
            lines = self.buffer.split(sep)
            # Keep the most recent value, as this may contain incomplete
            # data if read before the arduino finishes writing
            self.buffer = lines[-1]
            # return all values except the most recent
            # these are guaranteed to be complete writes
            return lines[:-1]
        # return a default value if the serial port is not open
        return [-1]

    def close(self):
        if self.is_open():
            print "Closing Serial Connection %s..."%self.port
            self.ser.flush()
            self.ser.close() 
            self.ser = None
        else:
            print "No open serial connection"