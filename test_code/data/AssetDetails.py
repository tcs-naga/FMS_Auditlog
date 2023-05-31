__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import dataclasses
from test_code.data.AssetClassModelDetails import AssetClassModelDetails

@dataclass
class AssetDetails:
    assetModelModel: AssetClassModelDetails = None
    assetDelayModel: str = None
    assetIdentifier: str = None
    equipmentType: int = 0
    id: str = None
    ipAddress: str = None
    isArchived: bool = False
    manningOperator: str = None
    manningOperatorFirstName: str = None
    manningOperatorSurname: str = None
    assetBehaviours: list = dataclasses.field(default_factory=list)
    healthEvents: str = None

    def get_asset_behaviour_value(self, type, asset_details) -> str:
        if asset_details is None:
            return next(map(lambda a: a.value, filter(lambda a: a.typeName==type, self.assetBehaviours)))
        else:
            return next(map(lambda a: a.value, filter(lambda a: a.typeName==type, asset_details.assetBehaviours)))

    