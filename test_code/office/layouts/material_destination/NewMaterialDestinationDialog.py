__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.office.layouts.material_destination.MaterialDestinationPanel import MaterialDestinationPanel
from selenium.webdriver.common.by import By
from test_code.data.MaterialDestinationDetails import MaterialDestinationDetails

class NewMaterialDestinationDialog(MaterialDestinationPanel):

    __dialog_title = 'New Material Destination'
    __dialog = './/div[contains(@class, \'dialog \') and .//div[text()=\'New Material Destination\']]'
    __material_source_id = 'mui-component-select-materialSourceId'
    __primary_destination_id = 'mui-component-select-primaryDumpId'
    __secondary_destination_id = 'mui-component-select-secondaryDumpId'
    __create_button = './/button[text()=\'Create\']'
    __create_button_disabled = './/button[text()=\'Create\' and @disabled]'
    __cancel_button = './/button[text()=\'Cancel\']'

    def __get_dialog(self):
        return self.get_panel().find_element(By.XPATH, self.__dialog)

    def fill_in_material_destination_details(self, material_destination: MaterialDestinationDetails):
        """ fills in the new material destination details

        Args:
            material_destination (MaterialDestinationDetails): the object containing the material destination
            primary_destination (str): primary destination
            secondary_destination (str, optional): secondary destination. Defaults to None.

        Examples:
            |   Fill In Material Destination Details  | ${material_destination_object}  |
        """
        self.select_material_source(material_destination.material_source.fullName)
        self.select_primary_destination(material_destination.primary_destination)

        if not material_destination.secondary_destination is None and material_destination.secondary_destination!='':
            self.select_secondary_destination(material_destination.secondary_destination)

    def select_material_source(self, value: str):
        """ selects the value from material source

        Args:
            value (str): the value to select

        Examples:
            |   Select Material Sournce |   HAZ01_01_0500_002_0503_BS02 |
        """
        self.select(self.__get_dialog().find_element(By.ID, self.__material_source_id), value)

    def select_primary_destination(self, value: str):
        """selects the value from the primary distination

        Args:
            value (str): the value to select

        Examples:
            |   Select Primary Destination Source |   HAZ01_RP02_001 |
        """
        self.select(self.__get_dialog().find_element(By.ID, self.__primary_destination_id), value)

    def select_secondary_destination(self, value:str):
        """selects the value from the secondary distination

        Args:
            value (str): the value to select

        Examples:
            |   Select Secondary Destination  |   HAZ01_RP02_001 |
        """
        self.select(self.__get_dialog().find_element(By.ID, self.__secondary_destination_id), value)

    def click_create(self):
        """ clicks the create button

        Examples:
            |   Click Create |
        """
        self.click(self.__get_dialog().find_element(By.XPATH, self.__create_button))

    def click_cancel(self):
        """ clicks the cancel button

        Examples:
            |   Click Cancel |
        """
        self.click(self.__get_dialog().find_element(By.XPATH, self.__cancel_button))

    def get_list_of_material_source_options(self) -> list:
        """ gets a list of material sources available to use

        Returns:
            list: list of material sources

        Examples:
            |   Get List of Material Source Options |
        """
        return self.get_select_options(self.__material_source_id)

    def get_list_of_primary_destination_options(self) -> list:
        """ gets a list of primary destinations available to use

        Returns:
            list: list of primary destinations

        Examples:
            |   Get List of Primary Destination Options |
        """
        return self.get_select_options(self.__primary_destination_id)

    def is_create_button_disabled(self) -> bool:
        """ get the status of whether the create button is disabled

        Returns:
            bool: True if the button is disabled otherwise false

        Examples:
            |   Is Create Button Disabled   |
        """
        try:
            self.__get_dialog().find_element(By.XPATH, self.__create_button_disabled)
            return True
        except:
            return False
