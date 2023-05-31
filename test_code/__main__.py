__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

"""
Implementing the command line entry point for executing tests.
"""

import os
import sys
import shutil
import argparse
import collections


from robot.run import run_cli


# Import this library, as this can be executed from different directory.
automated_test_dir_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/')
sys.path.insert(0, automated_test_dir_path)

# Add driver path for selenium.
os.environ["PATH"] += os.pathsep + os.path.join(automated_test_dir_path, 'drivers').replace('\\', '/')

# This is locally maintained copy with modifications to allow us manage image diff using robotframework-eyes
# This library is installed using poetry as it download's all other dependencies
sys.path.append(os.path.join(automated_test_dir_path, 'RobotEyes').replace('\\', '/'))

USAGE = """Robot Framework -- An automation test framework for imperium acceptance testing.

Usage:  python -m test_code test_cases

Robot Framework is a Python-based keyword-driven test automation framework for
acceptance level testing and acceptance test-driven development (ATDD).

It is used with RobotEyes, which uses image diff using imagemagik

Options
=======
{}

Examples
========

# Example to execute test
$ python -m test_code test_cases

"""

TEST_VARIABLES = collections.OrderedDict([
    ("Imperium Options", collections.OrderedDict([
        ('**compile**', [
            "COMPILE",
            "c",
            "Compile code before starting service (Default: False)",
            "store_true"
        ]),
        ('**interactive**', [
            "INTERACTIVE",
            "Start interactive test, which will let user put keyword on terminal (Default: False)",
            "store_true"
        ]),
        ('**skip_start_service**', [
            "DONOT_START_SERVICE",
            "s",
            "DONOT start any service, it has been started by start_fms.py -i chrome -r local(Default: False)",
            "store_true"
        ]),
        ('**update_images**', [
            "FORCE_UPDATE_IMAGES",
            "Force update base images for visual diff (Default: False)",
            "store_true"
        ]),
        ('docker', [
            "DOCKER_VERSION",
            "DOCKER VERSION to use, if not set, will try use latest version (Default: None)",
            0
        ]),
        ('service', [
            "SERVICE",
            "Service/s to start/stop, comma separated list(Default: all)",
            "all"
        ]),
        ('timeout', [
            "TIMEOUT",
            "Timeout for a service to start in seconds (Default: 30)",
            30
        ]),
        ('max_wait', [
            "MAX_WAIT",
            "Timeout for an element to appear (Default: 10)",
            10
        ]),
        ('start_delay',[
            "START_DELAY",
            "Delay to be added between service start (Default: 0)",
            0
        ]),
        ('env',[
            "RUN_ENV",
            "Run test against the environment (default: None)",
            "",
            ['dev', 'test', 'int', 'stg'],
        ]),
        ('release',[
            "RELEASE",
            "Run test against the release candidate (default: master)",
            "master",
            ['master', 'rc'],
        ]),
        ('run',[
            "RUN_LOCAL_DOCKER",
            "Run test using docker or local (default: local)",
            "local",
            ['local', 'docker'],
        ]),
        ('ip',[
            "HOST_IP",
            "Host IP address, if started using start_fms.py (default: None)",
            '',
        ]),
        ('port',[
            "START_PORT",
            "Network port to start FMS services (default: None)",
            '',
        ]),
        ('**clean_logs**', [
            "CLEAN_LOGS",
            "Delete logs dir after execution (Default: False)",
            "store_true"
        ]),
    ])),
    ("Browser Options", collections.OrderedDict([
        ('browser', [
            "BROWSER",
            "b",
            "Browser to run tests with (Default: chrome)",
            "chrome"
        ]),
        ('selenium_timeout', [
            "SELENIUM_TIMEOUT",
            "How long these keywords should wait for certain events or actions.",
            ""
        ]),
        ('selenium_speed', [
            "SELENIUM_SPEED",
            "Selenium execution speed can be slowed down globally",
            ""
        ]),
        ('selenium_implicit_wait', [
            "SELENIUM_IMPLICIT_WAIT",
            "How long Selenium waits when searching for elements",
            ""
        ]),
        ('remote_url', [
            "REMOTE_URL",
            "Selenium remote url http://127.0.0.1:4444/wd/hub, passing local will use local browser",
            ""
        ]),
    ])),
])


def main():
    parser = argparse.ArgumentParser(description='FMS acceptance test', add_help=False)
    parser.add_argument('-u', '--usage', action='store_true')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-t', '--trace', action='store_true')
    parser.add_argument('-k', '--key_verbose', action='store_true')

    options = ["%-15s  %-35s" % ('-u, --usage', 'Show supported fms options')]
    options += ["%-15s  %-35s" % ('-d, --debug', 'Show debug log messages on console')]
    options += ["%-15s  %-35s" % ('-t, --trace', 'Show trace log messages on console')]
    options += ["%-15s  %-35s" % ('-k, --key_verbose', 'Show all keywords on console')]

    # Add all supported variables for fms automated tests as options.
    for key, group in list(TEST_VARIABLES.items()):
        options.append("\n======== {} ========".format(key))
        for key, value in list(group.items()):
            if key.endswith('**') and key.startswith('**'):
                action = 'store_true'
                if len(value) == 4:
                    action = value[3]
                key = key.replace('**', '')
                parser.add_argument(f'-{value[1]}', f'--{key}', action=action, help=value[2])
            else:
                if len(value) == 4:
                    if isinstance(value[3], list):
                        parser.add_argument('--{}'.format(key), help=value[1], default=value[2], choices=value[3])
                    else:
                        parser.add_argument(f'-{value[1]}', '--{}'.format(key), help=value[2], default=value[3])
                else:
                    parser.add_argument(f'-{value[1]}', '--{}'.format(key), help=value[2])
            if len(value) == 4:
                if isinstance(value[3], list):
                    options.append("%-15s %-15s %-35s" % (('--' + key), value[0][:15], value[1]))
                else:
                    options.append("-%-1s %-15s %-35s" % ((value[1] + ', --' + key), value[0][:15], value[2]))
            else:
                options.append("%-15s %-15s %-35s" % (('--' + key), value[0][:15], value[1]))

    # Parse options.
    parsedargs, passed_command_options = parser.parse_known_args()

    # If passed usage, then show usage and exit.
    if parsedargs.usage:
        print(USAGE.format("\n".join(options)))
        return

    # List of test tags which need to be excluded from run.
    disable_tags = []
    if '-i' not in passed_command_options and '--include' not in passed_command_options:
        disable_tags.append('disable')

    # Parse allowed robot variables.
    robot_command_options = []
    for key, group in list(TEST_VARIABLES.items()):
        for key, value in list(group.items()):
            parsedkey = getattr(parsedargs, key.replace('**', ''))
            if parsedkey:
                robot_command_options += ['--variable', value[0]+':'+str(parsedkey)]

    output_dir = os.path.join(os.path.dirname(automated_test_dir_path), 'output').replace('\\', '/')
    if parsedargs.port:
        output_dir = os.path.join(output_dir, f'{parsedargs.port}')
    robot_command_options += [
        "--listener", "Listener.Listener",
        "--outputdir", output_dir
    ]
    if parsedargs.key_verbose or parsedargs.debug:
        robot_command_options += [
            "--listener", "ListenerPrintKeywords.ListenerPrintKeywords",
        ]

    # Do not delete output folder if not starting services.
    if not parsedargs.skip_start_service:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir, ignore_errors=True)
        os.makedirs(output_dir, exist_ok=True)
    else:
        # This needs starting service like data simulator.
        disable_tags.append('need_service_start')

    # If debug, then set debug level.
    if parsedargs.debug:
        robot_command_options += ['-L', 'DEBUG']

    # If trace, then set debug level.
    if parsedargs.trace:
        robot_command_options += ['-L', 'TRACE']

    # Run test against environment
    if parsedargs.env:
        # Only run smoke tests
        robot_command_options += ['-i', "smoke"]
        if parsedargs.port:
            raise Exception("Don't change port for smoke tests, as this will fail with hosted FMS")
    else:
        robot_command_options += ['--variable', f"RUN_ENV:"]
        # Exclude smoke tests
        disable_tags.append("smoke")

    # Default timeout is 30 sec.
    if not parsedargs.timeout:
        robot_command_options += ['--variable', "TIMEOUT:30"]

    # Default timeout is 10 sec.
    if not parsedargs.max_wait:
        robot_command_options += ['--variable', "MAX_WAIT:10"]

    # Ignore tests which are specific for environment local/docker.
    if parsedargs.run and parsedargs.run == 'local':
        disable_tags.append('env_docker')
    if parsedargs.run and parsedargs.run == 'docker':
        disable_tags.append('env_local')
        # Increase timeout for docker runs
        if not parsedargs.timeout or int(parsedargs.timeout) == 30:
            robot_command_options += ['--variable', "TIMEOUT:120"]

    # Exclude all unwanted tests
    robot_command_options += ['-e', 'OR'.join(disable_tags)]

    # Only run tests which have image compare tags.
    if parsedargs.update_images:
        robot_command_options += ['-i', 'image_compare']

    if parsedargs.interactive:
        robot_command_options += ['-i', 'service_only_run']
        robot_command_options += ['--runemptysuite']

    robot_command_options += passed_command_options

    if parsedargs.debug:
        print("\n** Executing following command to execute robot test: \npython -m test_code {}".format(" ".join(robot_command_options)))
    run_cli(robot_command_options)


if __name__ == '__main__':
    main()