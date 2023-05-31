__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
from typing import Dict
from typing import List

@dataclass
class LaneBoundary:
    type:str
    coordinates: List

@dataclass
class LaneDetails:
    id: str
    name: str
    speedLimitMetersPerSecond: float
    laneType: int
    onboardId: int
    enabled: bool
    laneBoundary: LaneBoundary

@dataclass
class Lanes:
    lanes: List[LaneDetails]