__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.database.Database import Database
from robot.api import logger

class AssetTimeLinesTable(Database):

    def get_all_timelines(self):
        """ get all the timelines in the asset timelines table

        Examples:
            | Get All Timelines |
        """

        sql_statement = 'Select AssetIdentifier, TimelineId, TimelineState From AssetStateReportingService.dbo.AssetTimeLines'
        result = self.query(sql_statement)

        return result