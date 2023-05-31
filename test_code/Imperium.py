__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import os
import requests
import json
import pendulum
import redis
import math
import httpx


from time import sleep
from typing import List, Dict, Any
from robot.libraries.BuiltIn import BuiltIn
from test_code.Const import SUPPORTED_SCREEN_RESOLUTIONS, \
                AUTOMATED_TEST_DIR, MAPS
from test_code.Environment import Environment
from test_code.ImperiumServices import ImperiumServices
from test_code.cache.FMSCache import FMSCache
from test_code.cache.FieldCache import FieldCache
from test_code.office.HomePage import HomePage
from test_code.services.asset_manager.AssetEndpoint import AssetEndpoint


class Imperium:
    _environment = None
    _imperium_services_object = None
    _imperium_services = None
    _docker_services = None
    fms_versions = {}

    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = "GLOBAL"


    @property
    def environment(self):
        if not self._environment:
            self._environment = Environment()
        return self._environment

    @property
    def imperium_services(self):
        return self.imperium_services_object.config.imperium_services

    @property
    def docker_services(self):
        return self.imperium_services_object.config.docker_services

    @property
    def imperium_services_object(self):
        if self._imperium_services_object:
            return self._imperium_services_object

        self._imperium_services_object = BuiltIn().get_library_instance('test_code.ImperiumServices')
        return self._imperium_services_object


    def open_link(self, url: str, title: str, in_docker: bool=True):
        """
        Open link

        Examples:
            | Open Link | URL | TITLE | In_DOCKER |
        """
        try_again = 0
        selenium_url = 'local'
        if in_docker:
            #http://127.0.0.1
            selenium_url = f"127.0.0.1:{self.imperium_services_object.selenium['port']}/wd/hub"
        while try_again < 5:
            try:
                BuiltIn().run_keyword('Open Link In Browser', url, title, selenium_url)
                break
            except Exception as e:
                try:
                    BuiltIn().run_keyword('Close Browser')
                except Exception as e:
                    pass
                BuiltIn().run_keyword('Sleep', 1)
                try_again +=1


        if not BuiltIn().get_variable_value('${BROWSER_OPENED_BY_SUITE}') and not self.environment.test_context.get('robot_eye_opened'):
            force_update_image = BuiltIn().get_variable_value('${FORCE_UPDATE_IMAGES}')
            start_port = self.imperium_services_object.start_port
            BuiltIn().run_keyword('Open Eyes', *['SeleniumLibrary', 0, '', None, force_update_image, start_port])
            self.environment.test_context.set('robot_eye_opened', True)


    def open_centurion(self, asset_id: str=None, skip_login=True) -> None:
        """
        Open Centurion web app

        Examples:
        | Open Centurion |
        """
        if not asset_id:
            asset_id = self.imperium_services_object.default_asset
        self.open_link(f"{self.imperium_services_object.get_service_url(f'Centurion_{asset_id}')}", 'FMS Field')
        BuiltIn().run_keyword('Set window size', SUPPORTED_SCREEN_RESOLUTIONS['Centurion'][0],
                    SUPPORTED_SCREEN_RESOLUTIONS['Centurion'][1], True)
        if skip_login:
            from test_code.field.login.LoginPage import LoginPage
            LoginPage().click_skip()


    def open_overwatch(self, skip_login=True) -> None:
        """
        Open Overwatch

        Examples:
        | Open Overwatch |
        """
        self.open_link(f"{self.imperium_services_object.get_service_url(f'Overwatch')}", 'FMS Office')
        BuiltIn().run_keyword('Set window size', SUPPORTED_SCREEN_RESOLUTIONS['Overwatch'][0],
                    SUPPORTED_SCREEN_RESOLUTIONS['Overwatch'][1], True)

        from test_code.office.LoginPage import LoginPage
        LoginPage().click_go_to_login()

        if skip_login:
            # Consecutive login can be skipped if the user is already logged in.
            try:
                from test_code.office.LoginPage import LoginPage
                LoginPage().click_skip()
            except Exception as e:
                pass


    def open_field_data_simulator(self) -> None:
        """
        Open Field Data Simulator

        Examples:
        | Open Field Data Simulator |
        """
        BuiltIn().run_keyword('Open Link In Browser', f'{self.imperium_services_object.get_service_url("DataSimulator")}/MapActions', 'Field Data Simulator', f"http://127.0.0.1:{self.imperium_services_object.selenium['port']}/wd/hub")
        BuiltIn().run_keyword('Set window size', SUPPORTED_SCREEN_RESOLUTIONS['DataSimulator'][0],
            SUPPORTED_SCREEN_RESOLUTIONS['DataSimulator'][1])

        # Make sure Data simulator is stable.
        BuiltIn().run_keyword('Sleep', 2)


    def load_lanes(self) -> None:
        """
        Load Lanes in FMS

        Examples:
        | Load Lanes |
        """
        data = os.path.join(BuiltIn().get_variable_value("${TEST_DATA_DIR}"), 'lane.json').replace('\\', '/')
        headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
        response = requests.post(f"http://{self.imperium_services_object.imperium_server_ip_address}:4010/LaneSegment", data=open(data, 'rb'), headers=headers)
        self.environment.env_log(response.text, 'debug')


    def set_asset_position_in_redis(self, for_service: str=None, x: int=0, y: int=0, z: int=0, yaw: int=0) -> None:
        """
        Sets asset position in redis

        Examples:
        | Set Asset Position In Redis |
        """
        for service, port in self.imperium_services_object.docker_services_port.items():
            if for_service and service != for_service:
                continue

            # Set Test Asset position in redis, to be used by tests.
            if service.startswith('Field_'):
                # Create redis connections, to be used by tests.
                redis_host = self.imperium_services_object.redis(service)['host']
                self.environment.test_context.redis_connections[service] = redis.Redis(host=redis_host, port=port, db=0)

                asset_id = service.split('_')[-1]
                self.environment.env_log(f'Setting {asset_id} position in redis {redis_host}:{port}', 'debug')
                if x==0:
                    x = MAPS['Hazelmere']['allowed_assets'][asset_id]['x']
                if y==0:
                    y = MAPS['Hazelmere']['allowed_assets'][asset_id]['y']
                if z==0:
                    z = MAPS['Hazelmere']['allowed_assets'][asset_id]['z']
                if yaw==0:
                    yaw = MAPS['Hazelmere']['allowed_assets'][asset_id]['yaw']
                FieldCache().set_asset_position(asset_id, x, y, z, yaw)

    def start_redis(self, for_service: str=None, add_new_asset=False) -> None:
        """
        Start redis for the service, Office/Field/FMS

        Examples:
        | Start Redis | Office |
        """
        
        overridevalue_do_not_start_service=BuiltIn().get_variable_value('${DONOT_START_SERVICE}')
        if add_new_asset:
            overridevalue_do_not_start_service=False
            
        for service, port in self.imperium_services_object.docker_services_port.items():
            if for_service and service != for_service:
                continue

            # Redis is only needed for Field, Office and FMS.
            if not (service.startswith('Field_') or service.startswith('Office') or service.startswith('FMS')):
                continue

            if BuiltIn().get_variable_value('${RUN_LOCAL_DOCKER}') in self.docker_services[f'redis_{for_service}']['run_options']:
                self.start_service_in_docker('redis_' + for_service, overridevalue_do_not_start_service)
            else:
                services_lib = BuiltIn().get_library_instance('test_code.Services')
                services_lib.start_service(f'redis_{service}', ['redis-server', '--port', str(port)], cwd=self.imperium_services_object.get_service_path(f'redis_{service}'))
                services_lib.ensure_service_is_ready(f'redis_{service}', 'Ready to accept connections')

            # Create redis connections, to be used by tests.
            self.environment.test_context.redis_connections[service] = redis.Redis(host=self.imperium_services_object.redis(for_service)['host'], port=port, db=0)

            # Set Test Asset position in redis, to be used by tests.
            if service.startswith('Field_'):
                self.set_asset_position_in_redis(for_service=service)


    def stop_redis(self, for_service: str=None, remove_asset=False) -> None:
        """
        Stop redis for a given service

        Examples:
        | Stop Redis | Office |
        """
        overridevalue_do_not_start_service=BuiltIn().get_variable_value('${DONOT_START_SERVICE}')
        if remove_asset:
            overridevalue_do_not_start_service=False

        services_lib = BuiltIn().get_library_instance('test_code.Services')
        services_lib.stop_service(f'redis_{for_service}', do_not_start_service=overridevalue_do_not_start_service)


    def start_service_in_docker(self, service_name: str=None, do_not_start_service:bool=None) -> None:
        """
        Start docker service

        Examples:
            | Start Service In Docker | {Docker_To_Start} (optional) |
        """

        # This can't be set in parameter initialisation as libspec will fail to document.
        if do_not_start_service is None:
            do_not_start_service = BuiltIn().get_variable_value('${DONOT_START_SERVICE}')

        # Ensure valid service name is passed.
        if service_name and service_name not in self.docker_services:
            raise Exception(f"Unknown service {service_name}, known services are:\n{', '.join(self.docker_services.keys())}")

        services_lib = BuiltIn().get_library_instance('test_code.Services')
        for service, options in self.docker_services.items():
            # Skip starting service which should not be started by default.
            if not service_name and 'do_not_start' in options and options['do_not_start']:
                self.environment.env_log(f'Ignoring {service}', 'info')
                continue
            if service_name and service_name != service:
                self.environment.env_log(f'Skipping running docker {service}', 'trace')
                continue

            # If docker is not supposed to run in env, then skip.
            if BuiltIn().get_variable_value('${RUN_LOCAL_DOCKER}') not in options['run_options']:
                if service.startswith('redis_') and (BuiltIn().get_variable_value('${RUN_LOCAL_DOCKER}') == 'local'):
                    BuiltIn().run_keyword('Start Redis', "_".join(service.split('_')[1:]))
                    continue
                self.environment.env_log(f'Skipping running docker {service} for {options["run_options"]} environment', 'trace')
                continue


            # Don't start docker for browser which is not used or remote url passed.
            if service in ['chrome', 'firefox']:
                if service != BuiltIn().get_variable_value('${BROWSER}'):
                    self.environment.env_log(f'Not starting {service}, as it is not the chosen browser', 'trace')
                    continue
                if BuiltIn().get_variable_value('${REMOTE_URL}'):
                    self.environment.env_log(f'Not starting {service}, remote url passed', 'debug')
                    continue

            if  do_not_start_service:
                self.environment.env_log(f'Not starting docker: {service}', 'trace')
                continue

            command, container_name = self.imperium_services_object.get_docker_command(service, default_port=True, return_list=True, name_suffix=BuiltIn().get_variable_value('${START_PORT}'))

            services_lib.start_service(container_name, command, cwd=self.imperium_services_object.get_service_path(service), env={}, is_docker=True, do_not_start_service=do_not_start_service)

            if 'start_string' in options and options['start_string']:
                services_lib.ensure_service_is_ready(container_name, options['start_string'], do_not_start_service)

            # Restore database for sqlserver
            if service == 'sqlserver' and BuiltIn().get_variable_value('${RESTORE_DB}'):
                self.restore_db()

            if BuiltIn().get_variable_value('${RUN_LOCAL_DOCKER}') in options['run_options'] and service.startswith('redis_'):
                # loop as connection not always active in time
                count = 0
                while count < 5:
                    try:
                        self.set_asset_position_in_redis(for_service="_".join(service.split('_')[1:]))
                        break
                    except:
                        count = count + 1
                        sleep(2)


    def start_web_app(self, service: str, do_not_start_service: bool=None) -> None:
        """
        Start Centurion - field web UI

        Examples:
            | Start Web App | Centurion |
        """
        if service not in self.imperium_services_object.web_app_services:
            raise Exception(f"Service not found, unable to start web app: {service}")

        if do_not_start_service is None:
            do_not_start_service = BuiltIn().get_variable_value('${DONOT_START_SERVICE}')

        services_lib = BuiltIn().get_library_instance('test_code.Services')
        if BuiltIn().get_variable_value('${COMPILE}'):
            services_lib.run_service(service, ['npm', 'install'], cwd=self.imperium_services_object.get_service_path(service), env=self.imperium_services[service]['environment'])
            services_lib.run_service(service, ['npm', 'run', 'build'], cwd=self.imperium_services_object.get_service_path(service), env=self.imperium_services[service]['environment'])
            # Run dotnet build to create config.js
            service_path = self.imperium_services_object.get_service_path(service, web_dot_net_path=True)
            services_lib.run_service(service, ['dotnet', 'build', '--no-incremental'], cwd=service_path, env=self.imperium_services[service]['environment'])

        # This is required for updating centurion and overwatch config.
        command, env, service_name = self.imperium_services_object.get_imperium_command(service, None, return_list=True, name_suffix=BuiltIn().get_variable_value('${START_PORT}'))
        if service_name.startswith('Centurion'):
            self.imperium_services_object.create_local_web_build_dir(service.split('_')[-1])
        elif service_name == 'Overwatch':
            self.imperium_services_object.create_local_web_build_dir()
        services_lib.start_service(service_name, command, cwd=self.imperium_services_object.get_service_path(service),
                                   env=env, do_not_start_service=do_not_start_service)
        services_lib.ensure_service_is_ready(service_name, "stop the server")


    def _get_docker_image(self, service: str) -> str:
        """
        Get latest version of imperium docker image which is used to run the service.
        """
        if not self.fms_versions:
            self.fms_versions = BuiltIn().get_variable_value('${DOCKER_VERSION}')
            if not self.fms_versions:
                self.fms_versions = self.imperium_services_object.get_latest_fms_version(self.imperium_services[service]['docker_image'])
                if not self.fms_versions:
                    raise Exception("Unable to get versions from Artifactory. Please check your credentials.")

        return f"artifactory.fmgl.com.au/docker-ams-fms/{self.imperium_services[service]['docker_image']}:{self.fms_versions}"


    def start_imperium_service(self, service: str, port: int=0, start_string=None, add_new_asset=False) -> None:
        """
        Start Imperium service

        Examples:
            | Start Imperium Service | SERVICE |
        """
        if self.environment.test_context.process_exists(service):
            env_vars = self.environment.test_context.get_process_context(service).get('env_vars')
            for key in env_vars:
                self.imperium_services[service]['environment'][key] = env_vars[key]

        overridevalue_do_not_start_service=BuiltIn().get_variable_value('${DONOT_START_SERVICE}')
        if add_new_asset:
            overridevalue_do_not_start_service = False
            
        if service not in self.imperium_services:
            raise Exception(f"Service not found, unable to start: {service}")

        is_docker = BuiltIn().get_variable_value('${RUN_LOCAL_DOCKER}').lower() == 'docker'

        # If webservice running locally then we use start web app
        if not is_docker and service in self.imperium_services_object.web_app_services:
            return BuiltIn().run_keyword("Start Web App", service, overridevalue_do_not_start_service)

        services_lib = BuiltIn().get_library_instance('test_code.Services')
        if BuiltIn().get_variable_value('${COMPILE}'):
            services_lib.run_service(service, ['dotnet', 'build', '--no-incremental'], cwd=self.imperium_services_object.get_service_path(service), env=self.imperium_services[service]['environment'])

        docker_version = None
        # If Service need to start as docker.
        if is_docker and 'docker_image' in self.imperium_services[service] and self.imperium_services[service]['docker_image']:
            self._get_docker_image(service)
            docker_version = self.fms_versions
        command, env, service_name = self.imperium_services_object.get_imperium_command(service, docker_version, return_list=True, name_suffix=BuiltIn().get_variable_value('${START_PORT}'))

        services_lib.start_service(service_name, command, cwd=self.imperium_services_object.get_service_path(service, is_docker), env=env, is_docker=is_docker, do_not_start_service=overridevalue_do_not_start_service)
        if start_string:
            services_lib.ensure_service_is_ready(service_name, start_string, do_not_start_service=overridevalue_do_not_start_service)
        else:
            services_lib.ensure_service_is_ready(service_name, self.imperium_services_object.get_service_start_string(service, port), do_not_start_service=overridevalue_do_not_start_service)


    def stop_imperium_service(self, service: str, remove_asset:bool=False) -> None:
        """
        Stop Imperium Service

        Examples:
            | Stop Imperium Service | SERVICE |
        """
        overridevalue_do_not_start_service=BuiltIn().get_variable_value('${DONOT_START_SERVICE}')
        if remove_asset:
            overridevalue_do_not_start_service=False
            
        if service not in self.imperium_services:
            raise Exception(f"Service not found, unable to stop: {service}")

        services_lib = BuiltIn().get_library_instance('test_code.Services')
 
        services_lib.stop_service(service, do_not_start_service=overridevalue_do_not_start_service)


    def start_all_imperium_services_for_smoke_test(self) -> None:
        """
        Start imperium services to run against test/dev environment.

        Examples:
            | Start All Imperium Services For Smoke Test |
        """
        BuiltIn().run_keyword('Start Service In Docker', f'redis_Field_{self.imperium_services_object.default_asset}')
        BuiltIn().run_keyword('Start Service In Docker', 'redis_Office')
        BuiltIn().run_keyword('Start Service In Docker', BuiltIn().get_variable_value('${BROWSER}'))
        for service in self.imperium_services_object.smoke_test_services:
            BuiltIn().run_keyword("Start Imperium Service", service)


    def start_all_imperium_services(self) -> None:
        """
        Start all Imperium Services

        Examples:
            | Start all Imperium Services |
        """
        BuiltIn().run_keyword('Start Service In Docker')

        # Create list of services which need to be started.
        services_to_start = []
        for service in self.imperium_services_object.config.fms_start_sequence:
            config = self.imperium_services_object.config.imperium_services[service]
            if config.get('do_not_start', False):
                continue
            services_to_start.append(service)

        services_started = 0
        for service in services_to_start:
            start_string = None
            # Seed environment before starting AssetDistributor Service.
            if service == 'AssetDistributorService':
                BuiltIn().run_keyword('Seed Imperium environment')

            if 'start_string_before_restart' in self.imperium_services[service]:
                start_string = self.imperium_services[service]['start_string_before_restart']
            BuiltIn().run_keyword("Start Imperium Service", service, 0, start_string)

            if 'seed_and_restart' in self.imperium_services[service]:
                BuiltIn().run_keyword("Stop Service", service)
                BuiltIn().run_keyword("Connect To Database", 'pymssql', 'AssetManager', 'sa', 'SupaDupaSecret!!!!',
                    self.imperium_services_object.sql()['host'], self.imperium_services_object.sql()['port'])
                db_script_path = os.path.join(AUTOMATED_TEST_DIR, 'test_data', self.imperium_services[service]['seed_and_restart']).replace('\\', '/')
                BuiltIn().run_keyword("Execute Sql Script", db_script_path)
                BuiltIn().run_keyword("Start Imperium Service", service)
            services_started += 1
            self.environment.env_log(f"** {services_started}/{len(services_to_start)} services started...")

    def stop_docker_services(self) -> None:
        """
        Stop all docker services

        Examples:
            | Stop Docker Services |
        """
        for service in self.docker_services.keys():
            BuiltIn().run_keyword("Stop Docker", service)


    def seed_imperium_environment(self):
        """
        Seed imperium environment with lanes, assets etc.

        Examples:
        | Seed Imperium environment |
        """

        params = [
            'dotnet',
            'run',
            'seed',
            '--environment',
            'Hazelmere',
            '--mineModelApi',
            self.imperium_services_object.get_service_url("MineModelService"),
            '--assetManagerApi',
            self.imperium_services_object.get_service_url("AssetManager"),
            '--stumpServiceApi',
            self.imperium_services_object.get_service_url("StateTimeUsageModelProvider"),
            '--identityServiceApi',
            self.imperium_services_object.get_service_url("IdentityService"),
        ]
        services_lib = BuiltIn().get_library_instance('test_code.Services')
        services_lib.run_service('SeedEnvironmentBuild', ['dotnet', 'build', '--no-incremental'], self.imperium_services_object.get_service_path('SeedEnvironment'))
        services_lib.run_service('SeedEnvironment', params, self.imperium_services_object.get_service_path('SeedEnvironment'), check_exit_code=False)
        services_lib.ensure_service_is_ready('SeedEnvironment', self.imperium_services_object.get_service_start_string('SeedEnvironment').format('Hazelmere'))


    def get_data_from_message(self, message: str, key1: str, key2: str, ) -> str:
        """
        Gets data from a 2-D dictionary for the given dictionary keys

        Examples:
        | Get Data From Message | Message | TelemetryData | TelemetryReading
        """
        self.environment.env_log(f"{message}")
        if not message[2:-1]:
            raise Exception(f"Unable to extract message from {message}")
        message_b = json.loads(message[2:-1])
        value = (message_b.get(key1))[0][key2]

        return value

    def get_version_from_docker(self, service: str) ->  str:
        """
        Gets the FMS version for the given service

        Examples:
        | Get FMS version from Docker
        """
        expected_version = self._get_docker_image(service)
        expected_version = expected_version.split(':', 1)[1].split('-', 1)[0]

        return expected_version

    def set_service_environment_variable(self, service:str, env_var:str, value:str):
        """ Sets the Environment Variable for the deployment of a service

        Args:
            service (str): the service
            env_var (str): the environment variable
            value (str): the value to set the environment variable

        Examples:
            | Set Service Environment Variable | Asset State Reporting Service | FeatureToggles__RulesEngineUseConfiguredRuleSets | true |
        """
        self.environment.test_context.create_process_context(service)
        env_vars = self.environment.test_context.get_process_context(service).get('env_vars')
        env_vars[env_var] = value
        self.environment.test_context.get_process_context(service).set('env_vars', env_vars)
