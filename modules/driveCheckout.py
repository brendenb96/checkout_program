import time
import os

class driveCheckout():
    """Class for testing external drives"""

    utilities = None

    def __init__(self, utilities):
        self.utilities = utilities

    def check_drives(self):
        """run the drive check"""

        # turn on the external drives
        self.utilities.communicate('power_control aux on')
        time.sleep(18)  # Waits for drives to be turned on and ready

        # mount the transfer drive and get inventory number
        response = self.utilities.communicate('mount /mnt/transfer')
        time.sleep(2)
        if os.listdir('/mnt/transfer'):  # not empty
            inv_filename = self.utilities.find_file('*disk*', '/mnt/transfer')
            if inv_filename:
                inv_file = open(inv_filename[0], 'r')
                inventory_number = inv_file.read().rstrip()
                inv_file.close()
            else:
                inventory_number = 'Could not find inventory number'

            response = self.utilities.communicate('df -hl /mnt/transfer')
            transfer_usage = response.split()[11]

            self.utilities.handle_print('Transfer Drive Check', 'pass', inventory_number)
            self.utilities.handle_json('transfer',{'mounts':True,'inventory_number':inventory_number,'usage':transfer_usage,'checkout_status':'pass'},'external_drives')
            self.utilities.communicate('umount /mnt/transfer')
            time.sleep(2)
        else:
            self.utilities.handle_print('Transfer Drive Check', 'fail', 'Could not mount the drive')
            self.utilities.handle_json('transfer',{'mounts':False,'inventory_number':'N/A','usage':'N/A','checkout_status':'fail'},'external_drives')

        # mount the backup drive and get the inventory number
        response = self.utilities.communicate('mount /mnt/backup')
        time.sleep(2)
        if os.listdir('/mnt/backup'):  # not empty
            inv_filename = self.utilities.find_file('*disk*', '/mnt/backup')
            if inv_filename:
                inv_file = open(inv_filename[0], 'r')
                inventory_number = inv_file.read().rstrip()
                inv_file.close()
            else:
                inventory_number = 'Could not find inventory number'

            response = self.utilities.communicate('df -hl /mnt/backup')
            backup_usage = response.split()[11]

            self.utilities.handle_print('Backup Drive Check', 'pass', inventory_number)
            self.utilities.handle_json('backup',{'mounts':True,'inventory_number':inventory_number,'usage':backup_usage,'checkout_status':'pass'},'external_drives')
            self.utilities.communicate('umount /mnt/backup')
            time.sleep(2)
        else:
            self.utilities.handle_print('Backup Drive Check', 'fail', 'Could not mount the drive')
            self.utilities.handle_json('backup',{'mounts':False,'inventory_number':'N/A','usage':'N/A','checkout_status':'fail'},'external_drives')

        self.utilities.communicate('power_control aux off')
        time.sleep(1)
        return