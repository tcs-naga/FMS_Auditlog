__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from test_code.field.BasePage import BasePage

class ConfirmLoginPage(BasePage):

    __are_you_message = '//div[text()=\'Are you {}?\']'
    __yes_button_text = 'Yes'
    __no_button_text = 'No'

    def is_are_you_message_displayed(self, name:str)->bool:
        """ returns a status based on whether the are you .... message displayed

        Args:
            name (str): the name to be in the message

        Returns:
            bool: true if the message is displayed otherwise false

        Examples:
            |   Is Are You Message Displayed    |   John Smith  |
        """
        try:
            BuiltIn().run_keyword('Wait Until Element Is Visible', self.__are_you_message.format(name))
            BuiltIn().run_keyword('Page Should Contain Element', self.__are_you_message.format(name))
            return True
        except:
            return False

    def click_yes(self):
        """clicks the Yes button

        Examples:
            |   Click Yes   |
        """
        self.click_button_by_text(self.__yes_button_text)

    def click_no(self):
        """clicks the No button

        Examples:
            |   Click No   |
        """
        self.click_button_by_text(self.__no_button_text)
