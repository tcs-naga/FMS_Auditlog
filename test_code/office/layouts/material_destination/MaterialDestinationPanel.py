__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from test_code.data.MaterialDestinationDetails import MaterialDestinationDetails
from test_code.office.layouts.BaseLayout import BaseLayout
from selenium.webdriver.common.by import By
from test_code.office.layouts.Table import Table
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage
import time
from robot.api import logger

class MaterialDestinationPanel(BaseLayout):

    __panel_title = 'Material Destination'
    __add_a_destination_button = './/button[text()=\'Add a destination\']'
    __add_a_destination_plus_sign = './/button[@aria-label=\'Add a destination\']'
    __table = './/table[./thead//th[text()=\'Material Block\']]'
    __table_menu_column = './/td[4]'
    __delete_menu_button = './/button[contains(text(), \'Delete\')]'
    __table_add_secondary_destination = './/td[3]//button'

    def get_panel(self):
        return self.get_layout(self.__panel_title)

    def click_add_a_destination_plus_sign(self):
        """
        clicks the add a destination plus sign in search area of the panel on the Material Destination Panel in Office.

        Examples:

            | Click Add A Destination | 
        """
        self.click(self.get_panel().find_element(By.XPATH, self.__add_a_destination_plus_sign))

    def click_add_a_destination(self):
        """
        clicks the add a destination button on the Material Destination Panel in Office.

        Examples:

            | Click Add A Destination | 
        """
        self.click(self.get_panel().find_element(By.XPATH, self.__add_a_destination_button))

    def __get_table(self):
        return Table(self.get_panel().find_element(By.XPATH, self.__table))

    def find_material_destination(self, material_destination: MaterialDestinationDetails):
        return self.__get_table().get_row([material_destination.material_source.fullName+material_destination.material_source.materialCode+material_destination.material_source.name, material_destination.primary_destination, material_destination.secondary_destination])

    def is_material_destination_listed(self, material_destination: MaterialDestinationDetails) -> bool:
        """ returns status of whether a meterial destination is listed on screen

        Args:
            material_destination (MaterialDestinationDetails): the material destination to search for

        Returns:
            bool: True if displayed otherwise False

        Example:
            |   Is Material Distination Listed |    ${material_destination_object}  |
        """
        retry_count = 30
        while retry_count:
            try:
                self.find_material_destination(material_destination)
                return True
            except Exception as e:
                retry_count -= 1
                time.sleep(0.5)

        return False

    def wait_for_material_destination_to_be_deleted(self, material_destination: MaterialDestinationDetails):
        """ waits for material destination to be deleted, as sometimes it may not disappear from DOM immediately after delete

        Args:
        material_destination (MaterialDestinationDetails): the material destination to search for

        Example:
        |   Wait For Material Destination To Be Deleted |    ${material_destination_object}  |
        """
        try:
            self.find_material_destination(material_destination)
            time.sleep(1)
        except Exception as e:
            pass

    def wait_for_upload_success(self):
        """ waits for the upload success message to display to ensure import was succesful

        Raises:
            Exception: Upload failed

        Examples:
            |   Wait For Upload Success |
        """
        action_complete = False
        count=0
        message = self.get_success_message()
        while count<10 and not action_complete:
            if 'Plan uploaded successfully' in message:
                return
            count=count+1
            time.sleep(0.5)
            message = self.get_success_message()
  
        if not action_complete:
            raise ExceptionWithScreenImage('Upload was not successful')

    def wait_for_upload_success_to_disappear(self):
        """ waits for the upload success message to disappear

        Raises:
            Exception: Popup Message is still displayed

        Examples:
            |   Wait for Upload Success To Disappear    |
        """
        action_complete = False
        count=0

        while count < 20:
            try:
                self.get_success_message()
                time.sleep(0.5)
            except:
                return
            count=count+1

        if not action_complete:
            raise ExceptionWithScreenImage('Popup Message is still displayed')

    def click_delete(self, material_destination: MaterialDestinationDetails):
        """ clicks delete for the material destination

        Args:
            material_destination (MaterialDestinationDetails): the meterial destination details

        Examples:
            |   Click Delete    |   ${material_destination_object}  |
        """
        row = self.find_material_destination(material_destination)
        self.click(row.find_element(By.XPATH, self.__table_menu_column))
        self.click(row.find_element(By.XPATH, self.__table_menu_column).find_element(By.XPATH, self.__delete_menu_button))

    def __get_all_rows(self):
        table = None
        try:
            table = self.__get_table()
        except:
            return []
        return table.get_all_rows()

    def has_material_destinations(self) -> bool:
        """ returns a status if material destinations exist

        Returns:
            bool: True if material destinations exist otherwise False

        Examples:
            |   Has Material Destinations   |
        """
        return len(self.__get_active_licence_rows())>0

    def remove_all_material_destinations(self):
        """ removes all the material destinations displayed

        Examples:
            |   Remove All Material Destinations    |
        """
        for material_destination in self.__get_all_rows():
            self.click(material_destination.find_element(By.XPATH, self.__table_menu_column))
            self.click(material_destination.find_element(By.XPATH, self.__table_menu_column).find_element(By.XPATH, self.__delete_menu_button))

    def add_secondary_destination(self, material_destination: MaterialDestinationDetails, secondary_destination: str):
        """ adds a secondary destination to an existing material destination

        Args:
            material_destination (MaterialDestinationDetails): material destination to add secondary destination
            secondary_destination (str): the secondary destination to add

        Examples:
            |   Add Secondary Destination   |   ${material_destination_object}  |   HAZ01_RP02_0002    |
        """
        self.select_from_menu(self.find_material_destination(material_destination).find_element(By.XPATH, self.__table_add_secondary_destination), secondary_destination)

    def get_list_of_secondary_destination_options(self, material_destination: MaterialDestinationDetails) -> list:
        """ Gets a list of options available to add as a secondary destination for the given material destination details

        Args:
            material_destination (MaterialDestinationDetails): the material destination details to get list of available options for

        Returns:
            list: list of secondary destination options
        """
        return self.get_menu_options(self.find_material_destination(material_destination).find_element(By.XPATH, self.__table_add_secondary_destination))
