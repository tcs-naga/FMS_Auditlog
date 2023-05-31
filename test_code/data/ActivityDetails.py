__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import dataclasses
import pendulum
@dataclass
class ActivityDetails:
    activity: str = None
    activity_friendly_name:str = None
    assetId: str = None
    timestamp: str = pendulum.now('UTC').to_iso8601_string()
    comment: str = None
    commentUserId: str = None
