__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass

@dataclass
class AssetBehaviourTypeDetails:
    id: str = None
    name: str = None
    allowedValues: str = None
    defaultValue: str = None
    relevantAssetClassType: int = None
