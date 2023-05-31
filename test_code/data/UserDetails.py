__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass

@dataclass
class UserDetails:
    sap_number: str = '111111'
    email: str = 'test_automation@fmgl.com.au'
    first_name: str = 'test'
    last_name: str = 'automation'
    department: str = 'Technology And Autonomy'
    crew: str = 'A'