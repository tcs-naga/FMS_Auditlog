__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import dataclasses
from robot.api import logger
from test_code.data.DelayCategoryDetails import DelayCategoryDetails

@dataclass
class DelayTypeDetails:
    category: DelayCategoryDetails = None
    durationInSeconds: int = None
    fmsFieldEnabled: bool = None
    friendlyId: str = None
    id: str = None
    name: str = None
    enabledAssetClassTypes: list = dataclasses.field(default_factory=list)
    fieldDisabledAssetClassTypes: list = dataclasses.field(default_factory=list)
    
    def get_list_of_delay_categories_for_asset_class(self, asset_class:int, list_of_delay_types: list, for_field: bool=False) -> list:
        """ given a list of delay types a filter is applied to get delay categories associated to a particular asset class

        Args:
            asset_class (int): the asset class to filter on
            list_of_delay_types (list): the list of delays
            for_field (bool, optional): true if its a filter for Field otherwise false. Defaults to False.

        Returns:
            list: list of delay categories
            
        Examples:
            | Get List Of Delay Categories For Asset Class | asset_class=3 | list_of_delay_types=${activities} |
            | Get List Of Delay Categories For Asset Class | asset_class=3 | list_of_delay_types=${activities} | for_field=True |
        """
        if for_field:
            return list(set(map(lambda y: y.category.name, filter(lambda x: asset_class in x.enabledAssetClassTypes and x.fmsFieldEnabled and asset_class not in x.fieldDisabledAssetClassTypes, list_of_delay_types))))
        else:
            return list(set(map(lambda y: y.category.name, filter(lambda x: asset_class in x.enabledAssetClassTypes , list_of_delay_types))))
        
    def get_list_of_delay_types_for_asset_class_and_category(self, asset_class:int, list_of_delay_types: list, delay_category:str, for_field: bool=False):
        """ given a list of delay types and category a filter is applied to get delay types associated to a particular asset class

        Args:
            asset_class (int): the asset class to filter on
            list_of_delay_types (list): the list of delays
            delay_category (str): the delay category
            for_field (bool, optional): true if its a filter for Field otherwise false. Defaults to False.

        Returns:
            list: list of delay types
            
        Examples:
            | Get List Of Delay Types For Asset Class And Category | asset_class=3 | list_of_delay_types=${activities} | delay_category=Operating Standby |
            | Get List Of Delay Types For Asset Class And Category | asset_class=3 | list_of_delay_types=${activities} | delay_category=Operating Standby | for_field=True |
        """
        if for_field:
            return list(map(lambda y: y.name.strip() + ('\n' + str(int(int(y.durationInSeconds)/60)) + ' minutes' if y.durationInSeconds is not None else '\nIndefinite'), filter(lambda x: asset_class in x.enabledAssetClassTypes and delay_category==x.category.name and x.fmsFieldEnabled and asset_class not in x.fieldDisabledAssetClassTypes, list_of_delay_types)))
        else:
            filtered_list = list(map(lambda y: y.name.strip() + ('\n' + str(int(int(y.durationInSeconds)/60)) + ' minutes' if y.durationInSeconds is not None else ''), filter(lambda x: asset_class in x.enabledAssetClassTypes and delay_category==x.category.name, list_of_delay_types)))
            logger.debug(filtered_list)
            return filtered_list