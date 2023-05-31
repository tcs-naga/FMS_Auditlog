__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.office.layouts.asset_details.DelayFormDialog import DelayFormDialog

class EditDelayDialog(DelayFormDialog):

    def get_dialog_title(self):
        return 'Edit Delay'