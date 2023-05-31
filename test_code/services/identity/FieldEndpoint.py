__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
from test_code.services.identity.IdentityService import IdentityService
from test_code.data.AssetDetails import AssetDetails
from robot.api import logger

class FieldEndpoint(IdentityService):
    
    __endpoint = '/Field'
        
    def login(self, assetId:str = None, userNumber:str=None) -> str:
        """ login to the field

        Args:
            assetId (str, optional): assetID. Defaults to None.
            userNumber (str, optional): userNumber. Defaults to None.

        Raises:
            Exception: failed response

        Returns:
            str: userId
            
        Examples:
            | Login | assetUd=DT5401 | userNUmber=123456 |
        """
        response = None

        response = self.post(self.__endpoint + '/Login', self.get_headers(), '{ "assetId": "' + assetId + '", "userNumber": "' + userNumber + '" }')
        
        if response.status_code != 200:
            raise Exception('Failed to get asset ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)
		
        return response.json()['userId']
    
    def logout(self, assetId:str = None, userId:str=None):
        """ logout of field

        Args:
            assetId (str, optional): assetID. Defaults to None.
            userId (str, optional): userID. Defaults to None.

        Raises:
            Exception: failed response
            
        Examples:
            | Logout | assetUd=DT5401 | userId=000000-0000000000000000-00000 |
        """
        response = None

        response = self.post(self.__endpoint + '/Logout', self.get_headers(), '{ "assetId": "' + assetId + '", "userId": "' + userId + '" }')
        
        if response.status_code != 200:
            raise Exception('Failed to get asset ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)

