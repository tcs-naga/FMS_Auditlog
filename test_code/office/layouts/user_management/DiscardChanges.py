__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.office.BasePage import BasePage

class DiscardChanges(BasePage):

    __cancel_button_Text = 'CANCEL'
    __discard_button_Text = 'DISCARD'

    def click_cancel(self):
        """ clicks cancel button

        Examples:
            |   Click Cancel   |
        """
        self.click_button_by_text(self.__cancel_button_Text)

    def click_discard(self):
        """ clicks discard button

        Examples:
            |   Click Discard   |
        """
        self.click_button_by_text(self.__discard_button_Text)