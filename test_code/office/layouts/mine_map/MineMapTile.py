__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.office.layouts.BaseLayout import BaseLayout
from selenium.webdriver.common.by import By

class MineMapTile(BaseLayout):

    __panel_title = 'Mine Map'

    def get_panel(self):
        return self.get_layout(self.__panel_title)

    def capture_image_of_tile(self):
        """ captures an image of the asset details tile

        Examples
            | Capture Image Of Tile |
        """
        self.capture_image(self.get_panel(), self.__panel_title.replace(" ", "_") + 'Tile')

    def capture_image_of_tile_and_compare(self):
        """
        Captures an image of tile and compare

        Examples
            | Capture Image Of Tile And Compare |
        """
        self.capture_image_and_compare(self.get_panel(), self.__panel_title.replace(" ", "_") + 'Tile')