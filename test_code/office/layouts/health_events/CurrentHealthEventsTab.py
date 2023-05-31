__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.data.HealthEventDetails import HealthEventDetails
from test_code.office.layouts.health_events.HealthEventsPanel import HealthEventsPanel
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_code.office.layouts.Grid import Grid
from robot.libraries.BuiltIn import BuiltIn
from time import sleep

class CurrentHealthEventsTab(HealthEventsPanel):

    __grid_class = '.MuiDataGrid-root'
    __current_health_events_data = '//div[@aria-rowindex=\'2\' and @data-rowindex=\'0\']'

    def __get_grid(self):
        return Grid(self._get_panel().find_element(By.CSS_SELECTOR, self.__grid_class))

    def __find_row(self, current_health_events: HealthEventDetails) -> WebElement:
        return self.__get_grid().get_row([current_health_events.assetId, current_health_events.level, current_health_events.eventType, current_health_events.operator], number_of_columns_to_skip_from_start=1)

    def wait_for_health_events_to_load(self) -> None:
        """ Wait until health events are loaded

        Examples:
            |   Wait For Health Events To Load   |   
        """
        BuiltIn().run_keyword('Wait Until Page Contains Element', self._get_panel().find_element(By.XPATH, self.__current_health_events_data))

    def wait_for_health_events_to_clear(self) -> None:
        """ Wait until health events are cleared

        Examples:
            |   Wait For Health Events To Clear   |   
        """
        sleep (2)
        try:
            self._get_panel().find_element(By.XPATH, self.__current_health_events_data)
            sleep (2)
        except:
            pass

    def is_health_event_displayed(self, current_health_event: HealthEventDetails) -> bool:
        """ gets a status based on if the health event is displayed

        Args:
            current_health_event (HealthEventDetails): the current health events to find

        Returns:
            bool: True if the current health events is displayed otherwise False

        Examples:
            |   Is health event Displayed   |   current_health_events={current_health_events_details_object}   |    
        """
        try:
            self.__find_row(current_health_event)
            return True
        except:
            return False
