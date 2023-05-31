__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
from test_code.data.AssetClassDetails import AssetClassDetails
import dataclasses

@dataclass
class AssetClassModelDetails:
    assetClass: AssetClassDetails = None
    classAbbreviation: str=None
    classType: int=None
    defaultPayloadTonnes: str=None
    heightCentimeters: str=None
    id: str=None
    lengthCentimeters: str=None
    manufacturer: str=None
    maximumSpeedMetersPerSecond: str=None
    model: str=None
    offsetFromCentreXCentimeters: str=None
    offsetFromCentreYCentimeters: str=None
    widthCentimeters: str=None

    def get_asset_class_id_from_list(self, asset_classes:list, class_type:int) -> str:
        return next(filter(lambda a: a.classType==class_type, asset_classes)).id