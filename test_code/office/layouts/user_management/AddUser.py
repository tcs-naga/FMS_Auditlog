__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.data.LicenceDetails import LicenceDetails
from test_code.office.layouts.BaseLayout import BaseLayout
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from selenium.webdriver.common.by import By
from test_code.office.layouts.Table import Table
from test_code.office.layouts.user_management.UserForm import UserForm

class AddUser(UserForm):

    __dialog_title = 'Add user'
    
    def get_tile_title(self):
        return self.__dialog_title
