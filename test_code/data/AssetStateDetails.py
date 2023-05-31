__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import dataclasses
import pendulum
from pendulum import DateTime
from test_code.services.asset_state_reporting_service.ActivityTypeEndpoint import ActivityTypeEndpoint
from robot.api import logger
from test_code.services.asset_state_reporting_service.StateTypeEndpoint import StateTypeEndpoint

@dataclass
class AssetStateDetails:
    id: str = None
    reportedAt: str = None
    endedAt: str = None
    state: str = None
    assetId: str = None
    comment: str = None
    
    def get_reported_at_in_display_format(self):
        perth_timezone = pendulum.timezone('Australia/Perth')
        perth_datetime = perth_timezone.convert(pendulum.parse(self.reportedAt))
        return perth_datetime.format('DD/MM/YYYY, h:mm:ss A').lower()
    
    def get_ended_at_in_display_format(self):
        if self.endedAt is not None and self.endedAt !='': 
            perth_timezone = pendulum.timezone('Australia/Perth')
            perth_datetime = perth_timezone.convert(pendulum.parse(self.endedAt))
            return perth_datetime.format('DD/MM/YYYY, h:mm:ss A').lower()
        return self.endedAt
    
    def get_reported_at_in_input_format(self):
        perth_timezone = pendulum.timezone('Australia/Perth')
        perth_datetime = perth_timezone.convert(pendulum.parse(self.reportedAt))
        return perth_datetime.format('DD/MM/YYYY h:mm:ss A')
    
    def get_ended_at_in_input_format(self):
        if self.endedAt is not None and self.endedAt !='': 
            perth_timezone = pendulum.timezone('Australia/Perth')
            perth_datetime = perth_timezone.convert(pendulum.parse(self.endedAt))
            return perth_datetime.format('DD/MM/YYYY h:mm:ss A')
        return self.endedAt
    
    def get_displayed_state_name(self):
        all_state_types = StateTypeEndpoint().get_all_state_types()
        entry = next(filter(lambda x: x.stateTypeId == self.state, all_state_types), None)
        
        logger.info(entry)
        
        if entry is None:
            return self.state
        else:
            return entry.name

    def set_reportedAt(self, reportedAt: str):
        self.reportedAt = reportedAt
        
    def set_endedAt(self, endedAt: str):
        self.endedAt = endedAt
        
    def set_dates_offset_from(self, date:str, duration:int, offset:int):
        reportedAt = pendulum.parse(date)
        self.reportedAt = reportedAt.subtract(seconds=offset+duration).to_iso8601_string()
        self.endedAt = reportedAt.subtract(seconds=offset).to_iso8601_string()
        logger.info(self.reportedAt)
        logger.info(self.endedAt)
        
    def get_duration(self):
        logger.info(self.reportedAt)
        logger.info(self.endedAt)
        hours = pendulum.parse(self.endedAt).diff(pendulum.parse(self.reportedAt)).in_hours()
        logger.info(hours)
        minutes = pendulum.parse(self.endedAt).subtract(hours=hours).diff(pendulum.parse(self.reportedAt)).in_minutes()
        logger.info(minutes)
        seconds = pendulum.parse(self.endedAt).subtract(hours=hours, minutes=minutes).diff(pendulum.parse(self.reportedAt)).in_seconds()
        logger.info(seconds)
        return str(hours).zfill(2) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)
    
    def set_state(self, state):
        self.state = state
        
    def set_comment(self, comment):
        self.comment = comment
        
    def set_asset(self, assetId):
        self.assetId = assetId
        
    def filter_list_of_asset_states(self, asset_states:list, state:str, after_time:str=None) -> list:
        all_state_types = StateTypeEndpoint().get_all_state_types()
        entry = list(map(lambda y: y.stateTypeId, filter(lambda x: x.name == state, all_state_types)))
        if len(entry) == 0:
            entry.append(state)
        logger.info(entry)
        filtered_list = list(filter(lambda a: a.state in entry and (after_time is None or pendulum.parse(a.reportedAt)>=pendulum.parse(after_time)), asset_states))
        logger.info(filtered_list)
        return filtered_list
        
    def get_last_known_state_start_date(self, asset_states:list): 
        return sorted(asset_states, key=lambda asset_state: asset_state.reportedAt, reverse=True)[0].reportedAt
    
    def get_last_known_state(self, asset_states:list): 
        return sorted(asset_states, key=lambda asset_state: asset_state.reportedAt, reverse=True)[0]
    
    def get_earliest_state(self, asset_states:list): 
        return sorted(asset_states, key=lambda asset_state: asset_state.reportedAt)[0]
