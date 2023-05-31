__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
from robot.api import logger
from test_code.office.BasePage import BasePage
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage
import time

class Grid(BasePage):
    
    __table = None
    __previous_page = './/div[contains(@class, \'MuiTablePagination-root\')]//button[@aria-label=\'Go to previous page\']'
    __next_page = './/div[contains(@class, \'MuiTablePagination-root\')]//button[@aria-label=\'Go to next page\']'
    __column_header = './/div[contains(@class,\'MuiDataGrid-columnHeader \') and .//div[contains(@class,\'MuiDataGrid-columnHeaderTitle\') and text()=\'{}\']]'
    def __init__(self, element):
        self.__table = element
        
    def get_row(self, search_criteria, pagination=False, ignore_disabled_rows=False, lazy_loading=True, number_of_columns_to_skip_from_start=0):
        """provides a repeatable mechanism for search table rows

        Args:
            search_criteria (_type_): a list of string where each entry represents the column to search, None ignores the column
            e.g. [None, 'firstname', None, 'date of birth']
            pagination (bool, optional): whether the table is paginated. Defaults to False.
            ignore_disabled_rows (bool, optional): whether disabled rows should be ignored in the search. Defaults to False.
            lazy_loading (bool, optional): whether table performs lazy loading. Defaults to True.
            number_of_columns_to_skip_from_start(int): 1 will skip the first column from compariosn and 2 will skip the first 2 columns
        Raises:
            Exception: no row found during search

        Returns:
            WebElement: the table row found during the search
        """
        if pagination and not self.is_first_page_disabled():
            self.go_to_first_page()
        
        last_row_text = None
        while True:
            try:
                row_xpath = ".//div[@role=\"row\" and "
                first_column = True
                for index, column in enumerate(search_criteria):
                    if not column is None:
                        if not first_column:
                            row_xpath = row_xpath + " and "
                        index += number_of_columns_to_skip_from_start
                        row_xpath = row_xpath + "div[" + str(index+1) + "][@role=\"cell\" and normalize-space(.)=\"" + column + "\""
                        if ignore_disabled_rows:
                            row_xpath=row_xpath + "  and not(contains(@class, \"disabled\"))"
                        row_xpath = row_xpath + "]"
                        first_column = False
                row_xpath = row_xpath + "]"
                print(row_xpath)
                logger.info(row_xpath)
                return self.__table.find_element(By.XPATH, row_xpath)
            except:
                if pagination:
                    if self.is_next_page_disabled():
                        break
                    else:
                        self.go_to_next_page()
                elif lazy_loading:
                    last_row = self.__table.find_element(By.XPATH, '(.//div[@role=\'row\'])[last()]')
                    last_row_text = last_row.text
                    BuiltIn().run_keyword('Scroll Element Into View', last_row)
                    time.sleep(.5)
                    last_row = self.__table.find_element(By.XPATH, '(.//div[@role=\'row\'])[last()]')
                    if last_row_text == last_row.text:
                        break
                else:
                    break
        raise ExceptionWithScreenImage('Unable to find row with {}'.format(str(search_criteria)))
    
    def go_to_previous_page(self):
        self.click(self.__table.find_element(By.XPATH, self.__previous_page))
        
    def is_next_page_disabled(self):
        logger.info(self.__table.find_element(By.XPATH, self.__next_page).get_attribute('disabled'))
        try:
            self.__table.find_element(By.XPATH, './/div[contains(@class, \'MuiTablePagination-root\')]//button[@aria-label=\'Go to next page\' and @disabled]')
            return True
        except:
            return False
    
    def is_previous_page_disabled(self):
        logger.info(self.__table.find_element(By.XPATH, self.__previous_page).get_attribute('disabled'))
        try:
            self.__table.find_element(By.XPATH, './/div[contains(@class, \'MuiTablePagination-root\')]//button[@aria-label=\'Go to previous page\' and @disabled]')
            return True
        except:
            return False
        
    def go_to_next_page(self):
        self.click(self.__table.find_element(By.XPATH, self.__next_page))
        
    def get_no_of_rows(self, lazy_loading:bool=True):
        if lazy_loading:
            count = 0
            last_row = None
            count = count + len(self.__table.find_elements(By.XPATH, './/div[@role=\'row\' and contains(@class, \'MuiDataGrid-row\')]'))
            last_row = self.__table.find_element(By.XPATH, '(.//div[@role=\'row\' and contains(@class, \'MuiDataGrid-row\')])[last()]')
            last_row_data_row_index = last_row.get_attribute('data-rowindex')
            
            while True:
                logger.info('lastrowtext' + last_row_data_row_index)
                BuiltIn().run_keyword('Scroll Element Into View', last_row)
                time.sleep(.5)
                last_row = self.__table.find_element(By.XPATH, '(.//div[@role=\'row\' and contains(@class, \'MuiDataGrid-row\')])[last()]')
                logger.info('lastrowtext after scroll' + last_row.get_attribute('data-rowindex'))
                if last_row_data_row_index == last_row.get_attribute('data-rowindex'):
                    return count
                else:
                    count = count + len(self.__table.find_elements(By.XPATH, './/div[@role=\'row\' and contains(@class, \'MuiDataGrid-row\') and @data-rowindex=\'' + last_row_data_row_index + '\']/following-sibling::div[@role=\'row\' and contains(@class, \'MuiDataGrid-row\')]'))
        else:
            return len(self.__table.find_elements(By.XPATH, './/div[@role=\'row\' and contains(@class, \'MuiDataGrid-row\')]'))
    
    def get_table_headers(self) -> list:
        header_elements = self.__table.find_elements(By.CSS_SELECTOR, '.MuiDataGrid-columnHeader')
        headers=[]
        for header_element in header_elements:
            headers.append(header_element.text)

        return headers

    def click_header(self, header, expect_sort=False):
        """ clicks the table header. Optionally you can specify if you expect aria-sort property of the element 
            is expcted to change. It will change from 'none' to 'descending' or 'ascending'
        Args:
            header (str): the header to click
            expect_sort: True if sorting is expected
        Examples:
            |   Click Table Header   |
        """
        element = self.__table.find_element(By.XPATH, self.__column_header.format(header))
        if expect_sort:
            aria_sort = element.get_attribute("aria-sort")
            timeout = 3
            while (aria_sort == element.get_attribute("aria-sort")) and timeout > 0:
                timeout -= 1
                self.click(element)
                time.sleep(.5)
            if aria_sort == element.get_attribute("aria-sort"):
                raise ExceptionWithScreenImage('Sorting did not happen or aria-sort property changed in AUT')
        else:
            self.click(element)

    def select_item_from_header_menu(self, header, menu_item):
        """ Selects the sorting menu from the table header, launches it and then selects the menu item from the menu
        Args:
            header (str): the header to click
            menu_item: The menu item to click
        Examples:
            |   Select Item From Header Menu   |
        """
        column_header = self.__table.find_element(By.XPATH, self.__column_header.format(header))
        column_menu_icon = column_header.find_element(By.XPATH, './/div[contains(@class, \'menuIcon\')]')
        if menu_item == 'descending':
            self.click(column_menu_icon.find_element(By.XPATH, '//ul[@role = \'menu\']/li[@data-value = \'desc\']'))
        if menu_item == 'ascending':
            self.click(column_menu_icon.find_element(By.XPATH, '//ul[@role = \'menu\']/li[@data-value = \'asc\']'))
        else:
            raise Exception('Only descending and ascending are supported. {} is not yet implemented'.format(menu_item))

    def get_column_index(self, header):
        headers = self.get_table_headers()
        return headers.index(header.upper())
    
    def get_all_values_from_column(self, header):
        values = []
        time.sleep(.5)  # Allows the column data to get refreshed.
        columns = self.__table.find_elements(By.XPATH, './/div[@role=\'row\' and contains(@class, \'MuiDataGrid-row\')]//div[' + str(self.get_column_index(header)+1) + '][@role=\'cell\']')
        for column in columns:
            values.append(column.text)
        return values
    
    def get_values_from_first_row(self):
        values = []
        first_row_columns = self.__table.find_elements(By.XPATH, './/div[1][@role=\'row\']//div[@role=\'cell\']')
        for column in first_row_columns:
            values.append(column.text)
        return values
    
    def select_rows_per_page(self, no_of_rows):
        self.select(self.__table.find_element(By.CSS_SELECTOR, '.MuiTablePagination-select'), no_of_rows)
        time.sleep(.5)
        
    def get_pages_per_row_text(self):
        return self.__table.find_element(By.CSS_SELECTOR, '.MuiTablePagination-displayedRows').text
                    