__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass

from test_code.data.MiningBlockDetails import MiningBlockDetails

@dataclass
class MaterialDestinationDetails:
    material_source: MiningBlockDetails = MiningBlockDetails()
    primary_destination: str = 'HAZ01_RP02_0001'
    secondary_destination: str = 'HAZ01_RP02_0002'

    def __init__(self):
        pass

    def __init__(self, material_source_name: str = 'HAZ01_01_0500_002_0503_BS02', material_source_block:str = 'BS02', material_source_material:str = 'LA', primary_destination: str = 'HAZ01_RP02_0001', secondary_destination: str = 'HAZ01_RP02_0002'):
        self.material_source = MiningBlockDetails(fullName=material_source_name, name=material_source_block, materialCode=material_source_material)
        self.primary_destination = primary_destination

        self.secondary_destination = secondary_destination

    def set_secondary_destination(self, secondary_destination: str):
        self.secondary_destination = secondary_destination

    def set_primary_destination(self, primary_destination: str):
        self.primary_destination = primary_destination
