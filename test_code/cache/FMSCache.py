import json
from test_code.Environment import Environment
from test_code.ImperiumServices import ImperiumServices
import redis
from time import sleep

class FMSCache:
    
    _imperium_services = None
    _environment = None
    __service = 'FMS'
    
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
    
    def __get_redis_connection(self):
        redis_host = self.imperium_services.redis(self.__service)['host']
        redis_port = self.imperium_services.redis(self.__service)['port']

        self.environment.env_log(f'Get connection in redis {redis_host}:{redis_port}', 'trace')
        if self.__service not in self.environment.test_context.redis_connections:
            # Create redis connections, to be used by tests.
            redis_connection = redis.Redis(host=redis_host, port=redis_port, db=0)
            self.environment.test_context.redis_connections[self.__service] = redis_connection
        else:
            redis_connection = self.environment.test_context.redis_connections[self.__service]
        return redis_connection
        
    def get_pose_data(self, asset_identifier: str) -> list:
        """
        Get asset pose data from redis FMS for an asset as a list

        Examples:
        | Get Pose Data From Redis FMS | DT5401 |
        """

        redis_connection = self.__get_redis_connection()
        
        for _ in range(self.environment.time_out - 1):
            sleep(1)
            redis_value = redis_connection.hget(f'AssetPoses', asset_identifier)
            if redis_value != None:
                break

        if not redis_value:
            raise Exception(f'Failed to find the value in redis: {self.__service} after {self.environment.time_out} seconds')

        return json.loads(redis_value).get("Poses")

    def get_telemetry(self, asset_id:str, telemetry_identifier: str, skip_timeout=False) -> str:
        """
        Get telemetry data for redis FMS

        Examples:
        | Get Telemetry | ${DEFAULT_ASSET_ID} |  inputvoltage |
        """
        redis_connection = self.__get_redis_connection()
        

        for _ in range(self.environment.time_out-1):
            sleep(1)
            redis_value = redis_connection.hget(f'Asset:Telemetry:{asset_id}', telemetry_identifier)
            if redis_value != None or skip_timeout==True:
                break
            
        if not redis_value and skip_timeout==False:
            raise Exception(f'Failed to find the value in redis: {self.__service} after {self.environment.time_out} seconds')

        return redis_value