__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import os

from dataclasses import field
from test_code.office.layouts.BaseLayout import BaseLayout
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
from test_code.Const import AUTOMATED_TEST_DIR

class DataImportPanel(BaseLayout):

    __panel_title = 'Data Import'
    __import_component = './/div[@class=\'heading\' and text()=\'{}\']/..'
    __input_file = './/input[@type=\'file\']'
    __import_button = './/button[text()=\'Import\']'
    __selected_file = '//span[@class=\'path\']'
    __remove_button = 'button.remove'
    __selected_file = 'div.selected-file,div.file-name'
    __selected_upload_details = 'div.file-user'
    __import_error_message = 'div.error-message'
    __selected_file_status = 'span.status'
    __imported_material_destination_plan = '//div[contains(@Class, \'file-name\') and . = \'{}\']'

    def get_panel(self):
        return self.get_layout(self.__panel_title)

    def __get_import_component(self, import_heading:str):
        return self.get_panel().find_element(By.XPATH, self.__import_component.format(import_heading))

    def set_import_file(self, import_heading:str, file_name):
        """ sets the file to import for the given heading via the hidden input file element

        Args:
            import_heading (str): the heading of the import section to use as an identifier for controls of that section
            file_name (str): the file must be in the test_data/file_upload directory

        Examples:

            | Set Import File | Material Destination Plan | my_file.csv

        """ 
        self.__get_import_component(import_heading).find_element(By.XPATH, self.__input_file).send_keys(str(os.path.join(AUTOMATED_TEST_DIR, "test_data", "file_upload").replace('\\', '/')) + '/' + file_name)
        logger.info(self.__get_import_component(import_heading).find_element(By.XPATH, self.__input_file).get_attribute('value'))

    def click_import(self, import_heading: str):
        """ Clicks the import button for the given heading

        Args:
            import_heading (str): the heading of the import section to use as an identifier for controls of that section

        Examples:

            | Click Import | Material Destination Plan |

        """
        self.click(self.__get_import_component(import_heading).find_element(By.XPATH, self.__import_button))

    def material_destination_is_uploaded_successfully(self, import_file: str):
        """Checks if material destination file is uploaded successfully

        Examples:
            | Material Destination Is Uploaded Successfully |
        """
        BuiltIn().run_keyword('Page Should Contain Element', self.__imported_material_destination_plan.format(import_file))

    def click_remove_file(self, import_heading:str):
        """click remove file for the given heading
           only a single file is available to import at a time, hence no need for file name
   

        Args:
            import_heading (str): the heading of the import section to use as an identifier for controls of that section

        Examples:

            | Click Remove File | Material Destination Plan |
        """
        self.click(self.__get_import_component(import_heading).find_element(By.CSS_SELECTOR, self.__remove_button))

    def get_selected_file_upload_details(self, import_heading:str):
        """get the selected file upload status, date, time and user displayed for import
           only a single file is available to import at a time so takes the first found in the section
   

        Args:
            import_heading (str): the heading of the import section to use as an identifier for controls of that section

        Returns:
           str: the text displayed on screen for the file

        Examples:

            | Get Selected File Name | Material Destination Plan |
        """
        return self.__get_import_component(import_heading).find_element(By.CSS_SELECTOR, self.__selected_upload_details).text

    def get_selected_file_name(self, import_heading:str):
        """get the selected file name displayed for import
           only a single file is available to import at a time so takes the first found in the section
   

        Args:
            import_heading (str): the heading of the import section to use as an identifier for controls of that section

        Returns:
           str: the text displayed on screen for the file

        Examples:

            | Get Selected File Name | Material Destination Plan |
        """
        return self.__get_import_component(import_heading).find_element(By.CSS_SELECTOR, self.__selected_file).text

    def get_selected_file_status(self, import_heading:str):
        """get the selected file status displayed for import
           only a single file is available to import at a time so takes the first found in the section
   

        Args:
            import_heading (str): the heading of the import section to use as an identifier for controls of that section

        Returns:
           str: the text displayed on screen for the file status

        Examples:

            | Get Selected File Name | Material Destination Plan |
        """
        return self.__get_import_component(import_heading).find_element(By.CSS_SELECTOR, self.__selected_file_status).text

    def get_import_file_error_message(self, import_heading:str):
        """get the error displayed for import
           only a single file is available to import at a time so takes the first found in the section
   

        Args:
            import_heading (str): the heading of the import section to use as an identifier for controls of that section

        Returns:
           str: the error message displayed

        Examples:

            | Get Error Message | Material Destination Plan |
        """
        return self.__get_import_component(import_heading).find_element(By.CSS_SELECTOR, self.__import_error_message).text

    def is_import_button_disabled(self, import_heading:str) -> bool:
        """returns the disabled status of the import button

        Args:
            import_heading (str): the heading of the import section  o use as an identifier for controls of that section

        Returns:
            bool: true if the button is disabled, false otherwise

        Examples:

            | Is Import Button Disabled | Material Destination Plan |
        """
        class_name = self.__get_import_component(import_heading).find_element(By.XPATH, self.__import_button).get_attribute('class')
        return 'Mui-disabled' in class_name

    def is_file_import_list_empty(self, import_heading:str) -> bool:
        """gives the status based on whether the file import list is empty

        Args:
            import_heading (str): the heading of the import section to use as an identifier for controls of that section

        Returns:
            bool: true if no files exist for import, false otherwise

        Examples:

            | Is File Import List Empty | Material Destination Plan |
        """
        try:
            self.__get_import_component(import_heading).find_element(By.CSS_SELECTOR, self.__selected_file)
            return False
        except:
            return True
