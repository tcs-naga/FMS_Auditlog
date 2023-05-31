__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from collections import namedtuple
import json
from dataclasses import dataclass
from dataclass_wizard import fromlist
from test_code.data.AssetClassModelDetails import AssetClassModelDetails
from test_code.services.asset_manager.AssetManagerService import AssetManagerService
from test_code.data.AssetDetails import AssetDetails
from robot.api import logger

class AssetClassEndpoint(AssetManagerService):
    
    __endpoint = '/AssetClass'
        
    def create_asset_class(self, asset_class_details:AssetClassModelDetails) -> str:
        """ create an asset class via AssetClass API Endpoint

        Args:
            asset_class_details (AssetClassModelDetails): asset class to create

        Raises:
            Exception: on Failure

        Returns:
            str: the asset class id
        """
        response = self.post(self.__endpoint, self.get_headers(), json.dumps(asset_class_details.__dict__))
        
        if response.status_code != 201:
            raise Exception('Failed to create asset class: '+ str(response.status_code) +  ' -> ' +response.text)
        
        return response.text.replace('"', '')

    def get_all_asset_classes(self) -> list:
        """ Get all asset classes

        Raises:
            Exception: Request fails

        Returns:
            list: list of asset class details
            
        Examples:
            | Get All Asset Classes |
        """
        response = self.get(self.__endpoint, self.get_headers())
        
        if response.status_code != 200:
            raise Exception('Failed to get asset classes: '+ str(response.status_code) +  ' -> ' +response.text)
        
        return fromlist(AssetClassModelDetails, response.json())

