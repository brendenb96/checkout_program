import subprocess
import serial
from time import sleep
from sys import stdout

class blsCheckout():
    """Class for testing the bright light sensor"""

    BLS_LOW = None
    BLS_HIGH = None

    def __init__(self, utilities):
        self.utilities = utilities
        self.BLS_LOW = utilities.MIN_BLS
        self.BLS_HIGH = utilities.MAX_BLS

    def initSerialPort(self):
        """init the bls serial"""

       # Arduino settings
        COM_DEVICE = "/dev/ttyACM0"
        COM_BAUDRATE = 9600
        COM_BYTESIZE = 8
        COM_STOPBITS = 1
        COM_PARITY = "N"
        COM_TIMEOUT = 1 

        # COLOURS
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

        ser = None

        # try to open the serial
        try:
            ser = serial.Serial(
                port=COM_DEVICE,
                baudrate=COM_BAUDRATE,
                bytesize=COM_BYTESIZE,
                stopbits=COM_STOPBITS,
                parity=COM_PARITY,
                timeout=COM_TIMEOUT)
            sleep(1)
            ser.flush()
            ser.flushInput()
            ser.close()
        except serial.SerialException as e:
            self.utilities.print_write(
                FAIL +
                "Error opening serial connection: %s" %
                (str(e)) +
                ENDC)

        # return
        return ser

    def check_bls(self):
        """run the check"""

        GET_BLS = "BLS?\n"

        # stop safetyd
        subprocess.Popen(
            'service imager_safetyd stop',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True).poll()
        sleep(1)
        self.utilities.communicate('pkill imager_safetyd')
        sleep(1)

        # open serial port for BLS
        stdout.flush()
        ser = self.initSerialPort()
        if (ser is None):
            self.utilities.handle_print('Bright Light Sensor','fail','Could not connect to BLS')
            self.utilities.handle_json('bls',{'bls_val':'N/A','dum_val':'510','checkout_status':'fail'})
            self.utilities.communicate('service imager_safetyd unlock')
            sleep(1)
            subprocess.Popen(
                'service imager_safetyd start',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True).poll()
            sleep(1)
            return
        ser.open()
        # give it a little extra time to get ready
        sleep(4)

        # try to read from the serial port
        try:
            # read from serial port
            ser.write(GET_BLS)
            bls, dum = ser.read(20).split(' ')
            if (int(bls) > self.BLS_LOW and int(bls) < self.BLS_HIGH):
                self.utilities.handle_print('Bright Light Sensor', 'pass', 'Value is at ' + bls)
                self.utilities.handle_json('bls',{'bls_val':bls,'dum_val':'510','checkout_status':'pass'})
            else:
                self.utilities.handle_print(
                    'Bright Light Sensor',
                    'warning',
                    'Value is incorrect for daylight at ' +
                    bls)
                self.utilities.handle_json('bls',{'bls_val':bls,'dum_val':'510','checkout_status':'warning'})

        except (serial.SerialException, KeyboardInterrupt) as e:
            self.utilities.print_write(FAIL + "\nERROR: Cannot self.utilities.communicate with BLS." + ENDC)
            # close serial port
        ser.close()

        # Start the safety deamon again
        sleep(1)
        self.utilities.communicate('service imager_safetyd unlock')
        sleep(1)
        subprocess.Popen(
            'service imager_safetyd start',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True).poll()
        sleep(1)
        return
