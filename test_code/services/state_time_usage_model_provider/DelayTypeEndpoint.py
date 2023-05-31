__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from collections import namedtuple
import json
from dataclasses import dataclass
from test_code.data.DelayTypeDetails import DelayTypeDetails
from robot.api import logger
from test_code.services.state_time_usage_model_provider.StateTimeUsageModelProviderService import StateTimeUsageModelProviderService
from dataclass_wizard import fromlist

class DelayTypeEndpoint(StateTimeUsageModelProviderService):
    
    __endpoint = '/DelayType'
        
    def get_all_delay_types(self) -> list:
        """ gets all delay types from the api endpoinrt

        Raises:
            Exception: failed response

        Returns:
            list: DelayTypeDetails
        """
        response = self.get(self.__endpoint, self.get_headers())
        
        if response.status_code != 200:
            raise Exception('Failed to get delay types: '+ str(response.status_code) +  ' -> ' +response.text)

        delay_type_details = json.loads(response.text, object_hook=customDelayDecoder)
        logger.debug(delay_type_details)
        return delay_type_details
    
def customDelayDecoder(assetDict):
    return namedtuple('X', assetDict.keys())(*assetDict.values())
