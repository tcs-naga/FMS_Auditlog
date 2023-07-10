from test_code.auditlog.BasePage import Basepage
from time import  sleep
import pandas as pd
from pathlib import Path


class AuditResults(Basepage):

    def verification_of_all_elements_in_audit_results_screen(self):
        # This method verify  all required  fields are present in new audit query search screen or not.
        """
        Verification Of All Elements In Audit Results Screen

        Examples:
        | Verification Of All Elements In Audit Results Screen |
        """
        self.check_if_elements_is_present_or_not(self.query_results_elements_dict)

    def validate_fid_in_circuit_created_field(self,fid):
        """
        Validate FID In Circuit Created Field

        Examples:
        | Validate FID In Circuit Created Field | ID |
        """
        #ccv : circuit_created_values
        self.search_with_id(fid)
        sleep(15)
        self.click(self.id_rows)
        sleep(2)
        ccv = self.get_text_from_element(self.circuit_created_values)
        sleep(2)
        ccv = ccv.split('\n')
        ccv_id = ccv[2]
        if fid == ccv_id:
            return 'Id is matched with CCV'
        else:
            return 'Id  is not matched with CCV'

    def validate_export_records_with_tabel_results_in_audit_result_screen(self):
        """
        Validate Export Records With Tabel Results in Audit Result Screen

        Examples:
        | Validate Export Records With Tabel Results in Audit Result Screen |
        """

        return self.validate_export_records_with_tabel_results()

    def validate_records_with_search_fid(self,fid):
        """
        Validate Records  With Search FID

        Examples:
        | Validate Records  With Search FID |
        """
        self.search_with_id(fid)
        sleep(15)
        rows = self.get_element_count(self.id_rows)
        rows = len(rows)
        print(rows)
        for i in range(1, rows+1):
            print(i)
            row_lines_id = "//tbody/tr/td["+str(i)+"]"
            self.click(row_lines_id)
            sleep(2)
            row_lines_id_text = self.get_text_from_element(row_lines_id)
            sleep(2)
            circuit_created_values_text=self.get_text_from_element(self.circuit_created_values)
            circuit_created_values_text=circuit_created_values_text.split('\n')
            print(fid)
            print(row_lines_id_text)
            print(circuit_created_values_text)
            circuit_created_values_id_text = circuit_created_values_text[2]
            if (fid == row_lines_id_text == circuit_created_values_id_text):
                if self.validate_export_records_with_tabel_results() == 'records count is matched':
                    return 'Id is matched with results & CCV & tabel count is match with export count'
                else:
                    return 'Id is matched with results & CCV & tabel count is not match with export count'
            else:
                return 'Id  is not match with results & CCV'

    def validate_no_records_when_search_with_invalid_fid(self,invalid_fid):

        """
        Validate No Records When Search With Invalid FID

        Examples:
       | Validate No Records When Search With Invalid FID | Invalid_Fid |
        """

        self.search_with_id(invalid_fid)
        sleep(5)
        no_record_text=self.get_text_from_element(self.tabel_no_records_label)
        if no_record_text=="No results found for your search":
            return 'no records found'
        else:
            return 'may be records found {or} no records found label is missed'

    def validate_event_type_with_search_function(self,*values):
        """
        Validate Event Type With Search Function

        Examples:
       | Validate Event Type With Search Function | Values |
        """
        self.search_with_filters(self.query_results_elements_dict['event_type_input'],*values)
        return self.validate_tabel_records_with_chip_texts_and_given_input('event','query_result', *values)

    def validate_entity_with_search_function(self,*values):
        """
        Validate Entity  With Search Function

        Examples:
       | Validate Entity  With Search Function | Values |
        """
        self.search_with_filters(self.query_results_elements_dict['entity_input'],*values)
        return self.validate_tabel_records_with_chip_texts_and_given_input('entity','query_result',*values)

    def validate_user_with_search_function(self,*values):
        """
        Validate User  With Search Function

        Examples:
       | Validate User  With Search Function | Values |
        """
        self.search_with_filters(self.query_results_elements_dict['user_input'],*values)
        return self.validate_tabel_records_with_chip_texts_and_given_input('user','query_result',*values)

    def validate_action_with_search_function(self,*values):
        """
        Validate Action  With Search Function

        Examples:
       | Validate Action  With Search Function | Values |
        """
        self.search_with_filters(self.query_results_elements_dict['action_input'],*values)
        return self.validate_tabel_records_with_chip_texts_and_given_input('action','query_result',*values)

    def validate_all_types_with_search_function(self, *values):

        """
        Validate All Types With Search Function

         Examples:
        | Validate All Types With Search Function | Values |
        """
        results_dict={}
        results=[]
        audit_record_excel_all=''

        self.export_records()
        sleep(2)

        try:
            downloads_path = str(Path.home() / "Downloads")
            audit_record_excel_all = pd.read_excel(downloads_path + "/AuditRecord.xlsx")
            audit_record_dataframe = pd.DataFrame(audit_record_excel_all)
        except:
            sleep(10)
            downloads_path = str(Path.home() / "Downloads")
            audit_record_excel_all = pd.read_excel(downloads_path + "/AuditRecord.xlsx")
            audit_record_dataframe = pd.DataFrame(audit_record_excel_all)

        print(audit_record_dataframe)
        no_of_row_count = len(audit_record_dataframe.index)
        col_table_list = []
        results_dict['records_count_app'] = no_of_row_count
        results_dict['records_count_export'] = int(self.get_records_count())
        output=[]
        if results_dict['records_count_app'] == results_dict['records_count_export']:
            col_table_event_list = []
            col_table_entity_list = []
            col_table_user_list = []
            col_table_action_list = []
            for i in range(0, int(results_dict['records_count_app'])):


                col_table_event_list.append(audit_record_dataframe.loc[i][5])
                col_table_entity_list.append(audit_record_dataframe.loc[i][4])
                col_table_user_list.append(audit_record_dataframe.loc[i][6])
                col_table_list.append(audit_record_dataframe.loc[i][2])
        results.append(col_table_event_list)
        results.append(col_table_entity_list)
        results.append(col_table_user_list)
        results.append(col_table_action_list)

        for i in range(0, len(values)):
            print(i)
            print(values[i])
            for r in range(0, int(results_dict['records_count_app'])):

                if values[i] in audit_record_dataframe.loc[r][4]:  # entity


                    self.search_with_filters(self.query_results_elements_dict['entity_input'],values[i])
                    break
                elif values[i] in audit_record_dataframe.loc[r][5]:  # event
                    self.search_with_filters(self.query_results_elements_dict['event_type_input'], values[i])
                    break
                elif values[i] in audit_record_dataframe.loc[r][6]:  # user
                    self.search_with_filters(self.query_results_elements_dict['user_input'], values[i])
                    break
                elif values[i] in audit_record_dataframe.loc[r][2]:  # action
                    self.search_with_filters(self.query_results_elements_dict['action_input'], values[i])
                    break

        return self.validate_tabel_records_with_chip_texts_and_given_input('all','query_result', *values)

    def validate_new_query_btn_functionality(self):
        """
         Validate New Query Btn Functionality

         Examples:
        | Validate New Query Btn Functionality|
         """
        self.new_query()

    def validate_sorting_functionality(self):
        """
         Validate Sorting Functionality

         Examples:
        | Validate Sorting Functionality|
         """
        record_count_app=self.get_records_count()
        last_record_num_table=int(self.get_text_from_element(self.id_rows))
        self.click(self.id_row_sort_arrow)
        sleep(5)
        first_record_num_table =int(self.get_text_from_element(self.id_rows))
        if int(record_count_app) == last_record_num_table:

            if first_record_num_table == last_record_num_table-(last_record_num_table-1):

                return 'PASS'
            else:
                return "FAIL"
        else:
            return "FAIL"

    def validate_pagination_functionality(self):
        """
        Validate Pagination Functionality

        Examples:
        | Validate Pagination Functionality|
        """

        pg_count=self.get_element_count(self.pagination_elements)
        record_count_app = self.get_records_count()
        self.click(f"//ul/child::li[{len(pg_count)}]")
        sleep(5)
        row_count = self.get_element_count('//tbody/tr')
        first_record_num_table=self.get_text_from_element(f"//tbody/tr[{len(row_count)}]/td[1]")
        if first_record_num_table=='1':
            self.click(self.left_double_arrow)
            sleep(5)
            last_record_num_table = self.get_text_from_element(self.id_rows)
            if record_count_app==last_record_num_table:
                self.click(f"//ul/child::li[{len(pg_count)-1}]")
                sleep(5)
                spg_row_text=self.get_text_from_element(self.id_rows)
                last_record_num_table=int(last_record_num_table)-10
                spg_row_text=int(spg_row_text)
                if spg_row_text==last_record_num_table:
                    self.click(self.left_single_arrow)
                    sleep(5)
                    last_record_num_table = self.get_text_from_element(self.id_rows)
                    if last_record_num_table==record_count_app:
                        return 'PASS'
                    else:
                        return "FAIL"
                else:
                    return "FAIL"
            else:
                return "FAIL"
        else:
            return "FAIL"

    def validate_user_activity_details(self):
        pass
