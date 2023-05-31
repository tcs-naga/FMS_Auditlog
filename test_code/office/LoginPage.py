__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from PageObjectLibrary import PageObject
from robot.libraries.BuiltIn import BuiltIn
from test_code.office.BasePage import BasePage


class LoginPage(BasePage):

    __skip_button_text = 'SKIP'
    __go_to_login = '//div[text()=\'Go to login.\']'
    def click_skip(self):
        """ clicks Skip Button
        
        Examples:
            | Click Skip |
        """
        self.click_button_by_text(self.__skip_button_text)

    def click_go_to_login(self):
        """ clicks the go to login button

        """
        try:
            BuiltIn().run_keyword('Click Element', self.__go_to_login) # Since this is an optional step the retry based click is not required.
        except Exception as e:
            pass
        
