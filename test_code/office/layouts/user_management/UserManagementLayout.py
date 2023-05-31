__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from time import sleep
from test_code.office.layouts.BaseLayout import BaseLayout
from selenium.webdriver.common.by import By
from test_code.office.layouts.Table import Table
from robot.api import logger
from test_code.office.layouts.user_management.AddUser import AddUser
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage
from robot.libraries.BuiltIn import BuiltIn

class UserManagementLayout(BaseLayout):

    __add_user_button_text = 'ADD USER'
    __window_title = 'User Management'
    __table = './/table[./thead//th[text()=\'NAME\']]'
    __table_name_column = './/td[1]'
    __table_status_column = './/td[4]'
    __table_menu_column = './/td[5]'


    def click_add_user(self):
        """ clicks the add user button

        Examples:
            | Click Add User |
        """
        # need to retry if add user not displayed as click doesn't always deliver
        try:
            self.click(self.get_tile().find_element(By.XPATH, './/button[. = \'{}\']'.format(self.__add_user_button_text)))
        except Exception as e:
            pass
        if not AddUser().is_page_displayed():
            self.click(self.get_tile().find_element(By.XPATH, './/button[. = \'{}\']'.format(self.__add_user_button_text)))

    def find_user(self, sap_id: str, timeout: int=0):
        if timeout:
            retry_count = timeout
        else:
            retry_count = 30

        while retry_count:
            try:
                return self.__get_table().get_row([None, sap_id], pagination=True)
            except Exception as e:
                retry_count -= 1
                if not retry_count:
                    raise e
                sleep(0.5)
        raise ExceptionWithScreenImage("Unable to find user")

    def is_user_displayed(self, sap_id: str, timeout: int=0) -> bool:
        """ gets a status based on if a user is displayed

        Args:
            sap_id (str): the sap_id to search for

        Returns:
            bool: True if the user is displayed otherwise False

        Examples: 
            | Is User Displayed | sap_id=123456 | timeout=0 |
        """
        try:
            self.find_user(sap_id, timeout)
            return True
        except Exception as e:
            return False

    def get_name(self, sap_id: str) -> str:
        """ get the name of the user

        Args:
            sap_id (str): the sap_id to find the user

        Returns:
            str: the name

        Examples: 
            | Get Name | sap_id=123456 |
        """
        return self.find_user(sap_id).find_element(By.XPATH, self.__table_name_column).text

    def get_status(self, sap_id: str) -> str:
        """ get the status of the user

        Args:
            sap_id (str): the sap_id to find the user

        Returns:
            str: the status

        Examples: 
            | Get Status | sap_id=123456 |
        """
        return self.find_user(sap_id).find_element(By.XPATH, self.__table_status_column).text

    def get_tile(self):
        return self.get_layout(self.__window_title)

    def __get_table(self):
        return Table(self.get_tile().find_element(By.XPATH, self.__table))

    def click_edit_user(self, sap_id: str):
        """ clicks edit for user

        Args:
            sap_id (str): the sap_id to find the user

        Examples:
            | Click Edit User | sap_id=123456 |
        """
        row = self.find_user(sap_id)
        BuiltIn().run_keyword('Wait Until Page Contains Element', row.find_element(By.XPATH, self.__table_menu_column))
        self.select(row.find_element(By.XPATH, self.__table_menu_column), 'Edit')

    def click_disable_user(self, sap_id: str):
        """ clicks disable for user

        Args:
            sap_id (str): the sap_id to find the user

        Examples:
            | Click Disable User | sap_id=123456 |
        """
        row = self.find_user(sap_id)
        self.select(row.find_element(By.XPATH, self.__table_menu_column), 'Disable')

    def click_enable_user(self, sap_id: str):
        """ clicks enable for user

        Args:
            sap_id (str): the sap_id to find the user

        Examples:
            | Click Enable User | sap_id=123456 |
        """
        row = self.find_user(sap_id)
        self.select(row.find_element(By.XPATH, self.__table_menu_column), 'Enable')
