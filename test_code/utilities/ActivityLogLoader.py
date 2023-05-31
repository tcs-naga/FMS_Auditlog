import json
import os
import pendulum
from test_code.Const import AUTOMATED_TEST_DIR
from robot.api import logger
from test_code.data.AssetStateDetails import AssetStateDetails
from test_code.services.asset_state_reporting_service.AssetStatesEndpoint import AssetStatesEndpoint

class ActivityLogLoader():
    
    def load_activity_log_from_file(self, file_name:str, offset_date:str=(pendulum.now().format('YYYYMMDD') if pendulum.now().hour >= 6 else pendulum.now().subtract(days=1).format('YYYYMMDD')), offset_shift:str=('D' if pendulum.now().hour >= 6 and pendulum.now().hour < 18 else 'N')):
        """ loads a json file of activity log details into the system via api's

        Args:
            file_name (str): the filename to load from the activity_logs directory
            offset_date (str, optional): the offset date to load the activities on. Defaults to pendulum.now().format('YYYYMMDD').
            offset_shift (str, optional): the shift to load the activities before. Defaults to 'D'.
        """
        file = open(str(os.path.join(AUTOMATED_TEST_DIR, 'test_data', 'activity_logs').replace('\\', '/')) + '/' + file_name)
        data = json.load(file)
        asset_states_endpoint = AssetStatesEndpoint()
        shift = offset_date + offset_shift
        logger.info('hour: {}'.format(pendulum.now().hour))
        # Current shift date is today's if more than 6:00am, else it was yesterday's shift.
        current_shift = (pendulum.now().format('YYYYMMDD') if pendulum.now().hour >= 6 else pendulum.now().subtract(days=1).format('YYYYMMDD')) + ('D' if pendulum.now().hour >= 6 and pendulum.now().hour < 18 else 'N')
        logger.info('current_shift: ' + current_shift)
        logger.info('shift: ' + shift)

        if shift != current_shift:
            asset_states = asset_states_endpoint.get_asset_states(data[0]['assetId'], shift)
            asset_states = sorted(asset_states, key=lambda asset_state: asset_state.reportedAt, reverse=True)
            last_asset_state = asset_states[len(asset_states)-1]
            logger.info('last_asset_state{}'.format(last_asset_state))
            last_asset_id = last_asset_state.id
            reportedAt = pendulum.parse(last_asset_state.reportedAt)
            new_endedAt = reportedAt
            start_of_shift = reportedAt.subtract(hours=12).format('YYYY-MM-DDT22:00:00.000+00:00')
            if offset_shift=='N':
                start_of_shift = reportedAt.subtract(hours=12).format('YYYY-MM-DDT10:00:00.000+00:00')
            new_asset_state = AssetStateDetails(reportedAt=start_of_shift, endedAt=new_endedAt.to_iso8601_string(), state='Travel Empty', assetId=data[0]['assetId'], comment='API Bring to start of Day')
            logger.info('need to load{}'.format(new_asset_state))
            asset_states_endpoint.insert_before(new_asset_state, last_asset_id)

        logger.info('before full load shift: ' + shift)
        # Load activity in FMS with full cycle.
        for activity in data:
            asset_states = asset_states_endpoint.get_asset_states(activity['assetId'], shift)
            if offset_shift == 'D':
                shift = pendulum.from_format(offset_date, 'YYYYMMDD').subtract(days=1).format('YYYYMMDD') + 'N'
            else:
                shift = offset_date + 'D'
            asset_states = sorted(asset_states, key=lambda asset_state: asset_state.reportedAt, reverse=True)
            last_asset_state = asset_states[len(asset_states)-1]
            last_asset_id = last_asset_state.id
            reportedAt = pendulum.parse(last_asset_state.reportedAt)
            new_reportedAt = reportedAt.subtract(seconds=activity['offset']+activity['duration'])
            new_endedAt = reportedAt.subtract(seconds=activity['offset'])
            logger.info(activity)
            new_asset_state = AssetStateDetails(reportedAt=new_reportedAt.to_iso8601_string(), endedAt=new_endedAt.to_iso8601_string(), state=activity['state'], assetId=activity['assetId'], comment=activity['comment'])
            logger.info(new_asset_state)
            asset_states_endpoint.insert_before(new_asset_state, last_asset_id)