__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from test_code.field.BasePage import BasePage

class WarningPage(BasePage):

    __warning = '//div[text()=\'WARNING\']'
    __accept_button_text = 'Accept'
    __reject_button_text = 'Reject'

    def is_warning_displayed(self) -> bool:
        """ returns a status based on the warning displayed

        Returns:
            bool: returns true if warning is displayed otherwise false

        Examples:
            |   Is Warning Displayed    |
        """
        try:
            BuiltIn().run_keyword('Page Should Contain Element', self.__warning)
            return True
        except:
            return False

    def click_accept(self):
        """ clicks the accept button

        Examples:
            |   Click Accept    |
        """
        self.click_button_by_text(self.__accept_button_text)

    def click_reject(self):
        """ clicks the reject button

        Examples:
            |   Click Reject    |
        """
        self.click_button_by_text(self.__reject_button_text)
