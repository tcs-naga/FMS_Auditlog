__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import os
import time
from click import command
import copy
import subprocess

from typing import List, Dict
from selenium import webdriver
from test_code.Const import IMPERIUM_DIR
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Process import Process
from test_code.Environment import Environment


class Services:
    _environment = None

    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    DEFAULT_BROWSER = 'chrome'

    # URL where selenium is running.
    DEFAULT_REMOTE_URL = "http://127.0.0.1:4444/wd/hub"

    __connection_established_notification = '//div[./div[contains(@class, \'Informational\')]]//div[text()=\'Connected to FMS Core\']'

    @property
    def environment (self):
        if not self._environment:
            self._environment = Environment()
        return self._environment


    def start_docker(self, service: str, image_name: str, container_args: dict, start_str_check: str=None) -> None:
        """
        Start Docker Service.
        NOTE: This is just a refrence to use docker python module. We are not using it for now, as it needs pywin32 which
        makes it hard to install on Windows.

        Examples:
            | Start Docker | {Docker_To_Start} (optional) |
        """
        import docker
        try:
            client = docker.from_env()
        except Exception as e:
            self.environment.env_log("Unable to start container. Please check docker is running", 'error')
            raise e

        process_output_file = os.path.join(self.environment.test_context.log_path, service + ".log").replace('\\', '/')
        process_error_file = os.path.join(self.environment.test_context.log_error_path, service + ".log").replace('\\', '/')
        self.environment.test_context.set('log_file', process_output_file, service)
        self.environment.test_context.set('error_log_file', process_error_file, service)

        if BuiltIn().get_variable_value('${DONOT_START_SERVICE}'):
            # Check if container running and use it, else skip.
            client = docker.from_env()
            container = client.containers.list({"name": service})
            if container:
                self.environment.test_context.set('container', container[0], service)
            else:
                raise Exception(f"Container {service} not running")
        else:
            container = client.containers.run(image_name, **container_args)
            self.environment.test_context.set('container', container, service)
            # Wait for docker instance to be ready.
            if start_str_check:
                timeout = self.environment.time_out * 1000
                while timeout:
                    for line in container.logs(stream=True):
                        line = line.decode('UTF-8').strip()
                        self.environment.env_log(line, 'trace')
                        if start_str_check in line:
                            return True
                        timeout -= 1


    def run_service(self, service: str, command: List, cwd: str=None, env: Dict={}, check_exit_code=True, do_not_start_service:bool=BuiltIn().get_variable_value('${DONOT_START_SERVICE}')) -> str:
        """
        Execute service and wait till it finish.
        Returns process op.

        Example:

            | ${process_handle}= | Run Service | SERVICE_NAME | COMMAND_TO_EXECUTE | PATH_TO_EXECUTE_FROM | ENV |
        """

        if not cwd:
            raise Exception("Pass working directory before executing command")

        if do_not_start_service:
            self.environment.env_log("Not running service: {}".format(service), 'trace')
            return True

        # Add common options which will be used.
        self.environment.test_context.create_process_context(service)
        self.environment.test_context.set('cmd', ' '.join(command), service)
        process_output_file = os.path.join(self.environment.test_context.log_path, service + ".log").replace('\\', '/')
        process_error_file = os.path.join(self.environment.test_context.log_error_path, service + ".log").replace('\\', '/')
        self.environment.test_context.set('log_file', process_output_file, service)
        self.environment.test_context.set('error_log_file', process_error_file, service)

        original_command = copy.deepcopy(command)

        command.append("shell=True")
        command.append("stderr=" + process_error_file)
        command.append("stdout=" + process_output_file)
        command.append("alias=" + service)
        command.append("cwd=" + cwd)
        command.append("timeout=5min")

        if BuiltIn().get_variable_value('${EXPORT_COMMAND}'):
            with open(self.environment.command_path, "a") as outfile:
                outfile.write(f"# Executing {service}\n")
                outfile.write(f"cd {cwd}\n")

        # Add environment variables.
        for env_key, env_value in env.items():
            command.append(f"env:{env_key}={env_value}")
            if BuiltIn().get_variable_value('${EXPORT_COMMAND}'):
                with open(self.environment.command_path, "a") as outfile:
                    outfile.write(f"export {env_key}='{env_value}'\n")

        self.environment.env_log("Executing {}: {}\n {}".format(service, cwd, ' '.join(original_command)), 'debug')
        if BuiltIn().get_variable_value('${EXPORT_COMMAND}'):
            with open(self.environment.command_path, "a") as outfile:
                outfile.write(' '.join(original_command) + '\n')

        result = BuiltIn().run_keyword('Run Process', *command)
        if check_exit_code and result.rc != 0:
            if os.path.exists(process_output_file):
                with open(process_output_file) as f_in:
                    lines = f_in.readlines()
                    error = "="*30 + "\n" + "".join([line for line in lines if line and line != "\n"]) + '='*30
            raise Exception(f"[Error] Unable to execute {service}\n{error}")
        return result.stdout


    def start_service(self, service: str, command: List, cwd: str=None, env: Dict={}, is_docker: bool=False, do_not_start_service: bool=None):
        """
        Start service in background and returns process handle.

        Examples:

            | ${process_handle}= | Start Service | COMMAND_LIST |
        """
        
        if do_not_start_service is None:
            do_not_start_service = BuiltIn().get_variable_value('${DONOT_START_SERVICE}')

        if do_not_start_service:
            return True

        if not cwd:
            raise Exception(f"Pass working directory before executing command: {cwd}")

        self.environment.test_context.create_process_context(service)
        self.environment.test_context.set('cmd', ' '.join(command), service)
        process_output_file = os.path.join(self.environment.test_context.log_path, service + ".log").replace('\\', '/')
        process_error_file = os.path.join(self.environment.test_context.log_error_path, service + ".log").replace('\\', '/')
        self.environment.test_context.set('log_file', process_output_file, service)
        self.environment.test_context.set('error_log_file', process_error_file, service)
        self.environment.test_context.set('is_docker', is_docker, service)

        # Set process o/p logs.
        configuration = []
        configuration.append("shell=True")
        configuration.append("stderr=" + process_error_file)
        configuration.append("stdout=" + process_output_file)
        # configuration.append("alias=" + service)
        configuration.append("cwd=" + cwd)

        original_arguments = copy.deepcopy(command)

        if BuiltIn().get_variable_value('${EXPORT_COMMAND}'):
            with open(self.environment.command_path, "a") as outfile:
                outfile.write(f"# Starting {service}\n")
                outfile.write(f"cd {cwd}\n")

        self.environment.env_log("-- Starting {}: {} --".format(service, cwd), 'debug')

        # Add environment variables.
        for env_key, env_value in env.items():
            command.append(f"env:{env_key}={env_value}")
            self.environment.env_log(f"export {env_key}='{env_value}'", 'debug')
            if BuiltIn().get_variable_value('${EXPORT_COMMAND}'):
                with open(self.environment.command_path, "a") as outfile:
                    outfile.write(f"export {env_key}='{env_value}'\n")

        self.environment.env_log("Command: {}".format(subprocess.list2cmdline(original_arguments)).replace("\=", "="), 'debug')
        if BuiltIn().get_variable_value('${EXPORT_COMMAND}'):
            with open(self.environment.command_path, "a") as outfile:
                outfile.write(' '.join(command) + ' &> ${logs}/' + f'{service}.log &\n')
                outfile.write('sleep ${delay_between_services}\n')

        command = command + configuration
        process_handle = BuiltIn().run_keyword('Start Process', *command)

        if not process_handle:
            with open(process_output_file, 'r') as f_in:
                self.environment.env_log('Tail of process output: \n%s' % '\n'.join(f_in.read().splitlines()[-50:]),
                         'error')
            msg = "Unable to start service {}".format(service)
            # Stop all services before throwing exception, else it will get into hang state,
            BuiltIn().run_keyword('Stop All Services')
            raise Exception(msg)

        self.environment.test_context.watch_log_file(process_output_file)

        self.environment.test_context.set('process_handle', process_handle, service)

        if self.environment.service_start_delay:
            BuiltIn().run_keyword('Sleep', self.environment.service_start_delay)

        return process_handle


    def stop_service(self, service_name: str, clean_process: bool=True, do_not_start_service:bool=BuiltIn().get_variable_value('${DONOT_START_SERVICE}')) -> None:
        """
        Set 1 sec timeout for process to terminate, if it can't gracefully terminate in 1 sec, then it should be killed.

        'Terminate Process' API sends the 'SIGTERM' to terminate process and waits for 30 seconds, if it can't grecefully
        terminate after 30 sec, then it kills process. This increases time of each robot test. So to reduce the time
        of robot test use this API, which sets grecefully terminate timeout to 1 sec.

        Example:

            | Stop Service | SERVICE_NAME_TO_STOP |
        """

        BuiltIn().run_keyword('Remove Service Pid', service_name)

        # If this is called from teardown and there is no process created, then don't do anything.
        if not self.environment.test_context.process_exists(service_name):
            return False

        # Get the name and handle of process or container.
        container = self.environment.test_context.get('container', service_name)
        if container:
            try:
                container.stop()
            except Exception:
                self.environment.env_log(f"Unable to stop docker for {service_name}")
            if clean_process:
                del self.environment.test_context.processes[service_name]
            return

        is_docker = self.environment.test_context.get('is_docker', service_name)
        if is_docker:
            self.stop_docker(service_name, do_not_start_service)
            if clean_process:
                del self.environment.test_context.processes[service_name]
            return

        process_handle = self.environment.test_context.get('process_handle', service_name)

        self.environment.env_log("Stopping process {}".format(service_name), 'Debug')
        # If we are running coverage, we want process to terminate gracefully, else just kill process.
        # Set terminate timeout.
        process_library = BuiltIn().run_keyword("Get Library Instance", "robot.libraries.Process")
        original_process_terminate_timeout = process_library.TERMINATE_TIMEOUT
        process_library.TERMINATE_TIMEOUT = 1
        BuiltIn().run_keyword("Terminate Process", process_handle)
        # Wait for defined timeout in sec and if process still exits, then kill it.
        BuiltIn().run_keyword("Wait For Process", process_handle, self.environment.time_out, 'kill')
        # Restore process terminate timeout.
        process_library.TERMINATE_TIMEOUT = original_process_terminate_timeout

        if clean_process:
            del self.environment.test_context.processes[service_name]


    def ensure_service_is_ready(self, service: str, start_text: str="started", error_log: bool=False, do_not_start_service=BuiltIn().get_variable_value('${DONOT_START_SERVICE}')) -> None:
        """
        We need to ensure is service running? This step will check logs and wait till
        specified start_text appears or timeout.

        Examples:

            | Ensure Service Is Ready | PROCESS_CONFIG_NAME | TEXT_DEFINING_SERVICE_IS_READY |
        """

        if do_not_start_service:
            self.environment.env_log("Not checking service logs: {}".format(service), 'trace')
            return True

        # Timeout is in sec. and we wait for 0.1 sec for each iteration and double default timeout, so multiply timeout
        # with 20 to wait for defined time.
        timeout = self.environment.time_out
        
        if error_log:
            log_file = self.environment.test_context.get('error_log_file', service)
        else:
            log_file = self.environment.test_context.get('log_file', service)
        increment = 0.1
        while not os.path.isfile(log_file) and timeout > 0:
            time.sleep(increment)
            timeout -= increment
        # This is to find if we have waited above for no reason. Log file can be created after sometime,
        # So we should wait above.
        if not os.path.isfile(log_file):
            raise Exception("Log file ({0}) is not available".format(log_file))

        log_data = ''
        with open(log_file) as log_file_handle:
            while timeout > 0 and start_text not in log_data:
                log_data = log_data[-20:] + log_file_handle.read()
                time.sleep(increment)
                timeout -= increment

        if start_text not in log_data:
            self.environment.env_log("Failed to find text '%s' in file %s'" % (start_text, log_file), 'warn')
            raise Exception("Service {} is not ready to execute test.".format(service))

        self.environment.env_log('service is ready', 'debug')

    def ensure_service_log_has_no_exceptions(self, service: str, noException: bool=False) -> bool:
        """
        Ensure there is no warning or Error in service log file.
        If 'noException' set to True, then exception won't be thrown and return value will be True if error.

        Examples:

            | Ensure Service Log Has No Exceptions | SERVICE | NO_EXCEPTION |
        """
        log_file = self.environment.test_context.get('log_file', service)
        errorFound = False
        if os.path.isfile(log_file):
            with open(log_file) as log_data:
                if any("Exception:" in line for line in log_data):
                    errorFound = True
                    if not noException:
                        raise Exception("Service {} log has exception, after executing test. Check {}".format(service, log_file))

        return errorFound


    def ensure_service_log_has(self, service: str, text_to_search: str, timeout: int=0) -> None:
        """
        Ensure service log has defined text

        Examples:
            | Ensure Service Log Has | PROCESS_CONFIG_NAME | TEXT_TO_SEARCH |
        """
        log_file = self.environment.test_context.get('log_file', service)

        timeout = self.environment.time_out if not timeout else timeout

        if not os.path.exists(log_file):
            raise Exception("Log file doesn't exist: {}".format(log_file))

        while timeout:
            with open(log_file) as log_data:
                if any(text_to_search in line for line in log_data):
                    return True
            time.sleep(1)
            timeout -= 1

        raise Exception("Expected text '{}' not found in log in: {}".format(text_to_search, log_file))


    def stop_all_services(self) -> List:
        """
        Stop all services started. if 'skip_error_check_in_log' set True then log file
        will not be checked for error.

        Examples:

            | ${errors}= | Stop All Services |
        """
        errors = []
        # Get list of all system processes, so we can check if we want to clean them forecfully.
        if not self.environment.test_context.processes:
            self.environment.env_log("No local processes to stop", 'trace')
            return errors

        for process_name, process_context in list(self.environment.test_context.processes.items()):
            if process_context.process_handle:
                # Check for error before stopping the service.
                if not self.environment.test_context.skip_error_check_in_log or self.environment.test_context.ensure_error_in_log:
                    if self.ensure_service_log_has_no_exceptions(process_context.name, True):
                        # Add this to report if we don't expect error in logs.
                        if not self.environment.test_context.ensure_error_in_log:
                            errors.append(process_context.name)
                    elif self.environment.test_context.ensure_error_in_log:
                        errors.append("Error was expected in {} log, but not found".format(process_context.name))

                BuiltIn().run_keyword('Stop Service', process_name, False)

            # TODO: Check error in container.
            if process_context.container:
                BuiltIn().run_keyword('Stop Service', process_name, False)

        self.environment.test_context.processes = {}

        if os.path.exists(self.environment.pid_path):
            os.remove(self.environment.pid_path)

        return errors


    def stop_docker(self, service: str, do_not_start_service:bool=BuiltIn().get_variable_value('${DONOT_START_SERVICE}')):
        """
        Stop docker service

        Examples:

            | Stop Docker | service |
        """
        self.run_service(f"{service}_stop", ['docker', 'stop', service], cwd=IMPERIUM_DIR, env={}, check_exit_code=False, do_not_start_service=do_not_start_service)


    def open_link_in_browser(self, url: str, title: str, default_remote_url: str) -> bool:
        """
        OPEN link in browser

        Examples:
        | Open Link In Browser | SERVICE | URL | TITLE |
        """
        # If browser is already opened, then just return that.
        if BuiltIn().get_variable_value('${BROWSER_OPENED}'):
            BuiltIn().run_keyword('Go To', url)
            BuiltIn().run_keyword('Title Should Be', title)
            return True

        browser = BuiltIn().get_variable_value('${BROWSER}')
        if not browser:
            browser = self.DEFAULT_BROWSER

        remote_url = BuiltIn().get_variable_value('${REMOTE_URL}')
        # changed to new code ####
        # if not remote_url:
        #     remote_url = default_remote_url
        # elif remote_url == 'local':
        #     remote_url = False
        #########
        if not remote_url and default_remote_url and default_remote_url != 'local':
            remote_url = default_remote_url
        elif remote_url == 'local' or not default_remote_url or default_remote_url == 'local':
            remote_url = False
        ##########
        desired_capabilities = None
        options = None
        executable_path = self.environment.driver_executable_path(browser)
        if browser == 'firefox':
            desired_capabilities = {
                'browserName': 'firefox',
                'acceptInsecureCerts': True,
            }
        elif browser == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('ignore-certificate-errors')
            options.add_argument('--disable-site-isolation-trials')
            options.add_argument("--disable-web-security") # don't enforce the same-origin policy
            # options.add_argument("--user-data-dir=/tmp") # applicable to windows os only
            options.add_argument('add_experimental_option("excludeSwitches",["ignore-certificate-errors"])')

        default_run_on_failure = BuiltIn().run_keyword('Register Keyword To Run On Failure', None)
        BuiltIn().run_keyword('Set Screenshot Directory', os.path.join(BuiltIn().get_variable_value('${OUTPUTDIR}'), 'screenshots').replace('\\', '/'))
        # Set initial timeout to be 2 sec if not defined
        selenium_timeout = BuiltIn().get_variable_value('${SELENIUM_TIMEOUT}')
        if selenium_timeout:
            BuiltIn().run_keyword('Set selenium Timeout', selenium_timeout)
        else:
            BuiltIn().run_keyword('Set selenium Timeout', 2)

        selenium_library = BuiltIn().get_library_instance('SeleniumLibrary')
        try:
            selenium_library.open_browser(url, browser, remote_url=remote_url,
               desired_capabilities=desired_capabilities, options=options, executable_path=executable_path)
            selenium_library.title_should_be(title)
            try_again = 0
        except Exception as e:
            try_again = self.environment.time_out
            pass
        
        while try_again:
            try:
                selenium_library.go_to(url)
                selenium_library.title_should_be(title)
                try_again = 0
            except Exception as e:
                BuiltIn().sleep(1, 'Wait for web service to be up')
                try_again -= 1
                if not try_again:
                    return False

        if title == 'FMS Field':
            try:
                BuiltIn().run_keyword('Wait Until Page Contains Element', self.__connection_established_notification)
            except:
                pass # we don't want to fail since it's possible to 'Connected to FMS Core' to appear before we reach here.

        BuiltIn().run_keyword('Register Keyword To Run On Failure', 'Capture Page Screenshot')

        # Set timeouts
        selenium_speed = BuiltIn().get_variable_value('${SELENIUM_SPEED}')
        if selenium_speed:
            BuiltIn().run_keyword('Set selenium Speed', selenium_speed)

        selenium_implicit_wait = BuiltIn().get_variable_value('${SELENIUM_IMPLICIT_WAIT}')
        if selenium_implicit_wait:
            BuiltIn().run_keyword('Set selenium Implicit Wait', selenium_implicit_wait)

        if not BuiltIn().get_variable_value('${BROWSER_OPENED_BY_SUITE}'):
            BuiltIn().set_test_variable('${BROWSER_OPENED}', True)
        return True