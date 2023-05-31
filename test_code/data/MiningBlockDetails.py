__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import dataclasses

@dataclass
class MiningBlockDetails:
    id: str = None
    pit: str = None
    fullName: str = 'HAZ01_01_0500_002_0503_BS02'
    subdivision: str = None
    stage: str = None
    bench: str = None
    blast: str = None
    flitch: str = None
    name: str = 'BS02'
    boundary: list = dataclasses.field(default_factory=list)
    materialCode: str = 'LA'
    originalMassTonnes:str = None
    originalVolumeMetersCubed:str = None
    isOpen: bool = False
    isArchived: bool = False
    grade: list = dataclasses.field(default_factory=list)
    