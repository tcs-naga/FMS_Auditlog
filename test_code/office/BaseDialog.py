__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import time

from test_code.office.BasePage import BasePage

class BaseDialog(BasePage):

    __dialog = '//div[@role=\'dialog\']'
    __cycle_update_dialog = '//div[contains(@class,\'dialog\') and ./div[.=\'Update Confirmation\']]'

    def _get_dialog(self):
        dialog = BuiltIn().run_keyword('Get WebElement', self.__dialog)
        return dialog

    def _get_cycle_update_dialog(self):
        dialog = BuiltIn().run_keyword('Get WebElement', self.__cycle_update_dialog)
        return dialog
