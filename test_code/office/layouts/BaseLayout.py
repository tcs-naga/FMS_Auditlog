__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from abc import abstractmethod
from robot.libraries.BuiltIn import BuiltIn
from test_code.office.BasePage import BasePage
from test_code.RobotEyes import RobotEyes
from robot.api import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class BaseLayout(BasePage):

    __layout = None
    __layout_div = '//div[@class=\'mosaic-tile\' and .//div[@class=\'mosaic-window-title\' and text()=\'{}\']]'
    __cached_for = None

    def get_layout(self, layout_title:str, dialog_title='', clear_cache=False) -> WebElement:       
        """ retrieves the tile of the application with the given layout and dialog titles
        
        Caching is used in order to save execution time so the same tile is repeatedly searched for

        Args:
            layout_title (str):  The layout title is the title in the blue bar at the top of the tile
            dialog_title (str, optional):  The dialog title is the title of the sub screen within the tile e.g. Edit user, Add user Defaults to ''.
            clear_cache (bool, optional):  clear the cache for issues such as stale element exceptions  Defaults to False
        Returns:
            WebElement: _description_
        """

        if self.__layout is None or clear_cache==True or layout_title+dialog_title != BaseLayout.__cached_for:
            BuiltIn().run_keyword('Wait Until Element Is Visible', self.__layout_div.format(layout_title))
            self.__layout = BuiltIn().run_keyword('Get WebElement', self.__layout_div.format(layout_title))
            BaseLayout.__cached_for = layout_title+dialog_title
        return self.__layout

    @abstractmethod
    def get_panel(self):
        pass

    def close_panel(self):
        """ closes the panel
            needs to be called from the panel declaration so it knows which panel to close

        Examples:
            | Close Panel |
        """
        self.click(self.get_panel().find_element(By.XPATH, './/button[2]'))
        BaseLayout.__cached_for = None

    @staticmethod
    def clear_cache():
        BaseLayout.__cached_for=None