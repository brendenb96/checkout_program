#! /usr/bin/env python
#
# Created by: Brenden Bickner
# Date: July 17, 2017
# Program designed for automated checkout on systems.
# This program reads from a configuration file in order to decide which modules should be ran

####################################################################################################
######################################### CHANGE LOG ###############################################
# Log any changes made to the file with date and name of individual modifying the file
# DO NOT MAKE CHANGES WITHOUT LOGGING THEM!!!!!!!!!!!!!!!!!!
####################################################################################################
# 2017-??-??    Brenden Bickner     Initial Release of Checkout Program

####################################################################################################
###################################### END OF CHANGE LOG ###########################################
####################################################################################################

# Librairies
import time
import os
import sys
from optparse import OptionParser

# Classes used for checkout
from modules.regoconfigCheckout import *
from modules.themisconfigCheckout import *
#from modules.blsCheckout import *
from modules.driveCheckout import *
from modules.firewallCheckout import *
from modules.imagerCheckout import *
from modules.ntpCheckout import *
from modules.servicesCheckout import *
from modules.Utilities import *
from modules.crxCheckout import *

# Globals
REPORT_FILE = None
FILENAME = ''
CONFIGFILENAME = ''
JSONFILENAME = ''
VERBOSE_MODE = False
VERYVERBOSE_MODE = False
WORKLISTER_MODE = False

# COLOURS
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


###################################
# Opens file for checkout results
###################################


def init_file():
    """ intialize text and json output file """
    global REPORT_FILE
    global FILENAME
    global JSONFILENAME
    try:
        FILENAME = '/usr/local/imager/automated-checkout/checkouts/SYSTEM_CHECKOUT_' + \
            time.strftime("%Y-%m-%dT%H:%M:%S") + '.txt'
        JSONFILENAME = '/usr/local/imager/automated-checkout/checkouts/SYSTEM_CHECKOUT_' + \
            time.strftime("%Y-%m-%dT%H:%M:%S") + '.json'
        
        REPORT_FILE = open(FILENAME, "w")
        REPORT_FILE.write("########### Automated Checkout ###########")
    except Exception as e:
        sys.exit(FAIL + "ERROR: Cannot open file to print to." + ENDC)
    return

##################################
# Main method
##################################


def main():
    """ Main checkout program """

    os.seteuid(0)
    # globals that will be needed
    global REPORT_FILE
    global FILENAME
    global JSONFILENAME
    global VERBOSE_MODE
    global VERYVERBOSE_MODE
    global WORKLISTER_MODE
    global CONFIGFILENAME
    utility = None

    # create an option menu for the program 
    usage = "./local_checkout.py [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose",help="prints details of test results")
    parser.add_option("-V", "--very verbose",
                      action="store_true", dest="veryverbose",help="prints details as well as configuration files")
    parser.add_option("-i", "--image",
                      action="store_true", dest="image",help="takes a test image")
    parser.add_option("-d", "--daemons",
                      action="store_true", dest="daemons",help="checks imager daemons")
    parser.add_option("-c", "--config",
                      action="store_true", dest="config",help="checks configuration files")
    parser.add_option("-n", "--ntp",
                      action="store_true", dest="ntp",help="checks ntp")
    parser.add_option("-e", "--external",
                      action="store_true", dest="external",help="checks external drives")
    parser.add_option("-f", "--firewall",
                      action="store_true", dest="firewall",help="checks firewall")
    parser.add_option("-b", "--bls",
                      action="store_true", dest="bls",help="checks bls values")
    parser.add_option("-s", "--services",
                      action="store_true", dest="services",help="checks services running")
    parser.add_option("-a", "--all",
                      action="store_true", dest="all",help="runs all checks except test image")
    parser.add_option("-w", "--worklister",
                      action="store_true", dest="worklister",help="only creates .txt and .json file for worklister")
    parser.add_option("-x", "--crx",
                      action="store_true", dest="crx",help="checks cr10x values")
    (options, args) = parser.parse_args()

    # turn on neccessary options
    if options.verbose:
        VERBOSE_MODE = True

    if options.veryverbose:
        VERYVERBOSE_MODE = True
        VERBOSE_MODE = True

    if options.worklister:
        VERBOSE_MODE = False
        VERYVERBOSE_MODE = False
        WORKLISTER_MODE = True
        
    # ensure user has put cap on camera
    try:
        if options.image:
            print WARNING + "\nPlease ensure the lens cap is on the camera " + ENDC,
            for i in range(5):
                stdout.write(WARNING + "." + ENDC)
                stdout.flush()
                sleep(1)
                stdout.flush()
            print "\n"

        # initialize the file and print the header
        init_file()

        # initialize utility and get configuration data
        utility = Utilities(REPORT_FILE, VERBOSE_MODE, VERYVERBOSE_MODE, WORKLISTER_MODE, JSONFILENAME)
        utility.access_config()

        # if configuration file is corrupt, raise configparser error
        if not utility.VALID_CONFIGURATION:
            raise ConfigParser.Error

        # print header
        utility.print_write(
            OKBLUE +
            '++++++++++++++++++++++++++++++++++++++++++++++++++\n         STARTING  CHECKOUT\n++++++++++++++++++++++++++++++++++++++++++++++\n' +
            ENDC)

        # run modules from the configuration file and options
        if utility.RUN_EXTERNAL_DRIVES and (options.external or options.all):
            drive_checkout = driveCheckout(utility)
            drive_checkout.check_drives()
        
        if utility.RUN_BLS and (options.bls or options.all):
            bls_checkout = blsCheckout(utility)
            bls_checkout.check_bls()

        if utility.RUN_IMAGER:
            imager_checkout = imagerCheckout(utility)
            if options.image:
                imager_checkout.check_camera()
            if options.daemons or options.all:
                imager_checkout.check_imager_daemons()

        if utility.RUN_NTP and (options.ntp or options.all):
            ntp_checkout = ntpCheckout(utility)
            ntp_checkout.check_ntp()

        if utility.RUN_SERVICES and (options.services  or options.all):
            services_checkout = servicesCheckout(utility)
            services_checkout.check_daemons_and_crons()

        if utility.RUN_REGO_CONFIG and (options.config  or options.all):
            regoconfig_checkout = regoconfigCheckout(VERBOSE_MODE, VERYVERBOSE_MODE, utility)
            regoconfig_checkout.check_configuration()

        if utility.RUN_THEMIS_CONFIG and (options.config  or options.all):
            themisconfig_checkout = themisconfigCheckout(VERBOSE_MODE, VERYVERBOSE_MODE, utility)
            themisconfig_checkout.check_configuration()

        if utility.RUN_FIREWALL and (options.firewall  or options.all):
            firewall_checkout = firewallCheckout(utility)
            firewall_checkout.check_firewall()

        if utility.RUN_CR10X and (options.crx  or options.all):
            crx_checkout = crxCheckout(utility)
            crx_checkout.check_crx()
            

        # Print the footer and close the file
        if not WORKLISTER_MODE:
            print(OKBLUE + '\nREPORT SAVED AT: ' + FILENAME + ENDC)
            
        utility.json_data['valid_checkout'] = True
        utility.write_json()
        utility.print_write(
            OKBLUE +
            '++++++++++++++++++++++++++++++++++++++++++++++++++\n          CHECKOUT COMPLETED\n++++++++++++++++++++++++++++++++++++++++++++++\n' +
            ENDC)
        REPORT_FILE.close()

        # Copy most recent checkout to main directory
        utility.communicate('cp ' + FILENAME + ' /usr/local/imager/automated-checkout/RECENT_CHECKOUT.txt')
        utility.communicate('cp ' + JSONFILENAME + ' /usr/local/imager/automated-checkout/RECENT_CHECKOUT.json')

        # Change file permissions to read only
        utility.communicate('chmod 444 ' + FILENAME)
        utility.communicate('chmod 444 ' + JSONFILENAME)

    # Catch keyboard interrupt or error and properly stop the program
    except (KeyboardInterrupt,ConfigParser.Error):
        print(WARNING + "\n Stopping the checkout." + ENDC)
        if utility is not None:
            utility.json_data['valid_checkout'] = False
            utility.write_json()
            utility.communicate('chmod 444 ' + JSONFILENAME)
        if REPORT_FILE is not None:
            REPORT_FILE.close()
            utility.communicate('chmod 444 ' + FILENAME)
        return -1

    return 0


#############################
if __name__ == "__main__":
    sys.exit(main())
#############################
