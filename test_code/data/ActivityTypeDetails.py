__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import dataclasses

@dataclass
class ActivityTypeDetails:
    id: str = None
    friendlyId: str = None
    name: str = None
    fmsFieldEnabled: bool = None
    enabledAssetClassTypes: list = dataclasses.field(default_factory=list)
    fieldDisabledAssetClassTypes: list = dataclasses.field(default_factory=list)
    
    def get_list_of_activity_types_for_asset_class(self, asset_class:int, list_of_activity_types: list, for_field: bool=False) -> list:
        """ given a list of activities a filter is applied to get activities associated to a particular asset class

        Args:
            asset_class (int): the asset class to filter on
            list_of_activity_types (list): the list of activities
            for_field (bool, optional): true if its a filter for Field otherwise false. Defaults to False.

        Returns:
            list: list of activities
            
        Examples:
            | Get List Of Activity Types For Asset Class | asset_class=3 | list_of_activity_types=${activities} |
            | Get List Of Activity Types For Asset Class | asset_class=3 | list_of_activity_types=${activities} | for_field=True |
        """
        if for_field:
            return list(map(lambda y: y.name, filter(lambda x: asset_class in x.enabledAssetClassTypes and x.fmsFieldEnabled  and asset_class not in x.fieldDisabledAssetClassTypes, list_of_activity_types)))
        else:
            return list(map(lambda y: y.name, filter(lambda x: asset_class in x.enabledAssetClassTypes , list_of_activity_types)))
