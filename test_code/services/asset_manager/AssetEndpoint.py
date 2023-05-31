__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from collections import namedtuple
import json
from dataclasses import dataclass
from test_code.services.asset_manager.AssetManagerService import AssetManagerService
from test_code.data.AssetDetails import AssetDetails
from robot.api import logger

class AssetEndpoint(AssetManagerService):
    
    __endpoint = '/Asset'
        
    def get_asset(self, id:str = None, asset_identifier:str=None) -> AssetDetails:
        """ performs an API call to get an asset

        Args:
            id (str, optional): the id of the asset to get. Defaults to None.
            asset_identifier (str, optional): the asset identifier to get. Defaults to None.

        Raises:
            Exception: thrown if both id and asset_identifier are passed
            Exception: thrown if the api call does not return a 200 success

        Returns:
            AssetDetails: the asset details returned from the api call
        """
        response = None
        
        if id is not None and asset_identifier is not None:
            raise Exception('Only provide a asset_identified or an id not both')
        elif id is not None:
            response = self.get(self.__endpoint + "/" + id, self.get_headers())
        elif asset_identifier is not None:
            response = self.get(self.__endpoint + "/assetIdentifier/" + asset_identifier, self.get_headers())
        else:
            response = self.get(self.__endpoint, self.get_headers())
        
        if response.status_code != 200:
            raise Exception('Failed to get asset ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)
		
        asset_details_json = json.loads(response.text, object_hook=customAssetDecoder)
        logger.debug(asset_details_json)
        return asset_details_json
    
    def create_asset(self, asset_class_id: str, asset_identifier:str, equipmentType: int) -> str:
        """ creates an asset via the Asset API Endpoint

        Args:
            asset_class_id (str): asset class id
            asset_identifier (str): asset identifier
            equipmentType (int): equipement type

        Returns:
            str: the response text

        Raises:
            Exception: on Failure
        """
        data = {}
        data['assetClassId'] = asset_class_id
        data['assetIdentifier'] = asset_identifier
        data['equipmentType'] = equipmentType
        data['ipAddress'] = "string"
        json_data = json.dumps(data)
        response = self.post(self.__endpoint, self.get_headers(), json_data)

        if response.status_code != 201:
            if response.text == '"Asset Identifier already exist"':
                logger.info('API response was Asset Identifier already exist')
            else:
                raise Exception('Failed to create asset: '+ str(response.status_code) +  ' -> ' +response.text)

        return response.text.replace('"', '')

    def set_asset_behaviour(self, asset_id:str, type_name:str, value:str):
        """ sets a new asset behaviour for the given asset

        Args:
            asset_id (str): the uuid of the asset
            type_name (str): typeName of the behaviour
            value (str): the value of the behaviour

        Examples:
            | Set Asset Behaviour | asset_id=30c2fe75-54ff-4a92-dcb9-08dad74f92f1 | type_name=AssetRuleset | value=HaulerNoTelemetry |
        """
        data = {}
        data['typeName'] = type_name
        data['value'] = value
        json_data = json.dumps(data)
        response = self.patch(self.__endpoint + '/' + asset_id + '/assetBehaviour', self.get_headers(), json_data)

        if response.status_code != 200:
            raise Exception('Failed to create asset: '+ str(response.status_code) +  ' -> ' +response.text)

def customAssetDecoder(assetDict):
    return namedtuple('X', assetDict.keys())(*assetDict.values())
