__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

"""
Listener to add hooks in start/end of suite/test.
"""

import os
import traceback
import shutil
import signal


from robot.model import Body, BodyItem, If, For, Keyword, Message, TestCase
from robot.running.model import UserKeyword
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from test_code.Environment import Environment
from test_code.Const import MAPS


class Listener(object):
    """
    Global scope library listener for robot test.
    """

    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    # Tag which will avoid error log check in log file.
    SKIP_LOG_ERROR_CHECK = 'skip_log_error_check'

    # Tag which will ensure there is an error in process log.
    ENSURE_ERROR_IN_LOG = 'ensure_error_in_log'

    RESTORE_DB = 'restore_db'

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.exception = False


    def start_suite(self, suite, attributes):
        """
        Starts the suite.

        Examples:
            | Start Suite | SUITE_NAME | ATTRIBUTES_TO_START |
        """
        testframework_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        test_dat_dir = os.path.join(testframework_dir, 'test_data').replace('\\', '/')

        BuiltIn().set_suite_variable('${TEST_FRAMEWORK_DIR}', testframework_dir)
        BuiltIn().set_suite_variable('${TEST_DATA_DIR}', test_dat_dir)
        BuiltIn().set_suite_variable('${DRIVER_DIR}', os.path.join(testframework_dir, 'drivers').replace('\\', '/'))
        BuiltIn().set_suite_variable('${IMPERIUM_DIR}', os.path.dirname(testframework_dir).replace('\\', '/'))
        BuiltIn().set_suite_variable('${CURDIR}', os.path.dirname(str(suite.source)).replace('\\', '/'))
        BuiltIn().set_suite_variable('${images_dir}', os.path.join(os.path.dirname(str(suite.source)), 'images').replace('\\', '/'))
        # Set default asset id which is used for tests
        BuiltIn().set_suite_variable('${DEFAULT_ASSET_ID}', MAPS['Hazelmere']['default_asset'])

        BuiltIn().run_keyword('Import Library', 'test_code.ImperiumServices')
        imperium_services = BuiltIn().get_library_instance('test_code.ImperiumServices')
        release = str(BuiltIn().get_variable_value('${RELEASE}'))
        if str(BuiltIn().get_variable_value('${RUN_LOCAL_DOCKER}')) == 'local':
            release = str(BuiltIn().get_variable_value('${RUN_LOCAL_DOCKER}'))

        run_env = BuiltIn().get_variable_value('${RUN_ENV}')
        output_dir = BuiltIn().get_variable_value('${OUTPUTDIR}')
        testdata_dir = BuiltIn().get_variable_value('${TEST_DATA_DIR}')
        start_port = BuiltIn().get_variable_value('${START_PORT}')
        if start_port:
            start_port = int(start_port)
        host_ip = BuiltIn().get_variable_value('${HOST_IP}')

        imperium_services.init(release, run_env, output_dir, testdata_dir, start_port=start_port, 
                timeout=BuiltIn().get_variable_value('${TIMEOUT}'), dotnet_build_on_run=False, host_ip_addr=host_ip,
                https=True)

        BuiltIn().set_suite_variable('${DB_HOST}', imperium_services.sql()['host'])
        BuiltIn().set_suite_variable('${DB_PORT}', imperium_services.sql()['port'])
        BuiltIn().set_suite_variable('${DB_SA_PASSWORD}', imperium_services.sql()['password'])
        BuiltIn().run_keyword('Import Library', 'robot.libraries.Process')
        BuiltIn().run_keyword('Import Library', 'SeleniumLibrary')
        BuiltIn().run_keyword('Import Library', 'DebugLibrary')
        BuiltIn().run_keyword('Import Library', 'DatabaseLibrary')
        BuiltIn().run_keyword('Import Library', 'test_code.RobotEyes')
        BuiltIn().run_keyword('Import Library', 'test_code.Environment')
        BuiltIn().run_keyword('Import Library', 'test_code.Services')
        BuiltIn().run_keyword('Import Library', 'test_code.Imperium')

        if BuiltIn().get_variable_value('${INTERACTIVE}'):
            testcase = suite.tests.create(name='Debug mode', tags=['service_only_run'])

            testcase.body.append(Keyword(name='Debug'))
            keyword_name = f'Debug'
            ukw = UserKeyword(name=keyword_name)
            ukw.body = testcase.body
            suite.resource.keywords.append(ukw)
            testcase.body.clear()
            testcase.body.create_keyword(name=keyword_name)

        env = Environment()
        env.initialize_environment()
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        logger.console("Stopping all services as signal captured...")
        services = BuiltIn().get_library_instance('test_code.Services')
        services.stop_all_services()
        BuiltIn().run_keyword('Fatal Error')
        raise SystemExit()

    def start_test(self, test, attributes):
        """
        Setup Test environment

        Examples:
            | Start Test | TEST_NAME | ATTRIBUTES_TO_START |
        """
        skip_error_check_in_log = False
        ensure_error_in_log = False

        # Extended timeout used by tests.
        if not BuiltIn().get_variable_value('${EXTENDED_TIMEOUT}'):
            BuiltIn().set_test_variable('${EXTENDED_TIMEOUT}', 3600)

        # If test tag is close_fms_before_test, then open a new FMS for the test with specific context
        tags = [x.lower() for x in attributes.tags]
        for tag in attributes.tags:
            if tag == self.SKIP_LOG_ERROR_CHECK:
                skip_error_check_in_log = True
            # Check if error in log is generated.
            if tag == self.ENSURE_ERROR_IN_LOG:
                ensure_error_in_log = True
            # Checek if test want to skip db init
            if tag == self.RESTORE_DB:
                BuiltIn().set_test_variable('${RESTORE_DB}', True)
        logger.info("Test Environment set for {}".format(test))

        env = Environment()
        env.initialize_environment()

        # If there is a failure coming from last test execution then environment set will fail.
        try:
            env.test_context.skip_error_check_in_log = skip_error_check_in_log
            env.test_context.ensure_error_in_log = ensure_error_in_log
        except Exception as e:
            logger.console("\n-- ** Error while setting test environment ** --")
            logger.console("\n " + traceback.format_exc(e))
            raise e


    def _end_test_suite(self, test, attributes, is_suite):
        """
        Common test teardown.
        - Stop Robot publisher
        - Stop Robot subscriber
        - Send termination for each started process
        - Wait for each process to finish.

        Examples:

            | End Test | TEST_NAME |
        """
        process_error = None
        # Close any open broser.
        if BuiltIn().get_variable_value('${BROWSER_OPENED}') or (is_suite and BuiltIn().get_variable_value('${BROWSER_OPENED_BY_SUITE}')):
            if attributes.status!='PASS':
                #take screenshot for troubleshooting as not all failures will have a screenshot
                try:
                    old_log_level = BuiltIn().run_keyword('Set Log Level', 'INFO')
                    BuiltIn().run_keyword('Capture Page Screenshot')
                    BuiltIn().run_keyword('Set Log Level', old_log_level)
                except Exception:
                    pass
            # Closing browser can fail because of selenium timeout.
            try:
                BuiltIn().run_keyword('Close Browser')
            except Exception:
                pass
            if not is_suite:
                BuiltIn().set_test_variable('${BROWSER_OPENED}', False)
            BuiltIn().set_suite_variable('${BROWSER_OPENED_BY_SUITE}', False)

        process_error = BuiltIn().run_keyword("Stop All Services")

        if process_error:
            process_error = "\n** Errors found in log for process:\n{}".format(process_error)

        test_error = None
        env = Environment()
        if env.test_context.errors:
            test_error = "\n** Error in test execution: **\n - {}".format("\n- ".join(env.test_context.errors))
        # Raise exception in the end, as we don't generate exception while checking for errors.
        # Reason being, we need to stop all services after checking log for error.
        # At this point we have stopped all our services and cleaned environment, so it's safe to report
        # What services have error.
        if process_error or test_error:
            logger.console(test_error if test_error else process_error)

        if BuiltIn().get_variable_value('${CLEAN_LOGS}') and is_suite:
            log_dir = os.path.join(BuiltIn().get_variable_value('${OUTPUTDIR}'), 'log')
            if os.path.exists(log_dir):
                try:
                    shutil.rmtree(log_dir, ignore_errors=True)
                except Exception as e:
                    pass


    def end_test(self, test, attributes):
        self._end_test_suite(test, attributes, False)

    def end_suite(self, suite, attributes):
        self._end_test_suite(suite, attributes, True)