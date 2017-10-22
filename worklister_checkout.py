#! /usr/bin/env python
#
# Created by: Brenden Bickner
# Date: July 17, 2017
# Program designed for remotely running a checkout and bringing data back to local machine:q

from optparse import OptionParser
import subprocess
import sys
import glob
from time import sleep
import re
from json2html import *
import json

##################################
# Main method
##################################


def main():
    """ Main checkout program """

    HTML = False
    OUTPUT_FOLDER = '/home/brenden/test_check'

    # create an option menu for the program 
    usage = "./worklister_checkout.py [options] destination"
    parser = OptionParser(usage=usage)
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
    parser.add_option("-x", "--crx",
                      action="store_true", dest="crx",help="checks THEMIS CR10X")
    parser.add_option("-a", "--all",
                      action="store_true", dest="all",help="runs all checks except test image")
    (options, args) = parser.parse_args()

    if not args:
        print(usage)
        return -1

    # Confirm that a valid IP address was entered
    IP_DEST = args[0]
    valid_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",IP_DEST)
    if not valid_ip:
        print "ERROR: Must pass a valid IP address."
        return -1

    # Strings used to make final command that is sent
    COMMAND = 'ssh imager@' + IP_DEST
    PATH = 'sudo /usr/local/imager/automated-checkout/local_checkout.py '
    OPTIONS = '-w'

    # configure options string from options selected
    if options.external or options.all:
        OPTIONS = OPTIONS + 'e'
    
    if options.bls or options.all:
        OPTIONS = OPTIONS + 'b'

    if options.image:
        OPTIONS = OPTIONS + 'i'

    if options.daemons or options.all:
         OPTIONS = OPTIONS + 'd'

    if options.ntp or options.all:
        OPTIONS = OPTIONS + 'n'

    if options.services  or options.all:
        OPTIONS = OPTIONS + 's'

    if options.config  or options.all:
        OPTIONS = OPTIONS + 'c'

    if options.firewall  or options.all:
        OPTIONS = OPTIONS + 'f'

    if options.crx  or options.all:
        OPTIONS = OPTIONS + 'x'
                
    # Create the final commands to be sent
    SEND_COMMAND = COMMAND + ' "' + PATH + OPTIONS + '"'
    SCP_JSON_SEND_COMMAND = 'scp imager@' + IP_DEST + ':/usr/local/imager/automated-checkout/RECENT_CHECKOUT.json ' + OUTPUT_FOLDER
    SCP_TXT_SEND_COMMAND = 'scp imager@' + IP_DEST + ':/usr/local/imager/automated-checkout/RECENT_CHECKOUT.txt ' + OUTPUT_FOLDER

    # Send the PROGRAM command
    process = subprocess.Popen(
            SEND_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)

    response = process.communicate()
    process.wait()

    # Check if there was an error in the output
    if response[1]:    
        if 'No route to host' in response[1]:
            print "ERROR: Could not connect to host."
            return -1

        if "no tty present" in response[1]:
            print "ERROR: File is not on the system or sudoers file is not configured."
            return -1

    # Send the SCP JSON command
    response = subprocess.Popen(
            SCP_JSON_SEND_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True).communicate()

    # Check if there was an error in the output
    if response[1]:    
        if 'No such file or directory' in response[1]:
            print "ERROR: JSON File was not made."

    # Send the SCP TXT command
    response = subprocess.Popen(
            SCP_TXT_SEND_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True).communicate()

    # Check if there was an error in the output
    if response[1]:    
        if 'No such file or directory' in response[1]:
            print "ERROR: TXT File was not made."

    # Optional - create a HTML doc from output
    if HTML:
        json_file = open(OUTPUT_FOLDER + '/RECENT_CHECKOUT.json')
        json_data = json_file.read()
        html_output = open(OUTPUT_FOLDER + '/output.html','w')
        html_output.write(json2html.convert(json = json_data))
        html_output.close()

    return 0


#############################
if __name__ == "__main__":
    sys.exit(main())
#############################
