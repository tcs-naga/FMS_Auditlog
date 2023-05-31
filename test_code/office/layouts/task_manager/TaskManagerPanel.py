__copyright__ = (
    "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved."
)

import time

from test_code.office.layouts.BaseLayout import BaseLayout
from selenium.webdriver.common.by import By
from robot.libraries.BuiltIn import BuiltIn

class TaskManagerPanel(BaseLayout):
    __tile_title = "Task Manager"
    __task_in_task_manager_panel = "//div[@id='taskItemsList']/div[.//div[text()='{}'] and .//div[text()='{}']]"
    __new_assignment_dialog = "//div[contains(@class, 'dialog MuiBox')]"
    __assign_now_button = __new_assignment_dialog + "//button[text()='Assign Now']"

    def click_asset(self, asset: str) -> None:
        """Clicks on the given asset in the Task Manager panel within
        FMS Office.

        The name or identifier of the asset is specified using `asset`,
        and should generally always be a string-type identifier.

        If the asset cannot be located, or if it is not able to be
        clicked, this keyword fails. This keyword never returns anything.

        Args:
            asset (str): The name or identifier of the asset.

        Examples:
        | ${result} = | Click Asset | ${asset} | # Value of ${result} is always None |

        See also `Get Asset List`, `Is Asset Displayed`.
        """
        self.click(self.__find_asset(asset))

    def click_context_menu_item(
        self, asset: str, context: str, item: str = None
    ) -> None:
        """Clicks on the given context menu item in the Task Manager
        panel within FMS Office.

        The name or identifier of the asset is specified using `asset`,
        the name or identifier of the context menu is specified using
        `context`, and the name or identifier of the context menu item
        is specified using `item`. All arguments should generally always
        be string-type identifiers.

        If the context menu item cannot be located, or if it is not able
        to be clicked, this keyword fails. This keyword never returns
        anything.

        Args:
            asset (str): The name or identifier of the asset.
            context (str): The name or identifier of the context menu.
            item (str, optional): The name or identifier of the context
            menu item. Defaults to None.

        Examples:
        | ${result} = | Click Context Menu Item | ${item} | # Value of ${result} is always None |

        See also `Get Context Menu Item List`, `Is Context Menu Item Displayed`.
        """
        BuiltIn().run_keyword("Wait Until Page Contains Element", self.__find_asset(asset))
        self.click(self.__find_asset(asset))
        BuiltIn().run_keyword("Wait Until Page Contains Element", self.__find_context_menu_item(context))
        self.click(self.__find_context_menu_item(context))
        if item is not None:
            self.click(self.__find_context_menu_item(item))

    def create_assignment_task(
        self, asset: str, context: str, item: str = None
    ) -> bool:
        """Creates an assignment for the given asset based on the given context and item.
           This method will select the asset, then select the context and then the item.
           Ones the task is created, it verifies that the task is created under task manager.
        Args:
            asset: Asset to be selected in Task Manager panel
            context: The task context. e.g:- Loader
            item: The asset which the context should be performed on. e.g:- {excavator} to Load from
        Examples:
        | Create Assignment Task | asset=${DEFAULT_ASSET_ID} | context=Loader | item=${excavator} |
        """
        self.click_context_menu_item(asset=asset, context=context, item=item)

        return self.is_task_visible_in_task_manager(
            source_asset=asset, destination_asset=item
        )

    def click_assign_now(self) -> None:
        """Clicks Assign Now button in New Assignment dialog box
        Examples:
        | Click Assign Now |
        """
        BuiltIn().run_keyword("Wait Until Page Contains Element", self.__new_assignment_dialog)
        self.click(self.__assign_now_button)

    def create_asap_assignment_task(
        self, asset: str, context: str, item: str = None
    ) -> bool:
        """Creates an asap assignment for the given asset based on the given context and item.
           This method will select the asset, then select the context and then the item.
           Then it selects 'As soon as possible' from the new assignemnt dialog
           Ones the task is created, it verifies that the task is created under task manager.

        Args:
            asset: Asset to be selected in Task Manager panel
            context: The task context. e.g:- Loader
            item: The asset which the context should be performed on. e.g:- {excavator} to Load from

        Examples:
        | Create Asap Assignment Task | asset=${DEFAULT_ASSET_ID} | context=Loader | item=${excavator} |

        """
        self.click_context_menu_item(asset=asset, context=context, item=item)
        self.click_assign_now()

        return self.is_task_visible_in_task_manager(
            source_asset=asset, destination_asset=item
        )

    def click_filter_menu_item(self, item: str) -> None:
        """Clicks on the given filter menu item in the Task Manager panel
        within FMS Office.

        The name or identifier of the filter is specified using `filter`,
        and should generally always be a string-type identifier.

        If the filter menu item cannot be located, or if it is not able
        to be clicked, this keyword fails. This keyword never returns
        anything.

        Args:
            item (str): The name or identifier of the filter menu item.

        Examples:
        | ${result} = | Click Filter Menu Item | ${item} | # Value of ${result} is always None |

        See also `Get Filter Menu Item List`, `Is Filter Menu Item Displayed`.
        """
        self.click(self.__find_filter())
        self.click(self.__find_filter_menu_item(item))

    def click_task_list_item(self, item: str) -> None:
        """Clicks on the given task list item in the Task Manager panel
        within FMS Office.

        The name or identifier of the task list item is specified using
        `item`, and should generally always be a string-type identifier.

        If the task list item cannot be located, or if it is not able to
        be clicked, this keyword fails. This keyword never returns
        anything.

        Args:
            item (str): The name or identifier of the task list item.

        Examples:
        | ${result} = | Click Task List Item | ${item} | # Value of ${result} is always None |

        See also `Is Task List Item Displayed`.
        """
        self.click(self.__find_task_list_item(item))

    def get_asset_list(self) -> list:
        """Returns the list of assets displayed in the Task Manager panel
        within FMS Office.

        This keyword returns an ordered list of asset names in the order
        by which they are displayed.

        If the list of assets cannot be located, this keyword fails.

        Returns:
            list: An ordered list of assets.

        Examples:
        | @{result} = | Get Asset List |

        See also `Click Asset`, `Is Asset Displayed`.
        """
        items = [i.text for i in self.__find_asset_list()]
        return items

    def get_context_menu_item_list(self, asset: str) -> list:
        """Returns the list of context menu items displayed for a given
        asset in the Task Manager panel within FMS Office.

        This keyword returns an ordered list of context menu item names
        in the order by which they are displayed.

        If the list of context menu items for a given asset cannot be
        located, this keyword fails.

        Returns:
            list: An ordered list of context menu items.

        Examples:
        | @{result} = | Get Context Menu Item List |

        See also `Click Context Menu Item`, `Is Context Menu Item Displayed`.
        """
        self.click(self.__find_asset(asset))
        items = [i.text for i in self.__find_context_menu_item_list()]
        return items

    def get_filter_menu_item_list(self) -> list:
        """Returns the list of filter menu items displayed in the Task
        Manager panel within FMS Office.

        This keyword returns an ordered list of filter menu item names
        in the order by which they are displayed.

        If the list of filter menu items for a given asset cannot be
        located, this keyword fails.

        Returns:
            list: An ordered list of filter menu items.

        Examples:
        | @{result} = | Get Filter Menu Item List |

        See also `Click Filter Menu Item`, `Is Filter Menu Item Displayed`.
        """
        self.click(self.__find_filter())
        items = [i.text for i in self.__find_filter_menu_item_list()]
        return items

    def is_asset_displayed(self, asset: str) -> bool:
        """Fails if the given asset is not displayed in the Task Manager
        panel within FMS Office.

        The name or identifier of the asset is specified using `asset`,
        and should generally always be a string-type identifier.

        This keyword returns `True` if, and only if, the given asset is
        displayed and found to be a valid or non-empty element. Otherwise,
        this keyword returns `False`.

        If the given asset cannot be located, this keyword fails.

        Args:
            asset (str): The name or identifier of the asset.

        Returns:
            bool: `True` if the asset is displayed; `False` otherwise.

        Examples:
        | ${result} = | Is Asset Displayed | ${asset} |

        See also `Click Asset`, `Get Asset List`.
        """
        if self.__find_asset(asset):
            return True
        return False

    def is_context_menu_item_displayed(self, item: str) -> bool:
        """Fails if the given context menu item is not displayed in the
        Task Manager panel within FMS Office.

        The name or identifier of the context menu item is specified
        using `item`, and should generally always be a string-type
        identifier.

        This keyword returns `True` if, and only if, the given context
        menu item is displayed and found to be a valid or non-empty
        element. Otherwise, this keyword returns `False`.

        If the given context menu item cannot be located, this keyword
        fails.

        Args:
            item (str): The name or identifier of the context menu item.

        Returns:
            bool: `True` if the context menu item is displayed; `False`
            otherwise.

        Examples:
        | ${result} = | Is Context Menu Item Displayed | ${item} |

        See also `Click Context Menu Item`, `Get Context Menu Item List`.
        """
        if self.__find_context_menu_item(item):
            return True
        return False

    def is_filter_menu_item_displayed(self, item: str) -> bool:
        """Fails if the given filter menu item is not displayed in the
        Task Manager panel within FMS Office.

        The name or identifier of the filter menu item is specified using
        `item`, and should generally always be a string-type identifier.

        This keyword returns `True` if, and only if, the given filter
        menu item is displayed and found to be a valid or non-empty
        element. Otherwise, this keyword returns `False`.

        If the given filter menu item cannot be located, this keyword
        fails.

        Args:
            item (str): The name or identifier of the filter menu item.

        Returns:
            bool: `True` if the filter menu item is displayed; `False`
            otherwise.

        Examples:
        | ${result} = | Is Filter Menu Item Displayed | ${item} |

        See also `Click Filter Menu Item`, `Get Filter Menu Item List`.
        """
        if self.__find_filter_menu_item(item):
            return True
        return False

    def is_task_list_item_displayed(self, item: str) -> bool:
        """Fails if the given task list item is not displayed in the Task
        Manager panel within FMS Office.

        The name or identifier of the task list item is specified using
        `item`, and should generally always be a string-type identifier.

        This keyword returns `True` if, and only if, the given task list
        item is displayed and found to be a valid or non-empty element.
        Otherwise, this keyword returns `False`.

        If the given task list item cannot be located, this keyword fails.

        Args:
            item (str): The name or identifier of the task list item.

        Returns:
            bool: `True` if the task list item is displayed; `False`
            otherwise.

        Examples:
        | ${result} = | Is Task List Item Displayed | ${item} |

        See also `Click Task List Item`.
        """
        retry_count = 30
        while retry_count:
            try:
                if self.__find_task_list_item(item):
                    return True
            except Exception:
                if not retry_count:
                    return False
                retry_count -= 1
                time.sleep(0.5)
        return False

    def is_task_visible_in_task_manager(
        self, source_asset: str, destination_asset: str
    ) -> bool:
        """
        Is task visible in task manager in the task manager when an asset is given an assignment
        e.g:- Load 'DT5401' at 'EX7109'

        Examples:
        | Is Task Visible In Task Manager | DT5401 | EX7109 |
        """
        try:
            self._get_panel().find_element(
                By.XPATH,
                self.__task_in_task_manager_panel.format(
                    source_asset, destination_asset
                ),
            )
            return True
        except:
            return False

    def refresh(self):
        return self.get_layout(self.__tile_title, clear_cache=True)

    def __find_asset(self, text):
        return self._get_panel().find_element(
            By.XPATH, f".//div[text() = '{text}']"
        )

    def __find_asset_list(self):
        return self._get_panel().find_elements(
            By.XPATH,
            f".//*[@data-icon = 'caret-down']/../following-sibling::div//div[@aria-label = 'On Delay']/../preceding-sibling::div",
        )

    def __find_context_menu_item(self, text):
        return self._get_panel().find_element(
            By.XPATH,
            f"//div[@role = 'button' and (.//span[text() = '{text}'] or .//div[text() = '{text}'])]",
        )

    def __find_context_menu_item_list(self):
        return self._get_panel().find_elements(
            By.XPATH,
            f"//div[@class = 'context-menu-items']/div[@role = 'button']",
        )

    def __find_filter(self):
        return self._get_panel().find_element(
            By.XPATH,
            f".//*[@data-icon = 'caret-down' or @data-icon = 'caret-up']/..",
        )

    def __find_filter_menu_item(self, text):
        return self._get_panel().find_element(
            By.XPATH, f".//li[text() = '{text}']"
        )

    def __find_filter_menu_item_list(self):
        return self._get_panel().find_elements(
            By.XPATH,
            f".//ul[@role = 'menu']/li[@role = 'menuitem']",
        )

    def __find_task_list_item(self, label):
        return self._get_panel().find_element(
            By.XPATH, f".//div[@aria-label = '{label}']"
        )

    def _get_panel(self):
        return self.get_layout(self.__tile_title)
