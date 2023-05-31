__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
from robot.libraries.BuiltIn import BuiltIn
from test_code.ImperiumServices import ImperiumServices


class Database:

    def __open_connection(self):
        imperium_services = ImperiumServices()
        BuiltIn().run_keyword('Connect To Database', 'pymssql', 'Identity', 'sa', imperium_services.sql()['password'], imperium_services.sql()['host'], imperium_services.sql()['port'])
        
    def __close_connection(self):
        BuiltIn().run_keyword('Disconnect From Database')

    def execute_command(self, command:str):
        self.__open_connection()
        BuiltIn().run_keyword('Execute Sql String', command)
        self.__close_connection()

    def query(self, command:str):
        self.__open_connection()
        result = BuiltIn().run_keyword('DatabaseLibrary.Query', command)
        self.__close_connection()
        return result

    def delete_user(self, sap_number:str):
        """
        Delete user which is created by this class.

        Example
        | Delete User | sap_number=123456 |
        """
        self.execute_command(f"DELETE ul FROM UserLicenses ul LEFT JOIN AspNetUsers anu ON ul.UserId = anu.Id WHERE anu.SapNumber='{sap_number}'")
        self.execute_command(f"DELETE anu FROM AspNetUsers anu WHERE anu.SapNumber='{sap_number}'")