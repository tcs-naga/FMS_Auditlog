__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
from typing import Dict

@dataclass
class StockpileDetails:
    id: str
    name: str
    grade: str
    materialCode: str
    capacityTon: int
    isSource: bool
    isSink: bool
    isOpen: bool
    isArchived: bool
    isArchivedUpdatedOn: str
    shape: Dict[str, object]
