
import pendulum
from datetime import datetime

class DateTimeFormatter():

    def convert_api_date_to_display_format(self, date:str) -> str:
        """ converts a date received via API to the display format

        Args:
            date (str): date

        Returns:
            str: converted date
        """
        perth_timezone = pendulum.timezone('Australia/Perth')
        perth_datetime = perth_timezone.convert(pendulum.parse(date))
        return perth_datetime.format('DD/MM/YYYY, h:mm:ss A').lower()

    def convert_time_to_twelve_hour(self, time_value) -> str:
        """Convert 24 hour time to 12 hour time format
           e.g:- 13:44 to 1:44

        Args:
            time_value (str): time in 24 hour format

        Returns:
            str: time in 12 hour format

        Examples:

            | Convert Time To Twelve Hour | 13:44 |
        """
        time_value_12_hour = datetime.strptime(time_value, "%H:%M").strftime("%I:%M %p")
        time_value_12_hour = time_value_12_hour[1:-3]
        return time_value_12_hour

    def convert_datetime_twelve_to_twentyfour_hour(self, date_time_value: str) -> str:
        """Convert 12 hour date time to 24 hour date time format
           e.g:- 12/03/2023, 6:00:00 pm to 12/03/2023, 18:00:00

        Args:
            date_time_value (str): date time in 12 hour format

        Returns:
            str: date time in 24 hour format

        Examples:

            | Convert Datetime Twelve To Twentyfour Hour | 12/03/2023, 6:00:00 pm |
        """
        date_time_value_split = date_time_value.split(", ")
        date_value = date_time_value_split[0]
        time_value = date_time_value_split[1]
        time_split = time_value.split(" ")
        time_values = time_split[0]
        am_pm_indicator = time_split[1]        
        time_values_split = time_values.split(":")        
        if am_pm_indicator == 'pm':
            hour_value_in_24hr = int(time_values_split[0]) + 12
        else:
            hour_value_in_24hr = int(time_values_split[0])
        time_value_in_24hr = str(hour_value_in_24hr) + ':' + time_values_split[1] + ':' + time_values_split[2]
        return date_value + ", " + time_value_in_24hr
