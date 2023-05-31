__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import os
import re
import sys
import json
import time
import socket


from webdrivermanager import AVAILABLE_DRIVERS as download_drivers
from typing import Dict, Optional, Any
from test_code.Const import REDACT_REGION, BROWSER_DRIVER
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger


class Environment(object):
    """
    This contains environment information for the running test.
    { 'SuiteName': {'TestName':
        _Test_Context {'processes':{'processConfigName': _Test_Process_Context}, 'office_path': PATH_TO_OFFICE...}
        }}

    To access test_context use:
        Environment().test_context
    To access TestProcessContext use:
        Environment().test_context.current_process_context
        OR
        Environment().test_context.processes[process_name]
        NOTE: Current process is set when you get or set first process environment
    """

    # Default similarity which will be used for image comparision.
    # Similarity varies from 0.0 (least match) to 1.0 (exact match)
    DEFAULT_SIMILARITY = 0.95

    # Keeps test data (test_context->processContext)
    _env_data: Dict = {}

    _timeout: int = None

    # Delay which will be used between the services start, to avoid random issues
    _service_start_delay: int = None

    # Get IP address of localhost, so it can be used by selenium docker.
    _imperium_server_ip_address: str = None


    """
    Single instance of this class, as Environment is created once per execution.
    """

    def __new__(class_):
        if not hasattr(class_, '_instance'):
            class_._instance = super(Environment, class_).__new__(class_)
        return class_._instance


    def _get_test_name(self) -> Optional[str]:
        """
        Return Name of the test.
        :return: (str|None)
        """
        test_name = BuiltIn().get_variable_value('${TEST NAME}')
        if test_name:
            return re.sub(r"^scenario: ", "", test_name, flags=re.IGNORECASE)\
                .replace(' ', '_').replace(',', '').replace('.', '')
        else:
            return "suite_context"


    def _get_suite_name(self) -> str:
        """
        Return suite name
        :return: (str)
        """
        # Keep suite name as the directory in which test are placed.
        return BuiltIn().get_variable_value('${SUITE NAME}').split('.')[-1].replace(' ', '_')


    def initialize_context(self, suite_name:str, test_name:str):
        """
        Context in which test specific data is saved. Returns Test Context for
        the specific test within suite.

        Examples:

            | ${context}= | Initialize Context | NAME_OF_SUITE | TEST_NAME |
        """
        if suite_name not in self._env_data:
            self._env_data[suite_name] = {test_name: _Test_Context(suite_name, test_name)}
        elif test_name not in self._env_data[suite_name]:
            self._env_data[suite_name][test_name] = _Test_Context(suite_name, test_name)

        return self._env_data[suite_name][test_name]


    def initialize_environment(self, suite_name:str=None, test_name:str=None) -> None:
        """
        Initialize environment for the test.

        Examples:
            | Initialize Environment | NAME_OF_SUITE | TEST_NAME |
        """
        if not suite_name:
            suite_name = self._get_suite_name()
        if not test_name:
            test_name = self._get_test_name()

        self.env_log(f"Initializing test environment for suite: {suite_name} and test: {test_name}", 'trace')

        if suite_name and test_name:
            self.initialize_context(suite_name, test_name)

        for region, rect in REDACT_REGION.items():
            BuiltIn().set_global_variable('${REDACT_REGION_'+region+'}', rect)

        # Ensure webdriver is available.
        browser = str(BuiltIn().get_variable_value('${BROWSER}'))
        if not browser:
            browser = 'chrome'
            BuiltIn().set_suite_variable('${BROWSER}', 'chrome')

        # Make driver directory, where all drivers will be stored.
        driver_dir = str(BuiltIn().get_variable_value('${DRIVER_DIR}'))
        if not os.path.exists(driver_dir):
            os.makedirs(driver_dir)

        # Download driver and if it fails, exit.
        if not os.path.exists(self.driver_executable_path(browser)):
            self.env_log(f"Downloading driver for browser: {browser}", 'trace')
            downloader = download_drivers[browser](None, driver_dir, 'win' if os.name == 'nt' else 'linux')
            try:
                extracted_binary, link = downloader.download_and_install(BROWSER_DRIVER[browser]['driver'])
            except ConnectionError:
                raise Exception("Unable to download webdriver's at this time due to network connectivity error")


    def env_log(self, msg:str, log_level:str='debug', html=False) -> None:
        asked_log_level = BuiltIn().get_variable_value('${LOG_LEVEL}')
        if asked_log_level.lower() == 'trace' or asked_log_level.lower() == log_level.lower():
            logger.console("- "+msg)

        if html:
            src = msg
            width = 100
            msg = '</td></tr><tr><td colspan="3">' + f'<a href="{src}"><img src="{src}" width="{width}px"></a>',
        BuiltIn().log(msg, log_level, html=html)


    @property
    def run_env(self):
        """
        Environment with which test should run. 
        If None, test will run against local environment, else dev
        """
        return str(BuiltIn().get_variable_value('${RUN_ENV}'))

    @property
    def release(self):
        """
        Release against which docker will be used for test to run. 
        master or rc or local
        """
        if str(BuiltIn().get_variable_value('${RUN_LOCAL_DOCKER}')) == 'local':
            return str(BuiltIn().get_variable_value('${RUN_LOCAL_DOCKER}'))
        return str(BuiltIn().get_variable_value('${RELEASE}'))

    @property
    def test_context(self):
        """
        Context which keep track of all the environment information for specific testcase.
        :return: Test Context for the specific test within suite.
        """
        suite_name = self._get_suite_name()
        test_name = self._get_test_name()

        if suite_name not in self._env_data or test_name not in self._env_data[suite_name]:
            if "suite_context" in self._env_data[suite_name]:
                test_name = "suite_context"
            else:
                raise Exception ("Context is not set for suite: {} and test: {}".format(suite_name, test_name))

        return self._env_data[suite_name][test_name]

    @property
    def imperium_server_ip_address(self) -> str:
        if not self._imperium_server_ip_address:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            try:
                s.connect(('10.255.255.255', 1))
                self._imperium_server_ip_address = s.getsockname()[0]
            except Exception:
                self._imperium_server_ip_address = '127.0.0.1'
            finally:
                s.close()
        return self._imperium_server_ip_address

    @property
    def time_out(self) -> int:
        """
        Timeout which will be used.
        :return:
        """
        if type(self)._timeout:
            return type(self)._timeout

        passed_timeout = BuiltIn().get_variable_value('${TIMEOUT}')
        # If no timeout passed, then set it to 30 sec.
        if not passed_timeout:
            passed_timeout = 30
        type(self)._timeout = int(passed_timeout)

        return type(self)._timeout


    @property
    def service_start_delay(self) -> int:
        """
        Add delay between services, as we start all services redis and other
        systems might get unresponsive.
        :return:
        """
        if type(self)._service_start_delay:
            return type(self)._service_start_delay

        passed_timeout = BuiltIn().get_variable_value('${START_DELAY}')
        # If no timeout passed, then set it to 0 sec.
        if not passed_timeout:
            passed_timeout = 0
        type(self)._service_start_delay = int(passed_timeout)

        return type(self)._service_start_delay


    @property
    def pid_path(self) -> str:
        return os.path.join(os.path.dirname(str(BuiltIn().
            get_variable_value('${OUTPUTDIR}'))), 'imperium_services.pids').replace('\\', '/')


    @property
    def command_path(self) -> str:
        return os.path.join(str(BuiltIn().get_variable_value('${OUTPUTDIR}')), 'commands.sh').replace('\\', '/')


    def set_service_pid(self, service: str, pid: int) -> None:
        """
        Saves pid of the service in test context.

        Examples:
        | Set Service PID | Service | PID |
        """
        pids = {}
        if os.path.exists(self.pid_path):
            with open(self.pid_path, 'r') as fp:
                pids = json.load(fp)

        if service in pids:
            raise Exception(f"Service already has pid: {pids[service]}")

        pids[service] = pid

        # Serializing json 
        json_object = json.dumps(pids, indent = 4)

        # Writing to pid_path
        with open(self.pid_path, "w") as outfile:
            outfile.write(json_object)

    def remove_service_pid(self, service: str) -> None:
        """
        Remove pid from service in test context.

        Examples:
        | Remove Service Pid | Service_Name |
        """
        pids = {}
        if not os.path.exists(self.pid_path):
            return

        with open(self.pid_path, 'r') as fp:
            pids = json.load(fp)

        if service not in pids:
            return

        # Remove service from the known list
        pid = pids[service]
        del pids[service]

        # Serializing json 
        json_object = json.dumps(pids, indent = 4)

        # Writing to pid_path
        with open(self.pid_path, "w") as outfile:
            outfile.write(json_object)

        if not self.test_context.process_exists(service):
            try:
                self.env_log(f"Killing {service} with pid: {pid}", 'trace')
                os.system(f'kill -9 -{pid}')
                if self.service_start_delay:
                    time.sleep(self.service_start_delay)
            except Exception as e:
                remove_pid_file = False
                self.env_log(f"Failed to kill service {service} pid: {pid}", 'debug')


    def is_windows(self) -> bool:
        if os.name == 'nt':
            return True
        else:
            return False


    def driver_executable_path(self, browser: str) -> str:
        if browser == 'firefox':
            driver = 'geckodriver'
        elif browser == 'chrome':
            driver = 'chromedriver'
        else:
            raise Exception(f'Browser not supported {browser}')

        if self.is_windows():
            driver = driver + '.exe'

        executable_path = os.path.join(BuiltIn().get_variable_value('${DRIVER_DIR}'), driver).replace('\\', '/')

        # self.env_log(f'Driver used: {executable_path}', 'debug')
        return executable_path


    def wait_for_user_input(self):
        """
        Wait for user input.

        Examples:
        | Wait For User Input |
        """
        self.env_log('Please press enter to continue...', 'debug')
        input('Please press any button to continue\n')


class _Test_Context(object):
    @property
    def environment (self):
        if not self._environment:
            self._environment = Environment()
        return self._environment

    @property
    def current_process_context(self):
        return self._currentProcessContext

    @current_process_context.setter
    def current_process_context(self, service_name: str):
        """
        Sets the current process context by name.
        :param processConfigName:
        """
        if service_name not in self.processes:
            raise Exception("There is no process {} to set. Known processes are {}".format(service_name, list(self.processes.keys())))
        self._currentProcessContext = self.processes[service_name]
        self.currentprocessConfigName = service_name


    def __init__(self, suite_name: str, test_name: str):
        self.suite_name = suite_name
        self.test_name = test_name
        self.errors = []
        self._environment = None
        self.processes = {}
        self.error_generator = []
        output_dir = str(BuiltIn().get_variable_value('${OUTPUTDIR}'))
        self.log_path = os.path.join(output_dir, 'log', suite_name, test_name).replace('\\', '/')
        self.log_error_path = os.path.join(self.log_path, 'error').replace('\\', '/')
        os.makedirs(self.log_path, exist_ok=True)
        os.makedirs(self.log_error_path, exist_ok=True)
        self.skip_error_check_in_log = False
        self.ensure_error_in_log = False
        self.robot_eye_opened = False
        self.redis_connections = {}
        # This can be a case when skip service is used.
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path, exist_ok=True)


    def process_exists(self, service_name: str) -> bool:
        """
        Return True if process information has been created, else false.
        :param processConfigName: Name of the process to check.
        :return; True if process info exits, else False.
        """
        if service_name in self.processes:
            return True
        else:
            return False


    def get(self, name: str, service_name: str=None) -> Any:
        """
        Return value for the test_context or processContext.
        :param name: (str) name of the variable
        :param processConfigName: (optional) (str) process name for which variable value should be returned.
        :return: (mixed)
        """
        # If service_name is passed then return process related information.
        if service_name and service_name not in self.processes:
            raise Exception("There is no config {} for process to get: {}".format(name, service_name))

        if service_name:
            self.current_process_context = service_name
            return self.processes[service_name].get(name)
        else:
            # If it's not process specific, then it's the env we are after.
            return getattr(self, name)


    def set(self, name: str, value: Any, service_name: str=None) -> None:
        """
        Set value for the test_context or processContext.
        :param name: (str) name of the variable
        :param processConfigName: (optional) (str) process name for which variable value should be set.
        """
        if service_name:
            process_context = self.get_process_context(service_name)
            process_context.set(name, value)
        else:
            setattr(self, name, value)


    def create_process_context(self, service_name: str):
        self.processes[service_name] = _Test_Process_Context(service_name, self)
        self.current_process_context = service_name
        return self.processes[service_name]


    def get_process_context(self, service_name: str):
        """
        Return processContext.
        :param service_name: (optional) (str) process name for which variable value should be returned.
        :param exists: Expects process context to be present.
        :param robotSocketFactory: Socker factory reference used for creating socket.
        :return: processContext
        """
        if self.processes and service_name not in self.processes:
            raise Exception("Process context '{}' is expected to be present".format(service_name))
        self.current_process_context = service_name
        return self.processes[service_name]


    def get_current_process_info(self, name:str):
        """
        Return value form the current processContext.
        :param name: (str) name of the variable
        :return: (mixed)
        """
        self.get(name, self.current_process_context)


    def set_current_process_info(self, name: str, value: Any) -> None:
        """
        set value for the current processContext.
        :param name: (str) name of the variable
        :param value: (mixed) Value to set.
        """
        self.set(name, value, self.current_process_context)


    def errors_in_log(self, filename: str):
        """Given a filename, return an iterator that yields lines containing errors
        or exceptions.

        A None indicates that there are no more errors / exceptions (for now)."""
        if not os.path.exists(filename):
            yield
        with open(filename) as f_in:
            while True:
                lines = f_in.readlines()
                errors = ''
                context = 0
                for line in lines:
                    is_error = 'Error' in line or 'Exception' in line
                    if is_error or context > 0:
                        if is_error:
                            context = 20
                        else:
                            context -= 1
                        errors += line
                    elif errors and context == 0:
                        yield errors + '\n--- end context'
                        errors = ''
                yield


    def watch_log_file(self, logFileName: str) -> None:
        """Watch a log file for errors."""
        errors = self.errors_in_log(logFileName)
        self.error_generator.append((logFileName, errors))


    def notify_process_errors(self) -> None:
        """Report on any errors in logfiles watched using watch_log_file().

        Note that errors are logged to sys.__stderr__ rather than using
        robot framework's logging as this method may be called from threads
        other than the main thread.
        """
        if self.skip_error_check_in_log:
            return
        for filename, iterator in self.error_generator:
            for err in iterator:
                if err:
                    sys.__stderr__.write('\nError from %s: %s\n' % (filename, err))
                else:
                    break


class _Test_Process_Context(object):
    """
    Keep track of process specific information.
    """
    _environment = None

    @property
    def environment (self):
        if not self._environment:
            self._environment = Environment()
        return self._environment


    def __init__(self, service_name: str, test_context):
        self.name = service_name
        self.test_context = test_context
        self.log_file = None
        self.error_log_file = None
        self.extra_params = {}
        self.cmd = None
        self.process_handle = None
        self.container = None
        self.is_docker = False
        self.env_vars = {}


    def set(self, name: str, value: Any) -> None:
        """
        Saves value for variable, instance
        :param variableName: Name of the varible
        :param value: Value to set.
        """
        setattr(self, name, value)


    def get(self, name: str) -> Any:
        """
        Return value for the specified attribute
        :param name: Name of the variable
        :return: value set in that variable
        """
        return getattr(self, name)
