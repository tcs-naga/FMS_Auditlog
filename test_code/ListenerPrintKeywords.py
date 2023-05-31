__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

"""
Listener to add hooks in start/end of suite/test.
"""

import os
import traceback


from robot.model import Body, BodyItem, If, For, Keyword, Message, TestCase
from robot.running.model import UserKeyword
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from test_code.Environment import Environment


class ListenerPrintKeywords(object):
    """
    Global scope library listener for robot test.
    """

    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self) -> None:
        self.suite_arg_names = {}
        self._started_keywords = 0
        self._running_test = False
        self.test_vars_local = {}
        self.last_attrs = None
        self.failed_tests = []

    def start_suite(self,name, attrs) -> None:
        self._running_test = True
        self.test_vars = BuiltIn().get_variables()

    def start_test(self, name, attrs) -> None:
        self.test_vars = BuiltIn().get_variables()
        self._running_test = True

    def end_test(self, name, attrs) -> None:
        self._running_test = False
        if attrs["status"] == "FAIL":
            self.failed_tests.append(attrs["longname"])

    def print_keyword_with_values(self, attrs) -> None:
        assigned_vars = ""
        # Get to actual keyword without any lib names from front of name 
        kword = attrs["kwname"]
        if "assign" in attrs.keys() and attrs["assign"] != []:
            assigned_vars = "{} = ".format(attrs["assign"])
        for k in self.test_vars.keys():
            search_k = k.replace("@", "$")
            if search_k in kword:
                kword = kword.replace(search_k, str(self.test_vars[k]))
        args_value = ""
        if attrs["args"] != []:
            args_value = []
            for arg in attrs["args"]:
                arg_value = arg
                for k in self.test_vars.keys():
                    search_k = k.replace("@", "$")
                    if search_k in arg:
                        arg_value = arg.replace(search_k, str(self.test_vars[k]))
                        break
                args_value.append(arg_value)
        logger.console(" {}{} {}".format(assigned_vars, kword, args_value))

    def start_keyword(self, name, attrs) -> None:
        # As Wait Until Keyword Succeeds is at the start of a wait it makes
        # more sense to print the keyword at the start rather than at the end
        if not self._started_keywords and self._running_test and self.last_attrs != attrs:
            self.print_keyword_with_values(attrs)
            self.last_attrs = attrs
            self._started_keywords += 1

    def end_keyword(self, name, attrs) -> None:
        if self._started_keywords:
            self._started_keywords -= 1

    def close(self) -> None:
        if self.failed_tests:
            logger.console("\nFailed tests: {}".format(self.failed_tests))
