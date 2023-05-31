__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
from test_code.services.routing_service.RoutingService import RoutingService
from test_code.data.StockpileDetails import StockpileDetails
from robot.api import logger

class RouteEndpoint(RoutingService):

    __endpoint = '/Route'

    def get_route(self, start_x:str, start_y:str, end_x:str, end_y:str):
        data = {}
        data_start = {}
        data_start['type'] = 'Point'
        data_start['coordinates'] = [ start_x, start_y]
        data['start'] = data_start
        data_end = {}
        data_end['type'] = 'Point'
        data_end['coordinates'] = [ end_x, end_y]
        data['end'] = data_end
        json_data = json.dumps(data)
        response = self.post(self.__endpoint + '/CalculateRouteFromPoints', self.get_headers(), json_data)
        return response.json()