
from time import sleep

class imagerCheckout():
    """Class for testing camera and imager daemons"""

    utilities = None
    expose_path = None

    def __init__(self, utilities):
        self.utilities = utilities
        self.expose_path = utilities.EXPOSE_PATH

    ############################################
    # Method that takes picture with the Camera
    ############################################


    def check_camera(self):
        """run the check"""

        imager_expose_command = self.expose_path
        if self.utilities.DEVICE_UID == 'themis':
            imager_expose_command = imager_expose_command + ' MSEC=100'

        # turn on the camera
        response = self.utilities.communicate('power_control imager on')
        sleep(5)
        response = self.utilities.communicate(self.expose_path)
        sleep(1)
        if 'Error' in response:
            self.utilities.handle_print('Test Image', 'fail', response)
            self.utilities.handle_json('image_collection',{'test_image':'/tmp/test_image.pgm','checkout_status':'fail'})
            
        else:
            self.utilities.handle_print('Test Image', 'pass', 'Saved at /tmp/test_image.pgm')
            self.utilities.handle_json('image_collection',{'test_image':'/tmp/test_image.pgm','checkout_status':'pass'})

        self.utilities.communicate('power_control imager off')
        return

    def check_imager_daemons(self):
        """run the check"""

        # check running process to see if the proper daemons are running
        response = self.utilities.communicate('ps aux | grep imager_filed')
        if '/usr/local/imager/imager_filed' in response:
            self.utilities.handle_print('Imager_filed running', 'pass', 'Running on PID - ' + response.split()[1])
            self.utilities.handle_json('imager_filed',{'running':'pass','pid':response.split()[1],'checkout_status':'pass'},'processes')
        else:
            self.utilities.handle_print(
                'Imager_filed running',
                'fail',
                'The daemon does not appear to be running!')
            self.utilities.handle_json('imager_filed',{'running':'fail','pid':'N/A','checkout_status':'fail'},'processes')
            

        response = self.utilities.communicate('ps aux | grep imager_framed')
        if '/usr/local/imager/imager_framed' in response:
            self.utilities.handle_print('Imager_framed running', 'pass', 'Running on PID - ' + response.split()[1])
            self.utilities.handle_json('imager_framed',{'running':'pass','pid':response.split()[1],'checkout_status':'pass'},'processes')
        else:
            self.utilities.handle_print(
                'Imager_framed running',
                'fail',
                'The daemon does not appear to be running!')
            self.utilities.handle_json('imager_filed',{'running':'fail','pid':'N/A','checkout_status':'fail'},'processes')
            

        response = self.utilities.communicate('ps aux | grep imagerd')
        if '/usr/local/imager/imagerd' in response:
            self.utilities.handle_print('Imagerd running', 'pass', 'Running on PID - ' + response.split()[1])
            self.utilities.handle_json('imagerd',{'running':'pass','pid':response.split()[1],'checkout_status':'pass'},'processes')
        else:
            self.utilities.handle_print(
                'Imagerd running',
                'fail',
                'The daemon does not appear to be running!')
            self.utilities.handle_json('imagerd',{'running':'fail','pid':'N/A','checkout_status':'fail'},'processes')

        if self.utilities.DEVICE_UID == "rego":
            response = self.utilities.communicate('ps aux | grep imager_safetyd')
            if response == '':
                self.utilities.handle_print(
                    'Imager_safetyd running',
                    'fail',
                    'The daemon does not appear to be running!')
                self.utilities.handle_json('imager_safetyd',{'running':'fail','pid':'N/A','checkout_status':'fail'},'processes')
            else:
                self.utilities.handle_print('Imager_safetyd running', 'pass', 'Running on PID - ' + response.split()[1])
                self.utilities.handle_json('imager_safetyd',{'running':'pass','pid':response.split()[1],'checkout_status':'pass'},'processes')


        return