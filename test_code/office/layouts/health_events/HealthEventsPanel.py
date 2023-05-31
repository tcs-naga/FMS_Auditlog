__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.office.layouts.BaseLayout import BaseLayout
from selenium.webdriver.common.by import By

class HealthEventsPanel(BaseLayout):

    __panel_title = 'Health Events'
    __historic_health_events = './/div[contains(@class, \'MuiTabs\')]//button[text()=\'Historic Health Events\']'
    __current_health_events = './/div[contains(@class, \'MuiTabs\')]//button[text()=\'Current Health Events\']'

    def _get_panel(self):
        return self.get_layout(self.__panel_title)

    def click_historic_health_events(self):
        """ Clicks the click historic health events tab

        Examples:
            |   Click Historic Health Events   |
        """
        self.click(self._get_panel().find_element(By.XPATH, self.__historic_health_events))

    def click_current_health_events(self):
        """ Clicks the click current health events tab

        Examples:
            |   Click Current Health Events   |
        """
        self.click(self._get_panel().find_element(By.XPATH, self.__current_health_events))