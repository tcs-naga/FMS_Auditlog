__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from abc import ABC, abstractmethod
from time import sleep
import time
from test_code.data.LicenceDetails import LicenceDetails
from test_code.data.UserDetails import UserDetails
from test_code.office.layouts.BaseLayout import BaseLayout
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from selenium.webdriver.common.by import By
from test_code.office.layouts.Table import Table
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage

class UserForm(BaseLayout, ABC, BaseException):

    __dialog = None
    __sap_number_id_textfield = 'id:sapnumber'
    __email_id_textfield = 'id:email'
    __firstname_id_textfield = 'id:firstname'
    __lastname_id_textfield = 'id:lastname'
    __department_id_select = 'id:department'
    __crew_id_select = 'id:crew'
    __asset_class_id_select = '//div[contains(@id, \'assetclass\')]'
    __licence_type_id_select = '//div[contains(@id, \'licencetype\')]'
    __issue_date_id_textfield = '//input[contains(@id, \'issuedate\')]'
    __expiry_date_id_textfield = '//input[contains(@id, \'expirydate\')]'
    __save_text_button = 'SAVE'
    __add_a_licence_text_button = 'ADD A LICENCE'
    __save_licence_text_button = 'SAVE LICENCE'
    __cancel_text_button = 'CANCEL'
    __disable_text_button = 'DISABLE'
    __enable_text_button = 'ENABLE'
    __table = './/table'
    __table_menu_column = './/td[5]'

    @abstractmethod
    def get_tile_title(self):
        pass

    def fill_in_user_details(self, user_details: UserDetails):
        """ fills in the user details form

        Args:
            user_details (UserDetails): user details to fill in

        Examples:
            |   Fill In User Details    |   ${user_details_object}  |
        """
        self.__get_dialog()
        self.set_sap_number(user_details.sap_number)
        self.set_email(user_details.email)
        self.set_firstname(user_details.first_name)
        self.set_lastname(user_details.last_name)
        self.select_department(user_details.department)
        self.select_crew(user_details.crew)

    def fill_in_license_details(self, licence_details: LicenceDetails):
        """ fills in the licence details form

        Args:
            licence_details (LicenceDetails): licence details to fill in

        Examples:
            |   Fill In License Details    |   ${licence_details_object}  |
        """
        self.__get_dialog()
        self.select_asset_class(licence_details.asset_class)
        self.select_licence_type(licence_details.licence_type)
        self.set_issue_date(licence_details.get_issue_date_formatted())
        self.set_expiry_date(licence_details.get_expiry_date_formatted())

    def set_sap_number(self, sap_number:str):
        """ fills in the sap number

        Args:
            sap_number (str): the sap number

        Examples:
            |   Set Sap Number  |   123456  |
        """
        self.send_keys(self.__sap_number_id_textfield, sap_number)
   
    def set_email(self, email:str):
        """ fills in the email

        Args:
            email (str): the email address

        Examples:
            |   Set Email  |   abc@test.com  |
        """
        self.send_keys(self.__email_id_textfield, email)

    def set_firstname(self, first_name:str):
        """ fills in the firstname

        Args:
            first_name (str): the first name

        Examples:
            |   Set Firstname  |   John  | 
        """
        self.send_keys(self.__firstname_id_textfield, first_name)

    def set_lastname(self, last_name:str):
        """ fills in the lastname

        Args:
            last_name (str): the lastname

        Examples:
            |   Set Lastname  |   Smith  | 
        """
        self.send_keys(self.__lastname_id_textfield, last_name)

    def select_department(self, department:str):
        """ selects the department from the dropdown

        Args:
            department (str): the department

        Examples:
            | Select Department | Training |
        """
        self.select(self.__department_id_select, department)

    def select_crew(self, crew:str):
        """ selects the crew from the dropdown

        Args:
            crew (str): the crew

        Examples:
            | Select Crew   | A |
        """
        self.select(self.__crew_id_select, crew)

    def select_asset_class(self, asset_class:str, index: int=1):
        """ selects the asset class from the dropdown

        Args:
            asset_class (str): the asset class

        Examples:
            | Select Asset Class | Dump Truck - Caterpillar CAT 793F |
        """
        self.select(self.__asset_class_id_select, asset_class, index)

    def select_licence_type(self, licence_type:str):
        """ selects the licence type from the dropdown

        Args:
            licence_type (str): the licence type

        Examples:
            | Select Licence Type | Qualified |
        """
        self.select(self.__licence_type_id_select, licence_type)

    def set_issue_date(self, issue_date:str):
        """ fills in the issue date

        Args:
            issue_date (str): the issue date

        Example:
            | Set Issue Date | 10/12/2022 |
        """
        self.send_keys(self.__issue_date_id_textfield, issue_date)

    def set_expiry_date(self, expiry_date:str):
        """ fills in the expiry date

        Args:
            expiry_date (str): the expiry date

        Examples:
            | Set Expiry Date | 12/12/2022 |
        """
        self.send_keys(self.__expiry_date_id_textfield, expiry_date)

    def click_save(self):
        """ clicks the save button

        Examples:
            | Click Save |
        """
        self.__get_dialog()
        self.click_button_by_text(self.__save_text_button)

    def click_add_licence(self):
        """ clicks the add licence button

        Examples:
            | Click Add Licence |
        """
        self.click_button_by_text(self.__add_a_licence_text_button)

    def click_save_licence(self):
        """ clicks save licence button

        Examples:
            | Click Save Licence |
        """
        self.click(self.__get_dialog().find_element(By.XPATH, './/button[.=\'' + self.__save_licence_text_button + '\']'))

    def click_cancel(self):
        """ clicks cancel button

        Examples:
            | Click Cancel |
        """
        self.__get_dialog()
        self.click_button_by_text(self.__cancel_text_button)

    def click_disable(self):
        """ clicks disable button

        Examples:
            | Click Disable |
        """
        self.click_button_by_text(self.__disable_text_button)

    def click_enable(self):
        """ clicks enable button

        Examples:
            | Click Enable Licence |
        """
        self.click_button_by_text(self.__enable_text_button)

    def get_sap_number_error_message(self) -> str:
        """ get the sap number error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Sap Number Error Message |
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__sap_number_id_textfield)
        sap_number = BuiltIn().run_keyword('Get WebElement', self.__sap_number_id_textfield)
        return sap_number.get_property('validationMessage')

    def get_email_error_message(self) -> str:
        """ get the email error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Email Error Message |
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__email_id_textfield)
        email = BuiltIn().run_keyword('Get WebElement', self.__email_id_textfield)
        return email.get_property('validationMessage')

    def get_firstname_error_message(self) -> str:
        """ get the firstname error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Firstname Error Message |
        """
        firstname = BuiltIn().run_keyword('Get WebElement', self.__firstname_id_textfield)
        return firstname.get_property('validationMessage')

    def get_lastname_error_message(self) -> str:
        """ get the lastname error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Lastname Error Message |
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__lastname_id_textfield)
        lastname = BuiltIn().run_keyword('Get WebElement', self.__lastname_id_textfield)
        return lastname.get_property('validationMessage')

    def get_department_error_message(self) -> str:
        """ get the department error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Department Error Message |
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__department_id_select)
        department = BuiltIn().run_keyword('Get WebElement', self.__department_id_select)
        return department.find_element(By.XPATH, './following-sibling::input').get_property('validationMessage')

    def get_crew_error_message(self) -> str:
        """ get the crew error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Crew Error Message |
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__crew_id_select)
        crew = BuiltIn().run_keyword('Get WebElement', self.__crew_id_select)
        return crew.find_element(By.XPATH, './following-sibling::input').get_property('validationMessage')

    def get_asset_class_error_message(self) -> str:
        """ get the asset class error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Asset Class Error Message |
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__asset_class_id_select)
        asset_class = BuiltIn().run_keyword('Get WebElement', self.__asset_class_id_select)
        return asset_class.find_element(By.XPATH, './following-sibling::input').get_property('validationMessage')

    def get_licence_type_error_message(self) -> str:
        """ get the licence type error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Licence Type Error Message |
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__licence_type_id_select)
        licence_type = BuiltIn().run_keyword('Get WebElement', self.__licence_type_id_select)
        return licence_type.find_element(By.XPATH, './following-sibling::input').get_property('validationMessage')

    def get_issue_date_error_message(self) -> str:
        """ get the issue date error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Issue Date Error Message |
        """
        try:
            BuiltIn().run_keyword('Wait Until Element Is Visible', self.__issue_date_id_textfield)
            issue_date = BuiltIn().run_keyword('Get WebElement', self.__issue_date_id_textfield)
            return issue_date.get_property('validationMessage')
        except:
            time.sleep(0.5)
            return issue_date.get_property('validationMessage')

    def get_expiry_date_error_message(self) -> str:
        """ get the expiry date error message displayed

        Returns:
            str: the error message

        Examples:
            | Get Expiry Date Error Message |
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__expiry_date_id_textfield)
        expiry_date = BuiltIn().run_keyword('Get WebElement', self.__expiry_date_id_textfield)
        return expiry_date.get_property('validationMessage')

    def is_sap_number_disabled(self) -> bool:
        """ gets the disabled status of the sap number field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Sap Number disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[@id=\'sapnumber\' and @disabled]')
            return True
        except:
            return False

    def is_email_disabled(self) -> bool:
        """ gets the disabled status of the email field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Email disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[@id=\'email\' and @disabled]')
            return True
        except:
            return False

    def is_first_name_disabled(self) -> bool:
        """ gets the disabled status of the firstname field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is First Name disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[@id=\'firstname\' and @disabled]')
            return True
        except:
            return False

    def is_last_name_disabled(self) -> bool:
        """ gets the disabled status of the last name field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Last Name disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[@id=\'lastname\' and @disabled]')
            return True
        except:
            return False

    def is_department_disabled(self) -> bool:
        """ gets the disabled status of the department field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Department disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[@name=\'department\' and @disabled]')
            return True
        except:
            return False

    def is_crew_disabled(self) -> bool:
        """ gets the disabled status of the crew field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Crew disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[@name=\'crew\' and @disabled]')
            return True
        except:
            return False

    def is_asset_class_disabled(self) -> bool:
        """ gets the disabled status of the asset class field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Asset Class disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[@name=\'assetclass\' and @disabled]')
            return True
        except:
            return False

    def is_licence_type_disabled(self) -> bool:
        """ gets the disabled status of the Licence type field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Licence Type disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[@name=\'licencetype\' and @disabled]')
            return True
        except:
            return False

    def is_issue_date_disabled(self) -> bool:
        """ gets the disabled status of the issue date field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Issue Date disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[contains(@id,\'issuedate\') and @disabled]')
            return True
        except:
            return False

    def is_expiry_date_disabled(self) -> bool:
        """ gets the disabled status of the expiry date field

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Expiry Date disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/input[contains(@id,\'expirydate\') and @disabled]')
            return True
        except:
            return False

    def is_add_a_licence_disabled(self) -> bool:
        """ gets the disabled status of the add a licence button

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Add A Licence disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/button[text()=\''+ self.__add_a_licence_text_button + '\' and @disabled]')
            return True
        except:
            return False

    def is_save_disabled(self) -> bool:
        """ gets the disabled status of the save button

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is Save disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/button[text()=\''+ self.__save_text_button + '\' and @disabled]')
            return True
        except:
            return False

    def is_user_disabled(self) -> bool:
        """ gets the status of whether the user account is currently disabled message is displayed

        Returns:
            bool: True if disabled otherwise False

        Examples:
            | Is User disabled |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/div[text()=\'This user account is currently disabled\']')
            return True
        except:
            return False

    def is_page_displayed(self) -> bool:
        try:
            self.__get_dialog()
            return True
        except:
            return False
        
    def __get_dialog(self):
        if self.__dialog is None:
            __dialog = self.get_layout('User Management', self.get_tile_title()).find_element(By.XPATH, './/div[contains(@class, \'dialog-container\') and .//div[contains(normalize-space(string()),\'' + self.get_tile_title() + '\')]]')
        return __dialog

    def __get_table(self):
        BuiltIn().run_keyword('Wait Until Page Contains Element', self.__get_dialog().find_element(By.XPATH, self.__table))
        return Table(self.__get_dialog().find_element(By.XPATH, self.__table))

    def find_licence(self, licence_details: LicenceDetails, ignore_disabled_rows=True):
        retry_count = 30
        while retry_count:
            try:
                return self.__get_table().get_row([licence_details.asset_class, licence_details.licence_type, licence_details.get_issue_date_formatted()], ignore_disabled_rows=ignore_disabled_rows)
            except Exception as e:
                if not retry_count:
                    raise ExceptionWithScreenImage(e)
                retry_count -= 1
                time.sleep(0.5)

    def is_licence_displayed(self, licence_details: LicenceDetails, ignore_disabled_rows=True) -> bool:
        """ gets the status of whether a licence is displayed

        Args:
            licence_details (LicenceDetails): the licence to find
            ignore_disabled_rows (bool, optional): ignore disabled rows in the search. Defaults to True.

        Returns:
            bool: True if the licence is found otherwise false

        Examples:
            | Is Licence Displayed | licence_details=${licence_details} |
            | Is Licence Displayed | licence_details=${licence_details} | ignore_disabled_rows=True |
        """
        try:
            self.find_licence(licence_details, ignore_disabled_rows)
            return True
        except Exception:
            sleep(0.5) # TODO: Need to find a better way to slow down the execution here,
                     #       so that we give enough time for the message to appear
            try:
                self.find_licence(licence_details, ignore_disabled_rows)
                return True
            except Exception:
                return False

    def click_edit_licence(self, licence_details: LicenceDetails):
        """ click edit licence

        Args:
            licence_details (LicenceDetails): the licence to edit

        Examples:
            | Click Edit Licence | licence_details=${licence_details} |
        """
        row = self.find_licence(licence_details)
        self.select(row.find_element(By.XPATH, self.__table_menu_column), 'Edit')

    def click_revoke_licence(self, licence_details: LicenceDetails):
        """ click revoke licence

        Args:
            licence_details (LicenceDetails): the licence to revoke

        Examples:
            | Click Revoke Licence | licence_details=${licence_details} |
        """
        row = self.find_licence(licence_details)
        self.select(row.find_element(By.XPATH, self.__table_menu_column), 'Revoke')

    def __get_active_licence_rows(self):
        table = None
        try:
            table = self.__get_table()
        except:
            return []
        return table.get_active_rows()

    def has_active_licences(self):
            return len(self.__get_active_licence_rows())>0

    def remove_all_active_licences(self):
        """ removes all the active licences displayed

        Examples:
            | Remove All Active Licences |
        """
        for active_licence_row in self.__get_active_licence_rows():
           self.select(active_licence_row.find_element(By.XPATH, self.__table_menu_column), 'Revoke')
   
    def is_licence_revoked(self, licence_details: LicenceDetails) -> bool:
        """ returns a status of the licence has been revoked

        Args:
            licence_details (LicenceDetails): the licence to check

        Returns:
            bool: True if revoked otherwise False

        Examples:
            | Is Licence Revoked | licence_details=${licence_details} |
        """
        row = self.find_licence(licence_details, ignore_disabled_rows=False)
        for cell in row.find_elements(By.XPATH, './/td[not(@style=\'cursor: pointer;\')]'):
            if not 'disabled' in cell.get_attribute('class'):
                return False
        return True

    def get_list_of_asset_class_options(self) -> list:
        """ get list of asset class options

        Returns:
            list: the list of options

        Examples:
            | Get List of Asset Class Options |
        """
        return self.get_select_options(self.__asset_class_id_select)

    def is_matching_licence_exists_error_displayed(self) -> bool:
        """ is the message "A matching licence already exists." displayed

        Returns:
            bool: True if message is displayed otherwise False

        Examples:
            | Is Matching Licence Exists Error Displayed |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, './/div[text()=\'A matching licence already exists.\']')
            return True
        except:
            return False