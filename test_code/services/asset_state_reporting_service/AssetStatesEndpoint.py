__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
from test_code.data.AssetStateDetails import AssetStateDetails
from test_code.services.asset_state_reporting_service.AssetStateReportingService import AssetStateReportingService
from dataclass_wizard import fromlist, asdict, DateTimePattern
from robot.api import logger

class AssetStatesEndpoint(AssetStateReportingService):
    
    __endpoint = '/Asset'
        
    def get_asset_states(self, assetId: str, shiftId: str) -> list:
        """ get asset states for asset and shift

        Args:
            assetId (str): asset id
            shiftId (str): shift id

        Raises:
            Exception: failed response

        Returns:
            list: list of AssetStateDetails
        """
        response = self.get(self.__endpoint + '/' + assetId + '/' + shiftId + '/States', self.get_headers())
        
        if response.status_code != 200:
            raise Exception('Failed to get activity types: '+ str(response.status_code) +  ' -> ' +response.text)
        
        return fromlist(AssetStateDetails, response.json())

    def insert_before(self, asset: AssetStateDetails, beforeStateId: str):
        """ insert before given state id, an new asset state detail

        Args:
            asset (AssetStateDetails): the asset state details
            beforeStateId (str): before state id

        Raises:
            Exception: failed response
            
        Examples:
            | Insert Before | asset=${asset_state_object} | beforeStateID=0000000-ffffffffffffff-ffffff |
        """
        data = {}
        data['assetId'] = asset.assetId
        data['beforeStateId'] = beforeStateId
        data['comment'] = asset.comment
        data['endTime'] = asset.endedAt
        data['reportedState'] = asset.state
        data['startTime'] = asset.reportedAt
        data['userId'] = '123456'
        json_data = json.dumps(data)
        response = self.post(self.__endpoint + '/States/' + beforeStateId + '/InsertBefore', self.get_headers(), json_data)
        
        if response.status_code != 200:            
            if "Duplicate state exists" in response.text:
                logger.info('API response was: Duplicate state exists')
            else:
                raise Exception('Failed to insert asset state: '+ str(response.status_code) +  ' -> ' +response.text)