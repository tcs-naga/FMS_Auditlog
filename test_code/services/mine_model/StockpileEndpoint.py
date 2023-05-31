__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from dataclasses import dataclass
from test_code.services.mine_model.MineModelService import MineModelService
from test_code.data.StockpileDetails import StockpileDetails
from robot.api import logger

class StockpileEndpoint(MineModelService):

    __endpoint = '/Stockpile'
        
    def get_stockpile(self, id:str = None, name:str=None) -> list:
        """ gets the stockpile using id or name

        Args:
            id (str, optional): id of the stockpile. Defaults to None.
            name (str, optional): name of the stockpile. Defaults to None.

        Raises:
            Exception: paramater errors
            Exception: failed response

        Returns:
            _type_: list
            
        Examples:
            | Get Stockpile | id=1234653 |
            | Get Stockpile | name=HAZ01_RP02 |
        """
        response = None

        if id is not None and name is not None:
            raise Exception('Only provide a name or an id not both')
        elif id is not None:
            response = self.get(self.__endpoint + "/" + id, self.get_headers())
        elif name is not None:
            response = self.get(self.__endpoint + "/" + name, self.get_headers())
        else:
            response = self.get(self.__endpoint, self.get_headers())

        if response.status_code != 200:
            raise Exception('Failed to get stockpile ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)
		
        stockpile_details_json = json.loads(response.text)
        stockpile_details = StockpileDetails(**stockpile_details_json)
        logger.info(stockpile_details)
        return stockpile_details

    def archive_stockpile(self, id:str):
        """ archive a stockpile

        Args:
            id (str): the block id

        Raises:
            Exception: failed response
            
        Examples:
            | Archive Stockpile | id=123336-35345-345123123 |
        """
        response = None

        response = self.patch(self.__endpoint + '/'+ id + '/archive', self.get_headers())

        if response.status_code != 200:
            raise Exception('Failed to archive stockpile ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)

    def unarchive_stockpile(self, id:str):
        """ unarchive a mining block

        Args:
            id (str): the block id

        Raises:
            Exception: failed response
            
        Examples:
            | Unarchive Stockpile | id=123336-35345-345123123 |
        """
        response = None

        response = self.patch(self.__endpoint + '/'+ id + '/unarchive', self.get_headers())

        if response.status_code != 200:
            raise Exception('Failed to unarchive stockpile ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)