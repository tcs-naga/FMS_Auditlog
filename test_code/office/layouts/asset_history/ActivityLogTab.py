__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.data.AssetStateDetails import AssetStateDetails
from test_code.office.layouts.asset_history.AssetHistoryPanel import AssetHistoryPanel
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from test_code.office.layouts.Grid import Grid
import time
from robot.libraries.BuiltIn import BuiltIn
from test_code.office.layouts.asset_history.UpdateConfirmation import UpdateConfirmation
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage
from test_code.utilities.DateTimeFormatter import DateTimeFormatter

class ActivityLogTab(AssetHistoryPanel):

    __asset_select_container = '.asset-select'
    __asset_select_button = 'button'
    __context_menu_item = './/div[@class="context-menu-items"]//div[@role=\'button\' and .//span[text()=\'{}\']]'
    __sub_menu_item = './/div[@role=\'button\' and .//span[text()=\'{}\']]'
    __grid_class = '.MuiDataGrid-root'

    def select_asset(self, asset_type: str, asset_name:str):
        """ selects an asset to display activity logs for

        Args:
            asset_type (str): the type of asset
            asset_name (str): the asset name
            
        Examples:
            |   Select Asset    |   asset_type=Dump Truck   |   asset_name=DT5401   |
        """
        container = self._get_panel().find_element(By.CSS_SELECTOR, self.__asset_select_container)
        asset_button = container.find_element(By.TAG_NAME, self.__asset_select_button)

        timeout = 5
        while timeout > 0:
            try:
                self.click(asset_button)
                context_menu_item = container.find_element(By.XPATH, self.__context_menu_item.format(asset_type))
                self.click(context_menu_item)
                break
            except:
                timeout = timeout - 1

        timeout = 2
        while timeout > 0:
            try:
                sub_menu_item = container.find_element(By.XPATH, self.__sub_menu_item.format(asset_name))
                self.click(sub_menu_item)
                break
            except:
                timeout = timeout - 1

        
    def __get_grid(self):
        return Grid(self._get_panel().find_element(By.CSS_SELECTOR, self.__grid_class))

    def __find_row(self, activity_log: AssetStateDetails) -> WebElement:
        return self.__get_grid().get_row([activity_log.get_reported_at_in_display_format(), activity_log.get_ended_at_in_display_format(), None, activity_log.get_displayed_state_name(), activity_log.comment])

    def click_insert_state_before(self, activity_log: AssetStateDetails):
        """ clicks the insert state before menu option for a given activity log

        Args:
            activity_log (AssetStateDetails): the activity log containing the menu
            
        Examples: 
            |   Click Insert State Before   |   activity_log={asset_state_details_object}   |
        """
        row = self.__find_row(activity_log)
        self.click(row.find_element(By.XPATH, './/div[@data-field=\'menuOpen\']//*[@data-icon=\'ellipsis-v\']'))
        BuiltIn().run_keyword('Scroll Element Into View', self._get_panel().find_element(By.XPATH, '//div[@role=\'button\' and .//span[text()=\'Insert state before\']]'))
        self.click(self._get_panel().find_element(By.XPATH, '//div[@role=\'button\' and .//span[text()=\'Insert state before\']]'))

    def get_list_of_menu_options(self, activity_log: AssetStateDetails) -> list:
        """ gets a list of menu options for an activity log

        Args:
            activity_log (AssetStateDetails):  the activity log containing the menu

        Returns:
            list: a list of menu options
            
        Examples:
            |   Get List Of Menu Options   |   activity_log={asset_state_details_object}   |
        """
        row = self.__find_row(activity_log)
        self.click(row.find_element(By.XPATH, './/div[@data-field=\'menuOpen\']//*[@data-icon=\'ellipsis-v\']'))
        time.sleep(.5)
        options = []
        timeout = 3
        while (len(options) == 0) and timeout > 0:
            timeout -= 1
            list_of_option_elements = self._get_panel().find_elements(By.XPATH, '//ul[contains(@class, \'MuiList-root\')]//div[@role=\'button\']')
            for option in list_of_option_elements:
                options.append(option.text)
            time.sleep(.5)    
        if len(options) == 0:
            raise ExceptionWithScreenImage('Failed to get list of menu options for: {}'.format(str(activity_log)))

        return options

    def get_duration(self, activity_log: AssetStateDetails) -> str:
        """ gets the duration displayed for a activity log

        Args:
            activity_log (AssetStateDetails): the activity log containing the duration to get

        Returns:
            str: the duration

        Examples:
            |   Get Duration   |   activity_log={asset_state_details_object}   |
        """
        row = self.__find_row(activity_log)
        return row.find_element(By.XPATH, './/div[3][@role=\'cell\']').text

    def is_activity_displayed(self, activity_log: AssetStateDetails) -> bool:
        """ gets a status based on if the activity is displayed

        Args:
            activity_log (AssetStateDetails): the activity log containing the duration to get

        Returns:
            bool: True if the activity log is displayed otherwise False

        Examples:
            |   Is Activity Displayed   |   activity_log={asset_state_details_object}   |    
        """
        try:
            self.__find_row(activity_log)
            return True
        except:
            return False

    def activity_should_be_displayed(self, activity_log: AssetStateDetails) -> bool:
        """ gets a status based on if the activity is displayed

        Args:
            activity_log (AssetStateDetails): the activity log containing the duration to get

        Returns:
            bool: True if the activity log is displayed otherwise False

        Examples:
            |   Activity Should Be Displayed   |   activity_log={asset_state_details_object}   |
        """
        # We wait for 0.5 sec, so double this value.
        timeout = int(BuiltIn().get_variable_value('${MAX_WAIT}')) * 2
        # Wait enough for first row to populate.
        while(timeout):
            timeout -= 1
            BuiltIn().run_keyword('Sleep', '0.5')
            if self.is_activity_displayed(activity_log):
                return True
        raise ExceptionWithScreenImage(f"Activity {activity_log} is not visible")

    def get_list_of_table_headers(self) -> list:
        """ gets a list of the table headers

        Returns:
            list: the list of table headers

        Examples:
            |   Get List of Table Headers   |
        """
        return self.__get_grid().get_table_headers()

    def click_table_header(self, header:str):
        """ clicks the table header to sort the table

        Args:
            header (str): the header to click

        Examples:
            |   Click Table Header   |
        """
        self.__get_grid().click_header(header, expect_sort=True)

    def get_list_of_column_values(self, header:str) -> list:
        """ gets a list of values displayed for a given column

        Args:
            header (str): the header of the column

        Returns:
            list: the values of the column

        Examples:
            |   Get List of Column Values   |
        """
        return self.__get_grid().get_all_values_from_column(header)

    def get_first_activity_log(self) -> list:
        """ gets a list of values for the first activity log

        Returns:
            list: list of values in the first row

        Examples:
            |   Get First Activity Log  |
        """
        return self.__get_grid().get_values_from_first_row()

    def first_activity_log_should_be(self, *args) -> bool:
        """ gets a list of values for the first activity log

        Returns:
            list: list of values in the first row

        Examples:
            |   Get First Activity Log And Compare | Col 1 | Col 2 | ... |
        """
        # We wait for 0.5 sec, so double this value.
        timeout = int(BuiltIn().get_variable_value('${MAX_WAIT}')) * 2
        row = None
        # Wait enough for first row to populate.
        while(timeout):
            timeout -= 1
            BuiltIn().run_keyword('Sleep', '0.5')
            row = self.get_first_activity_log()
            match = True
            for idx, arg in enumerate(args):
                if row[idx] != arg:
                    match = False
            if match:
                return True
        raise ExceptionWithScreenImage(f"Row in page {row}, doesn't match with {args}")

    def select_table_rows_per_page(self, no_of_rows: str):
        """ selects number of table rows to display per page

        Args:
            no_of_rows (str): the number of rows to display

        Examples:
            |   Select Table Rows Per Page  |   no_of_rows=25   |
        """
        self.__get_grid().select_rows_per_page(no_of_rows)

    def get_no_of_activity_logs_displayed(self) -> int:
        """ gets the no of activity logs displayed

        Returns:
            int: the number of activities displayed

        Examples:
            |   Get No of Activity Logs Displayed   |
        """
        return self.__get_grid().get_no_of_rows()

    def click_refresh(self):
        """ clicks the refresh button

        Examples:
            |   Click Refresh   |
        """
        self.click(self._get_panel().find_element(By.XPATH, './/button[./*[@data-icon=\'sync\']]'))

    def go_to_next_page_of_table_rows(self):
        """ clicks go to the next page in the table pagination

        Examples:
            |   Go To Next Page Of Table Rows   |
        """
        self.__get_grid().go_to_next_page()

    def is_next_page_of_table_rows_disabled(self) -> bool:
        """ returns a status based on if the next page is disabled

        Returns:
            bool: True if next page is disabled otherwise False
            
        Examples:
            |   Is Next Page of Table Rows Disabled |
        """
        return self.__get_grid().is_next_page_disabled()
    
    def is_previous_page_of_table_rows_disabled(self):
        """ returns a status based on if the previous page is disabled

        Returns:
            bool: True if previous page is disabled otherwise False

        Examples:
            |   Is Previous Page of Table Rows Disabled |
        """
        return self.__get_grid().is_previous_page_disabled()

    def get_pages_per_row_displayed_in_table(self) -> str:
        """ gets the pages per row displayed for the table

        Returns:
            str: the pages per row displayed

        Examples:
            |   Get Pages Per Row Displayed In Table    |
        """
        return self.__get_grid().get_pages_per_row_text()

    def __double_click_field_to_edit(self, activity_log: AssetStateDetails, column:str):
        column_index=self.__get_grid().get_column_index(column)
        self.double_click(self.__find_row(activity_log).find_element(By.XPATH, './/div[' + str(column_index+1) + '][@role=\'cell\']'))
        return self.__find_row(activity_log).find_element(By.XPATH, './/div[' + str(column_index+1) + '][@role=\'cell\' and contains(@class, \'MuiDataGrid-cell--editing\')]')

    def edit_reported_state_for_activity_log(self, activity_log: AssetStateDetails, value):
        """ Edits the Reported state for an activity log

        Args:
            activity_log (AssetStateDetails): the activity log to edit
            value (_type_): the value to set the report state to
        """
        editable_field = self.__double_click_field_to_edit(activity_log, 'Reported State')
        self.select(editable_field.find_element(By.CSS_SELECTOR, 'div.MuiSelect-select'), value)
        self.send_keys(editable_field, '\ue004')
        UpdateConfirmation().click_yes()

    def convert_datetime_to_twentyfour_hour(self, _list: list) -> list:
        """Convert a list having 12 hour date time values into a 24 hour date time list
           e.g:- list items converted from 12/03/2023, 6:00:00 pm to 12/03/2023, 18:00:00

        Args:
            _list (list): A list having date time values in 12 hour format

        Returns:
            list: A list having date time values in 24 hour format

        Examples:
            | Convert Datetime To Twentyfour Hour | list |
        """
        twentyfour_hour_list = []
        for date_time_value in _list:
            twentyfour_hour_list.append(DateTimeFormatter.convert_datetime_twelve_to_twentyfour_hour(self, date_time_value))
        return twentyfour_hour_list