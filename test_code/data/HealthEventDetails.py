__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import pendulum


@dataclass
class HealthEventDetails:
    assetId: str = None
    level: str = None
    eventType: str = None
    operator: str = None

    def get_asset(self):
        return self.assetId

    def get_level(self):
        return self.level

    def get_event_type(self):
        return self.eventType

    def get_operator(self):
        return self.operator
