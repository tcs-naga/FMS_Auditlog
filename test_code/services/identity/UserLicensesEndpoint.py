__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
import pendulum
from test_code.services.asset_manager.AssetEndpoint import AssetEndpoint
from test_code.services.identity.IdentityService import IdentityService
from test_code.data.AssetDetails import AssetDetails
from robot.api import logger

class UserLicensesEndpoint(IdentityService):
    
    __endpoint = '/licenses'
        
    def add_user_license(self, sap_number: str, asset_identifier: str) -> None:
        """
        Add user license to FMS

        Examples:
        | Add User License | 123456 | Asset Identifier |
        """
        asset_details=AssetEndpoint().get_asset(asset_identifier=asset_identifier)
        data = '{ "assetClass": "' + asset_details.assetModelModel.assetClass.id + '", "expiryDate": "' + pendulum.tomorrow('UTC').isoformat() + '", "issueDate": "' + pendulum.yesterday('UTC').isoformat() + '", "licenseType": 3 }'

        response = self.post(self.__endpoint + '/' + sap_number, self.get_headers(), data)

        if response.status_code != 200:
            raise Exception('Failed to get asset ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)

