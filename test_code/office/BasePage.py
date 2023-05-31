__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from time import sleep
from test_code.RobotEyes import RobotEyes
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage

class BasePage:

    __toggle_menu_button = '//button[@aria-label=\'Add Panels\']'
    __apply_layout_button = '//button[@aria-label=\'Apply Layout\']'
    __close_menu_div = '//div[@class=\'close-button\']'
    __logout_button = '//button[. = \'Log out\']'
    __button_with_text = '//button[. = \'{}\']'
    __apply_layout_menu_option = '//div[@role=\'button\' and .=\'{}\']'
    __add_panel_menu_option = '//div[@role=\'button\' and .//div[text()=\'{}\']]'
    __select_option = '//ul[contains(@class, \'MuiMenu-list\')]/li[.=\'{0}\' or text()=\'{0}\'][{1}]'
    __success_popup = '//div[contains(@class, \'Success\') and not(contains(@class, \'notification-icon-circle\'))]'
    __panel_close_button = '//div[@class=\'mosaic-tile\' and .//div[@class=\'mosaic-window-title\' and text()=\'{}\']]//button[2]//*[@data-icon = \'times\']'

    def logout(self):
        self.__click_menu_toggle()
        self.click(self.__logout_button)

    def __expand_add_panel(self):
        BuiltIn().run_keyword('SeleniumLibrary.Wait Until Element Is Visible', self.__toggle_menu_button)
        menu_button = BuiltIn().run_keyword('Get WebElement', self.__toggle_menu_button)
        button_class = BuiltIn().run_keyword('Get Element Attribute', menu_button, "class")
        
        if not 'active' in button_class:
            self.click(self.__toggle_menu_button)

    def add_panel(self, panel:str):
        """ opens the add panel menu and selects the panel to add to the layout screen
            it waits until the icon changes color to verify thet panel has been added
        Args:
            panel (str): the panel to add

        Raises:
            Exception: Panel could not be opened

        Examples:
            | Add Panel | panel=Task Manager |
        """
        from test_code.office.layouts.BaseLayout import BaseLayout
        BaseLayout.clear_cache()
        self.__expand_add_panel()
        self.click(self.__add_panel_menu_option.format(panel))
        
        count = 0
        action_complete = False

        while count < 10:
            svg_icons = BuiltIn().run_keyword('Get WebElements', '//div[@role=\'button\' and .//div[text()=\'' + panel + '\']]//*[local-name() = \'svg\']')
            color = svg_icons[len(svg_icons)-1].value_of_css_property('color')
            if color == 'rgba(0, 199, 230, 1)':
                action_complete = True
                break
            else:
                sleep(.5)
                self.click(self.__add_panel_menu_option.format(panel))
                count = count+1
            
        if not action_complete:
            raise ExceptionWithScreenImage('Panel {} could not be opened'.format(panel))
        self.close_menu()

    def close_panel(self, panel:str):
        """ closes the panel from the layout screen

        Args:
            panel (str): the panel to add

        Raises:
            Exception: Panel could not be closed

        Examples:
            | Close Panel | panel=Task Manager |
        """
        from test_code.office.layouts.BaseLayout import BaseLayout
        BaseLayout.clear_cache()
        self.click(self.__panel_close_button.format(panel))

    def __expand_apply_layout(self):
        menu_button = BuiltIn().run_keyword('Get WebElement', self.__apply_layout_button)
        button_class = BuiltIn().run_keyword('Get Element Attribute', menu_button, "class")
        
        if not 'active' in button_class:
            self.click(self.__apply_layout_button)

    def apply_layout(self, layout):
        """ opens the apply layout menu and selects the layout to display
        Args:
            layout (str): the layout to display

        Examples:
            | Apply Layout | layout=User Management |
        """
        retry_count = 30
        while retry_count:
            try:
                self.__expand_apply_layout()
                break
            except Exception as e:
                if not retry_count:
                    raise e
                retry_count -= 1
                sleep(0.5)
        self.click(self.__apply_layout_menu_option.format(layout))
        self.close_menu()
        from test_code.office.layouts.BaseLayout import BaseLayout
        BaseLayout.clear_cache()

    def close_menu(self):
        self.click(self.__close_menu_div)
        menu_button = BuiltIn().run_keyword('Get WebElement', self.__toggle_menu_button)
        button_class = BuiltIn().run_keyword('Get Element Attribute', menu_button, "class")
        logger.info(button_class)

    def click_button_by_text(self, button_text):
        self.click(self.__button_with_text.format(button_text))

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
                if timeout:
                    timeout -= 1
                    sleep(0.5)
                else:
                    raise e
        return False

    def is_element_visible(self, locator: str) -> bool:
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

    def wait_until_element_is_not_visible(self, locator):
        """
        Wait until element is not visible

        """
        BuiltIn().run_keyword('SeleniumLibrary.Wait Until Element Is Not Visible', locator)

    def send_keys(self, locator, value):
        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
        BuiltIn().run_keyword('Press Keys', locator, 'CTRL+A+DELETE')
        BuiltIn().run_keyword('Press Keys', locator, value)

    def select(self, locator, value, index=1):
        self.click(locator)
        sleep(0.5)
        BuiltIn().run_keyword('Wait Until Page Contains Element', self.__select_option.format(value, index))
        options = BuiltIn().run_keyword('Get WebElements', self.__select_option.format(value, index))
        retry_count=0
        while len(options) > 0 and retry_count < 5:
            try:
                # After selection the transition can fail. So wait.
                sleep(0.5)
                BuiltIn().run_keyword('Click Element', options[len(options)-1])
                sleep(.5)
                return True
            except:
                pass
            sleep(0.5)
            options = BuiltIn().run_keyword('Get WebElements', self.__select_option.format(value, index))
            retry_count = retry_count + 1
        if len(options) > 0:
            raise ExceptionWithScreenImage('Unable to select {}'.format(value))

    def select_from_menu(self, element, value, index=1):
        self.click(element)

        BuiltIn().run_keyword('Wait Until Page Contains Element', self.__select_option.format(value, index))
        options = BuiltIn().run_keyword('Get WebElements', self.__select_option.format(value, index))
        
        retry_count=0
        while len(options) > 0 and retry_count < 5:
            try:
                BuiltIn().run_keyword('Click Element', options[len(options)-1])
            except:
                pass
            sleep(.5)
            options = BuiltIn().run_keyword('Get WebElements', self.__select_option.format(value, index))
            retry_count = retry_count + 1
        if len(options)>0:
            raise ExceptionWithScreenImage('Unable to select {}'.format(value))

    def capture_image(self, element, name):
        BuiltIn().run_keyword('Capture Given Element', element, name)

    def capture_image_and_compare(self, element, name):
        BuiltIn().run_keyword('Capture Given Element And Compare', element, name)

    def get_select_options(self, locator) -> list:
        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
        BuiltIn().run_keyword('Click Element', locator)
        sleep(1)
        options = []
        list_of_option_elements = BuiltIn().run_keyword('Get WebElements', '//ul[contains(@class, \'MuiMenu-list\')]/li')
        
        if(len(list_of_option_elements)==0):
            BuiltIn().run_keyword('Click Element', locator)
            list_of_option_elements = BuiltIn().run_keyword('Get WebElements', '//ul[contains(@class, \'MuiMenu-list\')]/li')
        
        for option in list_of_option_elements:
            options.append(option.text)
        logger.info(options)
        BuiltIn().run_keyword('Click Element', 'css:div.MuiBackdrop-root')
        return options

    def get_menu_options(self, element):
        BuiltIn().run_keyword('Click Element', element)

        options = []
        list_of_option_elements = BuiltIn().run_keyword('Get WebElements', '//ul[contains(@class, \'MuiMenu-list\')]/li')
        
        for option in list_of_option_elements:
            options.append(option.text)
        logger.info(options)
        return options

    def get_success_message(self):
        message = BuiltIn().run_keyword('Get Text', self.__success_popup)
        return message

    def double_click(self, locator):
        """
        Click element on field web UI

        """
        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
        BuiltIn().run_keyword('Double Click Element', locator)
        
    def wait_for_success_popup_to_disappear(self):
        """ waits for the success message to disappear

        Raises:
            Exception: Popup Message is still displayed
            
        Examples:
            |   Wait for Success Popup To Disappear    |
        """
        action_complete = False
        count=0
        
        while count<10:
            try:
                message = self.get_success_message()
                if message == '':
                    return  True
                sleep(1)
            except:
                return True
            count=count+1

        if not action_complete:
            raise ExceptionWithScreenImage('Popup Message is still displayed')