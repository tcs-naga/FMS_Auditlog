from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from time import sleep
from selenium.webdriver.common.by import By

class Basepage:
    # element locators

    # Common functions / methods

    def send_keys(self, locator, value):
        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
        BuiltIn().run_keyword('Press Keys', locator, 'CTRL+A+DELETE')
        BuiltIn().run_keyword('Input Text', locator, value)

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

    def get_text_from_element (self,locator):

        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
        element_text = BuiltIn().run_keyword('Get Text', locator)
        return element_text

    def check_if_element_is_present_or_not(self,locator_dict):
        for i in locator_dict.values():

            BuiltIn().run_keyword('Wait Until Page Contains Element', str(i))
            BuiltIn().run_keyword('Page Should Contain Element', str(i))
