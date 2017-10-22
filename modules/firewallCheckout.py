
class firewallCheckout():
    """Class for testing firewall configuration"""

    utilities = None

    def __init__(self, utilities):
        self.utilities = utilities

    ##################################
    # Check the firewall
    ##################################

    def check_firewall(self):
        """run the check"""

        # Subnets allowed array
        if self.utilities.DEVICE_UID == 'rego':
            subnets_in_allowed = [''] * 3
            subnets_out_allowed = [''] * 3
        if self.utilities.DEVICE_UID == 'themis':
            subnets_in_allowed = [''] * 7
            subnets_out_allowed = [''] * 7

        # Test result bools
        firewall_host_in_good = True
        firewall_host_out_good = True

        # Check the host in lines
        response = self.utilities.communicate('/sbin/iptables --list host-in -n')
        host_in = response.splitlines()

        if self.utilities.DEVICE_UID == 'rego':
            if len(host_in) == 5:

                # Check line one of configuration
                host_in_one = host_in[2].split()
                subnets_in_allowed[0] = host_in_one[3]
                if host_in_one[3] != '136.159.0.0/16':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 1','fail','expected "136.159.0.0/16" but found "'+host_in_one[3]+'"')

                # Check line two of configuration
                host_in_two = host_in[3].split()
                subnets_in_allowed[1] = host_in_two[3]
                if host_in_two[3] != '192.168.63.1':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 2','fail','expected "192.168.63.1" but found "'+host_in_two[3]+'"')
                
                # Check line three of configuration
                host_in_three = host_in[4].split()
                subnets_in_allowed[2] = host_in_three[3]
                if host_in_three[3] != '192.168.63.0/24':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 3','fail','expected "192.168.63.0/24" but found "'+host_in_three[3]+'"')
            else:
                firewall_host_in_good = False

        if self.utilities.DEVICE_UID == 'themis':
            if len(host_in) == 9:

                # Check line one of configuration
                host_in_one = host_in[2].split()
                subnets_in_allowed[0] = host_in_one[3]
                if host_in_one[3] != '136.159.142.0/25':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 1','fail','expected "136.159.142.0/25" but found "'+host_in_one[3]+'"')

                # Check line two of configuration
                host_in_two = host_in[3].split()
                subnets_in_allowed[1] = host_in_two[3]
                if host_in_two[3] != '136.159.51.0/24':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 2','fail','expected "136.159.51.0/24" but found "'+host_in_two[3]+'"')
                
                # Check line three of configuration
                host_in_three = host_in[4].split()
                subnets_in_allowed[2] = host_in_three[3]
                if host_in_three[3] != '128.32.18.0/24':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 3','fail','expected "128.32.18.0/24" but found "'+host_in_three[3]+'"')

                # Check line three of configuration
                host_in_four = host_in[5].split()
                subnets_in_allowed[3] = host_in_four[3]
                if host_in_four[3] != '128.32.147.0/24':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 3','fail','expected "128.32.147.0/24" but found "'+host_in_four[3]+'"')

                # Check line three of configuration
                host_in_five = host_in[6].split()
                subnets_in_allowed[4] = host_in_five[3]
                if host_in_five[3] != '128.97.94.0/24':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 3','fail','expected "128.97.94.0/24" but found "'+host_in_five[3]+'"')

                # Check line three of configuration
                host_in_six = host_in[7].split()
                subnets_in_allowed[5] = host_in_six[3]
                if host_in_six[3] != '136.159.51.254':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 3','fail','expected "136.159.51.254" but found "'+host_in_six[3]+'"')

                # Check line three of configuration
                host_in_seven = host_in[8].split()
                subnets_in_allowed[6] = host_in_seven[3]
                if host_in_seven[3] != '136.159.51.0/24':
                    firewall_host_in_good = False
                    self.utilities.handle_print('Firewall Host In Line 3','fail','expected "136.159.51.0/24" but found "'+host_in_seven[3]+'"')
            else:
                firewall_host_in_good = False

        # Check the host out lines
        response = self.utilities.communicate('/sbin/iptables --list host-out -n')
        host_out = response.splitlines()

        if self.utilities.DEVICE_UID == 'rego':
            if len(host_out) == 5:

            # Check line one of configuration
                host_out_one = host_out[2].split()
                subnets_out_allowed[0] = host_out_one[4]
                if host_out_one[4] != '136.159.0.0/16':
                    firewall_host_out_good = False
                    self.utilities.handle_print('Firewall Host Out Line 1','fail','expected "136.159.0.0/16" but found "'+host_out_one[4]+'"')

                # Check line two of configuration
                host_out_two = host_out[3].split()
                subnets_out_allowed[1] = host_out_two[4]
                if host_out_two[4] != '192.168.63.1':
                    firewall_host_out_good = False
                    self.utilities.handle_print('Firewall Host Out Line 2','fail','expected "192.168.63.1" but found "'+host_out_two[4]+'"')

                # Check line three of configuration
                host_out_three = host_out[4].split()
                subnets_out_allowed[2] = host_out_three[4]
                if host_out_three[4] != '192.168.63.0/24':
                    firewall_host_out_good = False
                    self.utilities.handle_print('Firewall Host Out Line 3','fail','expected "192.168.63.0/24" but found "'+host_out_three[4]+'"')
            else:
                firewall_host_out_good = False

        if self.utilities.DEVICE_UID == 'themis':
                if len(host_out) == 9:

                    # Check line one of configuration
                    host_out_one = host_in[2].split()
                    subnets_out_allowed[0] = host_out_one[3]
                    if host_out_one[3] != '136.159.142.0/25':
                        firewall_host_out_good = False
                        self.utilities.handle_print('Firewall Host In Line 1','fail','expected "136.159.142.0/25" but found "'+host_out_one[3]+'"')

                    # Check line two of configuration
                    host_out_two = host_in[3].split()
                    subnets_out_allowed[1] = host_out_two[3]
                    if host_out_two[3] != '136.159.51.0/24':
                        firewall_host_out_good = False
                        self.utilities.handle_print('Firewall Host In Line 2','fail','expected "136.159.51.0/24" but found "'+host_out_two[3]+'"')
                    
                    # Check line three of configuration
                    host_out_three = host_in[4].split()
                    subnets_out_allowed[2] = host_out_three[3]
                    if host_out_three[3] != '128.32.18.0/24':
                        firewall_host_out_good = False
                        self.utilities.handle_print('Firewall Host In Line 3','fail','expected "128.32.18.0/24" but found "'+host_out_three[3]+'"')

                    # Check line three of configuration
                    host_out_four = host_in[5].split()
                    subnets_out_allowed[3] = host_out_four[3]
                    if host_out_four[3] != '128.32.147.0/24':
                        firewall_host_out_good = False
                        self.utilities.handle_print('Firewall Host In Line 3','fail','expected "128.32.147.0/24" but found "'+host_out_four[3]+'"')

                    # Check line three of configuration
                    host_out_five = host_in[6].split()
                    subnets_out_allowed[4] = host_out_five[3]
                    if host_out_five[3] != '128.97.94.0/24':
                        firewall_host_out_good = False
                        self.utilities.handle_print('Firewall Host In Line 3','fail','expected "128.97.94.0/24" but found "'+host_out_five[3]+'"')

                    # Check line three of configuration
                    host_out_six = host_in[7].split()
                    subnets_out_allowed[5] = host_out_six[3]
                    if host_out_six[3] != '136.159.51.254':
                        firewall_host_out_good = False
                        self.utilities.handle_print('Firewall Host In Line 3','fail','expected "136.159.51.254" but found "'+host_out_six[3]+'"')

                    # Check line three of configuration
                    host_out_seven = host_in[8].split()
                    subnets_out_allowed[6] = host_out_seven[3]
                    if host_out_seven[3] != '136.159.51.0/24':
                        firewall_host_out_good = False
                        self.utilities.handle_print('Firewall Host In Line 3','fail','expected "136.159.51.0/24" but found "'+host_out_seven[3]+'"')

                else:
                    firewall_host_out_good = False

        
        # Print the results of the test
        if firewall_host_in_good:
            self.utilities.handle_print('Firewall Host In','pass','this is configured properly')
            self.utilities.handle_json('subnets_inbound',{'subnets_allowed':subnets_in_allowed,'checkout_status':'pass'},'firewall')
        else:
            self.utilities.handle_print('Firewall Host In','fail','check this "iptables --list host-in -n"')
            self.utilities.handle_json('subnets_inbound',{'subnets_allowed':subnets_in_allowed,'checkout_status':'fail'},'firewall')

        if firewall_host_out_good:
            self.utilities.handle_print('Firewall Host Out','pass','this is configured properly')
            self.utilities.handle_json('subnets_outbound',{'subnets_allowed':subnets_out_allowed,'checkout_status':'pass'},'firewall')
        else:
            self.utilities.handle_print('Firewall Host Out','fail','check this "iptables --list host-out -n"')
            self.utilities.handle_json('subnets_outbound',{'subnets_allowed':subnets_out_allowed,'checkout_status':'fail'},'firewall')


        return