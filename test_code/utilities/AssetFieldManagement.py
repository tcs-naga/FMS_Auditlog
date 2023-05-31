import json
import math
import time
from robot.libraries.BuiltIn import BuiltIn
from test_code.Const import MAPS
from test_code.ImperiumServices import ImperiumServices
from test_code.cache.FieldCache import FieldCache
from test_code.cache.FMSCache import FMSCache
from test_code.data.AssetStateDetails import AssetStateDetails
from test_code.services.asset_state_reporting_service.AssetStatesEndpoint import AssetStatesEndpoint
import pendulum
from test_code.services.asset_state_reporting_service.StateTypeEndpoint import StateTypeEndpoint
from time import sleep
from robot.api import logger
from test_code.services.mine_model.LaneEndpoint import LaneEndpoint
from test_code.services.mine_model.MiningBlockEndpoint import MiningBlockEndpoint
from test_code.services.mine_model.StockpileEndpoint import StockpileEndpoint
from test_code.services.mine_model.LocationEndpoint import LocationEndpoint
import copy
from shapely.geometry import Polygon
import geopandas as gpd
from test_code.services.routing_service.RouteEndpoint import RouteEndpoint
from test_code.utilities.ExceptionWithScreenImage  import ExceptionWithScreenImage

class AssetFieldManagement:

    _imperium_services = None
    __fms_cache = FMSCache()
    __field_cache = FieldCache()
    
    @property
    def imperium_services(self):
        if not self._imperium_services:
            self._imperium_services = ImperiumServices()
        return self._imperium_services
    
    def create_asset(self, asset_id: str):
        """
        Create a new asset with the specified id.
        Following services will be started and limited to the list of seeded assets:
            - Redis for field
            - Field sync
            - Field signal
            - Centurion

        Examples:
            | Create Asset | asset_id |
        """
        if asset_id not in MAPS['Hazelmere']['allowed_assets'].keys():
            raise Exception(f"Asset id {asset_id} is not allowed to be created for Hazelmere map")

        BuiltIn().run_keyword('Add Asset Field Config', asset_id)

        # Start redis
        BuiltIn().run_keyword('Start Redis', f'Field_{asset_id}', 'add_new_asset=True')

        # Start asset shadow service
        BuiltIn().run_keyword('Start Imperium Service', f'AssetShadowService_{asset_id}', 'add_new_asset=True')

        # Start asset shadow instruction manager
        BuiltIn().run_keyword('Start Imperium Service', f'AssetShadowInstructionManager_{asset_id}', 'add_new_asset=True')

        # Start asset shadow state manager
        BuiltIn().run_keyword('Start Imperium Service', f'AssetShadowStateManager_{asset_id}', 'add_new_asset=True')

        # Start asset shadow task manager
        BuiltIn().run_keyword('Start Imperium Service', f'AssetShadowTaskManager_{asset_id}', 'add_new_asset=True')

        # Start field signal
        BuiltIn().run_keyword('Start Imperium Service', f'FieldSignal_{asset_id}', 'add_new_asset=True')

        # Start field sync
        BuiltIn().run_keyword('Start Imperium Service', f'FieldSync_{asset_id}', 'add_new_asset=True')

        # Start Centurion
        BuiltIn().run_keyword('Start Imperium Service', f'Centurion_{asset_id}', 'add_new_asset=True')

        BuiltIn().set_suite_variable('${Centurion_' + str(asset_id) + '_port}', self.imperium_services.get_service_port(f'Centurion_{asset_id}'))

    def delete_asset(self, asset_id: str):
        """
        Delete an asset with the specified id.
        Following services will be stopped:
            - Redis for field
            - Field sync
            - Field signal
            - Centurion

        Examples:
            | Delete Asset | asset_id |
        """
        if asset_id not in MAPS['Hazelmere']['allowed_assets'].keys():
            raise Exception(f"Asset id {asset_id} is not allowed to be deleted for Hazelmere map")

        # Stop Centurion
        BuiltIn().run_keyword('Stop Imperium Service', f'Centurion_{asset_id}', 'remove_asset=True')

        # Stop field sync
        BuiltIn().run_keyword('Stop Imperium Service', f'FieldSync_{asset_id}', 'remove_asset=True')

        # Stop field signal
        BuiltIn().run_keyword('Stop Imperium Service', f'FieldSignal_{asset_id}', 'remove_asset=True')

        # Stop asset shadow task manager
        BuiltIn().run_keyword('Stop Imperium Service', f'AssetShadowTaskManager_{asset_id}', 'remove_asset=True')

        # Stop asset shadow state manager
        BuiltIn().run_keyword('Stop Imperium Service', f'AssetShadowStateManager_{asset_id}', 'remove_asset=True')

        # Stop asset shadow instruction manager
        BuiltIn().run_keyword('Stop Imperium Service', f'AssetShadowInstructionManager_{asset_id}', 'remove_asset=True')

        # Stop asset shadow service
        BuiltIn().run_keyword('Stop Imperium Service', f'AssetShadowService_{asset_id}', 'remove_asset=True')

        # Stop redis
        BuiltIn().run_keyword('Stop Redis', f'Field_{asset_id}', 'remove_asset=True')

    def drive_asset_to_another_asset(self, source_asset: str, destination_asset: str=None, duration_in_seconds:float=1.5, reverse:bool=True, use_telemetry:bool=False) ->  None:
        """ Simulate an asset moving from source to the destination, in a straight line.
            The duration of travel is set to 1500ms.

        Returns:
            None:

        Examples:
            |   Drive Asset To Another Asset | DT5401 | EX7109 |
        """

        travel_segments = int(duration_in_seconds/.3)
        pose_source = self.__fms_cache.get_pose_data(source_asset)
        pose_destination = None
        destination_x = None
        destination_y = None
        
        pose_destination = self.__fms_cache.get_pose_data(destination_asset)
        destination_x = int(pose_destination[0]['X']) - 100  #Go beside asset
        destination_y = int(pose_destination[0]['Y']) - 100

        source_x = int(pose_source[0]['X'])
        source_y = int(pose_source[0]['Y'])

        self.__move_asset(source_asset, source_x, source_y, destination_x, destination_y, travel_segments, reverse=reverse, use_telemetry=use_telemetry)


    def drive_asset_to_location_boundary(self, source_asset: str, destination_mining_block:str=None, destination_stockpile:str=None, destination_location: str = None, cardinal_location:str='C', duration_in_seconds:float=1.5, use_telemetry:bool=False, offset_x:int=0, offset_y=0, report_payload_tonnes:int=0, reverse:bool=False, drive_direct=False) ->  None:
        """ Simulate an asset moving from source to the destination, in a straight line.
            The duration of travel is set to 1500ms.
            Cardinal Locations:   C = Centre
                                  N = North
                                  S = South
                                  W = West
                                  E = East
                                  NW
                                  NE
                                  SW
                                  SE

        Returns:
            None:

        Examples:
            |   Drive Asset To Location Boundary | DT5401 | destination_mining_block=HAZ_001_002 |
        """

        travel_segments = int(duration_in_seconds/.3)
        pose_source = self.__fms_cache.get_pose_data(source_asset)

        source_x = int(pose_source[0]['X'])
        source_y = int(pose_source[0]['Y'])

        pose_destination = None
        destination_x = None
        destination_y = None
        
        all_coordinates = None

        if destination_location is not None:
            location_details = LocationEndpoint().get_location_by_name(destination_location)
            all_coordinates = location_details.boundary["coordinates"][0]

        if destination_mining_block is not None:
            miningBlockDetails = MiningBlockEndpoint().get_mining_block(name=destination_mining_block)
            all_coordinates = miningBlockDetails.boundary['coordinates'][0]

        if destination_stockpile is not None:
            stockpileDetails = StockpileEndpoint().get_stockpile(name=destination_stockpile)
            all_coordinates = stockpileDetails.shape['coordinates'][0]

        x = 0
        y = 0
        lon_point_list = []
        lat_point_list = []

        # get furthest point from asset
        for coordinate in all_coordinates:
            x = x + int(coordinate[0])
            y = y + int(coordinate[1])
            lon_point_list.append(coordinate[0])
            lat_point_list.append(coordinate[1])

        polygon_geom = Polygon(zip(lon_point_list, lat_point_list))

        logger.info('lon_point_list{}'.format(lon_point_list))
        logger.info('lat_point_list{}'.format(lat_point_list))
        # Returns a tuple with minx, miny, maxx, maxy of bounding box
        b = polygon_geom.bounds
        logger.info('b{}'.format(b))
        # Find the NW corner of bounds (minx, maxy)
        nw_corner = (b[0], b[3])
        ne_corner = (b[2], b[3])
        ne_corner = (b[0], b[1])
        ne_corner = (b[2], b[1])

        logger.info('nw{}'.format(nw_corner))
        logger.info('ne{}'.format(ne_corner))

        if cardinal_location == 'NE':
            destination_x = b[2]-500
            destination_y = b[3]-2500
        elif cardinal_location == 'NW':
            destination_x = b[0]+1500
            destination_y = b[3]-700
        elif cardinal_location == 'SE':
            destination_x = b[2]-500
            destination_y = int(y/len(all_coordinates))-1000
        elif cardinal_location == 'SW':
            destination_x = b[0]+1500
            destination_y = int(y/len(all_coordinates))-1000
        elif cardinal_location == 'W':
            destination_x = b[0]+1500
            destination_y = int(y/len(all_coordinates))-1000
        elif cardinal_location == 'E':
            destination_x = b[2]-500
            destination_y = int(y/len(all_coordinates))-1000
        elif cardinal_location == 'S':
            destination_x = int(x/len(all_coordinates))
            destination_y = b[1] #-1000
        elif cardinal_location == 'N':
            destination_x = int(x/len(all_coordinates))
            destination_y = b[3]
        else:
            destination_x = int(x/len(all_coordinates))
            destination_y = int(y/len(all_coordinates))

        destination_x = destination_x + offset_x
        destination_y = destination_y + offset_y
        logger.info('destination_x_dir{}'.format(destination_x))
        logger.info('destination_y_dir{}'.format(destination_y))
        if cardinal_location == 'C' or drive_direct:
            self.__move_asset(source_asset, source_x, source_y, destination_x, destination_y, travel_segments, use_telemetry=use_telemetry, report_tonnes=report_payload_tonnes, reverse=reverse)
        else:
            self.__move_asset_along_road(source_asset, source_x, source_y, destination_x, destination_y, travel_segments, use_telemetry=use_telemetry, report_tonnes=report_payload_tonnes, reverse=reverse)

    def __move_asset_along_road(self, asset_identifier:str, source_x:int, source_y:int, destination_x:int, destination_y:int, travel_segments:int, reverse:bool=False, use_telemetry:bool=False, report_tonnes:int=0):
        
        final_destination_x = copy.deepcopy(destination_x)
        final_destination_y = copy.deepcopy(destination_y)
        route = RouteEndpoint().get_route(source_x, source_y, destination_x, destination_y)
        lanes = LaneEndpoint().get_lanes()

        travel_segments = int(travel_segments/(len(route['route'])+1))
        if travel_segments <3:
            travel_segments = 3

        for route in route['route']:
            
            route_coordinates = next(filter(lambda l: (l.onboardId == int(route)), lanes.lanes))
            
            all_coordinates = route_coordinates.laneBoundary.coordinates[0]
            x = 0
            y = 0
            for coordinate in all_coordinates:
                x = x + int(coordinate[0])
                y = y + int(coordinate[1])
            destination_x_lane = int(x/len(all_coordinates))
            destination_y_lane = int(y/len(all_coordinates))

            self.__move_asset(asset_identifier=asset_identifier, source_x=source_x, source_y=source_y, destination_x=destination_x_lane, destination_y=destination_y_lane, travel_segments=travel_segments, reverse=reverse, use_telemetry=use_telemetry, report_tonnes=report_tonnes)
            source_x = copy.deepcopy(destination_x_lane)
            source_y = copy.deepcopy(destination_y_lane)
        self.__move_asset(asset_identifier=asset_identifier, source_x=source_x, source_y=source_y, destination_x=final_destination_x, destination_y=final_destination_y, travel_segments=travel_segments, reverse=reverse, use_telemetry=use_telemetry, report_tonnes=report_tonnes+3)
            
            
    def __move_asset(self, asset_identifier:str, source_x:int, source_y:int, destination_x:int, destination_y:int, travel_segments:int, reverse:bool=False, use_telemetry:bool=False, report_tonnes:int=0):
        
        x_diff = abs(destination_x - source_x)
        y_diff = abs(destination_y - source_y)
        x_travel_segment = x_diff/travel_segments
        y_travel_segment = y_diff/travel_segments
        x_travel_segment = math.ceil(x_travel_segment)
        y_travel_segment = math.ceil(y_travel_segment)

        logger.info('source_x{}'.format(source_x))
        logger.info('source_y{}'.format(source_y))
        segment_pose_x = source_x
        segment_pose_y = source_y
        if destination_x - source_x > 0 and destination_y - source_y > 0:
            yaw_direction = math.atan2(destination_y - source_y, destination_x-source_x)
            if reverse:
                yaw_direction = yaw_direction+3.14
        elif destination_x - source_x < 0 and destination_y - source_y < 0:
            yaw_direction = math.atan2(source_y - destination_y , source_x - destination_x) + 3.14159
            if reverse:
                if yaw_direction > 3.14:
                    yaw_direction = yaw_direction -3.14
                else:
                    yaw_direction = yaw_direction + 1
        elif destination_x - source_x > 0 and destination_y - source_y < 0:
            yaw_direction = math.atan2(source_y - destination_y, destination_x-source_x)
            if yaw_direction < 2 and not reverse:
                yaw_direction = 6 - yaw_direction
            if reverse:
                if yaw_direction > 2:
                    yaw_direction = yaw_direction-(3.14/2)
                elif yaw_direction < 1 and yaw_direction > .5:
                    yaw_direction = yaw_direction + 1.6
                elif yaw_direction < 2 and yaw_direction > 1.5:
                    yaw_direction = yaw_direction - .5
                elif yaw_direction < 1.2 and yaw_direction > 1:
                    yaw_direction = yaw_direction + .8  # for NW -> S for 1.18 yaw
                elif yaw_direction < .5 and yaw_direction > .1:
                    yaw_direction = yaw_direction + 2.1
                elif yaw_direction < .1:
                    yaw_direction = yaw_direction + 2.8
        elif destination_x - source_x < 0 and destination_y - source_y > 0:
            yaw_direction = math.atan2(destination_y - source_y, source_x - destination_x)
            if yaw_direction < 1  and yaw_direction >0.05 and not reverse:
                yaw_direction = yaw_direction+(3.14/2)
            elif yaw_direction < 0.05 and not reverse:
                yaw_direction = yaw_direction+3.14
            if reverse:
                if yaw_direction < .5:
                    yaw_direction = yaw_direction + 6.1
                elif yaw_direction > .5 and yaw_direction <1:
                    yaw_direction = yaw_direction + 5.1  # from 4.1 to 5.1 for SE -> N
                else:
                    yaw_direction = yaw_direction+3.14
        elif source_x == destination_x and source_y - destination_y  > 0:
            yaw_direction = math.atan2(source_y - destination_y, destination_x-source_x)
            if reverse:
                yaw_direction = yaw_direction
        elif source_x == destination_x and source_y - destination_y  < 0:
            yaw_direction = math.atan2(destination_y - source_y, destination_x-source_x)
            if reverse:
                yaw_direction = yaw_direction+3.14
        elif source_x - destination_x < 0 and source_y == destination_y:
            yaw_direction = math.atan2(source_y - destination_y, destination_x-source_x)
            if reverse:
                yaw_direction = yaw_direction+3.14
        elif source_x - destination_x > 0 and source_y == destination_y:
            yaw_direction = math.atan2(destination_y - source_y, destination_x-source_x)
            if reverse:
                yaw_direction = yaw_direction+3.14
        else:
            yaw_direction = 0
            if reverse:
                yaw_direction = 3.14

        ground_speed = None

        if use_telemetry:
            current_speed = 0
            ground_speed = self.__fms_cache.get_telemetry(asset_identifier, 'groundSpeed', skip_timeout=True)

            if ground_speed is not None:
                current_speed = int(json.loads(ground_speed).get("TelemetryReading"))

        for segment in range(travel_segments):
            if (destination_x > source_x):
                segment_pose_x = segment_pose_x + x_travel_segment
            else:
                segment_pose_x = segment_pose_x - x_travel_segment

            if (destination_y > source_y):
                segment_pose_y = segment_pose_y + y_travel_segment
            else:
                segment_pose_y = segment_pose_y - y_travel_segment

            time.sleep(0.3)
            self.__field_cache.set_asset_position(asset_identifier=asset_identifier, x=segment_pose_x, y=segment_pose_y, z=0, yaw=yaw_direction)
            if use_telemetry:
                if reverse:
                    self.__field_cache.set_telemetry_field(asset_identifier, 'transmissionGear', '-1')
                else:
                    self.__field_cache.set_telemetry_field(asset_identifier, 'transmissionGear', '1')
                self.__field_cache.set_telemetry_field(asset_identifier, 'groundSpeed', str(current_speed))
                self.__field_cache.set_telemetry_field(asset_identifier, 'trayAngle', '0.3799999952316284')

            if report_tonnes > 0:
                self.__field_cache.set_telemetry_field(asset_identifier, 'sensorPayload', report_tonnes)

    def wait_for_asset_state(self, assetId: str, state:str, wait_time_seconds:int=60):
        current_state = None
        all_state_types = StateTypeEndpoint().get_all_state_types()
        entry = list(map(lambda a: a.stateTypeId, filter(lambda x: x.name == state, all_state_types)))

        if len(entry) == 0:
            entry.append(state)

        logger.info('looking for: {} with code of {}'.format(state, entry))

        timeout = 0
        while current_state not in entry and timeout < wait_time_seconds/5:
            current_shift = (pendulum.now().format('YYYYMMDD') if pendulum.now().hour >=6 else pendulum.now().subtract(days=1).format('YYYYMMDD')) + ('D' if pendulum.now().hour >=6 and pendulum.now().hour <18 else 'N')
            logger.info('current shift: {}'.format(current_shift))
            try:
                asset_states = AssetStatesEndpoint().get_asset_states(assetId, current_shift)
                sorted_list = sorted(asset_states, key=lambda asset_state: asset_state.reportedAt, reverse=True)
                logger.info(sorted_list)
                current_state = sorted_list[0].state
                logger.info('current state: {}'.format(current_state))
            except:
                pass
            timeout = timeout + 1
            sleep(5)

        if current_state not in entry:
            raise ExceptionWithScreenImage('asset has not reached desired state: {}'.format(state))

    def reset_asset_position(self, assetId):
        self.__field_cache.set_asset_position(assetId)

    def set_telemetry_ground_speed(self, assetId: str, speed:int=0, duration:float=3.5):
        """ Set the telemetry ground speed of an asset

        Args:
            assetId (str): the asset identifier

        Examples:
            | Set Telemetry Ground Speed | DT5401 | 50 |
        """
        current_speed = 0
        ground_speed = self.__fms_cache.get_telemetry(assetId, 'groundSpeed', skip_timeout=True)
        logger.info('ground_speed{}'.format(ground_speed))
        if ground_speed is not None:
            current_speed = int(json.loads(ground_speed).get("TelemetryReading"))

        speed_difference = 0
        if current_speed > speed:    
            speed_difference = current_speed - speed
        else:
            speed_difference = speed - current_speed

        occurences = duration/.5
        speed_blocks = speed_difference/5
        logger.info('speed_blocks{}'.format(speed_blocks))
        for x in range(int(occurences)):
            logger.info('current_speed {}'.format(current_speed))  
            new_speed = 0
            if current_speed < speed:
                new_speed = current_speed + speed_blocks
                current_speed = current_speed + speed_blocks
                logger.info('new speed < {}'.format(new_speed))  
            else:
                new_speed = current_speed - speed_blocks
                current_speed = current_speed - speed_blocks
                logger.info('new speed > {}'.format(new_speed))  
            logger.info('setting speed to {}'.format(new_speed))    
            self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', str(int(new_speed)))
            sleep(0.5)
        
        sleep(5)
        logger.info('setting speed to {}'.format(speed))
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', str(int(speed)))
        ground_speed = self.__fms_cache.get_telemetry(assetId, 'groundSpeed')
        logger.info('ground_speed{}'.format(ground_speed))
        
    def set_telemetry_load(self, assetId:str):
        self.__field_cache.set_telemetry_field(assetId, 'sensorPayload', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'sensorPayload', '50')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'sensorPayload', '75')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'sensorPayload', '222')
        sleep(5)

    def set_telemetry_reverse(self, assetId:str):
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '-1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)

    def set_telemetry_non_reverse(self, assetId:str):
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '1')
        sleep(.5)

    def set_telemetry_dump(self, assetId:str):
        self.__field_cache.set_telemetry_field(assetId, 'trayTilt', '0')
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '0.4099999964237213')
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '148')
        self.__field_cache.set_telemetry_field(assetId, 'sensorPayload', '224.90000915527344')
        self.__field_cache.set_telemetry_field(assetId, 'payloadState', '8')
        self.__field_cache.set_telemetry_field(assetId, 'parkBrakeState', '0')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayTilt', '32767')
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '19.350000381469727')
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '64')
        self.__field_cache.set_telemetry_field(assetId, 'sensorPayload', '232.10000610351562')
        self.__field_cache.set_telemetry_field(assetId, 'payloadState', '7')
        self.__field_cache.set_telemetry_field(assetId, 'parkBrakeState', '32767')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '22.43000030517578')
        self.__field_cache.set_telemetry_field(assetId, 'payloadState', '7')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '26.799999237060547')
        self.__field_cache.set_telemetry_field(assetId, 'payloadState', '4')
        self.__field_cache.set_telemetry_field(assetId, 'parkBrakeState', '0')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '31.10999870300293')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '33.84000015258789')
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '129')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '36.64999771118164')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '37.68000030517578')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '38.75')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '42.21999740600586')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '3.2019999027252197')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '46.57999801635742')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '3.2019999027252197')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '50.09000015258789')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '7.2044997215271')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '46.70000076293945')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '35.869998931884766')
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '64')
        self.__field_cache.set_telemetry_field(assetId, 'parkBrakeState', '32767')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '32.13999938964844')
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '64')
        self.__field_cache.set_telemetry_field(assetId, 'parkBrakeState', '32767')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '26.719999313354492')
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '64')
        self.__field_cache.set_telemetry_field(assetId, 'parkBrakeState', '32767')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '8.119999885559082')
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '64')
        self.__field_cache.set_telemetry_field(assetId, 'parkBrakeState', '32767')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '1.649999976158142')
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '64')
        self.__field_cache.set_telemetry_field(assetId, 'parkBrakeState', '32767')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(.5)
        self.__field_cache.set_telemetry_field(assetId, 'trayAngle', '0.3799999952316284')
        self.__field_cache.set_telemetry_field(assetId, 'transmissionGear', '64')
        self.__field_cache.set_telemetry_field(assetId, 'sensorPayload', '0')
        self.__field_cache.set_telemetry_field(assetId, 'payloadState', '5')
        self.__field_cache.set_telemetry_field(assetId, 'parkBrakeState', '32767')
        self.__field_cache.set_telemetry_field(assetId, 'groundSpeed', '0')
        sleep(5)
