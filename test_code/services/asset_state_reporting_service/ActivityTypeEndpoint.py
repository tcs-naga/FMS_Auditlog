__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
from test_code.data.ActivityTypeDetails import ActivityTypeDetails
from robot.api import logger
from test_code.services.asset_state_reporting_service.AssetStateReportingService import AssetStateReportingService
from dataclass_wizard import fromlist, asdict, DateTimePattern

class ActivityTypeEndpoint(AssetStateReportingService):
    
    __endpoint = '/ActivityType'
        
    def get_all_activity_types(self) -> list:
        """ Get all activity types

        Raises:
            Exception: Request fails

        Returns:
            list: list of Activity Type details
            
        Examples:
            | Get All Activity Types |
        """
        response = self.get(self.__endpoint, self.get_headers())
        
        if response.status_code != 200:
            raise Exception('Failed to get activity types: '+ str(response.status_code) +  ' -> ' +response.text)
        
        return fromlist(ActivityTypeDetails, response.json())
