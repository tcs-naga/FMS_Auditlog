__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
from test_code.data.ActivityTypeDetails import ActivityTypeDetails
from robot.api import logger
from test_code.services.state_time_usage_model_provider.StateTimeUsageModelProviderService import StateTimeUsageModelProviderService
from dataclass_wizard import fromlist

class ActivityTypeEndpoint(StateTimeUsageModelProviderService):
    
    __endpoint = '/ActivityType'
        
    def get_all_activity_types(self) -> list:
        """ get all activity types from api endpoint

        Raises:
            Exception: failed response

        Returns:
            list: list of ActivityTypeDetails
            
        Examples:
            | Get All Activity Types |
        """
        response = self.get(self.__endpoint, self.get_headers())
        
        if response.status_code != 200:
            raise Exception('Failed to get activity types: '+ str(response.status_code) +  ' -> ' +response.text)
        
        return fromlist(ActivityTypeDetails, response.json())
