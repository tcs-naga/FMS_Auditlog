from test_code.auditlog.AuditResults import AuditResults
from test_code.auditlog.BasePage import Basepage
from robot.api.deco import keyword
from datetime import date as datelibarary
from time import  sleep
import pandas as pd
from pathlib import Path


class AuditQuerySearch(Basepage):

    # Element_locators :

    query_search_elements_dict = {
                                    'new_audit_query_label':"//div[text()='New audit query']",
                                     #date range(from / to)
                                    'select_date_range_label':"//div[text()='Select a date range']",
                                     #from date
                                    'from_date_picker_btn':"//div[text()='From']/../div[2]/div/child::div/button",
                                     #select_typ_event_or_activity
                                    'select_typ_event_or_activity_label':"//div[text()='Select type of Event or Activity']",
                                    'select_typ_event_or_activity_dropdown_input':"//div[text()='Select type of Event or Activity']/../div[2]/div/div/input",
                                     #select_typ_entity_or_asset
                                     'select_typ_entity_or_asset_label': "//div[text()='Select Entity or Asset']",
                                    'select_typ_entity_or_Asset_dropdown_input': "//div[text()='Select Entity or Asset']/../div[2]/div/div/input",
                                     #user
                                    'user_input': "//div[text()='Select Users']/../following-sibling::div/div/div/input",
                                     #start_query_button
                                    'start_query_btn': "//button[text()='START QUERY']"}

    options_panel = "//div[@role='presentation']/descendant::div" #// div[ @ role = 'presentatio']  #//div[@class='makeStyles-rootPopper-1']
    new_query_back_btn = "//button/span[text()='New Query']"
    prev_month_arrow_btn = "//div[@class ='MuiPickersBasePicker-pickerView']/div[1]/div/button[1]/span"
    next_month_arrow_btn = "//div[@class ='MuiPickersBasePicker-pickerView']/div[1]/div/button[2]/span"
    moth_yyyy_label = "//div[@class ='MuiPickersBasePicker-pickerView'] /div[1]/div/child::div/p"

    time_hh = "// div[@class ='MuiPickersClock-clock']/span[text()='12']"
    time_mm = "// div[@class ='MuiPickersClock-clock']/span[text()='00']"
    ok_btn = "// span[text()='OK']"

    # event_type_chip_text = '//th[3]/div/descendant::div[3]/child::div[1]/span'
    # action_chip_text = '//th[4]/div/descendant::div[3]/child::div[1]/span'
    # entity_chip_text = '//th[5]/div/descendant::div[3]/child::div[1]/span'
    # user_chip_text = '//th[6]/div/descendant::div[3]/child::div[1]/span'

    ##Not in use
    today = datelibarary.today()
    # Textual month, day and year
    d2 = today.strftime("%B %d, %Y")
    print("d2 =", d2)
    # mm/dd/y
    d3 = today.strftime("%m/%d/%y")
    print("d3 =", d3)
    ##

    def verification_of_all_elements_in_audit_query_search(self):
        # This method verify  all required  fields are present in new audit query search screen or not.
        """
        Verification Of All Elements In Audit Query Search

        Examples:
            | Verification Of All Elements In Audit Query Search |
        """
        self.check_if_elements_is_present_or_not(self. query_search_elements_dict)
    # def query_search_with_all_fields(self,*values):
    #     # This method search the query with all required  fields in new audit query search screen.
    #     ## Event only y?
    #     """
    #     Query Search With All Fields
    #
    #      Examples:
    #     | Query Search With All Fields | Values |
    #     """
    #
    #     #self.from_date_mm_picker(input_year, input_month, input_date)
    #     self.select_dropdown_value(self.__query_search_elements_dict['select_typ_event_or_activity_dropdown_input'], values[0])
    #     self.select_dropdown_value(self.__query_search_elements_dict['select_typ_entity_or_Asset_dropdown_input'],values[1])
    #     self.select_dropdown_value(self.__query_search_elements_dict['user_input'], values[2])
    #     self.submit_start_query_btn()
    #    # return self.validate_column_records_and_chip_text_with_given_input(locator=self.event_type_chip_text,value_type='all')
    #     return self.validate_tabel_records_with_chip_texts_and_given_input('all',*values)

    def query_search_with_all_fields_in_multi_values(self,*values):
        # This method search the query with all required  fields with multi options in new audit query search screen.
        # Value input format should  Event , Entity , User
        """
        Query Search With All Fields In Multi Values

         Examples:
        | Query Search With All Fields In Multi Values | Values |
        """
        self.submit_start_query_btn()
        return  self.validate_tabel_records_with_chip_texts_and_given_input('all','query_search',*values)

    def select_event_or_activity_with_values(self, *values):
        # This method  perform query search with event_or_activity filed only
        """
        Select Event Or Activity With  Values

        Examples:
        | Select Event Or Activity With  Values | Values |
        """
        for i in range(0, len(values)):
            self.select_dropdown_value(self.query_search_elements_dict['select_typ_event_or_activity_dropdown_input'], values[i])

    def select_entity_or_asset_with_values(self, *values):
        # This method  perform query search with entity_or_asset filed only
        """
        Select Entity Or Asset With  Values

        Examples:
            | Select Entity Or Asset With  Values | Values |
        """
        for i in range(0, len(values)):
            self.select_dropdown_value(self.query_search_elements_dict['select_typ_entity_or_Asset_dropdown_input'], values[i])

    def select_user_with_values(self, *values):
        # This method  perform query search with user filed only
        """
        Select User With  Values

        Examples:
            | Select User With  Values| Values |
        """
        for i in range(0, len(values)):

            self.select_dropdown_value(self.query_search_elements_dict['user_input'],values[i])

    def query_search_with_date(self,input_year,input_month,input_date):
        #This method search the query with only date field in new audit query search screen
        """
        Query Search With Date

        Examples:
        | Query Search With Date | Year | Month | Date |
        """
        self.from_date_mm_picker(input_year,input_month,input_date)
        self.submit_start_query_btn()
        #return self.validate_column_records_and_chip_text_with_given_input(locator=None, value_type=None)
        return self.validate_tabel_records_with_chip_texts_and_given_input(screen=None,value_type=None)

    def search_with_date(self, input_year, input_month, input_date):
        # This method search the query with only date field in new audit query search screen
        """
         Search With Date

        Examples:
        |  Search With Date | Year | Month | Date |
        """
        self.from_date_mm_picker(input_year, input_month, input_date)
        # return self.validate_column_records_and_chip_text_with_given_input(locator=None, value_type=None)

    def query_search_with_event_or_activity(self,*values):
        # This method  perform query search with event_or_activity filed only
        """
        Query Search With Event Or Activity

        Examples:
        | Query Search With Event Or Activity | EventName |
        """
        self.select_event_or_activity_with_values(*values)
        self.submit_start_query_btn()
        return self.validate_tabel_records_with_chip_texts_and_given_input('event', 'query_search', *values)

    def query_search_with_entity_or_asset(self, *values):
        # This method  perform query search with entity_or_asset filed only
        """
        Query Search With Entity Or Asset

        Examples:
            | Query Search With Entity Or Asset | EntityValue |
        """
        self.select_entity_or_asset_with_values(*values)
        self.submit_start_query_btn()
        return self.validate_tabel_records_with_chip_texts_and_given_input('entity', 'query_search', *values)

    def query_search_with_user(self, *values):
        # This method  perform query search with user filed only
        """
        Query Search With User

        Examples:
            | Query Search With User | UserName |
        """
        self.select_user_with_values(*values)
        self.submit_start_query_btn()
        return self.validate_tabel_records_with_chip_texts_and_given_input('user', 'query_search', *values)

    def select_dropdown_value(self,element_name,value:str):
        self.send_keys(element_name,value)
        # self.click(self.user_option_panel)
        sleep(3)
        self.press_key(element_name, 'ARROW_DOWN')
        sleep(1)
        self.press_key(element_name, 'ENTER')
        sleep(1)
        self.click(element_name)

    def submit_start_query_btn(self):
        """
         Submit Start Query Btn

        Examples:
        | Submit Start Query Btn |
        """
        sleep(5)
        self.click(self.query_search_elements_dict['start_query_btn'])
        sleep(15)
        self.check_if_element_is_present_or_not(self.new_query_back_btn)

    def from_date_mm_picker(self,input_year,input_month,input_date):
        self.click(self.query_search_elements_dict['from_date_picker_btn'])
        text= self.get_text_from_element(self.moth_yyyy_label)
        text=text.split(' ')
        month= str(text[0])
        year = str(text[1])
        while year != input_year:
            self.click(self.prev_month_arrow_btn)
            text = self.get_text_from_element(self.moth_yyyy_label)
            text = text.split(' ')
            year = str(text[1])
            if year == input_year:
                while month != input_month:
                        self.click(self.prev_month_arrow_btn)
                        text = self.get_text_from_element(self.moth_yyyy_label)
                        text = text.split(' ')
                        month=str(text[0])
        else:
            while month != input_month:
                self.click(self.prev_month_arrow_btn)
                text = self.get_text_from_element(self.moth_yyyy_label)
                text = text.split(' ')
                month = str(text[0])
        sleep(2)
        self.click_on_date(input_date)
        sleep(2)
        self.click_on_ok_btn()

    def click_on_date(self,date):
        date = f"//div[@class ='MuiPickersCalendar-week']/div/button[@tabindex='0']/span/p[text()='{date}']"
        try:

            self.check_if_element_is_present_or_not(date)
            self.click(date)
        except:
            sleep(5)
            self.click(date)

    def click_on_ok_btn(self):
        self.click(self.ok_btn)
