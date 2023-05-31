__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json
from test_code.services.mine_model.MineModelService import MineModelService
from test_code.data.MiningBlockDetails import MiningBlockDetails
from robot.api import logger

class MiningBlockEndpoint(MineModelService):

    __endpoint = '/MiningBlock'
        
    def get_mining_block(self, id:str = None, name:str=None) -> MiningBlockDetails:
        """ Get Mining Block based on id or name

        Args:
            id (str, optional): id of the mining block. Defaults to None.
            name (str, optional): name of the mining block. Defaults to None.

        Raises:
            Exception: invalid parameters
            Exception: failed response

        Returns:
            MiningBlockDetails: the mining block details
            
        Examples:
            | Get Mining Block | id=454524 |
            | Get Mining Block | name=HAZ01_WS01 |
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
            raise Exception('Failed to get mining block ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)
		
        mining_block_details_json = json.loads(response.text)
        mining_block_details = MiningBlockDetails(** mining_block_details_json)
        logger.info( mining_block_details)
        return  mining_block_details

    def archive_mining_block(self, id:str):
        """ archive a mining block

        Args:
            id (str): the block id

        Raises:
            Exception: failed response
        
        Examples:
            | Archive Mining Block | id=123336-35345-345123123 |
        """
        response = None

        response = self.patch(self.__endpoint + '/'+ id + '/archive', self.get_headers())

        if response.status_code != 200:
            raise Exception('Failed to archive mining block ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)

    def unarchive_mining_block(self, id:str):
        """ unarchive a mining block

        Args:
            id (str): the block id

        Raises:
            Exception: failed response
            
        Examples:
            | Unarchive Mining Block | id=123336-35345-345123123 |
        """
        response = None

        response = self.patch(self.__endpoint + '/'+ id + '/unarchive', self.get_headers())

        if response.status_code != 200:
            raise Exception('Failed to unarchive mining block ' + id + ': '+ str(response.status_code) +  ' -> ' +response.text)