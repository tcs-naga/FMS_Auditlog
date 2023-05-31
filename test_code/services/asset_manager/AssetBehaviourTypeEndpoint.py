__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from collections import namedtuple
import json
from dataclasses import dataclass
from dataclass_wizard import fromlist
from test_code.data.AssetBehaviourTypeDetails import AssetBehaviourTypeDetails
from test_code.services.asset_manager.AssetManagerService import AssetManagerService
from robot.api import logger
import copy

class AssetBehaviourTypeEndpoint(AssetManagerService):
    
    __endpoint = '/AssetBehaviourType'
        
    def create_asset_behaviour_type(self, asset_behaviour_type_details:AssetBehaviourTypeDetails):
        """ create an asset behaviour type via AssetBehaviourType API Endpoint

        Args:
            asset_behaviour_type_details (AssetClassModelDetails): asset class to create

        Raises:
            Exception: on Failure

        Examples:
            | Create Asset Behaviour Type | asset_behaviour_type_details={asset_behaviour_type_details_object} |
        """
        asset_behaviour_type_details_copy = copy.deepcopy(asset_behaviour_type_details)
        del asset_behaviour_type_details_copy.id
        asset_behaviour_type_details_str = (str(asset_behaviour_type_details_copy.__dict__).replace(" ", "").replace("'", "\""))[1:-1]

        response_from_get = self.get(self.__endpoint, self.get_headers())
        response_from_get_text = response_from_get.text

        if asset_behaviour_type_details_str in response_from_get_text:
            logger.info("Asset behaviour type is already set")           
        else:  
            response = self.post(self.__endpoint, self.get_headers(), json.dumps(asset_behaviour_type_details.__dict__))
            if response.status_code != 201:
                raise Exception('Failed to create asset behaviour type: '+ str(response.status_code) +  ' -> ' +response.text)

