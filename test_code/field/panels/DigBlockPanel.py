__copyright__ = (
    "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"
)

from test_code.field.panels.BasePanel import BasePanel
from selenium.webdriver.common.by import By


class DigBlockPanel(BasePanel):
    __panel_title = "Dig Source"
    __dig_source_button = ".//button[@type = 'button' and .//div[text() = 'Dig Source' or @class = 'no-value']]"
    __clear_dig_source_button = ".//button[@type = 'button' and .//span[text() = 'Clear dig source']]"
    __select_dig_source_button = ".//button[@type = 'button' and .//div[@class = 'source-name' and text() = '{}']]"
    __material_type = '//button[.//div[@class=\'title\' and text()=\'Material Type\']]'
    __material_type_option = '//button[.//div[contains(@class,\'big\') and text()=\'{}\']]'
    __reset_material =\
        '//button[.//span[text()=\'Reset Material\']]'

    def clear_dig_source(self):
        self.click(
            self.__panel().find_element(By.XPATH, self.__dig_source_button)
        )
        self.click(
            self.__panel().find_element(
                By.XPATH, self.__clear_dig_source_button
            )
        )

    def select_dig_source(self, source: str):
        self.click(
            self.__panel().find_element(By.XPATH, self.__dig_source_button)
        )
        self.click(
            self.__panel().find_element(
                By.XPATH, self.__select_dig_source_button.format(source)
            )
        )

    def click_material(self):
        self.click(self.__panel().find_element(By.XPATH, self.__material_type))

    def select_dig_material(self, material_code: str):
        """
        Select a dig material from the selection panel.

        Examples:
        | Select Dig Material | DR |
        """
        self.click_material()
        self.click(
            self.__panel().find_element(
                By.XPATH, self.__material_type_option.format(material_code)
            )
        )

    def __panel(self):
        return self.get_panel(self.__panel_title)

    def reset_material(self):
        """ resets the material

        Examples:
            | Reset Material |
        """
        self.click_material()
        self.click(self.__panel().find_element(By.XPATH, self.__reset_material))
