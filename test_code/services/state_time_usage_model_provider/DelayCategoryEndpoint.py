__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
from test_code.data.DelayCategoryDetails import DelayCategoryDetails
from robot.api import logger
from test_code.services.state_time_usage_model_provider.StateTimeUsageModelProviderService import StateTimeUsageModelProviderService
from dataclass_wizard import fromlist

class DelayCategoryEndpoint(StateTimeUsageModelProviderService):
    
    __endpoint = '/DelayCategory'
        
    def get_all_delay_categories(self) -> list:
        """ gets all the delay categories from the api endpoint

        Raises:
            Exception: failed response

        Returns:
            _type_: list of DelayCategoryDetails
            
        Examples:
            | Get All Delay Categories |
        """
        response = self.get(self.__endpoint, self.get_headers())
        
        if response.status_code != 200:
            raise Exception('Failed to get delay categories: '+ str(response.status_code) +  ' -> ' +response.text)
        
        return fromlist(DelayCategoryDetails, response.json())
