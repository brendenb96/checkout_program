
from datetime import datetime

class ntpCheckout():
    """Class for checking ntp lock"""

    MAX_UC_DELAY = None
    MAX_UC_JITTER = None
    MAX_UC_OFFSET = None
    MAX_GPS_DELAY = None
    MAX_GPS_JITTER = None
    MAX_GPS_OFFSET = None


    utilities = None

    def __init__(self, utilities):
        self.utilities = utilities
        self.MAX_UC_DELAY = utilities.MAX_UC_DELAY
        self.MAX_UC_JITTER = utilities.MAX_UC_JITTER
        self.MAX_UC_OFFSET = utilities.MAX_UC_OFFSET
        self.MAX_GPS_DELAY = utilities.MAX_GPS_DELAY
        self.MAX_GPS_JITTER = utilities.MAX_GPS_JITTER
        self.MAX_GPS_OFFSET = utilities.MAX_GPS_OFFSET

    def check_ntp(self):
        """run the check"""

        gps_warning = False
        ntp_warning = False
        ntp_error = False

        # DEFININED LIMITS
        
        # get the hardware and system times
        sysdate_str = self.utilities.communicate('/bin/date +"%a %d %b %Y %r %Z"').rstrip()
        hwclock_str = self.utilities.communicate('/usr/sbin/hwclock')[:-20]

        # check if they are both in UTC time
        if sysdate_str.split()[6] == hwclock_str.split()[6] == 'UTC':
            
            # formats the two times into the same format and gets the difference
            sysdate = datetime.strptime(sysdate_str,"%a %d %b %Y %I:%M:%S %p %Z")
            hwclock = datetime.strptime(hwclock_str,"%a %d %b %Y %I:%M:%S %p %Z")
            time_difference = (hwclock-sysdate).seconds

            # if there is a large time distance print a warning
            if abs(time_difference) > 5:
                self.utilities.handle_print("Hardware/System Clock Sync","warning","difference of "+ str(time_difference) + " seconds")
                self.utilities.handle_json('clocks',{'software_time':sysdate_str,'software_in_utc':True,'hardware_time':hwclock_str,
                'hardware_in_utc':True,'hw_sw_sec_diff':time_difference,'checkout_status':'warning'},'time')
            else:
                self.utilities.handle_print("Hardware/System Clock Sync","pass","difference of "+ str(time_difference) + " seconds")
                self.utilities.handle_json('clocks',{'software_time':sysdate_str,'software_in_utc':True,'hardware_time':hwclock_str,
                'hardware_in_utc':True,'hw_sw_sec_diff':time_difference,'checkout_status':'pass'},'time')

        else:
            self.utilities.handle_print("Hardware/System Clock Sync","fail","these should both be set as UTC time")
            self.utilities.handle_json('clocks',{'software_time':sysdate_str,'software_in_utc':False,'hardware_time':hwclock_str,
                'hardware_in_utc':False,'hw_sw_milli_diff':'N/A','checkout_status':'fail'},'time')

        # get the NTP data
        response = self.utilities.communicate('/usr/sbin/ntpq -pn')
        response_lines = response.splitlines()

        if self.utilities.DEVICE_UID == 'rego':
            uofc = response_lines[4]
            gps = response_lines[5]
            iti = response_lines[3]

        if self.utilities.DEVICE_UID == 'themis':
            uofc = response_lines[3]
            gps = response_lines[5]
            iti = response_lines[4]

        uofc_data = uofc.split()
        uofc_delay = uofc_data[7]
        uofc_offset = uofc_data[8]
        uofc_jitter = uofc_data[9]

        gps_data = gps.split()
        gps_delay = gps_data[7]
        gps_offset = gps_data[8]
        gps_jitter = gps_data[9]

        # finds where the system is locked to 
        if gps[0] == '*':
            self.utilities.handle_print('NTP Lock','pass','locked on with GPS')
            self.utilities.handle_json('locked',{'locked_to':'gps','checkout_status':'pass'},'time')
        elif uofc[0] == '*':
            self.utilities.handle_print('NTP Lock','warning','locked to University of Calgary')
            self.utilities.handle_json('locked',{'locked_to':'UofC','checkout_status':'warning'},'time')
        elif iti[0] == '*':
            self.utilities.handle_print('NTP Lock','warning','locked to the ITI')
            self.utilities.handle_json('locked',{'locked_to':'ITI','checkout_status':'warning'},'time')
        else:
            self.utilities.handle_print('NTP Lock','fail','no lock established')
            self.utilities.handle_json('locked',{'locked_to':'None','checkout_status':'fail'},'time')

        # Check the UofC jitter and delay
        if abs(float(uofc_delay)) > self.MAX_UC_DELAY:
            ntp_warning = True
            self.utilities.handle_print(
                'UofC Delay',
                'warning',
                'This value is too high at ' +
                uofc_delay)

        elif float(uofc_delay) == 0.0:
            ntp_error = True
            self.utilities.handle_print(
                'UofC Delay',
                'fail',
                'This values is at 0, may not be connected')
        else:
            self.utilities.handle_print(
                'UofC Delay',
                'pass',
                'This value is good at ' +
                uofc_delay)

        if abs(float(uofc_offset)) > self.MAX_UC_OFFSET:
            ntp_warning = True
            self.utilities.handle_print(
                'UofC Offset',
                'warning',
                'This value is too high at ' +
                uofc_offset)
        elif float(uofc_offset) == 0.0:
            ntp_error = True
            self.utilities.handle_print(
                'UofC Offset',
                'fail',
                'This values is at 0, may not be connected')
        else:
            self.utilities.handle_print(
                'UofC Offset',
                'pass',
                'This value is good at ' +
                uofc_offset)

        if abs(float(uofc_jitter)) > self.MAX_UC_JITTER:
            ntp_warning = True
            self.utilities.handle_print(
                'UofC Jitter',
                'warning',
                'This value is too high at ' +
                uofc_jitter)
        elif float(uofc_jitter) == 0.0:
            ntp_error = True
            self.utilities.handle_print(
                'UofC Jitter',
                'fail',
                'This values is at 0, may not be connected')
        else:
            self.utilities.handle_print(
                'UofC Jitter',
                'pass',
                'This value is good at ' +
                uofc_jitter)

        # print the results of UofC analysis
        if ntp_error:
            self.utilities.handle_json('uofc',{'delay':uofc_delay,'jitter':uofc_jitter,'offset':uofc_offset,'checkout_status':'fail'},'time','ntp')
        elif ntp_warning:
            self.utilities.handle_json('uofc',{'delay':uofc_delay,'jitter':uofc_jitter,'offset':uofc_offset,'checkout_status':'warning'},'time','ntp')
        else:
             self.utilities.handle_json('uofc',{'delay':uofc_delay,'jitter':uofc_jitter,'offset':uofc_offset,'checkout_status':'pass'},'time','ntp')
        

        # Check the gps jitter and delay
        if abs(float(gps_delay)) > self.MAX_GPS_DELAY:
            gps_warning = True
            self.utilities.handle_print(
                'GPS Delay',
                'warning',
                'This value is too high at ' +
                gps_delay)

        else:
            self.utilities.handle_print('GPS Delay',
                'pass', 
                'This value is good at ' + 
                gps_delay)

        if abs(float(gps_offset)) > self.MAX_GPS_OFFSET:
            gps_warning = True
            self.utilities.handle_print(
                'GPS Offset',
                'warning',
                'This value is too high at ' +
                gps_offset)

        elif float(gps_offset) == 0.0:
            self.utilities.handle_print(
                'GPS Offset',
                'fail',
                'This values is at 0, may not be connected')
        else:
            self.utilities.handle_print(
                'GPS Offset',
                'pass',
                'This value is good at ' +
                gps_offset)

        if abs(float(gps_jitter)) > self.MAX_GPS_JITTER:
            gps_warning = True
            self.utilities.handle_print(
                'GPS Jitter',
                'warning',
                'This value is too high at ' +
                gps_jitter)

        elif float(gps_jitter) == 0.0:
            self.utilities.handle_print(
                'GPS Jitter',
                'fail',
                'This values is at 0, may not be connected')
        else:
            self.utilities.handle_print(
                'GPS Jitter',
                'pass',
                'This value is good at ' +
                gps_jitter)

        # print the results of the GPS analysis
        if gps_warning:
            self.utilities.handle_json('gps',{'delay':gps_delay,'jitter':gps_jitter,'offset':gps_offset,'checkout_status':'warning'},'time','ntp')
        else:
            self.utilities.handle_json('gps',{'delay':gps_delay,'jitter':gps_jitter,'offset':gps_offset,'checkout_status':'pass'},'time','ntp')

        return