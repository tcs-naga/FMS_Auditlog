__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
from robot.libraries.BuiltIn import BuiltIn
from test_code.ImperiumServices import ImperiumServices
from test_code.database.Database import Database


class FmsDatabase(Database):
    Con_result=''
    def search_and_validate_fid_in_db(self,fid):
        """
        Search And Validate Fid In DB

        Examples:
        | Search And Validate Fid In DB |FID|
        """
        result= self.query(f"select FriendlyID  from dbo.AuditRecords where FriendlyID='{fid}'")
        return result[0]


    def search_and_validate_Event_in_db(self,obj_id):
        """
        Search And Validate Event In DB

        Examples:
        | Search And Validate Event In DB |OBJ ID|
        """
        result= self.query(f"select DISTINCT Object  from dbo.AuditRecords where ObjectId='{obj_id}'")
        print(result[0])
        return result[0]


    def search_and_validate_Entity_in_db(self,obj_id):
        """
        Search And Validate Entity In DB

        Examples:
        | Search And Validate Entity In DB |OBJ ID|
        """
        result= self.query(f"select DISTINCT Entity   from dbo.AuditRecords where ObjectId='{obj_id}'")
        return result[0]


    def search_and_validate_user_in_db(self,obj_id):
        """
        Search And Validate User In DB

        Examples:
        | Search And Validate User In DB |OBJ ID|
        """
        result= self.query(f"select DISTINCT ChangedByID  from dbo.AuditRecords where ObjectId='{obj_id}'")
        return result[0]

    def search_and_validate_action_in_db(self,obj_id,values):
        """
        Search And Validate Action In DB

        Examples:
        | Search And Validate Action In DB |OBJ ID|
        """
        result= self.query(f"select DISTINCT ChangeType  from dbo.AuditRecords where ObjectId='{obj_id}'")

        for x in range(0,len(result)):
            if values == result[x][0]:
                self.Con_result = 'PASS'
                break
            else:
                print('fail')
                self.Con_result='FAIL'
        return self.Con_result

    def search_and_validate_exception_log_in_db(self,date):
        """
        Search And Validate Exception Log In DB

        Examples:
        | Search And Validate Exception Log In DB |Date|
        """
        result = self.query(f"select DISTINCT UserName,ExceptionDetails	from dbo.ExceptionDetails where DateTimeUTC='{date}'")
        return result[0]
