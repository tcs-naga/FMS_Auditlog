
__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import json

from typing import Dict
from deepdiff import DeepDiff
from robot.libraries.BuiltIn import BuiltIn

class CompareDictionary():

    def compare_json(self, expected: str, actual: str, sort_key: str='id', ignore_fields=[]):
        """
        Sorts two lists of dictionaries using the given item/key, and then compare them.

        Examples:
        | Compare Json | expected_response_text |actual_response_text | List of fields to ignore in comparison |
        """

        actual = actual.lower().replace("\'", "\"").encode('UTF-8')
        expected = expected.lower().replace("\'", "\"").encode('UTF-8')
        expected = expected.lower()
        expected_items = json.loads(expected)
        expected_items = json.dumps(expected_items, sort_keys=sort_key)
        expected_items = json.loads(expected_items)
        actual_items = json.loads(actual)
        actual_items = json.dumps(actual_items, sort_keys=sort_key)
        actual_items = json.loads(actual_items)

        if len(actual_items) != len(expected_items):
            raise Exception(f"Different values, Actual: {actual_items}, Expected: {expected_items}")

        # Remove fields from the dict which doesn't need compare.
        if ignore_fields:
            for ignore_field in ignore_fields:
                expected_items = [{key : val for key, val in expected_item.items() if key != ignore_field} for expected_item in expected_items]
                actual_items = [{key : val for key, val in actual_item.items() if key != ignore_field} for actual_item in actual_items]

        diff = DeepDiff(expected_items, actual_items)

        if (diff):
            raise Exception(f"Diff {diff}")