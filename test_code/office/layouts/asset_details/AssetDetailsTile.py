__copyright__ = (
    "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"
)

from test_code.data.ActivityDetails import ActivityDetails
from test_code.office.layouts.BaseLayout import BaseLayout
from selenium.webdriver.common.by import By
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import time
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage

class AssetDetailsTile(BaseLayout):
    __asset_properties_activity = ".//div[text() = 'Activity']/following-sibling::div"
    __asset_properties_assignment = ".//div[text() = 'Assignment']/following-sibling::div"
    __asset_properties_material = ".//div[text() = 'Material']/following-sibling::div"
    __asset_summary_activity = ".//div[text() = '{}']/following-sibling::div[2]"
    __asset_summary_assignment = ".//div[text() = '{}']/following-sibling::div[1]"
    __asset_summary_payload = ".//div[text() = '{}']/../following-sibling::div[1]//div[text() = 'PAYLOAD']/div[1]"
    __new_activity_button = './/following-sibling::div//button[text()=\'New Activity\']'
    __new_delay_button = './/following-sibling::div//button[text()=\'New Delay\']'
    __tile_title = "Asset Details"
    __stop_delay_button = './/following-sibling::div//button[text()=\'Stop Delay\']'

    def get_activity(self) -> str:
        element = self.get_tile().find_element(
            By.XPATH, self.__asset_properties_activity
        )
        return element.text
    
    def get_assignment(self) -> str:
        element = self.get_tile().find_element(
            By.XPATH, self.__asset_properties_assignment
        )
        return element.text

    def get_material(self) -> str:
        element = self.get_tile().find_element(
            By.XPATH, self.__asset_properties_material
        )
        return element.text

    def get_summary_activity(self) -> str:
        element = self.get_tile().find_element(
            By.XPATH, self.__asset_summary_activity
        )
        return element.text
    
    def get_summary_assignment(self) -> str:
        element = self.get_tile().find_element(
            By.XPATH, self.__asset_summary_assignment
        )
        return element.text

    def is_activity_set(self, activity: str) -> bool:
        element = self.get_tile().find_element(
            By.XPATH, self.__asset_properties_activity
        )
        if element.text == activity:
            return True
        logger.info('looking for activity: {}, and found {} in UI '.format(activity, element.text))
        return False

    def is_assignment_set(self, assignment: str) -> bool:
        element = self.get_tile().find_element(
            By.XPATH, self.__asset_properties_assignment
        )
        if element.text == assignment:
            return True
        return False
    
    def is_material_set(self, material: str) -> bool:
        element = self.get_tile().find_element(
            By.XPATH, self.__asset_properties_material
        )
        if element.text == material:
            return True
        return False

    def is_summary_activity_set(self, asset: str, activity: str) -> bool:
        try:
            element = self.get_tile().find_element(
                By.XPATH, self.__asset_summary_activity.format(asset)
            )
            if element.text == activity:
                return True
            logger.info('looking for activity: {}, and found {} in UI '.format(activity, element.text))
            return False
        except:
            return False

    def is_summary_assignment_set(
        self, asset: str, assignment: str
    ) -> bool:
        try:
            element = self.get_tile().find_element(
                By.XPATH, self.__asset_summary_assignment.format(asset)
            )
            if element.text == assignment:
                return True
            logger.info('looking for asset: {}, and assignment: {}, but found {}'.format(asset, assignment, element.text))
            return False
        except:
            logger.info('element {} not found'.format(element))
            return False

    def is_summary_payload_set(
        self, asset: str, payload: str
    ) -> bool:
        try:
            element = self.get_tile().find_element(
                By.XPATH, self.__asset_summary_payload.format(asset)
            )
            if element.text == payload:
                return True
            logger.info('looking for asset: {}, and payload: {}, but found {}'.format(asset, payload, element.text))
            return False
        except:
            logger.info('element {} not found'.format(element))
            return False

    def wait_for_asset_state(self, assetId: str, state:str, wait_time_seconds:int=60):
        current_state = (self.get_tile().find_element(By.XPATH, self.__asset_properties_activity)).text
        timeout = 0

        while current_state.strip().lower() != state.strip().lower() and timeout < wait_time_seconds/5:
            try:
                current_state = (self.get_tile().find_element(By.XPATH, self.__asset_properties_activity)).text
            except:
                pass
            timeout = timeout + 1
            time.sleep(5)

        if current_state.strip().lower() != state.strip().lower():
            raise ExceptionWithScreenImage('Asset {} has not reached desired state: {}'.format(assetId, state))

    def refresh(self):
        return self.get_layout(self.__tile_title, clear_cache=True)

    def get_tile(self):
        return self.get_layout(self.__tile_title)

    def capture_image_of_tile(self):
        """captures an image of the asset details tile
        Saves the image as Asset_DetailsTile

        Examples
            | Capture Image Of Tile |
        """
        self.capture_image(self.get_tile(), self.__tile_title.replace(" ", "_") + 'Tile')

    def capture_image_of_tile_and_compare(self):
        """
        Captures an image of tile and compare

        Examples
            | Capture Image Of Tile And Compare |
        """
        self.capture_image_and_compare(self.get_tile(), self.__tile_title.replace(" ", "_") + 'Tile')

    def select_asset(self, assetId: str):
        """ select asset

        Args:
            assetId (str): the asset
        """
        control = self.get_tile().find_element(By.XPATH, './/button[@aria-haspopup=\'listbox\']')
        BuiltIn().run_keyword('Sleep', '0.5')
        # We wait for 0.5 sec, so double this value.
        timeout = int(BuiltIn().get_variable_value('${MAX_WAIT}')) * 2
        while True:
            self.click(control)
            self.click(control.find_element(By.XPATH, './following-sibling::div//ul[@role=\'listbox\']//li[text()=\'{}\']'.format(assetId)))
            BuiltIn().run_keyword('Sleep', '0.5')
            timeout -= 1
            if self.__is_asset_selected(assetId)  or timeout == 0:
                break
        if not self.__is_asset_selected(assetId):
            raise ExceptionWithScreenImage('Failed to select Asset in Asset Details panel')

    def __is_asset_selected(self, assetId) -> bool:
        try:
            self.get_tile().find_element(By.XPATH, './/button[@aria-haspopup=\'listbox\' and contains(text(), \'{}\')]'.format(assetId))
            return True
        except:
            return False

    def edit_activity(self, activity: ActivityDetails):
        """ edit the activity for currently selected asset

        Args:
            activity (ActivityDetails): the activity details to edit

        Examples:
            | Edit Activity |
        """
        control = self.__expand_section('Activity')
        self.click(control.find_element(By.XPATH, './/following-sibling::div//button[text()=\'New Activity\']'))
        from test_code.office.layouts.asset_details.NewActivityDialog import NewActivityDialog
        new_activity_dialog = NewActivityDialog()
        new_activity_dialog.fill_in_new_activity_details(activity)
        new_activity_dialog.click_set()
    
    def __get_section(self, section):
        return self.get_tile().find_element(By.XPATH, './/div[contains(@class,\'expandable\') and .//div[text()=\'{}\']]'.format(section))
    
    def __expand_section(self, section):
        count=0
        while count<10:
            # a button appears in all expandable areas so will be used to determine expanded status
            try:
                control = self.__get_section(section)
                control.find_element(By.XPATH, './/following-sibling::div//button')
                break
            except:
                self.click(control)
                time.sleep(.5)

            count=count+1
        return self.__get_section(section)

    def get_current_activity(self) -> str:
        """ get the current activity for the currently selected asset

        Returns:
            str: the activity
            
        Examples:
            | Get Current Activity |
        """
        control = self.__get_section('Activity')
        return control.find_element(By.XPATH, './div[3]').text

    def current_activity_should_be(self, expected_activity: str) -> bool:
        """ get the current activity for the currently selected asset

        Returns:
            str: the activity

        Examples:
            | Current Activity Should Be | Expected Activity |
        """
        # We wait for 0.5 sec, so double this value.
        timeout = int(BuiltIn().get_variable_value('${MAX_WAIT}')) * 2
        while(timeout):
            timeout -= 1
            BuiltIn().run_keyword('Sleep', '0.5')
            actual_activity = self.get_current_activity()
            if actual_activity == expected_activity:
                return True
        raise ExceptionWithScreenImage(f"Expected activity {expected_activity}, doesn't match with actual activity {actual_activity}")


    def get_list_of_available_activities(self) -> list:
        """ get the list of available activities for selected asset removing the default

        Returns:
            list: list of activities

        Examples:
            | Get List of Available Activities |
        """
        control = self.__expand_section('Activity')
        self.click(control.find_element(By.XPATH, self.__new_activity_button))
        from test_code.office.layouts.asset_details.NewActivityDialog import NewActivityDialog
        new_activity_dialog = NewActivityDialog()
        BuiltIn().run_keyword("Sleep", 0.5)
        list = new_activity_dialog.get_list_of_activity_type_options()
        list.remove('Activity')
        return list
    
    def get_list_of_available_delays(self) -> list:
        """ get list of available delays

        Returns:
            list: list of delays

        Examples:
            | Get List OF Available Delays |
        """
        control = self.__expand_section('Delay')
        self.click(control.find_element(By.XPATH, self.__new_activity_button))
        from test_code.office.layouts.asset_details.NewDelayDialog import NewDelayDialog
        new_delay_dialog = NewDelayDialog()
        list = new_delay_dialog.get_list_of_delay_options()
        list.remove('Delay')
        return list
    
    def get_list_of_available_delay_categories(self) -> list:
        """ get list of available delay categories removing the default

        Returns:
            list: list of delay categories

        Examples:
            | Get List Of Available Delay Categories |
        """
        control = self.__expand_section('Delay')
        self.click(control.find_element(By.XPATH, self.__new_delay_button))
        from test_code.office.layouts.asset_details.NewDelayDialog import NewDelayDialog
        new_activity_dialog = NewDelayDialog()
        list = new_activity_dialog.get_list_of_delay_category_options()
        list.remove('Category')
        return list

    def create_new_delay(self, delay_category: str, delay: str, comment: str = None):
        """ edit the delay for currently selected asset

        Args:
            delay_category (str): the delay category
            delay (str): the delay

        Examples:
            | Edit Delay |  delay_category=Operating Delay |  delay=Cooling |
        """
        control = self.__expand_section('Delay')
        self.click(control.find_element(By.XPATH, './/following-sibling::div//button[text()=\'New Delay\']'))
        from test_code.office.layouts.asset_details.NewDelayDialog import NewDelayDialog
        new_delay_dialog = NewDelayDialog()
        new_delay_dialog.fill_in_delay_details(delay_category, delay, comment)
        new_delay_dialog.click_set()
        self.wait_for_success_popup_to_disappear()
        
    def get_current_delay(self) -> str:
        """ get the current delay for the currently selected asset

        Returns:
            str: the delay
            
        Examples:
            | Get Current Delay |
        """
        control = self.__get_section('Delay')
        return control.find_element(By.XPATH, './div[3]').text

    def current_delay_should_be(self, expected_delay: str) -> bool:
        """ get the current delay for the currently selected asset and compare with expected.

        Returns:
            str: Bool

        Examples:
            | Current Activity Should Be | Expected Activity |
        """
        # We wait for 0.5 sec, so double this value.
        timeout = int(BuiltIn().get_variable_value('${MAX_WAIT}')) * 2
        while(timeout):
            timeout -= 1
            BuiltIn().run_keyword('Sleep', '0.5')
            actual_delay = self.get_current_delay()
            if actual_delay == expected_delay:
                return True
        raise ExceptionWithScreenImage(f"Expected delay {expected_delay}, doesn't match with actual delay {actual_delay}")
        

    def click_stop_delay(self):
        """ clicks the stop delay button

        Examples:
            | Click Stop Delay |
        """
        control = self.__expand_section('Delay')
        self.click(control.find_element(By.XPATH, self.__stop_delay_button))
        self.wait_for_success_popup_to_disappear()
        
    def click_edit_delay(self):
        """ clicks the edit delay button

        Examples:
            | Click Edit Delay |
        """
        control = self.__expand_section('Delay')
        self.click(control.find_element(By.XPATH, './/following-sibling::div//button[text()=\'Edit Delay\']'))

    def get_configured_ruleset(self) -> str:
        """ gets the configured ruleset

        Returns:
            str: configured ruleset

        Examples:
            | Get Configured Ruleset |
        """

        BuiltIn().run_keyword('Scroll Element Into View', self.get_tile().find_element(By.XPATH, './/div[text()=\'Configured RuleSet\']/following-sibling::div'))
        return self.get_tile().find_element(By.XPATH, './/div[text()=\'Configured RuleSet\']/following-sibling::div').text

    def get_cycle_payload_evaluation_mode(self) -> str:
        """ gets the cycle payment evaluation mode

        Returns:
            str: cycle payment evaluation mode

        Examples:
            | Get Cycle Payload Evaluation Mode |
        """
        control = self.__get_section('Cycle Payload Evaluation Mode')
        return control.find_element(By.XPATH, './div[3]').text

    def get_dump_detection(self) -> str:
        """ gets the dump detection

        Returns:
            str: dump detection

        Examples:
            | Get Dump Detection |
        """
        control = self.__get_section('Dump Detection')
        return control.find_element(By.XPATH, './div[3]').text

    def is_stop_delay_displayed(self) -> bool:
        """ clicks the stop delay button

        Examples:
            | Is Stop Delay Displayed |
        """
        control = self.__expand_section('Delay')
        try:
            control.find_element(By.XPATH, self.__stop_delay_button)
            return True
        except:
            return False
        
    def click_new_delay(self):
        """ expands the delay section and clicks new delay

        Examples:
            | Click New Delay |
        """
        control = self.__expand_section('Delay')
        self.click(control.find_element(By.XPATH, './/following-sibling::div//button[text()=\'New Delay\']'))