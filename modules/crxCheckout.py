
import datetime
from time import sleep

class crxCheckout():
    """Class for checking cr10x"""

    utilities = None

    def __init__(self, utilities):
        self.utilities = utilities

    def check_crx(self):
        """run the cr10x check"""
        CRX_GOOD = True
        JSON_DATA = {}
        SLEEP_TIME = 0.5

        response = self.utilities.communicate("crx-rdloc 1").rstrip()

        if response.rstrip() == '':
            self.utilities.handle_print('cr10x','fail','Could not communicate with CR10X')
            self.utilities.handle_json('cr10x',{'checkout_status':'fail'})
            return

        year = int(self.utilities.communicate("crx-rdloc 1").rstrip()[:-2])
        sleep(SLEEP_TIME)
        battvolt = float(self.utilities.communicate("crx-rdloc 6").rstrip())
        sleep(SLEEP_TIME)
        int_temp = float(self.utilities.communicate("crx-rdloc 7").rstrip())
        sleep(SLEEP_TIME)
        ext_temp = float(self.utilities.communicate("crx-rdloc 8").rstrip())
        sleep(SLEEP_TIME)
        ce_temp = float(self.utilities.communicate("crx-rdloc 9").rstrip())
        sleep(SLEEP_TIME)
        asi_temp = float(self.utilities.communicate("crx-rdloc 10").rstrip())
        sleep(SLEEP_TIME)
        vline = float(self.utilities.communicate("crx-rdloc 11").rstrip())
        sleep(SLEEP_TIME)
        asi_duty = float(self.utilities.communicate("crx-rdloc 12").rstrip())
        sleep(SLEEP_TIME)  		
        ce_duty = float(self.utilities.communicate("crx-rdloc 13").rstrip())
        sleep(SLEEP_TIME) 	
        ac_duty = float(self.utilities.communicate("crx-rdloc 14").rstrip())
        sleep(SLEEP_TIME)   		 
        version = float(self.utilities.communicate("crx-rdloc 16").rstrip())
        sleep(SLEEP_TIME) 		
        ASI_TLo = float(self.utilities.communicate("crx-rdloc 17").rstrip())
        sleep(SLEEP_TIME)  	
        ASI_THys = float(self.utilities.communicate("crx-rdloc 18").rstrip())
        sleep(SLEEP_TIME) 		
        CE_TLo = float(self.utilities.communicate("crx-rdloc 19").rstrip())
        sleep(SLEEP_TIME) 
        CE_THys = float(self.utilities.communicate("crx-rdloc 20").rstrip())
        sleep(SLEEP_TIME)
        SYS_TLo = float(self.utilities.communicate("crx-rdloc 21").rstrip())
        sleep(SLEEP_TIME)	
        SYS_TLHys = float(self.utilities.communicate("crx-rdloc 22").rstrip())
        sleep(SLEEP_TIME) 
        SYS_THi = float(self.utilities.communicate("crx-rdloc 23").rstrip())
        sleep(SLEEP_TIME)  		
        SYS_THHys = float(self.utilities.communicate("crx-rdloc 24").rstrip())
        sleep(SLEEP_TIME)	
        SYS_VLo = float(self.utilities.communicate("crx-rdloc 25").rstrip())
        sleep(SLEEP_TIME) 	
        SYS_VHys = float(self.utilities.communicate("crx-rdloc 26").rstrip())
        sleep(SLEEP_TIME) 	
        CE_THi = float(self.utilities.communicate("crx-rdloc 28").rstrip())
        sleep(SLEEP_TIME)   
        CE_THiHys = float(self.utilities.communicate("crx-rdloc 29").rstrip())
        sleep(SLEEP_TIME)  	
        ce_humid = float(self.utilities.communicate("crx-rdloc 30").rstrip())
        sleep(SLEEP_TIME) 		  	
        BattChg = float(self.utilities.communicate("crx-rdloc 34").rstrip())
        sleep(SLEEP_TIME)  
        sol_imon = float(self.utilities.communicate("crx-rdloc 47").rstrip())
        sleep(SLEEP_TIME)   	
        sys_imon = float(self.utilities.communicate("crx-rdloc 48").rstrip())
        sleep(SLEEP_TIME)  		
        asi_vmon = float(self.utilities.communicate("crx-rdloc 50").rstrip())
        sleep(SLEEP_TIME)  		
        pwr_used = float(self.utilities.communicate("crx-rdloc 52").rstrip())
        sleep(SLEEP_TIME)  		 		
        pc_vmon = float(self.utilities.communicate("crx-rdloc 54").rstrip())
        sleep(SLEEP_TIME)    		
        stl_vmon = float(self.utilities.communicate("crx-rdloc 55").rstrip())
        sleep(SLEEP_TIME)

        state_sys = float(self.utilities.communicate("crx-rdloc 39").rstrip())
        sleep(SLEEP_TIME)
        VOK = float(self.utilities.communicate("crx-rdloc 43").rstrip())
        sleep(SLEEP_TIME)
        TOK = float(self.utilities.communicate("crx-rdloc 44").rstrip())
        sleep(SLEEP_TIME)

        if year == datetime.datetime.now().year:
            JSON_DATA['year'] = {'value' : year ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - year: ','pass','Value is: ' + str(year))
        else:
            JSON_DATA['year'] = {'value' : year ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - year: ','warning','Value is: ' + str(year))
            CRX_GOOD = False

        if battvolt >= self.utilities.CRX_VALS.getfloat('crx_min','battvolt') and battvolt <= self.utilities.CRX_VALS.getfloat('crx_max','battvolt'):
            JSON_DATA['battvolt'] = {'value' : battvolt ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - battvolt: ','pass','Value is: ' + str(battvolt))
        else:
            JSON_DATA['battvolt'] = {'value' : battvolt ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - battvolt: ','warning','Value is: ' + str(battvolt))
            CRX_GOOD = False

        if int_temp >= self.utilities.CRX_VALS.getfloat('crx_min','int_temp') and int_temp <= self.utilities.CRX_VALS.getfloat('crx_max','int_temp'):
            JSON_DATA['int_temp'] = {'value' : int_temp ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - int_temp: ','pass','Value is: ' + str(int_temp))
        else:
            JSON_DATA['int_temp'] = {'value' : int_temp ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - int_temp: ','warning','Value is: ' + str(int_temp))
            CRX_GOOD = False
        
        if ext_temp >= self.utilities.CRX_VALS.getfloat('crx_min','ext_temp') and ext_temp <= self.utilities.CRX_VALS.getfloat('crx_max','ext_temp'):
            JSON_DATA['ext_temp'] = {'value' : ext_temp ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - ext_temp: ','pass','Value is: ' + str(ext_temp))
        else:
            JSON_DATA['ext_temp'] = {'value' : ext_temp ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - ext_temp: ','warning','Value is: ' + str(ext_temp))
            CRX_GOOD = False

        if ce_temp >= self.utilities.CRX_VALS.getfloat('crx_min','ce_temp') and ce_temp <= self.utilities.CRX_VALS.getfloat('crx_max','ce_temp'):
            JSON_DATA['ce_temp'] = {'value' : ce_temp ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - ce_temp: ','pass','Value is: ' + str(ce_temp))
        else:
            JSON_DATA['ce_temp'] = {'value' : ce_temp ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - ce_temp: ','warning','Value is: ' + str(ce_temp))
            CRX_GOOD = False

        if asi_temp >= self.utilities.CRX_VALS.getfloat('crx_min','asi_temp') and asi_temp <= self.utilities.CRX_VALS.getfloat('crx_max','asi_temp'):
            JSON_DATA['asi_temp'] = {'value' : asi_temp ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - asi_temp: ','pass','Value is: ' + str(asi_temp))
        else:
            JSON_DATA['asi_temp'] = {'value' : asi_temp ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - asi_temp: ','warning','Value is: ' + str(asi_temp))
            CRX_GOOD = False

        if vline >= self.utilities.CRX_VALS.getfloat('crx_min','vline') and vline <= self.utilities.CRX_VALS.getfloat('crx_max','vline'):
            JSON_DATA['vline'] = {'value' : vline ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - vline: ','pass','Value is: ' + str(vline))
        else:
            JSON_DATA['vline'] = {'value' : vline ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - vline: ','warning','Value is: ' + str(vline))
            CRX_GOOD = False

        if asi_duty >= self.utilities.CRX_VALS.getfloat('crx_min','asi_duty') and asi_duty <= self.utilities.CRX_VALS.getfloat('crx_max','asi_duty'):
            JSON_DATA['asi_duty'] = {'value' : asi_duty ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - asi_duty: ','pass','Value is: ' + str(asi_duty))
        else:
            JSON_DATA['asi_duty'] = {'value' : asi_duty ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - asi_duty: ','warning','Value is: ' + str(asi_duty))
            CRX_GOOD = False

        if ce_duty >= self.utilities.CRX_VALS.getfloat('crx_min','ce_duty') and ce_duty <= self.utilities.CRX_VALS.getfloat('crx_max','ce_duty'):
            JSON_DATA['ce_duty'] = {'value' : ce_duty ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - ce_duty: ','pass','Value is: ' + str(ce_duty))
        else:
            JSON_DATA['ce_duty'] = {'value' : ce_duty ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - ce_duty: ','warning','Value is: ' + str(ce_duty))
            CRX_GOOD = False

        if ac_duty >= self.utilities.CRX_VALS.getfloat('crx_min','ac_duty') and ac_duty <= self.utilities.CRX_VALS.getfloat('crx_max','ac_duty'):
            JSON_DATA['ac_duty'] = {'value' : ac_duty ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - ac_duty: ','pass','Value is: ' + str(ac_duty))
        else:
            JSON_DATA['ac_duty'] = {'value' : ac_duty ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - ac_duty: ','warning','Value is: ' + str(ac_duty))
            CRX_GOOD = False

        if version >= self.utilities.CRX_VALS.getfloat('crx_min','version') and version <= self.utilities.CRX_VALS.getfloat('crx_max','version'):
            JSON_DATA['version'] = {'value' : version ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - version: ','pass','Value is: ' + str(version))
        else:
            JSON_DATA['version'] = {'value' : version ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - version: ','warning','Value is: ' + str(version))
            CRX_GOOD = False

        if ASI_TLo >= self.utilities.CRX_VALS.getfloat('crx_min','ASI_TLo') and ASI_TLo <= self.utilities.CRX_VALS.getfloat('crx_max','ASI_TLo'):
            JSON_DATA['ASI_TLo'] = {'value' : ASI_TLo ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - ASI_TLo: ','pass','Value is: ' + str(ASI_TLo))
        else:
            JSON_DATA['ASI_TLo'] = {'value' : ASI_TLo ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - ASI_TLo: ','warning','Value is: ' + str(ASI_TLo))
            CRX_GOOD = False

        if ASI_THys >= self.utilities.CRX_VALS.getfloat('crx_min','ASI_THys') and ASI_THys <= self.utilities.CRX_VALS.getfloat('crx_max','ASI_THys'):
            JSON_DATA['ASI_THys'] = {'value' : ASI_THys ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - ASI_THys: ','pass','Value is: ' + str(ASI_THys))
        else:
            JSON_DATA['ASI_THys'] = {'value' : ASI_THys ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - ASI_THys: ','warning','Value is: ' + str(ASI_THys))
            CRX_GOOD = False

        if CE_THys >= self.utilities.CRX_VALS.getfloat('crx_min','CE_THys') and CE_THys <= self.utilities.CRX_VALS.getfloat('crx_max','CE_THys'):
            JSON_DATA['CE_THys'] = {'value' : CE_THys ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - CE_THys: ','pass','Value is: ' + str(CE_THys))
        else:
            JSON_DATA['CE_THys'] = {'value' : CE_THys ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - CE_THys: ','warning','Value is: ' + str(CE_THys))
            CRX_GOOD = False

        if CE_TLo >= self.utilities.CRX_VALS.getfloat('crx_min','CE_TLo') and CE_TLo <= self.utilities.CRX_VALS.getfloat('crx_max','CE_TLo'):
            JSON_DATA['CE_TLo'] = {'value' : CE_TLo ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - CE_TLo: ','pass','Value is: ' + str(CE_TLo))
        else:
            JSON_DATA['CE_TLo'] = {'value' : CE_TLo ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - CE_TLo: ','warning','Value is: ' + str(CE_TLo))
            CRX_GOOD = False

        if SYS_TLo >= self.utilities.CRX_VALS.getfloat('crx_min','SYS_TLo') and SYS_TLo <= self.utilities.CRX_VALS.getfloat('crx_max','SYS_TLo'):
            JSON_DATA['SYS_TLo'] = {'value' : SYS_TLo ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - SYS_TLo: ','pass','Value is: ' + str(SYS_TLo))
        else:
            JSON_DATA['SYS_TLo'] = {'value' : SYS_TLo ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - SYS_TLo: ','warning','Value is: ' + str(SYS_TLo))
            CRX_GOOD = False

        if SYS_TLHys >= self.utilities.CRX_VALS.getfloat('crx_min','SYS_TLHys') and SYS_TLHys <= self.utilities.CRX_VALS.getfloat('crx_max','SYS_TLHys'):
            JSON_DATA['SYS_TLHys'] = {'value' : SYS_TLHys ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - SYS_TLHys: ','pass','Value is: ' + str(SYS_TLHys))
        else:
            JSON_DATA['SYS_TLHys'] = {'value' : SYS_TLHys ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - SYS_TLHys: ','warning','Value is: ' + str(SYS_TLHys))
            CRX_GOOD = False

        if SYS_THi >= self.utilities.CRX_VALS.getfloat('crx_min','SYS_THi') and SYS_THi <= self.utilities.CRX_VALS.getfloat('crx_max','SYS_THi'):
            JSON_DATA['SYS_THi'] = {'value' : SYS_THi ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - SYS_THi: ','pass','Value is: ' + str(SYS_THi))
        else:
            JSON_DATA['SYS_THi'] = {'value' : SYS_THi ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - SYS_THi: ','warning','Value is: ' + str(SYS_THi))
            CRX_GOOD = False
        
        if SYS_THHys >= self.utilities.CRX_VALS.getfloat('crx_min','SYS_THHys') and SYS_THHys <= self.utilities.CRX_VALS.getfloat('crx_max','SYS_THHys'):
            JSON_DATA['SYS_THHys'] = {'value' : SYS_THHys ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - SYS_THHys: ','pass','Value is: ' + str(SYS_THHys))
        else:
            JSON_DATA['SYS_THHys'] = {'value' : SYS_THHys ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - SYS_THHys: ','warning','Value is: ' + str(SYS_THHys))
            CRX_GOOD = False

        if SYS_VLo >= self.utilities.CRX_VALS.getfloat('crx_min','SYS_VLo') and SYS_VLo <= self.utilities.CRX_VALS.getfloat('crx_max','SYS_VLo'):
            JSON_DATA['SYS_VLo'] = {'value' : SYS_VLo ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - SYS_VLo: ','pass','Value is: ' + str(SYS_VLo))
        else:
            JSON_DATA['SYS_VLo'] = {'value' : SYS_VLo ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - SYS_VLo: ','warning','Value is: ' + str(SYS_VLo))
            CRX_GOOD = False

        if SYS_VHys >= self.utilities.CRX_VALS.getfloat('crx_min','SYS_VHys') and SYS_VHys <= self.utilities.CRX_VALS.getfloat('crx_max','SYS_VHys'):
            JSON_DATA['SYS_VHys'] = {'value' : SYS_VHys ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - SYS_VHys: ','pass','Value is: ' + str(SYS_VHys))
        else:
            JSON_DATA['SYS_VHys'] = {'value' : SYS_VHys ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - SYS_VHys: ','warning','Value is: ' + str(SYS_VHys))
            CRX_GOOD = False

        if CE_THi >= self.utilities.CRX_VALS.getfloat('crx_min','CE_THi') and CE_THi <= self.utilities.CRX_VALS.getfloat('crx_max','CE_THi'):
            JSON_DATA['CE_THi'] = {'value' : CE_THi ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - CE_THi: ','pass','Value is: ' + str(CE_THi))
        else:
            JSON_DATA['CE_THi'] = {'value' : CE_THi ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - CE_THi: ','warning','Value is: ' + str(CE_THi))
            CRX_GOOD = False

        if CE_THiHys >= self.utilities.CRX_VALS.getfloat('crx_min','CE_THiHys') and CE_THiHys <= self.utilities.CRX_VALS.getfloat('crx_max','CE_THiHys'):
            JSON_DATA['CE_THiHys'] = {'value' : CE_THiHys ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - CE_THiHys: ','pass','Value is: ' + str(CE_THiHys))
        else:
            JSON_DATA['CE_THiHys'] = {'value' : CE_THiHys ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - CE_THiHys: ','warning','Value is: ' + str(CE_THiHys))
            CRX_GOOD = False

        if ce_humid >= self.utilities.CRX_VALS.getfloat('crx_min','ce_humid') and ce_humid <= self.utilities.CRX_VALS.getfloat('crx_max','ce_humid'):
            JSON_DATA['ce_humid'] = {'value' : ce_humid ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - ce_humid: ','pass','Value is: ' + str(ce_humid))
        else:
            JSON_DATA['ce_humid'] = {'value' : ce_humid ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - ce_humid: ','warning','Value is: ' + str(ce_humid))
            CRX_GOOD = False
        
        if BattChg >= self.utilities.CRX_VALS.getfloat('crx_min','BattChg') and BattChg <= self.utilities.CRX_VALS.getfloat('crx_max','BattChg'):
            JSON_DATA['BattChg'] = {'value' : BattChg ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - BattChg: ','pass','Value is: ' + str(BattChg))
        else:
            JSON_DATA['BattChg'] = {'value' : BattChg ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - BattChg: ','warning','Value is: ' + str(BattChg))
            CRX_GOOD = False

        if sol_imon >= self.utilities.CRX_VALS.getfloat('crx_min','sol_imon') and sol_imon <= self.utilities.CRX_VALS.getfloat('crx_max','sol_imon'):
            JSON_DATA['sol_imon'] = {'value' : sol_imon ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - sol_imon: ','pass','Value is: ' + str(sol_imon))
        else:
            JSON_DATA['sol_imon'] = {'value' : sol_imon ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - sol_imon: ','warning','Value is: ' + str(sol_imon))
            CRX_GOOD = False

        if sys_imon >= self.utilities.CRX_VALS.getfloat('crx_min','sys_imon') and sys_imon <= self.utilities.CRX_VALS.getfloat('crx_max','sys_imon'):
            JSON_DATA['sys_imon'] = {'value' : sys_imon ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - sys_imon: ','pass','Value is: ' + str(sys_imon))
        else:
            JSON_DATA['sys_imon'] = {'value' : sys_imon ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - sys_imon: ','warning','Value is: ' + str(sys_imon))
            CRX_GOOD = False

        if asi_vmon >= self.utilities.CRX_VALS.getfloat('crx_min','asi_vmon') and asi_vmon <= self.utilities.CRX_VALS.getfloat('crx_max','asi_vmon'):
            JSON_DATA['asi_vmon'] = {'value' : asi_vmon ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - asi_vmon: ','pass','Value is: ' + str(asi_vmon))
        else:
            JSON_DATA['asi_vmon'] = {'value' : asi_vmon ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - asi_vmon: ','warning','Value is: ' + str(asi_vmon))
            CRX_GOOD = False

        if pwr_used >= self.utilities.CRX_VALS.getfloat('crx_min','pwr_used') and pwr_used <= self.utilities.CRX_VALS.getfloat('crx_max','pwr_used'):
            JSON_DATA['pwr_used'] = {'value' : pwr_used ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - pwr_used: ','pass','Value is: ' + str(pwr_used))
        else:
            JSON_DATA['pwr_used'] = {'value' : pwr_used ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - pwr_used: ','warning','Value is: ' + str(pwr_used))
            CRX_GOOD = False

        if pc_vmon >= self.utilities.CRX_VALS.getfloat('crx_min','pc_vmon') and pc_vmon <= self.utilities.CRX_VALS.getfloat('crx_max','pc_vmon'):
            JSON_DATA['pc_vmon'] = {'value' : pc_vmon ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - pc_vmon: ','pass','Value is: ' + str(pc_vmon))
        else:
            JSON_DATA['pc_vmon'] = {'value' : pc_vmon ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - pc_vmon: ','warning','Value is: ' + str(pc_vmon))
            CRX_GOOD = False

        if stl_vmon >= self.utilities.CRX_VALS.getfloat('crx_min','stl_vmon') and stl_vmon <= self.utilities.CRX_VALS.getfloat('crx_max','stl_vmon'):
            JSON_DATA['stl_vmon'] = {'value' : stl_vmon ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - stl_vmon: ','pass','Value is: ' + str(stl_vmon))
        else:
            JSON_DATA['stl_vmon'] = {'value' : stl_vmon ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - stl_vmon: ','warning','Value is: ' + str(stl_vmon))
            CRX_GOOD = False

        if state_sys == 1:
            JSON_DATA['state_sys'] = {'value' : state_sys ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - state_sys: ','pass','Value is: ' + str(state_sys))
        else:
            JSON_DATA['state_sys'] = {'value' : state_sys ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - state_sys: ','fail','Value is: ' + str(state_sys))
            CRX_GOOD = False

        if VOK == 1.0:
            JSON_DATA['VOK'] = {'value' : VOK ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - VOK: ','pass','Value is: ' + str(VOK))
        else:
            JSON_DATA['VOK'] = {'value' : VOK ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - VOK: ','fail','Value is: ' + str(VOK))
            CRX_GOOD = False

        if TOK == 1.0:
            JSON_DATA['TOK'] = {'value' : TOK ,'checkout_status' : 'pass'}
            self.utilities.handle_print('CR10X - TOK: ','pass','Value is: ' + str(TOK))
        else:
            JSON_DATA['TOK'] = {'value' : TOK ,'checkout_status' : 'fail'}
            self.utilities.handle_print('CR10X - TOK: ','fail','Value is: ' + str(TOK))
            CRX_GOOD = False

        if CRX_GOOD:
            JSON_DATA['checkout_status'] = 'pass'
            self.utilities.handle_print('CR10X - OVERALL','pass','All values are within limits')

        else:
            JSON_DATA['checkout_status'] = 'fail'
            self.utilities.handle_print('CR10X - OVERALL','warning','Some values are not within limits')

        self.utilities.handle_json('cr10x',JSON_DATA)

        return
