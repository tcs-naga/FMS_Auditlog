__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

class DataTypeConverters():

    def convert_list_to_lower(self, string_list: list):
        for i in range(len(string_list)):
            string_list[i] = string_list[i].lower()
        return string_list
