__copyright__ = (
    "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved."
)

from test_code.office.layouts.task_manager.TaskManagerPanel import (
    TaskManagerPanel,
)
from selenium.webdriver.common.by import By


class CreateCircuitDialog(TaskManagerPanel):
    __cancel_button = ".//button[text() = 'Cancel']"
    __create_button = ".//button[text() = 'Create']"
    __create_button_disabled = ".//button[text() = 'Create' and @disabled]"
    __dialog = ".//div[text() = 'Create Circuit']/../../.."
    __dropdown_items = "//ul[@role = 'listbox']/li[@data-value != '']"
    __dump_destination_dropdown = ".//div[@role = 'button' and @id = 'mui-component-select-dumpDestination']"
    __loading_tool_dropdown = ".//div[@role = 'button' and @id = 'mui-component-select-loadingTool']"
    __number_of_circuits_textfield = ".//input[@name = 'repeats']"
    __reoccurring_checkbox = ".//span[text() = 'Reoccurring']/preceding-sibling::span//input"
    __use_material_destination_plan_checkbox = ".//span[text() = 'Use the material destination plan']/preceding-sibling::span//input"

    def click_cancel(self) -> None:
        """Clicks on the 'Cancel' button in the 'Create Circuit' dialog
        in the Task Manager panel within FMS Office.

        If the 'Cancel' button cannot be located, or if it is not able
        to be clicked, this keyword fails. This keyword never returns
        anything.

        Examples:
        | ${result} = | Click Cancel | # Value of ${result} is always None |
        """
        self.click(
            self._get_dialog().find_element(By.XPATH, self.__cancel_button)
        )

    def click_create(self) -> None:
        """Clicks on the 'Create' button in the 'Create Circuit' dialog
        in the Task Manager panel within FMS Office.

        If the 'Create' button cannot be located, or if it is not able
        to be clicked, this keyword fails. This keyword never returns
        anything.

        Examples:
        | ${result} = | Click Create | # Value of ${result} is always None |

        See also `Is Create Button Disabled`.
        """
        self.click(
            self._get_dialog().find_element(By.XPATH, self.__create_button)
        )

    def get_dump_destination_list(self) -> list:
        """Returns the list of dump destination items displayed in the
        'Dump Destination' dropdown menu in the 'Create Circuit' dialog
        in the Task Manager panel within FMS Office.

        This keyword returns an ordered list of dump destination items
        in the order by which they are displayed.

        If the list of dump destination items or the 'Dump Destination'
        dropdown menu cannot be located, this keyword fails.

        Returns:
            list: A list of dump destination items.

        Examples:
        | @{result} = | Get Dump Destination List |

        See also `Set Dump Destination`, `Is Dump Destination Set`.
        """
        self.click(
            self._get_dialog().find_element(
                By.XPATH, self.__dump_destination_dropdown
            )
        )
        items = [
            i.text
            for i in self._get_dialog().find_elements(
                By.XPATH, self.__dropdown_items
            )
        ]
        return items

    def get_loading_tool_list(self) -> list:
        """Returns the list of loading tool items displayed in the
        'Loading Tool' dropdown menu in the 'Create Circuit' dialog in
        the Task Manager panel within FMS Office.

        This keyword returns an ordered list of loading tool items in the
        order by which they are displayed.

        If the list of loading tool items or the 'Loading Tool' dropdown
        menu cannot be located, this keyword fails.

        Returns:
            list: A list of loading tool items.

        Examples:
        | @{result} = | Get Loading Tool List |

        See also `Set Loading Tool`, `Is Loading Tool Set`.
        """
        self.click(
            self._get_dialog().find_element(
                By.XPATH, self.__loading_tool_dropdown
            )
        )
        items = [
            i.text
            for i in self._get_dialog().find_elements(
                By.XPATH, self.__dropdown_items
            )
        ]
        return items

    def is_create_button_disabled(self) -> bool:
        """Fails if the 'Create' button is enabled in the 'Create Circuit'
        dialog in the Task Manager panel within FMS Office.

        This keyword returns `True` if, and only if, the 'Create' button
        is disabled. Otherwise, this keyword returns `False`.

        If the 'Create' button cannot be located, this keyword fails.

        Returns:
            bool: `True` if the Create' button is disabled; `False`
            otherwise.

        Examples:
        | ${result} = | Is Create Button Disabled |

        See also `Click Create`.
        """
        try:
            self._get_dialog().find_element(
                By.XPATH, self.__create_button_disabled
            )
            return True
        except Exception:
            return False

    def is_dump_destination_set(self, dump_destination: str) -> bool:
        """Fails if the dump destination is not displayed in the 'Dump
        Destination' field in the 'Create Circuit' dialog in the Task
        Manager panel within FMS Office.

        The name or identifier of the dump destination is specified using
        `dump_destination`, and should generally always be a string-type
        identifier.

        This keyword returns `True` if, and only if, the given dump
        destination is displayed in the 'Dump Destination' field and
        found to be a valid or non-empty element. Otherwise, this keyword
        returns `False`.

        If the given dump destination or the 'Dump Destination' field
        cannot be located, this keyword fails.

        Args:
            dump_destination (str): The name or identifier of the dump
            destination.

        Returns:
            bool: `True` if the dump destination is displayed; `False`
            otherwise.

        Examples:
        | ${result} = | Is Dump Destination Set | ${dump_destination} |

        See also `Get Dump Destination List`, `Set Dump Destination`.
        """
        element = self._get_dialog().find_element(
            By.XPATH, self.__dump_destination_dropdown
        )
        if element.text == dump_destination:
            return True
        return False

    def is_loading_tool_set(self, loading_tool: str) -> bool:
        """Fails if the loading tool is not displayed in the 'Loading Tool'
        field in the 'Create Circuit' dialog in the Task Manager panel
        within FMS Office.

        The name or identifier of the loading tool is specified using
        `loading_tool`, and should generally always be a string-type
        identifier.

        This keyword returns `True` if, and only if, the given loading
        tool is displayed in the 'Loading Tool' field and found to be a
        valid or non-empty element. Otherwise, this keyword returns `False`.

        If the given loading tool or the 'Loading Tool' field cannot be
        located, this keyword fails.

        Args:
            loading_tool (str): The name or identifier of the loading
            tool.

        Returns:
            bool: `True` if the loading tool is displayed; `False`
            otherwise.

        Examples:
        | ${result} = | Is Loading Tool Set | ${loading_tool} |

        See also `Get Loading Tool List`, `Set Loading Tool`.
        """
        element = self._get_dialog().find_element(
            By.XPATH, self.__loading_tool_dropdown
        )
        if element.text == loading_tool:
            return True
        return False

    def is_number_of_circuits_set(self, number_of_circuits: str) -> bool:
        """Fails if the number of circuits is not displayed in the 'Number
        Of Circuits' field in the 'Create Circuit' dialog in the Task
        Manager panel within FMS Office.

        The number of circuits is specified using `number_of_circuits`,
        and should generally always be a string-type identifier.

        This keyword returns `True` if, and only if, the given number of
        circuits are displayed in the 'Number Of Circuits' field and
        found to be a valid or non-empty element. Otherwise, this keyword
        returns `False`.

        If the given number of circuits or the 'Number Of Circuits' field
        cannot be located, this keyword fails.

        Args:
            number_of_circuits (str): The number of circuits.

        Returns:
            bool: `True` if the number of circuits is displayed; `False`
            otherwise.

        Examples:
        | ${result} = | Is Number Of Circuits Set | ${number_of_circuits} |

        See also `Set Number Of Circuits`.
        """
        element = self._get_dialog().find_element(
            By.XPATH, self.__number_of_circuits_textfield
        )
        if element.get_attribute("value") == number_of_circuits:
            return True
        return False

    def is_reoccurring_set(self) -> bool:
        """Fails if the 'Reoccurring' checkbox is not set in the 'Create
        Circuit' dialog in the Task Manager panel within FMS Office.

        This keyword returns `True` if, and only if, the 'Reoccurring'
        checkbox is set and found to be a valid or non-empty element.
        Otherwise, this keyword returns `False`.

        If the 'Reoccurring' checkbox cannot be located, this keyword
        fails.

        Returns:
            bool: `True` if the 'Reoccurring' checkbox is set; `False`
            otherwise.

        Examples:
        | ${result} = | Is Reoccurring Set |

        See also `Set Reoccurring`, `Unset Reoccurring`.
        """
        element = self._get_dialog().find_element(
            By.XPATH, self.__reoccurring_checkbox
        )
        if element.get_attribute("checked"):
            return True
        return False

    def is_use_material_destination_plan_set(self) -> bool:
        """Fails if the 'Use Material Destination Plan' checkbox is not
        set in the 'Create Circuit' dialog in the Task Manager panel
        within FMS Office.

        This keyword returns `True` if, and only if, the 'Use Material
        Destination Plan' checkbox is set and found to be a valid or
        non-empty element. Otherwise, this keyword returns `False`.

        If the 'Use Material Destination Plan' checkbox cannot be located,
        this keyword fails.

        Returns:
            bool: `True` if the 'Use Material Destination Plan' checkbox
            is set; `False` otherwise.

        Examples:
        | ${result} = | Is Use Material Destination Plan Set |

        See also `Set Use Material Destination Plan`, `Unset Use Material Destination Plan`.
        """
        element = self._get_dialog().find_element(
            By.XPATH, self.__use_material_destination_plan_checkbox
        )
        if element.get_attribute("checked"):
            return True
        return False

    def set_dump_destination(self, dump_destination: str) -> None:
        """Sets the 'Dump Destination' field to the given dump destination
        in the 'Create Circuit' dialog in the Task Manager panel within
        FMS Office.

        The dump destination is specified using `dump_destination`, and
        should generally always be a string-type identifier.

        If the 'Dump Destination' field cannot be located, if it is not
        able to be clicked, or if the given dump destination does not
        correspond to an item in the 'Dump Destination' dropdown, this
        keyword fails. This keyword never returns anything.

        Args:
            dump_destination (str): The name or identifier of the dump
            destination.

        Examples:
        | ${result} = | Set Dump Destination | ${dump_destination} | # Value of ${result} is always None |

        See also `Get Dump Destination List`, `Is Dump Destination Set`.
        """
        self.select(
            self._get_dialog().find_element(
                By.XPATH, self.__dump_destination_dropdown
            ),
            dump_destination,
        )

    def set_loading_tool(self, loading_tool: str) -> None:
        """Sets the 'Loading Tool' field to the given loading tool in the
        'Create Circuit' dialog in the Task Manager panel within FMS
        Office.

        The loading tool is specified using `loading_tool`, and should
        generally always be a string-type identifier.

        If the 'Loading Tool' field cannot be located, if it is not able
        to be clicked, or if the given loading tool does not correspond
        to an item in the 'Loading Tool' dropdown, this keyword fails.
        This keyword never returns anything.

        Args:
            loading_tool (str): The name or identifier of the loading
            tool.

        Examples:
        | ${result} = | Set Dump Destination | ${dump_destination} | # Value of ${result} is always None |

        See also `Get Dump Destination List`, `Is Dump Destination Set`.
        """
        self.select(
            self._get_dialog().find_element(
                By.XPATH, self.__loading_tool_dropdown
            ),
            loading_tool,
        )

    def set_number_of_circuits(self, number_of_circuits: str) -> None:
        """Sets the 'Number Of Circuits' field to the given number of
        circuits in the 'Create Circuit' dialog in the Task Manager panel
        within FMS Office.

        The number_of_circuits is specified using `number_of_circuits`,
        and should generally always be a string-type identifier.

        If the 'Number Of Circuits' field cannot be located, or if the
        dropdown menu is not able to be clicked, this keyword fails. This
        keyword never returns anything.

        Args:
            number_of_circuits (str): The number of circuits.

        Examples:
        | ${result} = | Set Number Of Circuits | ${number_of_circuits} | # Value of ${result} is always None |

        See also `Is Number Of Circuits Set`.
        """
        self.send_keys(
            self._get_dialog().find_element(
                By.XPATH, self.__number_of_circuits_textfield
            ),
            number_of_circuits,
        )

    def set_reoccurring(self) -> None:
        """Sets the 'Reoccurring' checkbox in the 'Create Circuit' dialog
        in the Task Manager panel within FMS Office.

        If the 'Reoccurring' checkbox cannot be located, or if it is not
        able to be clicked, this keyword fails. This keyword never returns
        anything.

        Examples:
        | ${result} = | Set Reoccurring | # Value of ${result} is always None |

        See also `Is Reoccurring Set`, `Unset Reoccurring`.
        """
        element = self._get_dialog().find_element(
            By.XPATH, self.__reoccurring_checkbox
        )
        if not element.get_attribute("checked"):
            self.click(element)

    def set_use_material_destination_plan(self) -> None:
        """Sets the 'Use Material Destination Plan' checkbox in the
        'Create Circuit' dialog in the Task Manager panel within FMS
        Office.

        If the 'Use Material Destination Plan' checkbox cannot be located,
        or if it is not able to be clicked, this keyword fails. This
        keyword never returns anything.

        Examples:
        | ${result} = | Set Use Material Destination Plan | # Value of ${result} is always None |

        See also `Is Use Material Destination Plan Set`, `Unset Use Material Destination Plan`.
        """
        element = self._get_dialog().find_element(
            By.XPATH, self.__use_material_destination_plan_checkbox
        )
        if not element.get_attribute("checked"):
            self.click(element)

    def unset_reoccurring(self) -> None:
        """Unsets the 'Reoccurring' checkbox in the 'Create Circuit'
        dialog in the Task Manager panel within FMS Office.

        If the 'Reoccurring' checkbox cannot be located, or if it is not
        able to be clicked, this keyword fails. This keyword never returns
        anything.

        Examples:
        | ${result} = | Unset Reoccurring | # Value of ${result} is always None |

        See also `Is Reoccurring Set`, `Set Reoccurring`.
        """
        element = self._get_dialog().find_element(
            By.XPATH, self.__reoccurring_checkbox
        )
        if element.get_attribute("checked"):
            self.click(element)

    def unset_use_material_destination_plan(self) -> None:
        """Unsets the 'Use Material Destination Plan' checkbox in the
        'Create Circuit' dialog in the Task Manager panel within FMS
        Office.

        If the 'Use Material Destination Plan' checkbox cannot be located,
        or if it is not able to be clicked, this keyword fails. This
        keyword never returns anything.

        Examples:
        | ${result} = | Unset Use Material Destination Plan | # Value of ${result} is always None |

        See also `Is Use Material Destination Plan Set`, `Set Use Material Destination Plan`.
        """
        element = self._get_dialog().find_element(
            By.XPATH, self.__use_material_destination_plan_checkbox
        )
        if element.get_attribute("checked"):
            self.click(element)

    def _get_dialog(self):
        return self._get_panel().find_element(By.XPATH, self.__dialog)
