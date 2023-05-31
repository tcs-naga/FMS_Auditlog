__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from test_code.field.BasePage import BasePage
from time import sleep

class FailedAuthenticationPage(BasePage):

    __user_asset_not_found_message = '//div[text()=\'User or Asset not found\']'
    __no_licence_message = '//div[text()="You don\'t hold a valid licence for this asset class"]'
    __try_again_button = 'Try Again'
    __cancel_button = 'Cancel'

    def is_user_or_asset_not_found_message_displayed(self) -> bool:
        """ returns a status if the User or Asset not found message is displayed

        Returns:
            bool: return true if message is displayed otherwise false

        Examples:
            |   Is User Or Asset Not Found Message Displayed    |
        """
        try:
            BuiltIn().run_keyword('Page Should Contain Element', self.__user_asset_not_found_message)
            return True
        except:
            return False

    def is_you_dont_hold_a_valid_licence_message_displayed(self) -> bool:
        """ returns a status if the User or Asset not found message is displayed

        Returns:
            bool: return true if message is displayed otherwise false

        Examples:
            |   Is User Or Asset Not Found Message Displayed    |
        """
        try:
            BuiltIn().run_keyword('Wait Until Page Contains Element', self.__no_licence_message)
            BuiltIn().run_keyword('Page Should Contain Element', self.__no_licence_message)
            return True
        except:
            sleep(0.5) # TODO: Need to find a better way to slow down the execution here,
                     #       so that we give enough time for the message to appear
            try:
                BuiltIn().run_keyword('Page Should Contain Element', self.__no_licence_message)
                return True
            except:
                return False

    def click_try_again(self):
        """ clicks the try again button

        Examples:
            |   Click Try Again |
        """
        self.click_button_by_text(self.__try_again_button)

    def click_cancel(self):
        """ clicks the cancel button

        Examples:
            |   Click Cancel |
        """
        self.click_button_by_text(self.__cancel_button)