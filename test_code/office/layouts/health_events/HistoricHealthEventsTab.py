__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.data.HealthEventDetails import HealthEventDetails
from test_code.office.layouts.health_events.HealthEventsPanel import HealthEventsPanel
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_code.office.layouts.Grid import Grid

class HistoricHealthEventsTab(HealthEventsPanel):

    __asset_select_button = './/div[contains(@class, \'MuiInput\')]//div[@role=\'button\' and text()=\'{}\']'
    __grid_class = '.MuiDataGrid-root'

    def __get_grid(self):
        return Grid(self._get_panel().find_element(By.CSS_SELECTOR, self.__grid_class))

    def select_time_range(self, time_range: str):
        """ selects time range to display health events for

        Args:
            time_range (str): the time range to filter

        Examples:
            |   Select Time Range    |   Past 48 Hours   |
        """
        time_range_button = self._get_panel().find_element(By.XPATH, self.__asset_select_button.format('Past 15 Minutes'))
        self.select_from_menu(time_range_button, time_range)

    def __find_row(self, historic_health_events: HealthEventDetails) -> WebElement:
        return self.__get_grid().get_row([historic_health_events.assetId, historic_health_events.level, historic_health_events.eventType, historic_health_events.operator], number_of_columns_to_skip_from_start=2)

    def is_health_event_displayed(self, historic_health_event: HealthEventDetails) -> bool:
        """ gets a status based on if the health event is displayed

        Args:
            historic_health_event (HealthEventDetails): the historic health events to find

        Returns:
            bool: True if the historic health events is displayed otherwise False

        Examples:
            |   Is health event Displayed   |   historic_health_events={historic_health_events_details_object}   |    
        """
        try:
            self.__find_row(historic_health_event)
            return True
        except:
            return False
