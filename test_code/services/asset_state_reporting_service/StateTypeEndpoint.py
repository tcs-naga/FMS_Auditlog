__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
from test_code.data.StateTypeDetails import StateTypeDetails
from robot.api import logger
from test_code.services.asset_state_reporting_service.AssetStateReportingService import AssetStateReportingService
from dataclass_wizard import fromlist, asdict, DateTimePattern

class StateTypeEndpoint(AssetStateReportingService):
    
    __endpoint = '/StateType'
        
    def get_all_state_types(self) -> list:
        """ Get All State Types

        Raises:
            Exception: failed response

        Returns:
            list: list of states
            
        Examples:
            | Get All State Types |
        """
        response = self.get(self.__endpoint, self.get_headers())
        
        if response.status_code != 200:
            raise Exception('Failed to get state types: '+ str(response.status_code) +  ' -> ' +response.text)
        
        return fromlist(StateTypeDetails, response.json())
