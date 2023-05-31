__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.data.MaterialDestinationDetails import MaterialDestinationDetails
from test_code.office.layouts.BaseLayout import BaseLayout
from selenium.webdriver.common.by import By
from test_code.office.layouts.Table import Table
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage
from time import sleep

class AssetHistoryPanel(BaseLayout):
    
    __panel_title = 'Asset History'
    __shift_right = '//div[@class=\'shift-control\' and .//*[@data-icon=\'chevron-right\']]'
    __shift_left = '//div[@class=\'shift-control\' and .//*[@data-icon=\'chevron-left\']]'
    __shift_name = 'div.shift-name'
    def _get_panel(self):
        return self.get_layout(self.__panel_title)

    def click_shift_control_right(self):
        """ Clicks the shift control right button

        Examples:
            |   CLick Shift Control Right   |
        """     
        displayed_shift_name = self.get_shift_name()
        timeout = 3
        while (displayed_shift_name == self.get_shift_name()) and timeout > 0:
            timeout -= 1
            sleep(.5)
            self.click(self._get_panel().find_element(By.XPATH, self.__shift_right))
        if displayed_shift_name == self.get_shift_name():
            raise ExceptionWithScreenImage('Displayed shift name did not change')

    def click_shift_control_left(self):
        """ Clicks the shift control left button

        Examples:
            |   CLick Shift Control Left   |
        """
        displayed_shift_name = self.get_shift_name()
        timeout = 3
        while (displayed_shift_name == self.get_shift_name()) and timeout > 0:
            timeout -= 1
            sleep(.5)
            self.click(self._get_panel().find_element(By.XPATH, self.__shift_left))
        if displayed_shift_name == self.get_shift_name():
            raise ExceptionWithScreenImage('Displayed shift name did not change')

    def get_shift_name(self) -> str:
        """ gets the displayed shift name

        Returns:
            str: shift name

            Examples:
            | Get Shift Name |
        """
        return self._get_panel().find_element(By.CSS_SELECTOR, self.__shift_name).text