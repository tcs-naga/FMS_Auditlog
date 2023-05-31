__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
from test_code.data.ActivityDetails import ActivityDetails
from robot.api import logger
from test_code.services.asset_state_reporting_service.ActivityTypeEndpoint import ActivityTypeEndpoint
from test_code.services.asset_state_reporting_service.AssetStateReportingService import AssetStateReportingService
from test_code.utilities.AssetFieldManagement import AssetFieldManagement
from time import sleep

class ManualActivityEndpoint(AssetStateReportingService):
    
    __endpoint = '/ManualActivity'
        
    def create_activity(self, activity:ActivityDetails):
        """ Create activity via API requests

        Args:
            activity (ActivityDetails): the activity details

        Raises:
            Exception: failed response
            
        Examples:
            | Create Activity | activity=${activity_details_object}
        """
        retry_count=0
        while retry_count < 2:
            if activity.activity is None:
                sleep(0.5)
                all_activity_types = ActivityTypeEndpoint().get_all_activity_types()
                activity_type = next(filter(lambda x: x.name == activity.activity_friendly_name, all_activity_types), None)
                activity.activity = activity_type.friendlyId
            else:
                break
            retry_count=retry_count+1

        if activity.activity is None:
            raise Exception('Failed to get activity from ActivityTypeEndpoint. activity is: '+ str(activity))
        else:
            response = self.post(self.__endpoint, self.get_headers(), json.dumps(activity.__dict__))
            if response.status_code != 200:
                raise Exception('Failed to create activity: '+ str(response.status_code) +  ' -> ' +response.text)

    def create_activity_and_wait_for_asset_state(self, activity:ActivityDetails):
        try:
            self.create_activity(activity)
            AssetFieldManagement.wait_for_asset_state(self, assetId=activity.assetId, state=activity.activity_friendly_name)
        except:
            self.create_activity(activity)
            AssetFieldManagement.wait_for_asset_state(self, assetId=activity.assetId, state=activity.activity_friendly_name)
