__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.office.layouts.BaseLayout import BaseLayout
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage
from time import sleep

class MinePerformancePanel(BaseLayout):

    __panel_title = 'Mine Performance'
    __movement_container = './/div[div[@class=\'title-box\' and text()=\'{}\']]'
    __movement_value = './/div[@class=\'value-value\']'
    __movement_unit = './/div[@class=\'value-unit\']'
    __shift_right = './/div[@class=\'shift-control\' and .//*[@data-icon=\'chevron-right\']]'
    __shift_left = './/div[@class=\'shift-control\' and .//*[@data-icon=\'chevron-left\']]'
    __shift_date = 'div.shift-date'
    __shift_name = 'div.shift-name'

    def get_panel(self):
        return self.get_layout(self.__panel_title)

    def capture_image_of_tile(self):
        """ captures an image of the asset details tile

        Examples
            | Capture Image Of Tile |
        """
        self.capture_image(self.get_panel(), self.__panel_title.replace(" ", "_") + 'Tile')

    def capture_image_of_tile_and_compare(self):
        """
        Captures an image of tile and compare

        Examples
            | Capture Image Of Tile And Compare |
        """
        self.capture_image_and_compare(self.get_panel(), self.__panel_title.replace(" ", "_") + 'Tile')

    def select_loader(self, loader: str):
        """ Selects the loader to filter on

        Args:
            loader (str): loader

        Examples:
            | Select Loader | loader=EX7109 |
        """
        self.select(self.get_panel().find_element(By.CSS_SELECTOR, 'div.filter-select:nth-child(1)'), loader)

    def select_hauler(self, hauler: str):
        """ Selects the hauler to filter on

        Args:
            hauler (str): hauler

        Examples:
            | Select Hauler | hauler=DT5401 |
        """
        self.select(self.get_panel().find_element(By.CSS_SELECTOR, 'div.filter-select:nth-child(2)'), hauler)

    def select_source(self, source: str):
        """ Selects the source to filter on

        Args:
            source (str): source

        Examples:
            | Select Source | source=DT5401 |
        """
        self.select(self.get_panel().find_element(By.CSS_SELECTOR, 'div.filter-select:nth-child(3)'), source)

    def select_destination(self, destination: str):
        """ Selects the destination to filter on

        Args:
            destination (str): destination

        Examples:
            | Select Destination | destination=DT5401 |
        """
        self.select(self.get_panel().find_element(By.CSS_SELECTOR, 'div.filter-select:nth-child(4)'), destination)

    def __find_movement_container(self, movement_type) -> WebElement:
        return self.get_panel().find_element(By.XPATH, self.__movement_container.format(movement_type))

    def get_movement_amount(self, type:str) -> int:
        container = self.__find_movement_container(type)
        value = int(container.find_element(By.XPATH, self.__movement_value).text.replace(',', ''))
        return value

    def click_shift_control_right(self):
        """ Clicks the shift control right button

        Examples:
            |   CLick Shift Control Right   |
        """
        displayed_shift_name = self.get_shift_name()
        timeout = 3
        while (displayed_shift_name == self.get_shift_name()) and timeout > 0:
            timeout -= 1            
            self.click(self.get_panel().find_element(By.XPATH, self.__shift_right))
            sleep(.5)
        if displayed_shift_name == self.get_shift_name():
            raise ExceptionWithScreenImage('Displayed shift name did not change')

    def click_shift_control_left(self):
        """ Clicks the shift control left button

        Examples:
            |   CLick Shift Control Left   |
        """
        displayed_shift_name = self.get_shift_name()
        timeout = 3
        while (displayed_shift_name == self.get_shift_name()) and timeout > 0:
            timeout -= 1            
            self.click(self.get_panel().find_element(By.XPATH, self.__shift_left))
            sleep(.5)
        if displayed_shift_name == self.get_shift_name():
            raise ExceptionWithScreenImage('Displayed shift name did not change')

    def get_shift_date(self) -> str:
        """ gets the displayed shift date

        Returns:
            str: shift date

        Examples:
            | Get Shift Date |
        """
        return self.get_panel().find_element(By.CSS_SELECTOR, self.__shift_date).text

    def get_shift_name(self) -> str:
        """ gets the displayed shift name

        Returns:
            str: shift name

            Examples:
            | Get Shift Name |
        """
        return self.get_panel().find_element(By.CSS_SELECTOR, self.__shift_name).text
    