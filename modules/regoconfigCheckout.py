from time import sleep
import os
import re

class regoconfigCheckout():
    """Class for testing configuration files"""

    verbose_mode = False
    veryverbose_mode = False
    utilities = None
    camera_serial_path = None
    imager_directory = "/usr/local/imager/"
    project_directory = "/usr/local/etc/"
    imager_path = "/usr/local/imager/imager.conf"
    project_path = "/usr/local/etc/project.conf"
    hosts_path = "/etc/hosts"
    network_path = "/etc/sysconfig/network"


    def __init__(self,verbose,veryverbose,utilities):
        self.verbose_mode = verbose
        self.veryverbose_mode = veryverbose
        self.utilities = utilities
        self.camera_serial_path = utilities.SERIAL_PATH

    ######################################################
    # Method that checks the image and site configuration
    ######################################################


    def check_configuration(self):
        """run the check"""

        # Variables used in this check
        site_code_official = self.utilities.SITE_UID+'-'+self.utilities.DEVICE_UID
        site_code_imager = ''
        site_code_hosts = ''
        site_code_net = ''
        site_code_project = ''
        device_uid_official = ''
        project_device_uid = ''
        camera_serial_number = ''  
        imager_conf_serial = ''
        correct_camera_mode = False
        correct_sza = False
        sza = ''
        camera_mode = ''
        imager_conf_json = {}
        project_conf_json = {}

        # power on the camera and run program that prints the camera serial number from it
        response = self.utilities.communicate('power_control imager on')
        sleep(5)
        if 'Error' not in response:
            response = self.utilities.communicate(self.camera_serial_path)
            sleep(1)
            camera_serial_number = response[-6:].rstrip()
            device_uid_official = self.utilities.DEVICE_UID + '-' + camera_serial_number[-3:]

        self.utilities.communicate('power_control imager off')

        #### Host conf file #####
        # get the required data from the file
        counter = 0
        pattern = re.compile("[a-z][a-z][a-z][a-z]-rego")
        for i, line in enumerate(open(self.hosts_path)):
            for match in re.finditer(pattern, line):
                site_code_hosts = match.group()
                counter = counter + 1
        if counter == 2 and site_code_official == site_code_hosts:
            self.utilities.handle_print('Hosts Configuration file','pass','file appears to be configured properly as '+site_code_hosts)
            self.utilities.handle_json('hosts',{'hostname':site_code_hosts,'checkout_status':'pass'},'config_files')

        else:
            self.utilities.handle_print('Hosts Configuration file','fail','file not configured properly')
            self.utilities.handle_json('hosts',{'hostname':'N/A','checkout_status':'fail'},'config_files')
            site_code_hosts = ''

        #### Network conf file #####
        # get the required data from the file
        counter = 0
        pattern = re.compile("[a-z][a-z][a-z][a-z]-rego")
        for i, line in enumerate(open(self.network_path)):
            for match in re.finditer(pattern, line):
                site_code_net = match.group()
                counter = counter + 1
        if counter == 1 and site_code_official == site_code_net:
            self.utilities.handle_print('Network Configuration file','pass','file appears to be configured properly as '+site_code_net)
            self.utilities.handle_json('network',{'hostname':site_code_net,'checkout_status':'pass'},'config_files')
        else:
            self.utilities.handle_print('Network Configuration file','fail','file not configured properly')
            self.utilities.handle_json('network',{'hostname':site_code_net,'checkout_status':'fail'},'config_files')

        imager_exists = os.path.isfile(self.imager_path)
        project_exists = os.path.isfile(self.project_path)

        ##### Imager conf file ######
        # get the required data from the file
        # also checks for proper SZA and camera mode
        if imager_exists:

            imager_conf_json['exists'] = True

            pattern = re.compile("Solar zenith angle = ...")
            for i, line in enumerate(open(self.imager_path)):
                for match in re.finditer(pattern, line):
                    sza = match.group()[-3:]
                    
            if sza == '102':
                correct_sza = True

            if correct_sza:
                self.utilities.handle_print('Imager.conf Correct SZA','pass','this is properly configured as 102')
                imager_conf_json['sza'] = 102

            else:
                self.utilities.handle_print('Imager.conf Correct SZA','fail','this should be configured as 102')
                imager_conf_json['sza'] = int(sza)

            pattern = re.compile("Mode unique ID = ....")
            for i, line in enumerate(open(self.imager_path)):
                for match in re.finditer(pattern, line):
                    camera_mode = match.group()[-4:]

            if camera_mode == '6300':
                correct_camera_mode = True

            if correct_camera_mode:
                self.utilities.handle_print('Imager.conf Correct Mode','pass','this is properly configured as 6300')
                imager_conf_json['camera_mode'] = 6300
            else:
                self.utilities.handle_print('Imager.conf Correct Mode','fail','this should be configured as 6300')
                imager_conf_json['camera_mode'] = int(camera_mode)


            pattern = re.compile("Site unique ID = [a-z][a-z][a-z][a-z]")
            for i, line in enumerate(open(self.imager_path)):
                for match in re.finditer(pattern, line):
                    site_code_imager = match.group()[-4:]

            imager_conf_json['site_uid'] = site_code_imager
            
            pattern = re.compile("Camera Serial Number = \d\d\d\d\d")
            for i, line in enumerate(open(self.imager_path)):
                for match in re.finditer(pattern, line):
                    imager_conf_serial = match.group()[-5:]

            imager_conf_json['camera_serial'] = imager_conf_serial

            # cross comparison between camera serial number and conf file serial number
            if camera_serial_number == imager_conf_serial:
                self.utilities.handle_print('Imager.conf file and Camera Serial Match','pass','these match, the serial number is '+camera_serial_number)
                self.utilities.handle_json('cross_comparison',{'camera_serial':True},'config_files')
            else:
                self.utilities.handle_print('Imager.conf file and Camera Serial Match','fail','these do not match, the camera serial number should be '+camera_serial_number)

            response = self.utilities.communicate(
                'ls -la ' + self.imager_directory + ' | grep "imager.conf"').split()
            imager_conf = response[-3] + '  ' + response[-2] + '  ' + response[-1]
            imager_conf_file = self.utilities.communicate(
                'sed -n "5,29p;41q" '+ self.imager_path)
            if self.veryverbose_mode:
                self.utilities.handle_print('Imager Configuration Symlink and file','pass','\n'+imager_conf+'\n'+imager_conf_file)
                
            else:
                self.utilities.handle_print('Imager Configuration Symlink and file','pass',imager_conf)
            
            imager_conf_json['symlink_source'] = imager_conf.split()[2]
            imager_conf_json['file_content'] = imager_conf_file
            imager_conf_json['checkout_status'] = 'pass'
                
        else:
            self.utilities.handle_print('Imager Configuration Symlink and file','fail',"Imager configuration file doesn't exist")
            imager_conf_json['symlink_source'] = 'N/A'
            imager_conf_json['file_content'] = 'N/A'
            imager_conf_json['exists'] = False
            imager_conf_json['checkout_status'] = 'fail'

        ##### Project conf file ######
        # get the required data from the file
        if project_exists:
            project_conf_json['exists'] = True
            pattern = re.compile("site unique ID = [a-z][a-z][a-z][a-z]")
            for i, line in enumerate(open(self.project_path)):
                for match in re.finditer(pattern, line):
                    site_code_project = match.group()[-4:]

            project_conf_json['site_uid'] = site_code_project

            pattern = re.compile("device unique ID = [a-z][a-z][a-z][a-z]-\d\d\d")
            for i, line in enumerate(open(self.project_path)):
                for match in re.finditer(pattern, line):
                    project_device_uid = match.group()

            project_conf_json['device_uid'] = project_device_uid

            response = self.utilities.communicate(
                'ls -la ' + self.project_directory + ' | grep "project.conf"').split()
            project_conf = response[-3] + '  ' + response[-2] + '  '+ response[-1]
            project_conf_file = self.utilities.communicate(
                'sed -n "2,15p;41q" ' + self.project_path)
            if self.veryverbose_mode:
                self.utilities.handle_print('Project Configuration Symlink and file','pass','\n'+project_conf+'\n'+project_conf_file)
            else:
                self.utilities.handle_print('Project Configuration Symlink and file','pass',project_conf)

            project_conf_json['symlink_source'] = project_conf.split()[2]
            project_conf_json['file_content'] = project_conf_file
            project_conf_json['checkout_status'] = 'pass' 

        else:
            self.utilities.handle_print('Project Configuration Symlink and file','fail',"Project configuration file doesn't exist")
            project_conf_json['symlink_source'] = 'N/A'
            project_conf_json['file_content'] = 'N/A'
            project_conf_json['exists'] = False
            project_conf_json['checkout_status'] = 'fail'  


        ### Check if matching results
        # checks that all the site codes are the same
        # checks that device UID is as expected from the checkout configuration file and camera return
        if site_code_hosts[0:4] == site_code_imager == site_code_project == site_code_official[0:4] and device_uid_official == project_device_uid:
            self.utilities.handle_print('Hosts, Imager.conf, and Project.conf Match','pass','these files are configured properly with each other')
            self.utilities.handle_json('cross_comparison',{'miss_matched_files':False,'checkout_status':True},'config_files')
        else:
            self.utilities.handle_print('Hosts, Imager.conf, and Project.conf Match','fail','these files are not configured properly with each other')
            self.utilities.handle_json('cross_comparison',{'miss_matched_files':True,'checkout_status':False},'config_files')
            if self.verbose_mode:
                self.utilities.print_write('   Expected Site Code -> '+site_code_official[0:4])
                self.utilities.print_write('   Hosts Site Code -> '+site_code_hosts[0:4])
                self.utilities.print_write('   Imager.conf Site Code -> '+site_code_imager)
                self.utilities.print_write('   Project.conf Site Code -> '+site_code_project)
                self.utilities.print_write('   Expected Device UID -> '+device_uid_official)
                self.utilities.print_write('   Project.conf Device UID ->'+project_device_uid)

        self.utilities.handle_json('imager.conf',imager_conf_json,'config_files')
        self.utilities.handle_json('project.conf',project_conf_json,'config_files')

        return