from test_code.auditlog.BasePage import Basepage
from robot.api.deco import keyword


class AuditQuerySearch(Basepage):

    # Element_locators :
    __element_dict = {'Input_box': 'name:q', 'Input_box1': 'name:q'}

    def demo(self,element: str, input_text: str):
        """
        Demo

         Examples:
            | Demo | Element | Input_text |
        """
        self.send_keys(element,input_text)
    # This is demo function/method

    def verification_of_all_elements_in_audit_query_search(self):
        """
        Verification Of All Elements In Audit Query Search

        Examples:
            | Verification Of All Elements In Audit Query Search |
        """
        self.check_if_element_is_present_or_not(self.__element_dict)
    # This method verify  all required  fields are present in new audit query search screen or not.

    def query_search_with_all_fields(self):
        """
        Query Search With All Fields

         Examples:
            | Query Search With All Fields | Element | Input_text |
        """
        pass
    # This method search the query with all required  fields in new audit query search screen.

    def query_search_with_date_field(self):
        """
        This method search the query with only date field in new audit query search screen
        """