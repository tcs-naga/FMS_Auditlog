__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.data.AssetStateDetails import AssetStateDetails
from test_code.office.BaseDialog import BaseDialog
from selenium.webdriver.common.by import By
from time import sleep
from robot.api import logger

class NewStateDialog(BaseDialog):
    
    __start_input = './/div[text()=\'Start\']/following-sibling::div//input'
    __end_input = './/div[text()=\'End\']/following-sibling::div//input'
    __duration_input = './/div[text()=\'Duration\']/following-sibling::div//input'
    __reported_state_select = './/div[text()=\'Reported State\']/following-sibling::div//div[@role=\'button\']'
    __comment_textarea = './/div[text()=\'Comment\']/following-sibling::div//textarea'
    __cancel_button = './/button[text()=\'Cancel\']'
    __insert_button = './/button[text()=\'Insert\']'
    
    def fill_in_new_state_details(self, new_state: AssetStateDetails):
        """ fills in the new state details

        Args:
            new_state (AssetStateDetails): the asset state details to set
            
        Examples:
            |   Fill In New State Details   |   new_state=${new_asset_state_details_object} |
        """
        self.send_keys(self._get_dialog().find_element(By.XPATH, self.__start_input), new_state.get_reported_at_in_input_format())
        self.send_keys(self._get_dialog().find_element(By.XPATH, self.__end_input), new_state.get_ended_at_in_input_format())
        self.select(self._get_dialog().find_element(By.XPATH, self.__reported_state_select), new_state.state)
        self.send_keys(self._get_dialog().find_element(By.XPATH, self.__comment_textarea), new_state.comment)
        
    def click_cancel(self):
        """ clicks the cancel button
        
        Examples:
            |   Clicks the Cancel Button    |
        """
        self.click(self._get_dialog().find_element(By.XPATH, self.__cancel_button))
        sleep(.5)
        
    def click_insert(self):
        """ clicks the insert button
        
        Examples:
            |   Clicks the Insert Button    |
        """
        self.click(self._get_dialog().find_element(By.XPATH, self.__insert_button))
        
    def get_duration(self) -> str:
        """ gets the duration value displayed

        Returns:
            str: the duration
            
        Examples:
            |   Get Duration    |
        """
        return self._get_dialog().find_element(By.XPATH, self.__duration_input).get_attribute('value')
    
    def is_dialog_displayed(self) -> bool:
        """ returns a status based on whether the dialog is displayed

        Returns:
            bool: True id displayed otherwise False
            
        Examples:
            |   Is Dialog Displayed     |
        """
        try:
            self._get_dialog()
            return True
        except:
            return False