__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
from robot.libraries.BuiltIn import BuiltIn
from test_code.ImperiumServices import ImperiumServices
import docker


class Database:
    RUNNING = "running"
    container_id='<Container: 73fad99f1e42>'
    def check_sql_running_in_docker(self):


        try:
            docker_client = docker.from_env()
            container = docker_client.containers.get('fmssqldb')
            print(container)
        except docker.errors.NotFound as exc:
            print(f"Check container name!\n{exc.explanation}")
        else:
            container_state = container.attrs["State"]

            if container_state["Status"] == self.RUNNING and container== self.container_id:
                print('sql services is already running docker')
                self.__running_connection()

            else:
                    print(' docker initialized  sql service')
                    self.__open_connection()

    def __open_connection(self):

        imperium_services = ImperiumServices()
        BuiltIn().run_keyword('Connect To Database', 'pymssql', 'FMSAuditDB', 'sa', imperium_services.sql()['password'], imperium_services.sql()['host'], imperium_services.sql()['port'])

    def __running_connection(self):

        #imperium_services = ImperiumServices()
        BuiltIn().run_keyword('Connect To Database', 'pymssql', 'FMSAuditDB', 'sa', 'master@5',
                              '127.0.0.1', '1433')

    def __close_connection(self):
        BuiltIn().run_keyword('Disconnect From Database')

    def execute_command(self, command:str):
        #self.__open_connection()
        self.check_sql_running_in_docker()
        BuiltIn().run_keyword('Execute Sql String', command)
        self.__close_connection()

    def query(self, command:str):

        # self.__open_connection()
        self.check_sql_running_in_docker()
        result = BuiltIn().run_keyword('DatabaseLibrary.Query', command)
        self.__close_connection()
        return result

    def delete_user(self, sap_number:str):
        """
        Delete user which is created by this class.

        Example
        | Delete User | sap_number=123456 |
        """
        # self.__open_connection()
        self.check_sql_running_in_docker()
        # self.execute_command(f"DELETE ul FROM UserLicenses ul LEFT JOIN AspNetUsers anu ON ul.UserId = anu.Id WHERE anu.SapNumber='{sap_number}'")
        # self.execute_command(f"DELETE anu FROM AspNetUsers anu WHERE anu.SapNumber='{sap_number}'")