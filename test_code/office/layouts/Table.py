__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
from robot.api import logger
from test_code.office.BasePage import BasePage
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage

class Table(BasePage):

    __table = None
    __first_page = './..//nav//li[.//button[@aria-label=\'Go to first page\']]'
    __next_page = './..//nav//li[.//button[@aria-label=\'Go to next page\']]'
    
    def __init__(self, element):
        self.__table = element
        
    def get_row(self, search_criteria, pagination=False, ignore_disabled_rows=False):
        """provides a repeatable mechanism for search table rows

        Args:
            search_criteria (_type_): a list of string where each entry represents the column to search, None ignores the column
            e.g. [None, 'firstname', None, 'date of birth']
            pagination (bool, optional): whether the table is paginated. Defaults to False.
            ignore_disabled_rows (bool, optional): whether disabled rows should be ignored in the search. Defaults to False.

        Raises:
            Exception: no row found during search

        Returns:
            WebElement: the table row found during the search
        """
        if pagination and not self.is_first_page_disabled():
            self.go_to_first_page()

        while True:
            try:
                row_xpath = './/tr['
                first_column = True
                for index, column in enumerate(search_criteria):
                    if not column is None:
                        if not first_column:
                            row_xpath = row_xpath + ' and '
                        row_xpath = row_xpath + 'td[' + str(index+1) + '][normalize-space(.)=\'' + column + '\''
                        if ignore_disabled_rows:
                            row_xpath=row_xpath + '  and not(contains(@class, \'disabled\'))'
                        row_xpath = row_xpath + ']'
                        first_column = False
                row_xpath = row_xpath + ']'
                print(row_xpath)
                logger.info(row_xpath)
                return self.__table.find_element(By.XPATH, row_xpath)
            except:
                if pagination:
                    if self.is_next_page_disabled():
                        break
                    else:
                        self.go_to_next_page()
                else:
                    break
        raise ExceptionWithScreenImage('Unable to find row with {}'.format(str(search_criteria)))

    def go_to_first_page(self):
        self.click(self.__table.find_element(By.XPATH, self.__first_page))

    def is_next_page_disabled(self):
        logger.info(self.__table.find_element(By.XPATH, self.__next_page).get_attribute('disabled'))
        try:
            self.__table.find_element(By.XPATH, './..//nav//li[.//button[@aria-label=\'Go to next page\' and @disabled]]')
            return True
        except:
            return False

    def is_first_page_disabled(self):
        logger.info(self.__table.find_element(By.XPATH, self.__first_page).get_attribute('disabled'))
        try:
            self.__table.find_element(By.XPATH, './..//nav//li[.//button[@aria-label=\'Go to first page\' and @disabled]]')
            return True
        except:
            return False

    def go_to_next_page(self):
        self.click(self.__table.find_element(By.XPATH, self.__next_page))

    def get_no_of_rows(self):
        return len(self.__table.find_elements(By.XPATH, './/tr'))

    def get_active_rows(self):
        return self.__table.find_elements(By.XPATH, './/tr[./td[1][not(contains(@class, \'disabled\'))]]')

    def get_all_rows(self):
        return self.__table.find_elements(By.XPATH, './/tr[./td]')
