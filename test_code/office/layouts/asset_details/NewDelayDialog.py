__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from selenium.webdriver.common.by import By
import time
from robot.api import logger
from test_code.office.layouts.asset_details.DelayFormDialog import DelayFormDialog

class NewDelayDialog(DelayFormDialog):
    
    def get_dialog_title(self):
        return 'Set Delay'