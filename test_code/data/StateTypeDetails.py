__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass

@dataclass
class StateTypeDetails:
    stateTypeId: str = None
    name: str = None
    sourceDelayTypeId: str = None
    isDelay: bool = None