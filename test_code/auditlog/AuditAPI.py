from time import sleep
import requests

import json

from test_code.services.BaseClient import BaseClient


class AuditAPI():
    headers={'content-type': 'application/json'}

    user_details_headers = {

    'x-user-userid':'000001',
    'x-user-firstname':'AUT_TEST_FN',
    'x-user-lastname':'AUT_TEST_LN',
    'x-user-emailaddress':'AUT_TEST@fmgl.com.au',
    'x-user-username':'AUT.TEST-XX'
    }

    audit_record_details={
        "pageNumber": 0,
        "pageSize": 0,
        "utcStartDateTime": "2023-06-28T07:51:35.369Z",
        "utcEndDateTime": "2023-06-28T07:51:35.369Z",
        "auditRecordID": [
            "string"
        ],
        "actions": [
            "string"
        ],
        "users": [
            "string"
        ],
        "assets": [
            "string"
        ],
        "entity": [
            "string"
        ],
        "isExportToExcel": True,
        "sortColumn": "string",
        "sortOrder": "string"
    }
    jsonData = json.dumps(audit_record_details)

    def get_api_method(self,url):
        """
        Get API Method

        Examples:
        | Get API Method | Url |
        """
        results = {}
        sleep(2)
        response = requests.get(url,headers=self.headers)

        sleep(5)
        print(response)
        results['status_code'] = self.get_status_code_from_response(response, '[', ']')
        results['Content'] = response.content
        return results

    def get_api_method_with_user_details_headers(self, url,):
        """
        Get API Method With User Details Headers

        Examples:
        | Get API Method With User Details Headers | Url |
        """
        results = {}
        sleep(2)
        response = requests.get(url, headers=self.user_details_headers)
        sleep(5)
        results['status_code'] = self.get_status_code_from_response(response, '[', ']')
        results['Content'] = response.content
        return results

    def post_api_method(self,url,data):
        """
        Post API Method

        Examples:
        | Post API Method | Url | Data |
        """
        results = {}
        sleep(2)
        response = requests.post(url, data, headers=self.headers)
        sleep(5)
        results['status_code'] = self.get_status_code_from_response(response, '[', ']')
        results['Content'] = response.content
        return results

    def audit_record_post_api_method(self,url):
        """
        Audit Record Post API Method

        Examples:
        | Audit Record Post API Method | Url | Data |
        """
        results = {}
        sleep(2)
        response = requests.post(url, self.jsonData, headers=self.headers)
        print(response)
        sleep(5)
        results['status_code'] = self.get_status_code_from_response(response, '[', ']')
        results['Content'] = response.content
        return results

    def audit_record_get_api_method(self, url):
        """
        Audit Record Get API Method

        Examples:
        | Audit Record Get API Method | Url | Data |
        """
        results = {}
        sleep(5)
        response = requests.get(url, self.jsonData, headers=self.headers)
        print(response)
        sleep(8)
        results['status_code'] = self.get_status_code_from_response(response, '[', ']')
        results['Content'] = response.content
        return results
    def patch_api_method(self,url,data):
        """
        Patch API Method

        Examples:
        | Patch API Method | Url | Data |
        """
        results={}
        sleep(2)
        response= requests.patch(url,data,headers=self.headers)
        sleep(5)
        results['status_code']=self.get_status_code_from_response(response,'[',']')
        results['Content'] = response.content
        return results

    def delete_api_method(self,url,data):
        """
        Delete API Method

        Examples:
        | Delete API Method | Url | Data |
        """
        results = {}
        sleep(10)
        response = requests.delete(url,data=data,headers=self.headers)
        sleep(10)
        results['status_code'] = self.get_status_code_from_response(response, '[', ']')
        results['Content'] = response.content
        return results

    def get_status_code_from_response(self,response,deli_1:str,deli_2:str):
        response = str(response).split(deli_1)
        response = str(response[1]).split(deli_2)
        status_code = response[0]
        return status_code

    def convert_to_json(self,data):
        """
          Convert To Json

          Examples:
          | Convert To Json |
        """
        return   json.loads(data)
