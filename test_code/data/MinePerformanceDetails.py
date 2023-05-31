__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import dataclasses

@dataclass
class MinePerformanceDetails:
    destinations: list = dataclasses.field(default_factory=list)
    haulers: list = dataclasses.field(default_factory=list)
    loaders: list = dataclasses.field(default_factory=list)
    metrics: list = dataclasses.field(default_factory=list)
    sourceLocations: list = dataclasses.field(default_factory=list)