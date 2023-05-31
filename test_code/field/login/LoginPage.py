__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from test_code.field.BasePage import BasePage
from test_code.field.login.ConfirmLoginPage import ConfirmLoginPage
from test_code.field.login.WarningPage import WarningPage

class LoginPage(BasePage):

    __skip_button_text = 'Skip'
    __first_employee_id_text_field = '//div[text()=\'Login with your employee ID\']/parent::div/div[3]//div/span'
    __employee_id_entered_text = "//div[text()='Login with your employee ID']"
    
    def capture_full_screen(self):
        """ captures an image for comparison of the full screen without the header and notification popups
            Image name is: CenturionLoginPage

        Examples:
            |  Capture Full Screen   |
        """
        self.capture_full_screen_without_header('CenturionLoginPage')

    def capture_full_screen_and_compare(self):
        """
            Captures and compare an image of the full screen without the header and notification popups
            Image name is: CenturionLoginPage

        Examples:
            |  Capture Full Screen   |
        """
        self.capture_full_screen_without_header_and_compare('CenturionLoginPage')

    def click_skip(self):
        """ clicks the skip button

        Examples:
            |   Click Skip    |
        """
        self.click_button_by_text(self.__skip_button_text)

    def verify_login_message_is_displayed(self):
        """ Verifies the Login with your employee ID message is displayed
        """
        BuiltIn().run_keyword('Page Should Contain Element', '//div[. = \'Login with your employee ID\']')

    def key_in_employee_id(self, employee_id: str):
        """ Enter User SAP ID for login

        Examples:
        | Key In Employee ID | employee_SAP_id |
        """
        locator = self.__employee_id_entered_text
        for digit in range(0, len(employee_id)):
            self.click_button_by_text(employee_id[digit])
            locator += "/..//div[.='{}']".format(employee_id[digit])
            if digit < len(employee_id)-1:
                BuiltIn().run_keyword("Wait Until Page Contains Element", locator)

    def clear_employee_id(self):
        """ Clear entered empoyee id

        Examples:
            | Clear Employee ID |
        """
        for _ in range(0, 6):
            self.click_delete_button()

    def login(self, employee_id: str):
        """ login with the given employee id
            Confirms the user and accepts the warnings
        Args:
            employee_id (str): the employee id
        """
        BuiltIn().run_keyword('Wait Until Element Is Enabled', self.__first_employee_id_text_field)
        try:
            self.key_in_employee_id(employee_id)
        except Exception as e:
            self.clear_employee_id()
            self.key_in_employee_id(employee_id)
        ConfirmLoginPage().click_yes()
        WarningPage().click_accept()
        BasePage().close_menu_bar()
        