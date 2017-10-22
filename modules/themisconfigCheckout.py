import os
import re

class themisconfigCheckout():
    """Class for testing configuration files"""

    verbose_mode = False
    veryverbose_mode = False
    utilities = None
    imager_directory = "/usr/local/imager/"
    project_directory = "/usr/local/site/"
    imager_path = "/usr/local/imager/imager.conf"
    project_path = "/usr/local/site/current"
    hosts_path = "/etc/hosts"
    network_path = "/etc/sysconfig/network"


    def __init__(self,verbose,veryverbose,utilities):
        self.verbose_mode = verbose
        self.veryverbose_mode = veryverbose
        self.utilities = utilities

    ######################################################
    # Method that checks the image and site configuration
    ######################################################


    def check_configuration(self):
        """run the check"""

        # Variables used in this check
        site_code_official = self.utilities.SITE_UID
        site_code_imager = ''
        site_code_hosts = ''
        site_code_net = ''
        site_code_project = ''

        imager_conf_json = {}
        project_conf_json = {}

        #### Host conf file #####
        # get the required data from the file
        pattern = re.compile("127.0.0.1\s\s\s\s[a-z][a-z][a-z][a-z]")
        for i, line in enumerate(open(self.hosts_path)):
            for match in re.finditer(pattern, line):
                site_code_hosts = match.group()[-4:]
        if site_code_official == site_code_hosts:
            self.utilities.handle_print('Hosts Configuration file','pass','file appears to be configured properly as '+site_code_hosts)
            self.utilities.handle_json('hosts',{'hostname':site_code_hosts,'checkout_status':'pass'},'config_files')

        else:
            self.utilities.handle_print('Hosts Configuration file','fail','file not configured properly')
            self.utilities.handle_json('hosts',{'hostname':'N/A','checkout_status':'fail'},'config_files')
            site_code_hosts = ''

        #### Network conf file #####
        # get the required data from the file
        counter = 0
        pattern = re.compile("HOSTNAME=[a-z][a-z][a-z][a-z]")
        for i, line in enumerate(open(self.network_path)):
            for match in re.finditer(pattern, line):
                site_code_net = match.group()[-4:]
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

            pattern = re.compile("site unique ID = [a-z][a-z][a-z][a-z]")
            for i, line in enumerate(open(self.imager_path)):
                for match in re.finditer(pattern, line):
                    site_code_imager = match.group()[-4:]

            imager_conf_json['site_uid'] = site_code_imager


            response = self.utilities.communicate(
                'ls -la ' + self.imager_directory + ' | grep "imager.conf"').split()
            imager_conf = response[-3] + '  ' + response[-2] + '  ' + response[-1]
            if self.veryverbose_mode:
                self.utilities.handle_print('Imager Configuration Symlink and file','pass','\n'+imager_conf)
            
            imager_conf_json['symlink_source'] = imager_conf.split()[2]
            imager_conf_json['checkout_status'] = 'pass'
                
        else:
            self.utilities.handle_print('Imager Configuration Symlink and file','fail',"Imager configuration file doesn't exist")
            imager_conf_json['symlink_source'] = 'N/A'
            imager_conf_json['exists'] = False
            imager_conf_json['checkout_status'] = 'fail'

        ##### Project conf file ######
        # get the required data from the file
        if project_exists:
            project_conf_json['exists'] = True
            pattern = re.compile("site unique ID = [aA-zZ][aA-zZ][aA-zZ][aA-zZ]")
            for i, line in enumerate(open(self.project_path)):
                for match in re.finditer(pattern, line):
                    site_code_project = match.group()[-4:].lower()

            project_conf_json['site_uid'] = site_code_project

            response = self.utilities.communicate(
                'ls -la ' + self.project_directory + ' | grep "current"').split()
            project_conf = response[-3] + '  ' + response[-2] + '  '+ response[-1]
            project_conf_file = self.utilities.communicate(
                'cat ' + self.project_path)
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
        if site_code_hosts == site_code_imager == site_code_project == site_code_official:
            self.utilities.handle_print('Hosts, Imager.conf, and Project.conf Match','pass','these files are configured properly with each other')
            self.utilities.handle_json('cross_comparison',{'miss_matched_files':False,'checkout_status':True},'config_files')
        else:
            self.utilities.handle_print('Hosts, Imager.conf, and Project.conf Match','fail','these files are not configured properly with each other')
            self.utilities.handle_json('cross_comparison',{'miss_matched_files':True,'checkout_status':False},'config_files')
            if self.verbose_mode:
                self.utilities.print_write('   Expected Site Code -> '+site_code_official)
                self.utilities.print_write('   Hosts Site Code -> '+site_code_hosts)
                self.utilities.print_write('   Imager.conf Site Code -> '+site_code_imager)
                self.utilities.print_write('   Current File Site Code -> '+site_code_project)

        self.utilities.handle_json('imager.conf',imager_conf_json,'config_files')
        self.utilities.handle_json('project.conf',project_conf_json,'config_files')

        return