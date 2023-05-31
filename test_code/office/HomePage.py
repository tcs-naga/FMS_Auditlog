__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from PageObjectLibrary import PageObject
from robot.libraries.BuiltIn import BuiltIn
from test_code.office.BasePage import BasePage


class HomePage(BasePage):
    
    __version = '//img[@alt=\'FMG logo\']/../following::div[1]/span'
    
    def get_version(self) -> str:
        """ gets the version of the office deployed

        Returns:
            str: version
        """
        return BuiltIn().run_keyword('Get Text', self.__version)