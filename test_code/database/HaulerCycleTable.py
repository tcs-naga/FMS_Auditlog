__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.data.HaulerCycleDetails import HaulerCycleDetails
from test_code.database.Database import Database
from robot.api import logger
from time import sleep

class HaulerCycleTable(Database):

    def create_cycle(self, cycle: HaulerCycleDetails):
        """ creates a cycle directly in the database

        Args:
            cycle (HaulerCycleDetails): the cycle

        Examples:
            | Create Cycle | cycle=${hauler_cycle_object} |
        """
        dict = cycle.__dict__
        
        columns = ''
        values = ''
        for key in dict:
            if dict[key] is not None:
                if columns == '':
                    columns = str(key)
                    values = str(dict[key]) if isinstance(dict[key], int) or isinstance(dict[key], float) else '\'{}\''.format(dict[key])
                else:
                    columns = columns + ', {}'.format(key)
                    values = values + ', ' + (str(dict[key]) if isinstance(dict[key], int) or isinstance(dict[key], float) else '\'{}\''.format(dict[key]))
        sql_statement = 'INSERT INTO AssetStateReportingService.dbo.HaulerCycles (' + columns + ') VALUES (' + values + ');'
        logger.info(sql_statement)
        self.execute_command(sql_statement)
        # TODO: Need to find a better solution for the following.
        # It takes few seconds for the FMS UI to update with the inserted Tonnes data.
        sleep(2)

    def delete_all_hauler_cycles(self):
        """ Delete all data from from AssetStateReportingService.dbo.HaulerCycles table to
            bring the table to a clean state. This eliminates any residue records from previous broken tests
            interfearing with the current test case.

        Args:
            None

        Examples:
            | Delete All Hauler Cycles |
        """
        sql_reported_tonnes = 'DELETE from AssetStateReportingService.dbo.HaulerCycles;'
        logger.info(sql_reported_tonnes)
        self.execute_command(sql_reported_tonnes)
