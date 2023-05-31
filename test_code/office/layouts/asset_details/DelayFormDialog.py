__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from abc import ABC, abstractmethod
from selenium.webdriver.common.by import By
import time
from robot.api import logger

from test_code.office.layouts.asset_details.AssetDetailsTile import AssetDetailsTile

class DelayFormDialog(AssetDetailsTile, ABC):
    

    __delay_category_select = './/div[text()=\'Delay Category *\']/following-sibling::div//div[@role=\'button\']'
    __delay_select = './/div[text()=\'Delay *\']/following-sibling::div//div[@role=\'button\']'
    __comment_textarea = './/div[text()=\'Comment\']/following-sibling::div//textarea'
    __cancel_button = './/button[text()=\'Cancel\']'
    __set_button = './/button[text()=\'Set\']'
    __comment_textarea = './/div[text()=\'Comment\']/following-sibling::div//textarea'
    __dialog = './/div[contains(@class, \'dialog \') and .//div[text()=\'{}\']]'

    @abstractmethod
    def get_dialog_title(self):
        pass
    
    def __get_dialog(self):
        dialog = self.get_tile().find_element(By.XPATH, self.__dialog.format(self.get_dialog_title()))
        return dialog
        
    def select_delay_category(self, delay_category: str):
        """ selects the delay category

        Args:
            delay_category (str): the delay category
        """
        self.select(self.__get_dialog().find_element(By.XPATH, self.__delay_category_select), delay_category)
        
    def click_cancel(self):
        """ clicks the cancel button
        
        Examples:
        
            |   Click Cancel    |
        """
        self.click(self.__get_dialog().find_element(By.XPATH, self.__cancel_button))
        time.sleep(.5)
        
    def click_set(self):
        """ clicks the set button
        
        Examples:
        
            |   Click Set    |
        """
        self.click(self.__get_dialog().find_element(By.XPATH, self.__set_button))
    
    def is_dialog_displayed(self) -> bool:
        """ returns a status based on whether the New Activity Dialog is displayed

        Returns:
            bool: True if displayed otherwise False
        """
        try:
            self.__get_dialog()
            return True
        except:
            return False
        
    def get_list_of_delay_category_options(self):
        """ get a list of the options available for a delay category
            
        Examples:
            |   Get List Of Delay Category Options    |
        """
        return self.get_select_options(self.__get_dialog().find_element(By.XPATH, self.__delay_category_select))
    
    def get_list_of_delay_options(self) -> list:
        """ get a list of the options available for a delay category
            
        Examples:
            |   Get List Of Delay Options    |
        """
        list = self.get_select_options(self.__get_dialog().find_element(By.XPATH, self.__delay_select))
        list.remove('Delay')
        logger.debug(list)
        return list

    def select_delay(self, delay: str):
        """ selects the delay category

        Args:
            delay_category (str): the delay category
        """
        self.select(self.__get_dialog().find_element(By.XPATH, self.__delay_select), delay)

    def set_comment(self, comment:str):
        """ sets the comment textarea

        Args:
            comment (str): comment
            
        Examples:
            |  Set Comment |
        """
        self.send_keys(self.__get_dialog().find_element(By.XPATH, self.__comment_textarea), comment)

    def fill_in_delay_details(self, delay_category: str, delay: str, comment: str = None):
        """ fill in the delay details

        Args:
            delay_category (str): delay category
            delay (str): delay
            comment (str, optional): comment. Defaults to None.
            
        Examples:
            | Fill In Delay Details | delay_category=Operating Delay | delay=Cooling | comment=change of delay |
        """
        self.select_delay_category(delay_category)
        self.select_delay(delay)
        if comment is not None:
            self.set_comment(comment)
        
    def is_dialog_displayed(self) -> bool:
        """ returns a status on whether the dialog is displayed

        Returns:
            bool: true if displayed otherwise false

        Examples:
            | Is Dialog Displayed |
        """
        try:
            self.__get_dialog()
            return True
        except:
            return False
