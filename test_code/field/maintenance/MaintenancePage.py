__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from selenium.webdriver.common.by import By
from test_code.field.HomePage import HomePage
from time import sleep

class MaintenancePage(HomePage):

    __keypad_number_button = '//button[. = \'{}\']'
    __refuel_menu_title = "Refuel Amount"
    __refuel_keypad_number_visibility = '//div[@class=\'indicator\']/parent::div[.=\'{}L\']'
    __smu_hours_menu_title = "SMU Hours"
    __smu_hours_keypad_number_visibility = '//div[@class=\'indicator\']/parent::div[.=\'{}H\']'
    __backspace_button = '//button[./*[@data-icon=\'backspace\']]'
    __save_button = '//button[text()=\'Save\']'

    def key_in_refuel_liters(self, refuel_liters: str):
        """
        Enter refuel_liters for Maintenance

        Examples:
        | Key In Refuel Liters |
        """
        digits = ''
        for digit in range(0, len(refuel_liters)):
            sleep(0.1)
            digits += str(refuel_liters[digit])
            digits = str("{:0,}".format(int(digits.replace(',',''))))
            self.click(locator=self.__refuel_menu().find_element(By.XPATH, self.__keypad_number_button.format(refuel_liters[digit])))

    def verify_refuel_liters_have_been_entered(self, refuel_liters: str) -> bool:
        """
        Verify Refuel liters entered on field are correct

        Example:
            | Verify Refuel Liters Have Been Entered | REFUEL_LITERS |
        """
        return self.is_element_visible(self.__refuel_keypad_number_visibility.format(refuel_liters))

    def __refuel_menu(self):
        return HomePage.get_menu(self, self.__refuel_menu_title)

    def key_in_smu_hours(self, smu_hours: str):
        """
        Enter SMU Hours for Maintenance

        Examples:
        | Key In Smu Hours |
        """
        digits = ''
        for digit in range(0, len(smu_hours)):
            sleep(0.1)
            digits += smu_hours[digit]
            digits = str("{:0,}".format(int(digits.replace(',',''))))
            self.click(locator=self.__smu_hours_menu().find_element(By.XPATH, self.__keypad_number_button.format(smu_hours[digit])))

    def verify_smu_hours_have_been_entered(self, smu_hours: str) -> bool:
        """
        Verify SMU hours have been entered on field

        Examples:
            | Verify SMU Hours Have Been Entered | SMU_HOURS |
        """
        return self.is_element_visible(self.__smu_hours_keypad_number_visibility.format(smu_hours))

    def __smu_hours_menu(self):
        return HomePage.get_menu(self, self.__smu_hours_menu_title)

    def click_backspace(self):
        """ clicks the backspace button on the keypad

        Examples:
            | Click Backspace |
        """
        self.click(self.__backspace_button)

    def click_save(self):
        """ clicks the save button

        Examples:
            | Click Save |
        """
        self.click(self.__save_button)
