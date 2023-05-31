__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.data.ActivityDetails import ActivityDetails
from selenium.webdriver.common.by import By
import time

from test_code.office.layouts.asset_details.AssetDetailsTile import AssetDetailsTile

class NewActivityDialog(AssetDetailsTile):
    

    __activity_type_select = './/div[text()=\'Activity Type *\']/following-sibling::div//div[@role=\'button\']'
    __comment_textarea = './/div[text()=\'Comment\']/following-sibling::div//textarea'
    __cancel_button = './/button[text()=\'Cancel\']'
    __set_button = './/button[text()=\'Set\']'
    
    __dialog = './/div[contains(@class, \'dialog \') and .//div[text()=\'New Activity\']]'

    def __get_dialog(self):
        dialog = self.get_tile().find_element(By.XPATH, self.__dialog)
        return dialog
    
    def fill_in_new_activity_details(self, activity: ActivityDetails):
        """ fills in the new activity details form

        Args:
            activity (ActivityDetails): the activity details to fill in
            
        Examples:
            |   Fill In New Activity Details    |   activity=${activity_details_object} |
        """
        self.select(self.__get_dialog().find_element(By.XPATH, self.__activity_type_select), activity.activity_friendly_name)
        self.send_keys(self.__get_dialog().find_element(By.XPATH, self.__comment_textarea), activity.comment)
        
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
        
    def get_list_of_activity_type_options(self):
        """ get a list of the options available for an activity type
            
        Examples:
            |   Get List Of Activity Type Options    |
        """
        return self.get_select_options(self.__get_dialog().find_element(By.XPATH, self.__activity_type_select))
