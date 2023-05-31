__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from time import sleep
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from robot.libraries.BuiltIn import BuiltIn
from test_code.field.BasePage import BasePage
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage

class HomePage(BasePage):

    __menu = None
    __menu_div = '//div[text()=\'{}\']'
    __actions_menu_title = "ACTIONS"
    __mark_as_complete_button = '//div[string()=\'Mark {} as complete\']'
    __save_button = '//button[. = \'Save\']'
    __select_loading_tool = '//div[text()=\'Select Loading Tool\']/..//div[text()=\'{}\']'
    __version = '//div[contains(@class, \'menu-user-block\')]/following-sibling::div/span'
    __travel_loaded_status = '//button[contains(@class, \'status-block\')]//div[contains(@class, \'activity\') and text()=\'{}\']'

    def capture_full_screen(self):
        """ captures the full screen image for comparison without the header and popup messages
            Saves the image as Centurion

            |   Capture Full Screen |
        """
        self.capture_full_screen_without_header('Centurion')

    def load(self, loading_tool: str):
        """
        Click 'Mark Load As Complete' button, select a loading tool and save,
        and wait until 'mark dump as complete' button is displayed.

        Examples:
        | Load | EX7109 |
        """
        self.__mark_load_as_complete()
        self.__select_loading_tool_and_save(loading_tool)
        self.__wait_until_mark_dump_as_complete_button_displayed()
        self.__wait_until_travel_loaded_status_displayed()

    def dump(self):
        """
        Click 'Mark Dump As Complete' button,
        and wait until 'mark load as complete' button is displayed.

        Examples:
        | Dump |
        """
        self.__mark_dump_as_complete()
        self.__wait_until_mark_load_as_complete_button_displayed()

    def __mark_load_as_complete(self):
        """
        Click Mark Load As Complete button

        Examples:
        | Mark Load As Complete |
        """
        self.click(self.__mark_as_complete_button.format('Load'))

    def __mark_dump_as_complete(self):
        """
        Click Mark Load As Complete button

        Examples:
        | Mark Load As Complete |
        """
        self.click(self.__mark_as_complete_button.format('Dump'))

    def __select_loading_tool_and_save(self, loading_tool: str):
        """
        Select a loading tool and save

        Examples:
        | Select Loading Tool And Save | EX7109 |
        """
        self.click(self.__select_loading_tool.format(loading_tool))
        self.click(self.__save_button)

    def __wait_until_mark_dump_as_complete_button_displayed(self):
        """
        Wait until 'mark dump as complete' button is displayed

        Examples:
        | Wait Until Mark Dump As Complete Button Displayed |
        """
        timeout = 3
        while not self.is_element_visible(self.__mark_as_complete_button.format('Dump')) and timeout > 0:
            timeout = timeout - 1
            sleep(2)

        if not self.is_element_visible(self.__mark_as_complete_button.format('Dump')):
            raise ExceptionWithScreenImage('Mark Dump As Complete button has not appeared')

        BuiltIn().run_keyword('Capture Page Screenshot') # TODO: Remove this line when debugging is complete

    def __wait_until_travel_loaded_status_displayed(self):
        """
        Wait 30s until 'TRAVEL LOADED' status is displayed.
        The rule is if dump detection is manual (means when we click the button manually to mark load as complete,
        then 'TRAVEL LOADED' should appear immediately. 

        Examples:
        | Wait Until Travel Loaded Status Displayed |
        """
        timeout = 6
        while not self.is_element_visible(self.__travel_loaded_status.format('Travel Loaded')) and timeout > 0:
            timeout = timeout - 1
            sleep(5)

        if not self.is_element_visible(self.__travel_loaded_status.format('Travel Loaded')):
            raise ExceptionWithScreenImage('TRAVEL LOADED status did not appear in Field')

        BuiltIn().run_keyword('Capture Page Screenshot') # TODO: Remove this line when debugging is complete

    def navigate_to_smu_hours_sub_menu_item(self):
        """ Click the 'SMU hours' menu item from the main menu -> Maintenance in Field

            |   Navigate To Maintenance->SMU Hours Sub Menu Item |
        """
        self._open_sub_menu_option('Maintenance', 'SMU hours')

    def navigate_to_refuel_sub_menu_item(self):
        """ Click the 'Refuel' menu item from the main menu -> Maintenance in Field

            |   Navigate To Maintenance->Refuel Sub Menu Item |
        """
        self._open_sub_menu_option('Maintenance', 'Refuel')

    def __actions_menu(self):
        return self.get_menu(self.__actions_menu_title)

    def get_menu(self, menu_title:str) -> WebElement:
        """ retrieves the menu in the Field application for the given menu title

        Args:
            menu_title (str):  The menu title is the title at the top of the menu
        Returns:
            WebElement: _description_
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__menu_div.format(menu_title))
        self.__menu = BuiltIn().run_keyword('Get WebElement', self.__menu_div.format(menu_title))
        return self.__menu

    def __wait_until_mark_load_as_complete_button_displayed(self):
        """
        Wait 30s until 'mark load as complete' button is displayed

        Examples:
        | Wait Until mark_load_as_complete_button_displayed |
        """
        timeout = 6 # Status might not change immediately after dumping
        while not self.is_element_visible(self.__mark_as_complete_button.format('Load')) and timeout > 0:
            timeout = timeout - 1
            sleep(5)

        if not self.is_element_visible(self.__mark_as_complete_button.format('Load')):
            raise ExceptionWithScreenImage('Mark Load as complete button has not appeared')

    def get_list_of_activity_options(self) -> list:
        """ gets a list of activities available to the asset

        Returns:
            list: list of activities
            
        Examples:
            | Get List Of Activity Options |
        """
        return self._get_list_of_menu_options('Activity')
    
    def get_list_of_delay_category_options(self) -> list:
        """ gets a list of delay category options

        Returns:
            list: list of delay categories
            
        Examples:
            | Get List Of Delay Category Options |
        """
        return self._get_list_of_menu_options('Delays')
    
    def get_list_of_delays_options(self, delay_category: str) -> list:
        """ get a list of delay options for a delay category

        Args:
            delay_category (str): the delay category

        Returns:
            list: list of delays
            
        Examples:
            | Get List of Delays Options |
        """
        return self._get_list_of_menu_options('Delays', delay_category)

    def get_version(self):
        """ gets the version of the office deployed

        Returns:
            str: version
        """
        self._click_menu_toggle()
        BuiltIn().run_keyword('Wait Until Element is Visible', self.__version)
        return BuiltIn().run_keyword('Get Text', self.__version)

    def is_mark_dump_as_complete_button_displayed(self) -> bool:
        """
        Wait until 'mark dump as complete' button is displayed

        Examples:
        | Is Mark Dump As Complete Button Displayed |
        """
        return self.is_element_visible(self.__mark_as_complete_button.format('Dump'))
