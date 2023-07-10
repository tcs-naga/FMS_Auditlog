from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from time import sleep
from selenium.webdriver.common.by import By
import os
from pathlib import Path
import pandas as pd


class Basepage:
    # element locators

    # Audit Result Screen Elements
    query_results_elements_dict = {'audit_result_label': "//div[text()='Audit results']",
                                     'records_found_label': "//div[@class='MuiBox-root css-169zjxt'][2]/div",
                                     'new_query_back_btn': "//button/span[text()='New Query']",
                                     'refresh_btn': "//div[@class='MuiBox-root css-169zjxt'][3]/div/button",
                                     'export_btn': "//div[@class='MuiBox-root css-1xhj18k']/div[2]/button",
                                     # input
                                     'from_date_input': "//th[1]/div/descendant::input[1]",
                                     'to_date_input': "//th[1]/div/descendant::input[2]",
                                     'id_input': "//th[2]/div/descendant::input",
                                     'event_type_input': "//th[3]/div/descendant::input",
                                     'action_input': "//th[4]/div/descendant::input",
                                     'entity_input': "//th[5]/div/descendant::input",
                                     'user_input': "//th[6]/div/descendant::input"}
    id_rows = "//tbody/tr/td[1]"
    id_row_sort_arrow =  "//span[text()='ID']"
    circuit_created_values = "//div[text()='Circuit created']/../following-sibling::div[1]/div"
    tabel_no_records_label = "//table/descendant::div[@class='css-6xt45o']/.."

    event_type_chip_text = '//th[3]/div/descendant::div[3]/child::div[1]/span'
    event_type_chip_text_arrow = '//th[3]/div/descendant::input/following::div[1]'
    event_type_multi_chip_text = '//th[3]/div/descendant::div[3]/child::div/span'

    action_chip_text = '//th[4]/div/descendant::div[3]/child::div[1]/span'
    action_chip_text_arrow = '//th[4]/div/descendant::input/following::div[1]'
    action_chip_multi_chip_text = '//th[4]/div/descendant::div[3]/child::div/span'

    entity_chip_text = '//th[5]/div/descendant::div[3]/child::div[1]/span'
    entity_chip_text_arrow = '//th[5]/div/descendant::input/following::div[1]'
    entity_chip_multi_chip_text = '//th[5]/div/descendant::div[3]/child::div/span'

    user_chip_text = '//th[6]/div/descendant::div[3]/child::div[1]/span'
    user_chip_text_arrow = '//th[6]/div/descendant::input/following::div[1]'
    user_chip_multi_chip_text = '//th[6]/div/descendant::div[3]/child::div/span'

    #pagination:
    #pagination_elements="//nav[@aria-label='pagination navigation']/ul/child::li"
    pagination_elements="//ul/child::li"
    left_single_arrow = "//nav[@aria-label='pagination navigation']/ul/child::li[2]"
    left_double_arrow="//nav[@aria-label='pagination navigation']/ul/child::li[1]"
    right_single_arrow = "//nav[@aria-label='pagination navigation']/ul/child::li[7]"
    right_double_arrow = "//nav[@aria-label='pagination navigation']/ul/child::li[7]"

    downloads_path = str(Path.home() / "Downloads")
    audit_record_excel_file_path = downloads_path + "/AuditRecord.xlsx"

    # Common functions / methods
    def send_keys(self, locator, value):
        BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
       # BuiltIn().run_keyword('Press Keys', locator, 'CTRL+A+DELETE')
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
        sleep(3)
        return element_text

    def check_if_elements_is_present_or_not(self,locator_dict):
        for i in locator_dict.values():
            BuiltIn().run_keyword('Wait Until Page Contains Element', str(i))
            BuiltIn().run_keyword('Page Should Contain Element', str(i))

    def check_if_element_is_present_or_not(self,locator,timeout=10):
            # it verifys only single element
            BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
            BuiltIn().run_keyword('Page Should Contain Element', locator)

            while timeout:
                try:
                    BuiltIn().run_keyword('Wait Until Page Contains Element', locator)
                    BuiltIn().run_keyword('Page Should Contain Element', locator)
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

    def press_key(self,locator,keyname):
        BuiltIn().run_keyword('Press Keys', locator, keyname)

    def get_element_count(self,locator):
        element_count= BuiltIn().run_keyword('Get WebElements', locator)
        return element_count

    #Common Audit Functions
    def export_records(self):

            if os.path.exists(self.audit_record_excel_file_path):
                sleep(2)
                os.remove(self.audit_record_excel_file_path)
                sleep(2)
                self.click(self.query_results_elements_dict['export_btn'])
                sleep(5)
            else:
                self.click(self.query_results_elements_dict['export_btn'])
                sleep(5)

    def refresh_results(self):
        self.click(self.query_results_elements_dict['refresh_btn'])

    def new_query(self):
        self.click(self.query_results_elements_dict['new_query_back_btn'])
        sleep(2)
        self.check_if_element_is_present_or_not("//button[text()='START QUERY']")


    def get_records_count(self):
        records_count_lst = str(
            self.get_text_from_element(self.query_results_elements_dict['records_found_label'])).split(' ')
        records_count = str(records_count_lst[0])
        return records_count

    def search_with_id(self, fid):
        self.send_keys(self.query_results_elements_dict['id_input'], fid)

    def search_with_filters(self,locator, *args):



        for i in args:
            self.send_keys(locator, i)
            sleep(1)
            self.press_key(locator, 'ARROW_DOWN')
            sleep(1)
            self.press_key(locator, 'ENTER')
            sleep(1)
            self.click(locator)
        self.press_key(locator, 'TAB')
        sleep(5)

    def validate_export_records_with_tabel_results(self):
        """
        Validate Export Records With Tabel Results

        Examples:
        | Validate Export Records With Tabel Results |
        """
        self.export_records()
        sleep(2)
        audit_record_excel = pd.read_excel(self.audit_record_excel_file_path)
        audit_record_dataframe = pd.DataFrame(audit_record_excel)
        print(audit_record_dataframe)
        no_of_row_count = len(audit_record_dataframe.index)

        if no_of_row_count == int(self.get_records_count()):
            # logic is in progress for tabel validation
            print("record count is matched")
            return 'records count is matched'
        else:
            print("record count is not matched")
            return 'records count is  not_matched'

    def validate_tabel_records_with_chip_texts_and_given_input(self,value_type,screen,*values):
        # this function validate the in tabel result columns(event,entity & user) and chip text with given inputs #single options
        results = []
        multi_chip_text_list = []
        results_dict = {}
        audit_record_excel=''
        sleep(2)
        if value_type == 'event':
            self.click(self.event_type_chip_text_arrow)
            event_chip_texts_count = self.get_element_count(self.event_type_multi_chip_text)
            for i in range(1, len(event_chip_texts_count) + 1):
                event_type_multi_chip_text = self.get_text_from_element(f"//th[3]/div/descendant::div[3]/child::div[{i}]/span")
                multi_chip_text_list.append( event_type_multi_chip_text)

        elif value_type == 'entity':
            self.click(self.entity_chip_text_arrow)
            entity_chip_texts_count = self.get_element_count(self.entity_chip_multi_chip_text)
            for i in range(1, len(entity_chip_texts_count) + 1):
                entity_type_multi_chip_text =self.get_text_from_element( f"//th[5]/div/descendant::div[3]/child::div[{i}]/span")
                multi_chip_text_list.append(entity_type_multi_chip_text)

        elif value_type == 'user':
            self.click(self.user_chip_text_arrow)
            user_chip_texts_count = self.get_element_count(self.user_chip_multi_chip_text)
            for i in range(1, len(user_chip_texts_count) + 1):
                user_type_multi_chip_text = self.get_text_from_element(f"//th[6]/div/descendant::div[3]/child::div[{i}]/span")
                multi_chip_text_list.append(user_type_multi_chip_text)

        elif value_type == 'action':
            self.click(self.action_chip_text_arrow)
            action_chip_texts_count = self.get_element_count(self.action_chip_multi_chip_text)
            for i in range(1, len(action_chip_texts_count) + 1):
                action_type_multi_chip_text = self.get_text_from_element(f"//th[4]/div/descendant::div[3]/child::div[{i}]/span")
                multi_chip_text_list.append(action_type_multi_chip_text)

        elif value_type == 'all':
            self.click(self.event_type_chip_text_arrow)
            event_chip_texts_count = self.get_element_count(self.event_type_multi_chip_text)
            for i in range(1, len(event_chip_texts_count) + 1):
                event_type_multi_chip_text = self.get_text_from_element(f"//th[3]/div/descendant::div[3]/child::div[{i}]/span")
                multi_chip_text_list.append(event_type_multi_chip_text)

            self.click(self.entity_chip_text_arrow)
            entity_chip_texts_count = self.get_element_count(self.event_type_multi_chip_text)
            for i in range(1, len(entity_chip_texts_count) + 1):
                entity_type_multi_chip_text = self.get_text_from_element(f"//th[5]/div/descendant::div[3]/child::div[{i}]/span")
                multi_chip_text_list.append(entity_type_multi_chip_text)

            self.click(self.user_chip_text_arrow)
            user_chip_texts_count = self.get_element_count(self.event_type_multi_chip_text)
            for i in range(1, len(user_chip_texts_count) + 1):
                user_type_multi_chip_text = self.get_text_from_element(f"//th[6]/div/descendant::div[3]/child::div[{i}]/span")
                multi_chip_text_list.append(user_type_multi_chip_text)

            self.click(self.action_chip_text_arrow)
            action_chip_texts_count = self.get_element_count(self.action_chip_multi_chip_text)
            for i in range(1, len(action_chip_texts_count) + 1):
                action_type_multi_chip_text = self.get_text_from_element(
                    f"//th[4]/div/descendant::div[3]/child::div[{i}]/span")
                multi_chip_text_list.append(action_type_multi_chip_text)

        self.export_records()
        sleep(2)
        try:
            downloads_path = str(Path.home() / "Downloads")
            audit_record_excel = pd.read_excel(downloads_path + "/AuditRecord.xlsx")
            audit_record_dataframe = pd.DataFrame(audit_record_excel)
        except:
            sleep(10)
            downloads_path = str(Path.home() / "Downloads")
            audit_record_excel = pd.read_excel(downloads_path + "/AuditRecord.xlsx")
            audit_record_dataframe = pd.DataFrame(audit_record_excel)

        print(audit_record_dataframe)
        no_of_row_count = len(audit_record_dataframe.index)
        col_table_list = []
        results_dict['records_count_app'] = no_of_row_count
        results_dict['records_count_export'] = int(self.get_records_count())
        if results_dict['records_count_app'] == results_dict['records_count_export']:
            col_table_event_list = []
            col_table_entity_list = []
            col_table_user_list = []
            col_table_action_list = []
            for i in range(0, int(results_dict['records_count_app'])):
                if value_type == 'event':
                    col_table_list.append(audit_record_dataframe.loc[i][5])
                elif value_type == 'entity':
                    col_table_list.append(audit_record_dataframe.loc[i][4])
                elif value_type == 'user':
                    col_table_list.append(audit_record_dataframe.loc[i][6])
                elif value_type == 'action':
                    col_table_list.append(audit_record_dataframe.loc[i][2])

                elif value_type == 'all':

                    col_table_event_list.append(audit_record_dataframe.loc[i][5])
                    col_table_entity_list.append(audit_record_dataframe.loc[i][4])
                    col_table_user_list.append(audit_record_dataframe.loc[i][6])
                    col_table_action_list.append(audit_record_dataframe.loc[i][2])

                else:
                    results_dict['chip_text'] = 'None'

        else:
            col_table_list.append("export records count is mismatched to tabel records")

        results.append(col_table_list)
        results.append(results_dict)
        results.append(col_table_event_list)
        results.append(col_table_entity_list)
        results.append(col_table_user_list)
        results.append(col_table_action_list)
        if len(multi_chip_text_list):
            results.append(multi_chip_text_list)
            matched_records_count = 0
            x = 0
            print(values)
            for i in range(0, len(values)):
                print(i)
                print(values[i])
                print(value_type)
                if value_type == 'all':
                    for r in range(0, int(results_dict['records_count_app'])):

                        if values[i] in audit_record_dataframe.loc[r][5]:#event
                            x = results[2].count(values[i])
                        elif values[i] in audit_record_dataframe.loc[r][4]:#entity
                            x = results[3].count(values[i])
                        elif values[i] in audit_record_dataframe.loc[r][6]:#user
                            x = results[4].count(values[i])
                        elif values[i] in audit_record_dataframe.loc[r][2]:#action
                            x = results[5].count(values[i])
                else:
                    x = results[0].count(values[i])

                print(x)
                matched_records_count += x

            print(matched_records_count)
            if value_type =='all' and screen=='query_result':

                matched_records_count=int(matched_records_count/4)

            elif value_type == 'all' and screen == 'query_search':

               # matched_records_count = int(matched_records_count / len(values))
                matched_records_count = int(matched_records_count /3)

            elif screen == 'query_search' or screen == 'query_result':

                matched_records_count = int(matched_records_count)

            else:
                matched_records_count=int(matched_records_count/len(values))

            output = []
            print(results[1]['records_count_app'],type(results[1]['records_count_app']))
            print(matched_records_count,type(matched_records_count))
            if results[1]['records_count_app'] == matched_records_count:
                print(matched_records_count)
                print(results[1]['records_count_app'])

                print(results[6])
                print(results[len(results)-1])
                chip_texts=results[len(results)-1]
                print(len(chip_texts))
                for i in range(0, len(chip_texts)):

                    chip_text = chip_texts[i]
                    print(chip_text)
                    print(values[i])
                    print(chip_texts)
                    if values[i] in chip_texts:
                        print(values[i])
                        output.append('PASS')
                    else:

                        output.append('FAIL')
            else:

                output.append('FAIL')

            print(output)

            if 'FAIL' not in output:
                return 'PASS'
            else:
                return 'FAIL'

        else:
            print('no chips')
            return results
