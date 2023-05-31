__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import pendulum
from pendulum import DateTime
from dataclasses import dataclass

@dataclass
class LicenceDetails:
    issue_date: DateTime = pendulum.now().subtract(days=-1)
    expiry_date: DateTime = pendulum.now().add(days=2)
    asset_class: str = 'Dump Truck - Caterpillar CAT 793F'
    licence_type: str = 'Qualified'

    def __init__(self):
        pass

    def __init__(self, asset_class: str = 'Dump Truck - Caterpillar CAT 793F', licence_type: str = 'Qualified', issue_days_from_today: int = -1, expiry_days_from_today: int = 2):
        self.issue_date = pendulum.now().add(days=issue_days_from_today)
        self.expiry_date = pendulum.now().add(days=expiry_days_from_today)
        self.asset_class = asset_class
        self.licence_type = licence_type

    def get_issue_date_formatted(self):
        return self.issue_date.format('DD/MM/YYYY')

    def get_expiry_date_formatted(self):
        return self.expiry_date.format('DD/MM/YYYY')