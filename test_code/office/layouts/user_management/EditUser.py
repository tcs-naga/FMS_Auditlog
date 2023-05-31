__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.office.layouts.user_management.UserForm import UserForm


class EditUser(UserForm):

    __dialog_title = 'Edit user'

    def get_tile_title(self):
        return self.__dialog_title