from test_code.office.BaseDialog import BaseDialog
from selenium.webdriver.common.by import By

class UpdateConfirmation(BaseDialog):
    
    def click_yes(self):
        """ clicks the yes button on update confirmation dialog
        
        Examples:
            | Click Yes |
        """
        self.click(self._get_cycle_update_dialog().find_element(By.XPATH, './/button[text()=\'Yes\']'))
        
    def click_no(self):
        """ clicks the no button on update confirmation dialog
        
        Examples:
            | Click No |
        """
        self.click(self._get_cycle_update_dialog().find_element(By.XPATH, './/button[text()=\'No\']'))