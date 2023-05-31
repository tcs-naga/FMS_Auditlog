__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from test_code.field.BasePage import BasePage
from selenium.webdriver.remote.webelement import WebElement

class BasePanel(BasePage):

    __panel = None
    __panel_div = '//div[text()=\'{}\']/../..'

    def get_panel(self, panel_title:str) -> WebElement:   
        """ retrieves the panel in the Field application for the given panel name

        Args:
            panel_title (str):  The panel title is the title in the gray bar at the top of the panel
        Returns:
            WebElement: _description_
        """
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__panel_div.format(panel_title))
        self.__panel = BuiltIn().run_keyword('Get WebElement', self.__panel_div.format(panel_title))
        return self.__panel   
