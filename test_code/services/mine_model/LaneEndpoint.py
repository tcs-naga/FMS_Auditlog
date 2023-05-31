__copyright__ = (
    "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved."
)

import json
from dataclass_wizard import fromlist, fromdict
from test_code.services.mine_model.MineModelService import MineModelService
from test_code.data.LaneDetails import Lanes
from robot.api import logger


class LaneEndpoint(MineModelService):
    __endpoint = "/Lane"

    def get_lanes(self) -> Lanes:
        pass
        response = self.get(
            self.__endpoint, self.get_headers()
        )

        lane_details = fromdict(Lanes, response.json())

        return lane_details
