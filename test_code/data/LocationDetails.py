__copyright__ = (
    "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved."
)

import dataclasses


@dataclasses.dataclass
class Boundary:
    type: str = "Polygon"
    coordinates: list = dataclasses.field(
        default_factory=lambda: [[[0, 0, 0], [1, 1, 0], [1, 0, 1], [0, 0, 0]]]
    )


@dataclasses.dataclass
class LocationDetails:
    locationId: str = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    locationType: int = 0
    name: str = "string"
    isSource: bool = True
    isSink: bool = True
    isOpen: bool = True
    boundary: dict = dataclasses.field(
        default_factory=lambda: Boundary().__dict__
    )
