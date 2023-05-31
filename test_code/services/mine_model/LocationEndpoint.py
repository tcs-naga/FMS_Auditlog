__copyright__ = (
    "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved."
)

import json
from test_code.services.mine_model.MineModelService import MineModelService
from test_code.data.LocationDetails import LocationDetails
from robot.api import logger


class LocationEndpoint(MineModelService):
    __base_endpoint = "/Location"
    __name_endpoint = "/Location/name/{}"

    def get_location_by_name(self, name: str):
        if name is None:
            raise Exception
        response = self.get(
            self.__name_endpoint.format(name), self.get_headers()
        )
        location_details = LocationDetails(**json.loads(response.text))
        logger.debug(location_details)
        return location_details
