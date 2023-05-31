import pendulum
import json
import redis
import os

from test_code.Const import MAPS
from test_code.Environment import Environment
from test_code.ImperiumServices import ImperiumServices
from robot.api import logger
from test_code.Const import TELEMETRY_DATA, AUTOMATED_TEST_DIR
from time import sleep

class FieldCache:
    
    _imperium_services = None
    _environment = None
    
    @property
    def imperium_services(self):
        if not self._imperium_services:
            self._imperium_services = ImperiumServices()
        return self._imperium_services

    @property
    def environment(self):
        if not self._environment:
            self._environment = Environment()
        return self._environment
    
    def __get_redis_connection(self, asset_identifier):
        for service, port in self.imperium_services.docker_services_port.items():
            if service != 'Field_' + asset_identifier:
                continue
            else:
                # Create redis connections, to be used by tests.
                redis_host = self.imperium_services.redis(service)['host']
                redis_connection = redis.Redis(host=redis_host, port=port, db=0)
                self.environment.test_context.redis_connections[service] = redis_connection
                return redis_connection
            
        raise Exception('Unable to establish redis connection: ' + 'Field_' + asset_identifier)
    
    def set_asset_position(self, asset_identifier: str=None, x: int=0, y: int=0, z: int=0, yaw: float=0) -> None:
        """
        Sets asset position in redis

        Examples:
        | Set Asset Position In Redis |
        """
        redis_connection = self.__get_redis_connection(asset_identifier)

        if x==0:
            x = MAPS['Hazelmere']['allowed_assets'][asset_identifier]['x']
        if y==0:
            y = MAPS['Hazelmere']['allowed_assets'][asset_identifier]['y']
        if z==0:
            z = MAPS['Hazelmere']['allowed_assets'][asset_identifier]['z']
        if yaw==0:
            yaw = MAPS['Hazelmere']['allowed_assets'][asset_identifier]['yaw']

        pose = {
            "Poses":[{
            "Id": "Pose-1",
            "X": str(x),
            "Y": str(y),
            "Z": str(z),
            "Yaw": str(yaw),
            "LastUpdatedTimeUtc": pendulum.now('UTC').isoformat()
        }]}

        logger.info('setting pose{}'.format(pose))
        pose = json.dumps(pose)
        redis_connection.hset('LocalAsset', 'Pose', pose)
        redis_connection.hset("LocalAsset", "Identifier", f'"{asset_identifier}"')

    def set_telemetry_field(self, asset_identifier: str, telemetry_identifier:str, value: str, last_updated_utc: str=None) -> None:
        """
        Set telemetry data in redis for field

        Examples:
        | Set Telemetry Field | DT5401 | InputVoltage | 27.308000564575195 |
        """
        redis_connection = self.__get_redis_connection(asset_identifier)
        telemetry_data = {
            "Identifier": TELEMETRY_DATA[telemetry_identifier]['identifier'],
            "Value": str(value),
            "Description": TELEMETRY_DATA[telemetry_identifier]['description'],
            "TimestampUtc": last_updated_utc if last_updated_utc else pendulum.now('UTC').isoformat()
        }
        logger.info('setting telemetry{}'.format(telemetry_data))
        telemetry_data = json.dumps(telemetry_data)
        score = pendulum.now().int_timestamp
        redis_connection.zadd("LocalAsset:FieldTelemetry", {telemetry_data: score})

    def set_health_event_data(self, asset_identifier: str, file_name: str) -> None:
        """
        Set health_event data in redis for the asset

        Args:
            asset_identifier (str): the asset identifier
            file_name (str): the test data file that contains health event data to upload

        Examples:
        | Set Health Event Data | DT5401 | health_events.json |
        """
        file = open(str(os.path.join(AUTOMATED_TEST_DIR, 'test_data', 'health_events').replace('\\', '/')) + '/' + file_name)
        health_event_data = json.load(file)

        redis_connection = self.__get_redis_connection(asset_identifier)
        for index in range(len(health_event_data)):
            if len(health_event_data[index]) == 1:
                health_event_entry = {
                    "EventIdentifier": health_event_data[index]['EventIdentifier'],
                    "HealthEvents": [],
                    "Timestamp": pendulum.now('UTC').isoformat()
                }
            else:
                health_event_entry = {
                    "EventIdentifier": health_event_data[index]['EventIdentifier'],                 
                    "HealthEvents": [{
                                    "EventIdentifier":health_event_data[index]['EventIdentifier'],
                                    "Timestamp":pendulum.now('UTC').isoformat(),
                                    "EventTypeId":health_event_data[index]['EventTypeId'],
                                    "Level":health_event_data[index]['Level'],
                                    "SourceSystem":health_event_data[index]['SourceSystem'],
                                    "SourceEventIdentifier":health_event_data[index]['SourceEventIdentifier'],
                                    "SourceEventTypeId":health_event_data[index]['SourceEventTypeId']
                                    }],
                    "Timestamp": pendulum.now('UTC').isoformat()
                }
            logger.info('setting health event data {}'.format(health_event_entry))
            health_event_entry = json.dumps(health_event_entry)
            score = pendulum.now().int_timestamp
            redis_connection.zadd("LocalAsset:FieldHealth", {health_event_entry: score})
            sleep(2)
