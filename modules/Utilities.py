import re
import os
import sys
import fnmatch
import subprocess
import json
import time
import ConfigParser

class Utilities():
    """Class that contains utilities for printing to console and files and holds configuration values"""

    report_file = None
    verbose_mode = False
    worklister_mode = False
    jsonfilename = ''
    json_data = {}
    config_file = '/usr/local/imager/automated-checkout/checkout_config.cfg'
    crx_config_file = '/usr/local/imager/automated-checkout/configs/crx_values.cfg'

    VALID_CONFIGURATION = True

    # MODULE BOOLEANS #
    RUN_NTP = False
    RUN_IMAGER = False
    RUN_SERVICES = False
    RUN_REGO_CONFIG = False
    RUN_THEMIS_CONFIG = False
    RUN_EXTERNAL_DRIVES = False
    RUN_FIREWALL = False
    RUN_BLS = False
    RUN_CR10X = False

    # MODULE INFORMATION #
    EXPOSE_PATH = None
    SERIAL_PATH = None
    DEVICE_UID = None
    SITE_UID = None
    PROJECT_UID = None
    CRX_VALS = None

    MAX_UC_DELAY = None
    MAX_UC_JITTER = None
    MAX_UC_OFFSET = None
    MAX_GPS_DELAY = None
    MAX_GPS_JITTER = None
    MAX_GPS_OFFSET = None

    MAX_BLS = None
    MIN_BLS = None


    def __init__(self, reportfile,verbose,veryverbose, worklister, jsonfilename):
        self.report_file = reportfile
        self.verbose_mode = verbose
        self.worklister_mode = worklister
        self.jsonfilename = jsonfilename

        self.json_data['date performed'] = time.strftime("%Y-%m-%dT%H:%M:%S")
        if veryverbose:
            self.json_data['verbosity'] = 'very'
        elif verbose:
            self.json_data['verbosity'] = 'verbose'
        else:
            self.json_data['verbosity'] = 'quiet'

        self.json_data['tests'] = {}

    def access_config(self):
        """ parses configuration file and assigns values """
        config = ConfigParser.ConfigParser()
        config.read(self.config_file)
        
        # SYSTEM SECTION CONFIGURATION
        try:
            self.SITE_UID = config.get('system','site_uid')
            self.DEVICE_UID = config.get('system','device_uid')
            self.PROJECT_UID = config.get('system','project_uid')
        except ConfigParser.Error:
            print('Configuration Error in SYSTEM section')
            self.VALID_CONFIGURATION = False
        
        # NTP SECTION CONFIGURATION
        try:
            self.RUN_NTP = config.getboolean('ntp','run')
            self.MAX_UC_DELAY = config.getfloat('ntp','max_uc_delay')
            self.MAX_UC_JITTER = config.getfloat('ntp','max_uc_jitter')
            self.MAX_UC_OFFSET = config.getfloat('ntp','max_uc_offset')
            self.MAX_GPS_DELAY = config.getfloat('ntp','max_gps_delay')
            self.MAX_GPS_JITTER = config.getfloat('ntp','max_gps_jitter')
            self.MAX_GPS_OFFSET = config.getfloat('ntp','max_gps_offset')
        except ConfigParser.Error:
            print('Configuration Error in NTP section')
            self.VALID_CONFIGURATION = False

        # IMAGER SECTION CONFIGURATION
        try:
            self.RUN_IMAGER = config.getboolean('imager','run')
            self.EXPOSE_PATH = config.get('imager','expose_path')
        except ConfigParser.Error:
            print('Configuration Error in IMAGER section')
            self.VALID_CONFIGURATION = False

        # SERVICES SECTION CONFIGURATION
        try:
            self.RUN_SERVICES = config.getboolean('services','run')
        except ConfigParser.Error:
            print('Configuration Error in SERVICES section')
            self.VALID_CONFIGURATION = False

        # REGO_CONFIGURATION_FILES SECTION CONFIGURATION
        try:
            self.RUN_REGO_CONFIG = config.getboolean('rego_config_files','run')
            self.SERIAL_PATH = config.get('rego_config_files','serial_path')
        except ConfigParser.Error:
            print('Configuration Error in REGO_CONFIGURATION_FILES section')
            self.VALID_CONFIGURATION = False

        # THEMIS_CONFIGURATION_FILES SECTION CONFIGURATION
        try:
            self.RUN_THEMIS_CONFIG = config.getboolean('themis_config_files','run')
        except ConfigParser.Error:
            print('Configuration Error in THEMIS_CONFIGURATION_FILES section')
            self.VALID_CONFIGURATION = False

        # EXTERNAL_DRIVES SECTION CONFIGURATION
        try:
            self.RUN_EXTERNAL_DRIVES = config.getboolean('external_drives','run')
        except ConfigParser.Error:
            print('Configuration Error in EXTERNAL_DRIVES section')
            self.VALID_CONFIGURATION = False

        # FIREWALL SECTION CONFIGURATION
        try:
            self.RUN_FIREWALL = config.getboolean('firewall','run')
        except ConfigParser.Error:
            print('Configuration Error in FIREWALL section')
            self.VALID_CONFIGURATION = False

        # BLS SECTION CONFIGURATION
        try:
            self.RUN_BLS = config.getboolean('bls','run')
            self.MAX_BLS = config.getint('bls','max_val')
            self.MIN_BLS = config.getint('bls','min_val')
        except ConfigParser.Error:
            print('Configuration Error in BLS section')
            self.VALID_CONFIGURATION = False

        # CR10X SECTION CONFIGURATION
        try:
            self.RUN_CR10X = config.getboolean('cr10x','run')
            if self.RUN_CR10X:
                self.CRX_VALS = ConfigParser.ConfigParser()
                self.CRX_VALS.read(self.crx_config_file)

        except ConfigParser.Error:
            print('Configuration Error in CR10X section')
            self.VALID_CONFIGURATION = False

        
        return


        

    def print_write(self,message):
        """prints messages to console and file"""
        try:
            # print to console
            if not self.worklister_mode:
                print(message)
            # remove colour coding and write to text file
            ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
            self.report_file.write("\n" + ansi_escape.sub('', message))
        except IOError as e:
            self.report_file.close()
            sys.exit("Error writing to file")
        return

    def handle_json(self,json_title,json_message,json_category = None,json_subcategory=None):
        """ updates json data """

        # follwing code block checks if a category exists and if not it creates it
        # this was created for easy addition of different categories in the dictionary
        if json_subcategory != None:
            if json_category not in self.json_data['tests']:
                self.json_data['tests'][json_category] = {}
            if json_subcategory not in self.json_data['tests'][json_category]:
                self.json_data['tests'][json_category][json_subcategory] = {}

            self.json_data['tests'][json_category][json_subcategory][json_title] = json_message

        elif json_category != None:
            if json_category not in self.json_data['tests']:
                self.json_data['tests'][json_category] = {}

            self.json_data['tests'][json_category][json_title] = json_message
        else:
            self.json_data['tests'][json_title] = json_message
        return


    ####################################################################
    # Used for printing test results to the file and console
    ####################################################################


    def handle_print(self, type_check, result, message):
        """prints results to console and file"""
        # COLOURS
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

        # does the colour encoding for results of tests
        # Green = pass, Red = fail, Yellow = warning
        try:
            if not self.worklister_mode:
                if self.verbose_mode:
                    if result == 'fail':
                        print("[ " + type_check + " ] : " + FAIL + "FAIL" + ENDC + " : " + message)

                    elif result == 'pass':
                        print("[ " + type_check + " ] : " + OKGREEN + "PASS" + ENDC + " : " + message)

                    elif result == 'warning':
                        print("[ " + type_check +" ] : " + WARNING + "WARNING" + ENDC +" : " + message)

                    else:
                        print("[ " + type_check + " ] : " + result.capitalize() + " : " + message)

                else:
                    if result == 'fail':
                        print("[ " + type_check + " ] : " + FAIL + "FAIL" + ENDC)

                    elif result == 'pass':
                        print("[ " + type_check + " ] : " + OKGREEN + "PASS" + ENDC)

                    elif result == 'warning':
                        print("[ " + type_check + " ] : " + WARNING + "WARNING" + ENDC)

                    else:
                        print("[ " + type_check + " ] : " + result.capitalize() + " : " + message)

            self.report_file.write("\n[ " + type_check + " ] : " + result.capitalize() + " : " + message)
        except IOError as e:
            self.report_file.close()
            sys.exit("Error writing to file")
        return

    ######################################################################
    # Method for writing data to json file
    ######################################################################


    def write_json(self):
        """ writes the dictionary to a json file"""
        try:
            with open(self.jsonfilename, 'w') as outfile:  
                json.dump(self.json_data, outfile,sort_keys=True,indent=4)
        except IOError as e:
            print('Error: Could not write to JSON file.')

        return
        

    ######################################################################
    # Method for sending shell commands and returning the response
    ######################################################################


    def communicate(self,command):
        """ sends commands to machine """
        return subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True).communicate()[0]

    ######################################################################
    # Used to search for filename
    ######################################################################


    def find_file(self,pattern, path):
        """ finds file within a certain path """
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
                    return result
        return result