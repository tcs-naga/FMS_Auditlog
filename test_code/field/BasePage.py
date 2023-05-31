__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from time import sleep
from selenium.webdriver.common.by import By
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage

class BasePage:

    __logged_in_user_class = 'class:user-name-widget'
    __smu_hours_button = '//div[.=\'SMU hours\']'    
    __open_toggle_menu_button = '//button[@aria-label=\'toggle menu\' and //*[@data-icon=\'bars\']]'
    __close_toggle_menu_button = '//button[@aria-label=\'toggle menu\' and //*[@data-icon=\'times\']]'
    __logout_button = '//button[. = \'Log out\']'
    __button_with_text = '//button[. = \'{}\']'
    __delete_button = '//button[.=\'0\']/../button[2]'
    __menu_item = '//nav//li[.=\'{}\']'
    __header = '//div[./div[contains(@class, \'status-signal-widget \')]]'
    __sub_menu = '//nav/../following-sibling::div[.//div[text()=\'{}\']]'
    __sub_menu_header = '//div[contains(@class, \'select-menu-heading\') and text()=\'{}\']'
    __sub_menu_item = './/div[@role=\'button\' and (text()=\'{0}\' or ./div[text()=\'{0}\'])]'
    __activity_button = '//button[@class=\'status-block\']'
    __activity = 'div.activity'
    __delay_button = 'button.delay-block'
    __delay = 'button.delay-block div.upper'
    __status_block_activity = "//button[@class = 'status-block']/div[contains(@class, 'row top')]/div[contains(@class, 'activity')]"
    __status_block_assignment = "//button[@class = 'status-block']/div[contains(@class, 'row bottom')]/span"
    __status_block_material = "//button[@class = 'status-block']/div[contains(@class, 'row top')]/div[contains(@class, 'material')]"

    def is_status_block_activity_set(self, activity: str) -> bool:
        element = BuiltIn().run_keyword(
            'Get WebElement', self.__status_block_activity
        )
        if element.text == activity:
            return True
        logger.info('looking for activity: {}, and found {} in UI '.format(activity, element.text))
        return False

    def wait_for_asset_state(self, assetId: str, state:str, wait_time_seconds:int=60):
        current_state = (BuiltIn().run_keyword('Get WebElement', self.__status_block_activity)).text
        timeout = 0

        while current_state.strip().lower() != state.strip().lower() and timeout < wait_time_seconds/5:
            try:
                current_state = (BuiltIn().run_keyword('Get WebElement', self.__status_block_activity)).text
            except:
                pass
            timeout = timeout + 1
            sleep(5)

        if current_state.strip().lower() != state.strip().lower():
            raise ExceptionWithScreenImage('Asset {} has not reached desired state: {}'.format(assetId, state))

    def is_status_block_assignment_set(self, assignment: str) -> bool:
        element = BuiltIn().run_keyword(
            'Get WebElements', self.__status_block_assignment
        )
        if len(element) > 1:
            if f"{element[0].text} {element[1].text}" == assignment:
                return True
        else:
            if element[0].text == assignment:
                return True
        return False
    
    def is_status_block_material_set(self, material: str) -> bool:
        element = BuiltIn().run_keyword(
            'Get WebElement', self.__status_block_material
        )
        if element.text == material:
            return True
        return False
    
    def get_logged_in_user(self) -> str:
        """ gets the currently logged in user

        Returns:
            str: the user logged in

        Examples:
            |   Get Logged In User  |
        """
        return BuiltIn().run_keyword('Get Text', self.__logged_in_user_class)

    def logout(self):
        """ logs the current user out of the application

        Example:
            |   Logout  |
        """
        self._click_menu_toggle()
        # This can fail as menu open is slow, so try for 15 sec, before failing.
        timeout = 30
        success = False
        while timeout and not success:
            try:
                self.click(self.__logout_button)
                success = True
            except Exception as e:
                if timeout:
                    timeout -= 1
                    sleep(0.5)
                else:
                    raise e

    def _click_menu_toggle(self):
        if BuiltIn().run_keyword_and_return_status('Page Should Contain Element', self.__open_toggle_menu_button):
            try:
                self.click(self.__open_toggle_menu_button)
            except:
                pass

    def __wait_for_page_load(self):
        BuiltIn().run_keyword('Wait Until Page Contains Element', self.__smu_hours_button)

    def close_menu_bar(self):
        """ Close menu bar to close SMU hours window

        Example:
            |   Close Menu Bar  |
        """
        self.__wait_for_page_load()
        self.click(self.__close_toggle_menu_button)

    def click(self, locator, timeout=10):
        """
        Click element on field web UI

        """
        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
        while timeout:
            try:
                BuiltIn().run_keyword('Click Element', locator)
                return True
            except Exception as e:
                # TODO: Remove following line when debugging is complete
                logger.info('Exception occured: {}'.format(e))
                if timeout:
                    timeout -= 1
                    sleep(0.5)
                else:
                    raise e
        return False

    def is_element_visible(self, locator) -> bool:
        """ opens the apply layout menu and selects the layout to display
        Args:
            locator (str): the element

        Returns:
            bool: `True` if the locator is displayed; `False` otherwise.

        Examples:
            | Is Element Visible | locator |
        """
        try:
            BuiltIn().run_keyword('Page Should Contain Element', locator)
            return True
        except:
            return False

    def click_button_by_text(self, button_text:str):
        locator = self.__button_with_text.format(button_text)
        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
        self.click(locator)

    def click_delete_button(self):
        locator = self.__delete_button
        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
        self.click(locator)

    def send_keys(self, locator, value):
        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
        BuiltIn().run_keyword('Press Keys', locator, 'CTRL+A+DELETE')
        BuiltIn().run_keyword('Press Keys', locator, value)

    def capture_image(self, element, name):
        BuiltIn().run_keyword('Capture Given Element', element, name)

    def capture_image_and_compare(self, element, name):
        BuiltIn().run_keyword('Capture Given Element And Compare', element, name)

    def __get_header(self):
        BuiltIn().run_keyword('Wait Until Element Is Visible', self.__header)
        return BuiltIn().run_keyword('Get WebElement', self.__header)

    def capture_full_screen_without_header(self, name):
        redact_region = BuiltIn().get_variable_value('${REDACT_REGION_Centurion}')
        logger.info('redact_region {}'.format(redact_region))

        BuiltIn().run_keyword('test_code.RobotEyes.Capture Full Screen', 'redact={}'.format('["' + self.__header + '"]'), 'name={}'.format(name), 'redact_region={}'.format(redact_region))

    def capture_full_screen_without_header_and_compare(self, name):
        redact_region = BuiltIn().get_variable_value('${REDACT_REGION_Centurion}')
        logger.info('redact_region {}'.format(redact_region))

        BuiltIn().run_keyword('test_code.RobotEyes.Capture Full Screen And Compare', 'redact={}'.format('["' + self.__header + '"]'), 'name={}'.format(name), 'redact_region={}'.format(redact_region))


    def _open_menu_option(self, menu_item):
        self._click_menu_toggle()
        try:
            self.click(self.__menu_item.format(menu_item))
        except:
            self.click(self.__menu_item.format(menu_item))
        #header changes for delays
        if menu_item=='Delays':
            menu_item='Delay'
        return BuiltIn().run_keyword('Get WebElement', self.__sub_menu.format(menu_item))

    def _open_sub_menu_option(self, menu_item, sub_menu_item):
        sub_menus = self._open_menu_option(menu_item)
        try:
            self.click(sub_menus.find_element(By.XPATH, './/div[contains(@class, \'MuiListItemButton-root\') and text()=\'' + sub_menu_item + '\']'))
        except:
            self.click(self.__menu_item.format(menu_item))

    def _get_list_of_menu_options(self, menu_item:str, sub_menu_item: str=None) -> list:
        sub_menus = self._open_menu_option(menu_item)
        if sub_menu_item is None:
            list_of_menu_item_elements = sub_menus.find_elements(By.CSS_SELECTOR, '.MuiListItemButton-root')
            menus = []
            for menu_item in list_of_menu_item_elements:
                menus.append(menu_item.text)
            return menus
        else:
            self.click(sub_menus.find_element(By.XPATH, './/div[contains(@class, \'MuiListItemButton-root\') and text()=\'' + sub_menu_item + '\']'))
            BuiltIn().run_keyword("Wait Until Page Contains Element", self.__sub_menu_header.format(sub_menu_item))
            BuiltIn().run_keyword("Sleep", 0.5)
            sub_menu_items = sub_menus.find_element(By.XPATH, './following-sibling::div').find_elements(By.CSS_SELECTOR, '.MuiListItemButton-root')
            menus = []
            for menu_item in sub_menu_items:
                menus.append(menu_item.text)
            return menus

    def change_activity(self, new_activity: str):
        """ changes the activity in the field

        Args:
            new_activity (str): the activity to select
            
        Examples:
            |  Change Activity  |  new_activity=Load  |
        """
        self.click(self.__activity_button)
        activity_menu = BuiltIn().run_keyword('Get WebElement', self.__sub_menu.format('Activity'))
        self.click(activity_menu.find_element(By.XPATH, self.__sub_menu_item.format(new_activity)))
        count = 0
        while count < 5 and new_activity.upper() !=self.get_activity():
            sleep(.5)
            count = count + 1
            pass
        
        if new_activity.upper() !=self.get_activity():
            raise ExceptionWithScreenImage('Activity has not changed to: ' + new_activity + 'current displaying: ' + self.get_activity())

    def get_activity(self) -> str:
        """ gets the currently displayed activity in the Field

        Returns:
            str: activity
            
        Examples:
            | Get Activity |
        """
        activity = BuiltIn().run_keyword('Get WebElement', 'css:' + self.__activity)
        return activity.text
    
    def is_activity_displayed(self) -> bool:
        """ returns a status on whether an activity is displayed on screen

        Returns:
            bool: True if activity is displayed otherwise false
            
        Examples:
            |  Is Activity Displayed  | 
        """
        try:
            BuiltIn().run_keyword('Get WebElement', self.__activity_button)
            return True
        except:
            return False
        
    def select_menu_option(self, menu_item:str, sub_menu_item:str=None):
        sub_menus = self._open_menu_option(menu_item)
        if sub_menu_item is not None:
            self.click(sub_menus.find_element(By.XPATH, './/div[contains(@class, \'MuiListItemButton-root\') and text()=\'' + sub_menu_item + '\']'))

    def change_delay(self, delay_category: str, new_delay: str):
        """ changes the delay in the field

        Args:
            delay_category (str): the delay category delay
            new_delay (str): the delay to select
            
        Examples:
            |  Change Delay  |  delay_category=Operating Delay  |  new_delay=Cooling  |
        """
        self.click('css:' + self.__delay_button)
        BuiltIn().run_keyword("Wait Until Page Contains Element", self.__sub_menu.format('Delay'))
        delay_categories_menu = BuiltIn().run_keyword('Get WebElement', self.__sub_menu.format('Delay'))
        BuiltIn().run_keyword("Wait Until Page Contains Element", self.__sub_menu.format(delay_category))
        self.click(delay_categories_menu.find_element(By.XPATH, self.__sub_menu_item.format(delay_category)))
        self.click(delay_categories_menu.find_element(By.XPATH, './following-sibling::div').find_element(By.XPATH, self.__sub_menu_item.format(new_delay)))
        count = 0
        while count < 5 and new_delay.upper() !=self.get_delay():
            sleep(.5)
            count = count + 1
            pass

        if new_delay.upper() !=self.get_delay():
            raise ExceptionWithScreenImage('Delay has not changed to: ' + new_delay)
        
    def get_delay(self) -> str:
        """ gets the currently displayed dealy in the Field

        Returns:
            str: delay
            
        Examples:
            | Get Delay |
        """
        activity = BuiltIn().run_keyword('Get WebElement', 'css:' + self.__delay)
        return activity.text

    def stop_delay(self):
        """ Stops the current delay

        Args:
            new_dealy (str): the delay to select
            
        Examples:
            |  Stop Delay  |
        """
        self.click('css:' + self.__delay_button)
        BuiltIn().run_keyword("Wait Until Page Contains Element", self.__sub_menu.format('Delay'))
        delay_categories_menu = BuiltIn().run_keyword('Get WebElement', self.__sub_menu.format('Delay'))
        self.click(delay_categories_menu.find_element(By.XPATH, './/button[text()=\'Stop\']'))