
class servicesCheckout():
    """Class for checking proper services and crons are running"""

    utilities = None

    def __init__(self, utilities):
        self.utilities = utilities

    def check_daemons_and_crons(self):
        """run the check"""
    
    # Check for monitor acquire to be running
        if self.utilities.DEVICE_UID == 'rego':
            response = self.utilities.communicate('service monitor_acquire status')
            if 'monitor_acquire is running as process' not in response:
                self.utilities.handle_print('Monitor Acquire running', 'fail', 'Does not appear to be running')
                self.utilities.handle_json('monitor_acquire',{'running':False,'pid':'N/A','checkout_status':'fail'})
            else:
                pid = response.split()[5]
                self.utilities.handle_print('Monitor Acquire running', 'pass', 'Running properly')
                self.utilities.handle_json('monitor_acquire',{'running':True,'pid':pid,'checkout_status':'pass'})

        if self.utilities.DEVICE_UID == 'themis':
            response = self.utilities.communicate('service monitor.acquire status')
            if 'monitor.acquire is running as process' not in response:
                self.utilities.handle_print('Monitor Acquire running', 'fail', 'Does not appear to be running')
                self.utilities.handle_json('monitor_acquire',{'running':False,'pid':'N/A','checkout_status':'fail'})
            else:
                pid = response.split()[5]
                self.utilities.handle_print('Monitor Acquire running', 'pass', 'Running properly')
                self.utilities.handle_json('monitor_acquire',{'running':True,'pid':pid,'checkout_status':'pass'})

    # Check for the cron daemon to be running
        response = self.utilities.communicate('service crond status')
        if 'is stopped' in response:
            self.utilities.handle_print('Cron Daemon Running', 'fail', 'Does not appear to be running')
            self.utilities.handle_json('crond',{'running':False,'pid':'N/A','checkout_status':'fail'})
        else:
            pid = self.utilities.communicate('pgrep crond').rstrip()
            self.utilities.handle_print('Cron Daemon Running', 'pass', 'Running properly')
            self.utilities.handle_json('crond',{'running':True,'pid':pid,'checkout_status':'pass'})

    # Check for the ntp daemon to be running
        response = self.utilities.communicate('service ntpd status')
        if 'is stopped' in response:
            self.utilities.handle_print('NTP Daemon Running', 'fail', 'Does not appear to be running')
            self.utilities.handle_json('ntpd',{'running':False,'pid':'N/A','checkout_status':'fail'})
        else:
            pid = self.utilities.communicate('pgrep xinetd').rstrip()
            self.utilities.handle_print('NTP Daemon Running', 'pass', 'Running properly')
            self.utilities.handle_json('ntpd',{'running':True,'pid':pid,'checkout_status':'pass'})

        return