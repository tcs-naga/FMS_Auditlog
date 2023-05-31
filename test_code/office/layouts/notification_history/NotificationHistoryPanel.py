__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.office.layouts.BaseLayout import BaseLayout
from selenium.webdriver.common.by import By

class NotificationHistoryPanel(BaseLayout):
    __window_title = 'Notification History'
    __notification_container = './/div[contains(@class, \'unread\') and .//div[@class=\'notification-title\' and text()=\'{}\']]'
    __notification_date = './/div[@class=\'notification-context\']/div[2]'

    def __get_panel(self):
        return self.get_layout(self.__window_title)

    def __get_notification(self, notification_title:str):
        return self.__get_panel().find_element(By.XPATH, self.__notification_container.format(notification_title))

    def  is_notification_displayed(self, notification_title:str) -> bool:
        """returns a status based on whether the notification is displayed

        Args:
            notification_title (str): the title of the notifcation to search

        Returns:
            bool: True if the notification is displayed/False if not

        Examples:
            |   Is Notification Displayed  |    Plan uploaded successfully  |
        """

        try:
            self.__get_notification(notification_title)
            return True
        except:
            return False

    def get_upload_date_and_time(self, notification_title:str) -> str:
        """ gets the date and time information from the notifcation history panel

        Args:
            notification_title (str): the date and time

        Returns:
            str: the date and time of notification

        Examples:
            |   Is Notification Displayed  |    Plan uploaded successfully  |
        """
        return self.__get_notification(notification_title).find_element(By.XPATH, self.__notification_date).get_attribute('aria-label')