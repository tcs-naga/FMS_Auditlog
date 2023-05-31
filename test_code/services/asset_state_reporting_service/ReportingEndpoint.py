__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import json
from test_code.data.MinePerformanceDetails import MinePerformanceDetails
from test_code.services.asset_state_reporting_service.AssetStateReportingService import AssetStateReportingService
from dataclass_wizard import fromlist

class ReportingEndpoint(AssetStateReportingService):
    
    __endpoint = '/Reporting'
        
    def get_movement_metrics(self, shift:str, destination:str='', hauler:str='', loader:str='', source_location:str='') -> MinePerformanceDetails:
        """ Get Movement Metrics

        Raises:
            Exception: failed response

        Returns:
            list: list of states
            
        Examples:
            | Get Movement Metrics |
        """
        response = self.get(self.__endpoint + '?shiftId=' + shift + '&haulerId=' + hauler + '&loaderId=' + loader + '&sourceLocation=' + source_location + '&destination=' + destination, self.get_headers())
        
        if response.status_code != 200:
            raise Exception('Failed to get movement metrics: '+ str(response.status_code) +  ' -> ' +response.text)
        
        mining_block_details_json = json.loads(response.text)
        mining_block_details = MinePerformanceDetails(** mining_block_details_json)
        return mining_block_details
