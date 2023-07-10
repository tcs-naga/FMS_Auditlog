__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

"""
IMPORTANT:

This file is being used by scripts and outside robot framework. Please do not add
any robot framework dependency.
"""

import copy
import collections
import os
import glob
import socket, errno
import requests
import pendulum
import shutil
import subprocess


from time import sleep
from typing import Dict, List
from test_code.Const import ARTIFACTORY_DOCKER_URL, MAPS, SUPPORTED_SCREEN_RESOLUTIONS, \
    AUTOMATED_TEST_DIR, IMPERIUM_DIR, BROWSER_DRIVER, \
    ARTIFACTORY_DOCKER_URL, DEPLOYED_ENVS, ASSET_PORTS_START, \
    ARTIFACTORY_DOCKER_IMAGE_PREFIX, ARTIFACTORY_URL

from dynaconf import Dynaconf, loaders, settings

class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ImperiumServices(metaclass=Singleton):

    """
    Single instance of this class, as Environment is created once per execution.
    """
    def __init__(self, release: str='master', run_env: str=None, output_dir: str=None,
        testdata_dir: str=None, map: str='Hazelmere', debug: str='Information',
        fms_bridge_domain: str=None, fms_bridge_robot_ip: Dict={},
        host_ip_addr: str=None, start_port: int=None, timeout: int=10, participant_id: Dict={},
        dotnet_build_on_run: bool=True, https: bool=False) -> None:

        """
        run_env defines imperium service running against which environment.
        it can be None/test/dev/hazelmere. None means local environment as dotnet or docker.

        :params: release - [master|rc|local], if master or rc then docker will be used, local will use dotnet code.
        :params: run_env [test|dev|hazelmere]
        """
        self.init(release, run_env, output_dir, testdata_dir, map, debug, fms_bridge_domain, fms_bridge_robot_ip,
                host_ip_addr, start_port, timeout, participant_id, dotnet_build_on_run, https)

        # Used for docker network if used by script
        self.docker_network = None

    def set_docker_network(self, network_name: str):
        """
        Use docker network
        """
        self.docker_network = network_name
        return subprocess.list2cmdline(['docker', 'network', 'create', '--driver', 'bridge', self.docker_network])

    def delete_docker_network(self):
        """
        Remove docker network
        """
        self.docker_network = None
        return subprocess.list2cmdline(['docker', 'network', 'rm', self.docker_network])

    def update_config(self, value):
        """
        Update config read for fms and docker.
        """
        if type(value) == int:
            return str(value)
        elif type(value) == str:
            return self.substitute_config_value(value)
        elif isinstance(value, list):
            return [self.update_config(i) for i in value] 
        elif isinstance(value, collections.abc.Mapping):
            return {k: self.update_config(i) for k, i in value.items()}
        else:
            return value

    def substitute_config_value(self, value: str):
        """
        Substitute dynaconf config value with env which it's being used for.
        """
        supported_value_substitute_strings = [
            '#{redis-fms-uri}',
            '#{redis-field-uri}',
            '#{redis-office-uri}',
            "#{zipkin}",
            "#{rabbitmq-uri}",
            "#{init-pear}",
            "#{map-x}",
            "#{map-y}",
        ]

        # Convert int to string, as we need to concatenate value for env.
        if type(value) != str:
            return value

        # Validate unknown substitute should not be allowed.
        if value.startswith('#{'):
            if (not value.startswith("#{sql-uri") and not value.startswith("#{service-uri") and not value.startswith("#{ws-service-uri") and
                not value.startswith("#{test_data_dir-") and not value.startswith("#{docker_data_dir-") and
                value not in supported_value_substitute_strings and not value.startswith('#{artifactory-repo}')):
                raise Exception(f"Unknown url to normalise {value}")
            if value.startswith("#{service-uri-") and value.replace("#{service-uri-", "").split('}')[0] not in self.config.fms_start_sequence:
                raise Exception(f"unknown service, can't substitute {value}")

        if value.startswith('#{artifactory-repo}'):
            return value.replace("#{artifactory-repo}", ARTIFACTORY_URL)
        elif value.startswith("#{service-uri-"):
                value = value.replace("#{service-uri-", "")
                # If url has /xyz, then substitute it.
                value = value.split('}')
                if(len(value) == 1):
                    return self.get_service_url(value[0])
                else:
                    return self.get_service_url(value[0]) + value[1]
        elif value.startswith("#{ws-service-uri-"):
                value = value.replace("#{ws-service-uri-", "")
                # If url has /xyz, then substitute it.
                value = value.split('}')
                if(len(value) == 1):
                    return self.get_service_url(value[0], websocket=True)
                else:
                    return self.get_service_url(value[0], websocket=True) + value[1]
        elif value.startswith('#{docker_data_dir-'):
            value = value.replace('#{docker_data_dir-', '').replace('}', '')
            return os.path.join(self.get_docker_map_dir(self.testdata_dir), value).replace('\\', '/')
        elif value.startswith('#{test_data_dir-'):
            value = value.replace('#{test_data_dir-', '').replace('}', '')
            return os.path.join(self.testdata_dir, value).replace('\\', '/')
        elif value == "#{redis-fms-uri}":
            return f"{self.redis('FMS')['host']}:{self.redis('FMS')['port']},abortConnect=false"
        elif value == '#{redis-field-uri}':
            return f"{self.redis('FMS')['host']}:" + str(self.redis(f'Field')['port']) + ",abortConnect=false"
        elif value == '#{redis-office-uri}':
            return f"{self.redis('FMS')['host']}:{self.redis('Office')['port']},abortConnect=false"
        elif value == "#{zipkin}":
            return self.zipkin['uri']
        elif value == "#{rabbitmq-uri}":
            return self.rabbitmq['uri']
        elif value.startswith("#{sql-uri"):
            return f"Server={self.sql(value.split('-')[-1].replace('}', ''))['uri']}"
        elif value == "#{init-pear}":
            return f"[0]@udpv4://{self.fms_bridge_aht_robot_ip[self.default_asset]}"
        elif value == "#{map-x}":
            return MAPS[self.map]['x']
        elif value == "#{map-y}":
            return MAPS[self.map]['y']
        else:
            return value

    def init_config_values(self):
        """
        List of values which should be available for config to evaluate.
        """
        # Set default values used for testing.
        self.config.override = {}
        self.config.override.default_asset_id = self.default_asset
        self.config.override.default_asset_class = self.default_asset_class
        self.config.override.fms_bridge_domain = self.fms_bridge_domain
        self.config.override.default_asset_participant_id = self.default_asset_participant_id
        # Selenium specific config.
        self.config.override.selenium = {}
        self.config.override.selenium.chrome = {}
        self.config.override.selenium.firefox = {}
        self.config.override.selenium.chrome.docker_image = BROWSER_DRIVER['chrome']['docker_image']
        self.config.override.selenium.firefox.docker_image = BROWSER_DRIVER['firefox']['docker_image']
        self.config.override.selenium.port = self.selenium['port']
        self.config.override.selenium.vpn_port = self.selenium['vpn_port']
        self.config.override.selenium.width = int(SUPPORTED_SCREEN_RESOLUTIONS['Overwatch'][0]) + 100
        self.config.override.selenium.height = int(SUPPORTED_SCREEN_RESOLUTIONS['Overwatch'][0]) + 100
        self.config.override.selenium.chrome.driver = BROWSER_DRIVER['chrome']['driver']
        self.config.override.selenium.firefox.driver = BROWSER_DRIVER['firefox']['driver']
        # RabbitMQ
        self.config.override.rabbitmq = {}
        self.config.override.rabbitmq.port = self.rabbitmq['port']
        self.config.override.rabbitmq.manager_port = self.rabbitmq['manager_port']
        self.config.override.rabbitmq.user = self.rabbitmq["user"]
        self.config.override.rabbitmq.password = self.rabbitmq["password"]
        # Redis
        self.config.override.redis = {}
        self.config.override.redis.field_port = self.redis(f'Field')['port']
        self.config.override.redis.fms_port = self.redis(f'FMS')['port']
        self.config.override.redis.office_port = self.redis(f'Office')['port']
        # Sql
        self.config.override.sql = {}
        self.config.override.sql.port = self.sql()["port"]
        self.config.override.sql.sa_password = self.sql()['password']
        # Zipkin
        self.config.override.zipkin = {}
        self.config.override.zipkin.port = self.zipkin["port"]


    def reload_config(self, service: str):
        """
        Reload config for a service with more modification.
        """
        config = Dynaconf(
            preload=[
                os.path.join(AUTOMATED_TEST_DIR, "config", "ports.yaml"),
                os.path.join(AUTOMATED_TEST_DIR, "config", "start_sequence.yaml"),
            ],
            includes = [
                os.path.join(AUTOMATED_TEST_DIR, "config", "fms", f"{service.split('_')[0]}.yaml"),
            ],
            environments = False,
            load_dotenv = False,
            envvar_prefix="FMS_",
            env_switcher="START_FMS_ENV",  # to switch environments `export START_FMS_ENV=production'
        )
        config.override = self.config.override
        # We don't have config for asset specific service. use default values.
        org_service = service
        if len(service.split("_")) > 1:
            org_service = service.split("_")[0]
        setattr(self.config.imperium_services, service, self.update_config(getattr(config.imperium_services, org_service)))
        if len(service.split("_")) == 2:
            self.add_asset_field_config(service.split("_")[1], reload_config=True)


    def init(self, release: str='master', run_env: str=None, output_dir: str=None,
        testdata_dir: str=None, map: str='Hazelmere', debug: str='Information',
        fms_bridge_domain: str=None, fms_bridge_robot_ip: Dict={},
        host_ip_addr: str=None, start_port: int=None, timeout: int=10, participant_id: Dict={},
        dotnet_build_on_run: bool=True, https: bool=False):

        self.https = https

        # Environment for which tests will be executed, test or dev. None => local.
        if not run_env or run_env == '':
            self.run_env = 'local'
        elif run_env not in DEPLOYED_ENVS.keys():
            raise Exception(f"Un-supported deployed environment {run_env}. Known environments are \n{DEPLOYED_ENVS.keys()}")
        else:
            self.run_env = run_env

        self.dotnet_build_on_run = dotnet_build_on_run

        # Output directory, keep this in sync with output folder.
        self.output_dir = output_dir
        if not output_dir:
            self.output_dir = os.path.join(AUTOMATED_TEST_DIR, 'output')
        # Test Data directory, keep this in sync with test_data folder path.
        self.testdata_dir = testdata_dir
        if not testdata_dir:
            self.testdata_dir = os.path.join(AUTOMATED_TEST_DIR, 'test_data')

        settings_files = []
        for file_name in glob.glob(os.path.join(AUTOMATED_TEST_DIR, 'config/*.yaml')):
            settings_files.append(file_name)

        # Load configuration.
        self.config = Dynaconf(
            preload=[
                os.path.join(AUTOMATED_TEST_DIR, "config", "ports.yaml"),
                os.path.join(AUTOMATED_TEST_DIR, "config", "start_sequence.yaml"),
            ],
            includes = [
                os.path.join(AUTOMATED_TEST_DIR, "config", "fms", "*.yaml"),
                os.path.join(AUTOMATED_TEST_DIR, "config", "docker", "*.yaml"),
            ],
            environments = False,
            load_dotenv = False,
            envvar_prefix="FMS_",
            env_switcher="START_FMS_ENV",  # to switch environments `export START_FMS_ENV=production'
        )

        # Map to use for seeding env.
        self.map = map

        self.default_asset = MAPS[self.map]['default_asset']
        self.default_asset_class = MAPS[self.map]['allowed_assets'][self.default_asset]['class']

        self.smoke_test_services = [
            f'FieldSignal', 'FieldSignalOffice', f'FieldSync', 'OfficeSync',
        ]

        self.redis_ports = self.config.redis_ports
        self.service_ports = self.config.fms_service_ports
        self.web_app_services: List = [f'Centurion_{self.default_asset}', 'Overwatch']

        # Release we want to get docker version
        self.release = release
        # Start port range for FMS services. Default is None which means use default port range
        self.start_port = start_port
        # IP address of localhost, so it can be used by selenium docker.
        self._imperium_server_ip_address: str = None
        # IP Address of Host machine.
        if host_ip_addr:
            self._imperium_server_ip_address = host_ip_addr
        # Next port which can be used by asset field
        self.field_asset_port = ASSET_PORTS_START
        # Show debug information.
        self.debug = debug
        # Set timeout
        self.timeout = timeout

        # List of docker images.
        self._docker_images = {}
        # List of ports used by docker services
        self.docker_services_port = {}

        # FMS Bridge domain id.
        if fms_bridge_domain:
            self.fms_bridge_domain = fms_bridge_domain
        else:
            self.fms_bridge_domain = MAPS[self.map]['fms_domain']

        # FMS Bridge AHT ip.
        if not fms_bridge_robot_ip:
            if 'ip' in MAPS[map]['allowed_assets'][self.default_asset]:
                fms_bridge_robot_ip = {self.default_asset: MAPS[map]['allowed_assets'][self.default_asset]['ip']}
            else:
                fms_bridge_robot_ip = {self.default_asset: self.server_host_ip()}
        self.fms_bridge_aht_robot_ip = fms_bridge_robot_ip
        # TODO: Only set Asset shadow Bridge for autonomous assets.
        self.fms_bridge_aht_robot_ip[self.default_asset] = self.server_host_ip()

        # List of participant id's for AHT
        self.participant_id = participant_id
        if self.default_asset in self.participant_id:
            self.default_asset_participant_id = participant_id[self.default_asset]
        else:
            self.default_asset_participant_id = MAPS[self.map]['default_participant_id']

        # Get all redis services in local object.
        for service, port in self.redis_ports.items():
            self.docker_services_port[service] = self.service_port(port)
            if self.is_port_used(self.docker_services_port[service], self.timeout):
                raise Exception(f"Docker service {service} can't be started on port: {self.docker_services_port[service]}, it's already in use")

        # Update ports which will be used by service.
        for service, port in self.service_ports.items():
            self.service_ports[service] = self.service_port(self.service_ports[service])
            if self.is_port_used(self.service_ports[service], self.timeout):
                raise Exception(f"Imperium service {service} can't be started on port: {self.service_ports[service]}, it's already in use")

        # This is hack to get imperium services url from docker image.
        for service, config in self.config.imperium_services.items():
            if 'docker_image' in config:
                self._docker_images[service] = config['docker_image']

        # Init imperium services.
        self.init_config_values()
        for service, _ in self.config.imperium_services.items():
            setattr(self.config.imperium_services, service, self.update_config(getattr(self.config.imperium_services, service)))
            if self.https and self.config.imperium_services[service].environment.get('Kestrel__EndpointDefaults__Protocols', None):
                self.config.imperium_services[service].environment['Kestrel__EndpointDefaults__Protocols'] = 'Http2'

        # Init docker services used by imperium.
        for service, _ in self.config.docker_services.items():
            setattr(self.config.docker_services, service, self.update_config(getattr(self.config.docker_services, service)))

        # Update host files, this is needed when connecting using selenium docker.
        self.hosts_modified_file = self.update_hosts_file()

        # Add default asset by default.
        self.add_asset_field_config(self.default_asset, True)


    def is_port_used(self, port: int, timeout: int=1):
        """
        Check if local port is in use. Check port availability before starting service to avoid surprise.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        is_used = False
        while timeout and is_used:
            try:
                s.bind(("127.0.0.1", port))
                is_used = False
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    is_used = True
                else:
                    is_used = False
            timeout -= 1
            sleep(1)
        s.close()
        return is_used


    def service_port(self, default_port: int):
        """
        Service port which will be used by service.
        """
        if not self.start_port:
            return default_port

        self.start_port += 1
        return self.start_port

    @property
    def certs(self):
        if self.run_env != 'local' or (self.https and self.run_env == 'local'):
            return DEPLOYED_ENVS[self.run_env]['certs']
        else:
            return {}

    @property
    def certs_key(self):
        if self.run_env != 'local' or (self.https and self.run_env == 'local'):
            return DEPLOYED_ENVS[self.run_env]['certs_key']
        else:
            return {}

    @property
    def imperium_server_ip_address(self, force_ip=False) -> str:
        return self.server_host_ip()

    @property
    def rabbitmq(self):
        if 'rabbitmq' not in self.docker_services_port:
            self.docker_services_port['rabbitmq'] = self.service_port(5672)
        if 'rabbitmq_manager' not in self.docker_services_port:
            self.docker_services_port['rabbitmq_manager'] = self.service_port(15672)
        return {
            'host': self.imperium_server_ip_address,
            'port': self.docker_services_port['rabbitmq'],
            'manager_port': self.docker_services_port['rabbitmq_manager'],
            'user': 'user',
            'password': 'user',
            'uri': f"amqp://user:user@{self.imperium_server_ip_address}:{self.docker_services_port['rabbitmq']}"
        }

    def server_host_ip(self, force_ip=False):
        # If https, then we need atf.apps.fms-dev.local
        if self.https and not force_ip:
            # Un-commented for testing
            #return 'atf.apps.fms-dev.local'
            return '127.0.0.1'

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
    def zipkin(self):
        if 'zipkin' not in self.docker_services_port:
            self.docker_services_port['zipkin'] = self.service_port(9411)
        return {
            'host': self.imperium_server_ip_address,
            'port':  self.docker_services_port['zipkin'],
            'uri': f"http://{self.imperium_server_ip_address}:{self.docker_services_port['zipkin']}"
        }

    @property
    def selenium(self):
        if 'selenium' not in self.docker_services_port:
            self.docker_services_port['selenium'] = self.service_port(4444)
        if 'selenium_vpn' not in self.docker_services_port:
            self.docker_services_port['selenium_vpn'] = self.service_port(7900)
        return {
            'port': self.docker_services_port['selenium'],
            'vpn_port': self.docker_services_port['selenium_vpn']
        }

    def redis(self, service):
        return {
            'host': self.imperium_server_ip_address,
            'port': self.docker_services_port[service]
        }

    def sql(self, database: str=None):
        host = self.imperium_server_ip_address
        #password = 'SupaDupaSecret!!!!'
        password = 'master@5'
        if 'sql' not in self.docker_services_port:
            self.docker_services_port['sql'] = self.service_port(1433)
        return {
            'host': host,
            'port': self.docker_services_port['sql'],
            'user': 'sa',
            'password': password,
            'uri': f"{host},{ self.docker_services_port['sql']};Database={database};User ID=sa;Password={password};TrustServerCertificate=true"
        }

    def get_service_url(self, service: str, websocket: bool=False) -> str:
        """
        Create a service url and return value
        """
        # Local deployed environment url.
        if self.run_env == 'local' and not websocket and not self.https:
            #added localhost
            #return f"http://127.0.0.1:{self.service_ports[service]}"
            return f"http://{self.imperium_server_ip_address}:{self.service_ports[service]}"

        # Local deployed environment websocket url.
        elif self.run_env == 'local' and websocket and not self.https:
            return f"ws://{self.imperium_server_ip_address}:{self.service_ports[service]}"
        # AWS test environment url.
        elif self.run_env and not websocket:
            if service.startswith('AssetShadowService_'):
                docker_image = "asset-shadow-"+service.split('_')[1]
            elif service.startswith('Centurion_'):
                docker_image = "field-web"
            elif service.startswith('Overwatch'):
                docker_image = "office-web"
            elif (service.startswith('AssetShadowBridge_') or service.startswith('AssetShadowTaskManager_') or
                service.startswith('AssetShadowService_') or service.startswith('AssetShadowStateManager_') or
                service.startswith('AssetShadowInstructionManager_')):
                docker_image = self._docker_images[service]+"-"+service.split('_')[1]
            else:
                if service == 'RoutingService':
                    docker_image = 'routing-service'
                elif service in self._docker_images:
                    docker_image = self._docker_images[service]
                else:
                    docker_image = None
            url = DEPLOYED_ENVS[self.run_env]['url'].format(docker_image)
            if self.https and self.run_env == 'local':
                url = f"https://{self.imperium_server_ip_address}:{self.service_ports[service]}"
            return url
        # AWS test environment websocket url.
        elif self.run_env and websocket:
            url = f"wss://{self.imperium_server_ip_address}:{self.service_ports[service]}"
            return url


    def get_latest_fms_version(self, docker_image: str=None, artifactory_api_key: str=None, artifactory_docker_url: str=None):
        """
        Get the latest versions of FMS docker
        """

        if not artifactory_docker_url:
            artifactory_docker_url = ARTIFACTORY_DOCKER_URL

        if not artifactory_api_key:
            if "ArtifactoryAPIKey" in os.environ:
                artifactory_api_key = os.environ.get('ArtifactoryAPIKey')
            else:
                raise Exception("Please set environment variable ArtifactoryAPIKey")

        versions = {}
        image_dates = {}
        fms_services_count = 0
        header = {"X-JFrog-Art-Api": artifactory_api_key}
        for fms_service in self.config.fms_start_sequence:
            # If requested for a specific service version then, just return that.
            if not self.config.imperium_services[fms_service].get('docker_image', None) or self.config.imperium_services[fms_service].get('do_not_start', False):
                continue

            fms_docker_image = self.config.imperium_services[fms_service].get('docker_image')
            if docker_image and fms_docker_image != docker_image:
                continue

            response = requests.get(artifactory_docker_url.format(fms_docker_image), headers=header, timeout=5, verify=False)
            if response.status_code != 200:
                raise Exception("Unable to connect to artifactory, please check ArtifactoryAPIKey environment variable")
            data = response.json()
            fms_services_count += 1
            if 'files' in data:
                for file in data['files']:
                    # Get latest master version.
                    if 'lastModified' in file and (f"-{self.release}" in file['uri']):
                        updated_date = pendulum.parse(file['lastModified']).format('YYYY-MM-DD-HH')
                        # Keep list of images we have
                        if updated_date not in image_dates:
                            image_dates[updated_date] = []
                        image_dates[updated_date].append({
                            'docker_version': file['uri'].replace('/', ''),
                            'docker_image': fms_docker_image
                        })

        image_dates = dict(sorted(image_dates.items(), reverse=True))
        for _, images in image_dates.items():
            if len(images) == fms_services_count:
                for image in images:
                    versions[image['docker_image']] = image['docker_version']
                break
        if docker_image:
            return versions[docker_image]
        else:
            return versions


    def is_windows(self) -> bool:
        if os.name == 'nt':
            return True
        else:
            return False


    def remove_default_field_services(self):
        """
        If user wants to start specific asset, then don't start default.
        """
        self.config.docker_services[f'redis_Field_{self.default_asset}']['do_not_start'] = True
        self.config.imperium_services[f'FieldSignal_{self.default_asset}']['do_not_start'] = True
        self.config.imperium_services[f'AssetShadowService_{self.default_asset}']['do_not_start'] = True
        self.config.imperium_services[f'AssetShadowTaskManager_{self.default_asset}']['do_not_start'] = True
        self.config.imperium_services[f'AssetShadowStateManager_{self.default_asset}']['do_not_start'] = True
        self.config.imperium_services[f'AssetShadowBridge_{self.default_asset}']['do_not_start'] = True
        self.config.imperium_services[f'AssetShadowInstructionManager_{self.default_asset}']['do_not_start'] = True
        self.config.imperium_services[f'FieldSync_{self.default_asset}']['do_not_start'] = True
        self.config.imperium_services[f'Centurion_{self.default_asset}']['do_not_start'] = True


    def add_asset_field_config(self, asset_id: str, default_port: bool=False, reload_config: bool=False):
        """
        Adds config to the list of docker and imperium services in this class.
        This should be called before starting new asset except default asset.
        """
        if asset_id not in MAPS[self.map]['allowed_assets'].keys():
            raise Exception(f"Asset id {asset_id} is not allowed to be created for {self.map}.")

        # Don't add this, as asset config is already available.
        if not reload_config and f'Field_{asset_id}' in self.docker_services_port:
            return

        # Don't add asset if FieldSignal is no longer a service - TCS specific code.
        if 'FieldSignal' not in self.config.imperium_services:
            return


        # Initialise this port, so it can be incremented and used for other asset id's.
        field_asset_port = self.service_port(self.field_asset_port)

        # Field redis
        if default_port:
            field_asset_port = int(self.config.docker_services[f'redis_Field']['ports']['6379/tcp'])
        if reload_config and f'Field_{asset_id}' in self.redis_ports:
            field_asset_port = self.redis_ports[f'Field_{asset_id}']
        self.docker_services_port[f'Field_{asset_id}'] = field_asset_port
        self.config.docker_services[f'redis_Field_{asset_id}'] = copy.deepcopy(self.config.docker_services[f'redis_Field'])
        self.config.docker_services[f'redis_Field_{asset_id}']['ports'] = {"6379/tcp": field_asset_port}
        self.config.docker_services[f'redis_Field_{asset_id}']['do_not_start'] = False
        redis_port = field_asset_port
        self.redis_ports[f'Field_{asset_id}'] = field_asset_port
        self.config.docker_start_sequence += [f'redis_Field_{asset_id}']
        self._docker_images[f'redis_Field_{asset_id}'] = self.config.docker_services[f'redis_Field_{asset_id}']['image']
        field_asset_port += 1

        # Field signal
        field_signal_port = field_asset_port
        if default_port:
            field_signal_port = self.config.imperium_services[f'FieldSignal']['port']
        if reload_config and f'FieldSignal_{asset_id}' in self.service_ports:
            field_signal_port = self.service_ports[f'FieldSignal_{asset_id}']

        self.config.imperium_services[f'FieldSignal_{asset_id}'] = copy.deepcopy(self.config.imperium_services[f'FieldSignal'])
        self.config.imperium_services[f'FieldSignal_{asset_id}']['do_not_start'] = False
        self.config.imperium_services[f'FieldSignal_{asset_id}']['port'] = field_signal_port
        self.config.imperium_services[f'FieldSignal_{asset_id}']['environment']["ExternalCache__Url"] = f"{self.imperium_server_ip_address}:{redis_port}"
        self.service_ports[f'FieldSignal_{asset_id}'] = field_signal_port
        self.config.fms_start_sequence += [f'FieldSignal_{asset_id}']
        self._docker_images[f'FieldSignal_{asset_id}'] = self.config.imperium_services[f'FieldSignal_{asset_id}']['docker_image']
        field_asset_port += 1

        # Asset shadow service
        asset_shadow_port = field_asset_port
        if default_port:
            asset_shadow_port = int(self.config.imperium_services[f'AssetShadowService']['port'])
        if reload_config and f'AssetShadowService_{asset_id}' in self.service_ports:
            asset_shadow_port = self.service_ports[f'AssetShadowService_{asset_id}']
        self.config.imperium_services[f'AssetShadowService_{asset_id}'] = copy.deepcopy(self.config.imperium_services[f'AssetShadowService'])
        self.config.imperium_services[f'AssetShadowService_{asset_id}']['do_not_start'] = False
        self.config.imperium_services[f'AssetShadowService_{asset_id}']['port'] = asset_shadow_port
        self.config.imperium_services[f'AssetShadowService_{asset_id}']['environment']["AssetId"] = asset_id
        self.service_ports[f'AssetShadowService_{asset_id}'] = asset_shadow_port
        self.config.fms_start_sequence += [f'AssetShadowService_{asset_id}']
        self._docker_images[f'AssetShadowService_{asset_id}'] = self.config.imperium_services[f'AssetShadowService_{asset_id}']['docker_image']
        field_asset_port += 1

        # Asset shadow task manager
        asset_shadow_task_manager_port = field_asset_port
        if default_port:
            asset_shadow_task_manager_port = self.config.imperium_services[f'AssetShadowTaskManager']['port']
        if reload_config and f'AssetShadowTaskManager{asset_id}' in self.service_ports:
            asset_shadow_task_manager_port = self.service_ports[f'AssetShadowTaskManager_{asset_id}']
        self.config.imperium_services[f'AssetShadowTaskManager_{asset_id}'] = copy.deepcopy(self.config.imperium_services[f'AssetShadowTaskManager'])
        # self.config.imperium_services[f'AssetShadowTaskManager_{asset_id}']['do_not_start'] = False
        self.config.imperium_services[f'AssetShadowTaskManager_{asset_id}']['port'] = asset_shadow_task_manager_port
        self.config.imperium_services[f'AssetShadowTaskManager_{asset_id}']['environment']["AssetId"] = asset_id
        self.service_ports[f'AssetShadowTaskManager_{asset_id}'] = asset_shadow_task_manager_port
        self.config.fms_start_sequence += [f'AssetShadowTaskManager_{asset_id}']
        self._docker_images[f'AssetShadowTaskManager_{asset_id}'] = self.config.imperium_services[f'AssetShadowTaskManager_{asset_id}']['docker_image']
        field_asset_port +=1

        # Asset shadow bridge
        asset_shadow_bridge_port = field_asset_port
        if default_port:
            asset_shadow_bridge_port = self.config.imperium_services[f'AssetShadowBridge']['port']
        if reload_config and f'AssetShadowBridge_{asset_id}' in self.service_ports:
            asset_shadow_bridge_port = self.service_ports[f'AssetShadowBridge_{asset_id}']
        self.config.imperium_services[f'AssetShadowBridge_{asset_id}'] = copy.deepcopy(self.config.imperium_services[f'AssetShadowBridge'])
        # self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['do_not_start'] = False
        self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['port'] = asset_shadow_bridge_port
        self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['environment']["AssetId"] = (f'{asset_id}')
        self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['environment']["AssetPermissionServiceConfiguration"] = self.get_service_url(f'AssetPermissionService')
        self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['environment']["AssetShadowServiceConfiguration"] = self.get_service_url(f'AssetShadowService_{asset_id}')
        self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['environment']["AssetShadowTaskManagerConfiguration"] = self.get_service_url(f'AssetShadowTaskManager_{asset_id}')
        self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['environment']["DdsConfiguration__ParticipantConfiguration__InitialPeers"] = f"[0]@udpv4://{self.fms_bridge_aht_robot_ip.get(asset_id, '127.0.0.1')}"
        if asset_id.startswith("AHT")  and 'ParticipantId' in MAPS[self.map]['allowed_assets'][asset_id] and asset_id in f"{self.participant_id}":
            self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['environment']["DdsConfiguration__ParticipantConfiguration__ParticipantId"] = f"{self.participant_id[asset_id]}"
        elif asset_id.startswith("AHT")  and 'ParticipantId' in MAPS[self.map]['allowed_assets'][asset_id]:
            self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['environment']["DdsConfiguration__ParticipantConfiguration__ParticipantId"] = f"{MAPS[self.map]['allowed_assets'][asset_id]['ParticipantId']}"
        self.service_ports[f'AssetShadowBridge_{asset_id}'] = asset_shadow_bridge_port
        self.config.fms_start_sequence += [f'AssetShadowBridge_{asset_id}']
        self._docker_images[f'AssetShadowBridge_{asset_id}'] = self.config.imperium_services[f'AssetShadowBridge_{asset_id}']['docker_image']
        field_asset_port +=1

        # Asset shadow instruction manager
        asset_shadow_instruction_manager_port = field_asset_port
        if default_port:
            asset_shadow_instruction_manager_port = self.config.imperium_services[f'AssetShadowInstructionManager']['port']
        if reload_config and f'AssetShadowInstructionManager_{asset_id}' in self.service_ports:
            asset_shadow_instruction_manager_port = self.service_ports[f'AssetShadowInstructionManager_{asset_id}']
        self.config.imperium_services[f'AssetShadowInstructionManager_{asset_id}'] = copy.deepcopy(self.config.imperium_services[f'AssetShadowInstructionManager'])
        self.config.imperium_services[f'AssetShadowInstructionManager_{asset_id}']['do_not_start'] = False
        self.config.imperium_services[f'AssetShadowInstructionManager_{asset_id}']['port'] = asset_shadow_instruction_manager_port
        self.config.imperium_services[f'AssetShadowInstructionManager_{asset_id}']['environment']["AssetId"] = asset_id
        self.config.imperium_services[f'AssetShadowInstructionManager_{asset_id}']['environment']["IsMannedAsset"] = str('mode' not in MAPS[self.map]['allowed_assets'][asset_id] or MAPS[self.map]['allowed_assets'][asset_id]['mode'] != "auto")
        self.service_ports[f'AssetShadowInstructionManager_{asset_id}'] = asset_shadow_instruction_manager_port
        self.config.fms_start_sequence += [f'AssetShadowInstructionManager_{asset_id}']
        self._docker_images[f'AssetShadowInstructionManager_{asset_id}'] = self.config.imperium_services[f'AssetShadowInstructionManager_{asset_id}']['docker_image']
        field_asset_port += 1

        # Asset shadow state manager
        asset_shadow_state_manager_port = field_asset_port
        if default_port:
            asset_shadow_state_manager_port = self.config.imperium_services[f'AssetShadowStateManager']['port']
        if reload_config and f'AssetShadowStateManager_{asset_id}' in self.service_ports:
            asset_shadow_state_manager_port = self.service_ports[f'AssetShadowStateManager_{asset_id}']
        self.config.imperium_services[f'AssetShadowStateManager_{asset_id}'] = copy.deepcopy(self.config.imperium_services[f'AssetShadowStateManager'])
        self.config.imperium_services[f'AssetShadowStateManager_{asset_id}']['do_not_start'] = False
        self.config.imperium_services[f'AssetShadowStateManager_{asset_id}']['port'] = asset_shadow_state_manager_port
        self.config.imperium_services[f'AssetShadowStateManager_{asset_id}']['environment']["AssetId"] = asset_id
        self.config.imperium_services[f'AssetShadowStateManager_{asset_id}']['environment']["AssetClass"] = MAPS[self.map]['allowed_assets'][asset_id]['class']
        self.service_ports[f'AssetShadowStateManager_{asset_id}'] = asset_shadow_state_manager_port
        self.config.fms_start_sequence += [f'AssetShadowStateManager_{asset_id}']
        self._docker_images[f'AssetShadowStateManager_{asset_id}'] = self.config.imperium_services[f'AssetShadowStateManager_{asset_id}']['docker_image']
        field_asset_port += 1

        # Field sync
        field_sync_port = field_asset_port
        if default_port:
            field_sync_port = self.config.imperium_services[f'FieldSync']['port']
        if reload_config and f'FieldSync_{asset_id}' in self.service_ports:
            field_sync_port = self.service_ports[f'FieldSync_{asset_id}']
        self.config.imperium_services[f'FieldSync_{asset_id}'] = copy.deepcopy(self.config.imperium_services[f'FieldSync'])
        self.config.imperium_services[f'FieldSync_{asset_id}']['do_not_start'] = False
        self.config.imperium_services[f'FieldSync_{asset_id}']['port'] = field_sync_port
        self.config.imperium_services[f'FieldSync_{asset_id}']['environment']["ExternalCache__Url"] = f"{self.imperium_server_ip_address}:{redis_port}"
        self.config.imperium_services[f'FieldSync_{asset_id}']['environment']['AssetId'] = asset_id
        self.config.imperium_services[f'FieldSync_{asset_id}']['environment']['AssetShadowServiceConfiguration'] = self.get_service_url(f'AssetShadowService_{asset_id}')
        self.service_ports[f'FieldSync_{asset_id}'] = field_sync_port
        self.config.fms_start_sequence += [f'FieldSync_{asset_id}']
        self._docker_images[f'FieldSync_{asset_id}'] = self.config.imperium_services[f'FieldSync_{asset_id}']['docker_image']
        field_asset_port += 1

        # Centurion
        centurion_port = field_asset_port
        if default_port:
            centurion_port = self.config.imperium_services[f'Centurion']['port']
        if reload_config and f'Centurion_{asset_id}' in self.service_ports:
            centurion_port = self.service_ports[f'Centurion_{asset_id}']
        self.web_app_services.append(f'Centurion_{asset_id}')
        self.config.imperium_services[f'Centurion_{asset_id}'] = copy.deepcopy(self.config.imperium_services[f'Centurion'])
        self.config.imperium_services[f'Centurion_{asset_id}']['do_not_start'] = False
        self.config.imperium_services[f'Centurion_{asset_id}']['port'] = centurion_port
        # Copy centurion to output directory, so it can be served with new config.
        if self.release == 'local':
            self.create_local_web_build_dir(asset_id)

        self.config.imperium_services[f'Centurion_{asset_id}']['environment']["CenturionConfig__ImperiumHubUrl"] = self.get_service_url(f"FieldSignal_{asset_id}", True) + "/ImperiumHub"
        self.config.imperium_services[f'Centurion_{asset_id}']['environment']["ImperiumHubUrl"] = self.get_service_url(f"FieldSignal_{asset_id}", True) + "/ImperiumHub"
        self.service_ports[f'Centurion_{asset_id}'] = centurion_port
        self.config.fms_start_sequence += [f'Centurion_{asset_id}']
        self._docker_images[f'Centurion_{asset_id}'] = self.config.imperium_services[f'Centurion_{asset_id}']['docker_image']
        field_asset_port += 1

        # If not default port used, then update start port, so next asset can be allocated with next port range.
        if not default_port:
            if self.start_port:
                self.start_port = field_asset_port
            else:
                self.field_asset_port = field_asset_port

        return self.get_service_url(f"Centurion_{asset_id}"), redis_port


    def create_local_web_build_dir(self, asset_id: str=None) -> str:
        """
        Create local centurion directory for running python web server, if asset_id passed it will create centurion, else it will create overwatch.
        return: path relative path of build dir.
        """
        if asset_id:
            final_build_dir = os.path.join(self.output_dir, f'centurion_{asset_id}').replace('\\', '/')
            if not os.path.exists(final_build_dir):
                shutil.copytree(self.get_service_path('Centurion'), final_build_dir)
            self._update_centurion_config(final_build_dir, asset_id)
            self.config.imperium_services[f'Centurion_{asset_id}']['path'] = os.path.relpath(final_build_dir, IMPERIUM_DIR)
        else:
            final_build_dir = os.path.join(self.output_dir, f'overwatch').replace('\\', '/')
            if not os.path.exists(final_build_dir):
                shutil.copytree(self.get_service_path(f'Overwatch'), final_build_dir)
            self._update_overwatch_config(final_build_dir)
            self.config.imperium_services[f'Overwatch']['path'] = os.path.relpath(final_build_dir, IMPERIUM_DIR)

        # Path used in self.config.imperium_services is relative to IMPERIUM_DIR
        return os.path.relpath(final_build_dir, IMPERIUM_DIR)


    def get_docker_command(self, service: str, default_port: bool=False, return_list: bool=False, name_suffix: str=None):
        """
        Create docker command and return
        """
        # Add field config for asset if it's not already set.
        if service.startswith('redis_Field_'):
            asset_id = service.split('_')[2]
            if f'redis_Field_{asset_id}' not in self.config.docker_services.keys():
                self.add_asset_field_config(asset_id, default_port)

        command = []
        arguments = []
        container_name = service
        if name_suffix:
            container_name = f"{service}_{name_suffix}"
        for docker_service, options in self.config.docker_services.items():
            if service and docker_service != service:
                continue

            docker_image = options['image']
            command = ['docker']
            arguments = ["run", "--name", container_name, "--rm"]

            for key, value in options['environment'].items():
                arguments.append("-e")
                if self.is_windows():
                    arguments.append(f"{key}\={value}")
                else:
                    arguments.append(f"'{key}\={value}'")

            if 'ports' in options:
                for port_container, port_host in options['ports'].items():
                    port_container = port_container.replace('/tcp', '')
                    arguments.append("-p")
                    arguments.append(f"{port_host}:{port_container}")

            if 'shm_size' in options:
                arguments.append('--shm-size')
                arguments.append(options['shm_size'])

            # Append alias for browser.
            if service in ['chrome', 'firefox']:
                for map_host, map_container in self.certs.items():
                    arguments.append("-v")
                    arguments.append(f"{map_host}:{map_container}")
                for map_host, map_container in self.certs_key.items():
                    arguments.append("-v")
                    arguments.append(f"{map_host}:{map_container}")
                # Also map host file for url resolution.
                arguments.append("-v")
                hosts_modified = self.update_hosts_file()
                arguments.append(f"{hosts_modified}:/etc/hosts:ro")
            if service in ['chrome', 'firefox', 'sqlserver']:
                # map files for testing file upload
                arguments.append("-v")
                file_upload_dir = os.path.join(self.testdata_dir, "file_upload").replace('\\', '/')
                arguments.append(f"{file_upload_dir}:{self.get_docker_map_dir(file_upload_dir, True)}")
            if self.docker_network:
                arguments.append("--network")
                arguments.append(self.docker_network)
            arguments.append(docker_image)

        return subprocess.list2cmdline(command + arguments) if not return_list else command + arguments, container_name

    def get_docker_map_dir(self, path, is_docker=False):
        if self.is_windows() and (is_docker or self.release != 'local'):
            return path.replace('C:', '/tmp').replace('c:', '/tmp')
        else:
            return path

    def get_imperium_build_command(self, service: str):
        """
        Return build command for imperium service
        """
        # Add field config for asset if it's not already set.
        if service not in self.config.fms_start_sequence:
            if len(service.split('_')) != 2:
                raise Exception(f"{service} not known")
            asset_id = service.split('_')[1]
            self.add_asset_field_config(asset_id)

        env = {}

        if service in self.web_app_services:
            command = {
                f'{service}_npm_install': ['npm', 'ci'],
                f'{service}_npm_build': ['npm', 'run', 'build']
            }
        else:
            command = {f'{service}_build': ['dotnet', 'build', '--no-incremental']}

        return command, env


    def get_imperium_command(self, service: str, docker_version: str=None, return_list: bool=False,
        add_dotnet_cli: bool=False, name_suffix: str=None):
        """
        Create imperium command from the variables passed.
        If docker_version is passed for service then docker command will be returned,
        else local command we be returned.
        """
        # Add field config for asset if it's not already set.
        if service not in self.config.imperium_services:
            if len(service.split('_')) != 2:
                raise Exception(f"{service} not known")
            asset_id = service.split('_')[1]
            self.add_asset_field_config(asset_id)

        service_info = self.config.imperium_services[service]

        service_info['environment']["Serilog__MinimumLevel__Default"] = self.debug
        service_info['environment']["ASPNETCORE_LOGGING__CONSOLE__DISABLECOLORS"] = "true"
        service_info['environment']["Serilog__MinimumLevel__Override__Microsoft"] = "Warning"
        service_info['environment']["Serilog__MinimumLevel__Override__Microsoft.Hosting.Lifetime"] = "Warning"
        service_info['environment']["DOTNET_gcServer"] = "0"
        service_info['environment']['TZ'] = "Australia/Perth"

        # If running against deployed environment, we need certificates.
        if self.run_env != 'local' or self.https:
            if docker_version:
                service_info['environment']["Kestrel__Certificates__Default__Path"] = list(self.certs.values())[0].split(":")[0]
                service_info['environment']["Kestrel__Certificates__Default__KeyPath"] = list(self.certs_key.values())[0].split(":")[0]
            else:
                # Robot framework handles this internally, so need for this.
                if not return_list or add_dotnet_cli:
                    service_info['environment']['DOTNET_CLI_HOME'] = self.output_dir if self.is_windows() else '/tmp'
                service_info['environment']["Kestrel__Certificates__Default__Path"] = list(self.certs.keys())[0]
                service_info['environment']["Kestrel__Certificates__Default__KeyPath"] = list(self.certs_key.keys())[0]
        elif not docker_version and (not return_list or add_dotnet_cli):
            service_info['environment']['DOTNET_CLI_HOME'] = self.output_dir if self.is_windows() else '/tmp'

        # Service start url.
        port = service_info['port']
        http = "http"
        if self.run_env != 'local' or self.https:
            http = "https"
        url = f'{http}://0.0.0.0:{port}'

        # Define command to be used, local or docker.
        command = ['dotnet']
        arguments = ['run']

        # ATF don't build again.
        if not self.dotnet_build_on_run:
            arguments.append('--no-build')
        env = service_info['environment']
        if 'launch_profile' in service_info:
            arguments += [
                '--profile', f"'{service_info['launch_profile']}'", '--urls', url
            ]
        else:
            arguments += [
                '--no-launch-profile', '--urls', url
            ]

        container_name = service
        if name_suffix:
            container_name = f"{service}_{name_suffix}"
        if docker_version and 'docker_image' in self.config.imperium_services[service]:
            command = ['docker']
            arguments = ["run", "--name", container_name, "--rm"]

            for key, value in service_info['environment'].items():
                arguments.append("-e")
                if type(value) == str:
                    value = value.replace('=', '\=')
                arguments.append(f"{key}\={value}")

            arguments.append("-e")
            arguments.append(f"ASPNETCORE_URLS\={http}://0.0.0.0:{port}")

            arguments.append("-p")
            arguments.append(f"{port}:{port}")

            for map_host, map_container in self.certs.items():
                arguments.append("-v")
                map_host = map_host.replace('\\', '/')
                map_container = map_container.replace('\\', '/')
                arguments.append(f"{map_host}:{map_container}")
            for map_host, map_container in self.certs_key.items():
                arguments.append("-v")
                map_host = map_host.replace('\\', '/')
                map_container = map_container.replace('\\', '/')
                arguments.append(f"{map_host}:{map_container}")
            # Also map host file for url resolution.
            arguments.append("-v")
            arguments.append(f"{self.hosts_modified_file}:/etc/hosts:ro")
            if 'docker_volume' in service_info:
                for docker_volume in service_info['docker_volume']:
                    arguments.append("-v")
                    host_dir = docker_volume['host_map'].replace('\\', '/')
                    docker_map = docker_volume['docker_map'].replace('\\', '/')
                    arguments.append(f"{host_dir}:{docker_map}:ro")

            if self.docker_network:
                arguments.append("--network")
                arguments.append(self.docker_network)

            docker_image = f"{ARTIFACTORY_DOCKER_IMAGE_PREFIX}/{service_info['docker_image']}:{docker_version}"
            arguments.append(docker_image)
            # Reset env, as docker environment is passed via command line arguments.
            env = {}
        elif self.release == 'local' and ((service.startswith('Centurion_') or service.startswith('Overwatch'))):
            # If running centurion or overwatch locally, then reset default command.
            if service.startswith('Centurion_'):
                self.create_local_web_build_dir(service.split('_')[-1])
            elif service == 'Overwatch':
                self.create_local_web_build_dir()
            command = ['docker']
            arguments = ['run', '--rm']
            arguments.append("-p")
            arguments.append(f"{self.get_service_port(service)}:{self.get_service_port(service)}")
            arguments.append("-v")
            arguments.append(f"{self.get_service_path(service)}:{self.get_docker_map_dir(self.get_service_path(service), True)}")

            for map_host, map_container in self.certs.items():
                arguments.append("-v")
                map_host = map_host.replace('\\', '/')
                map_container = map_container.replace('\\', '/')
                arguments.append(f"{map_host}:{map_container}")
            for map_host, map_container in self.certs_key.items():
                arguments.append("-v")
                map_host = map_host.replace('\\', '/')
                map_container = map_container.replace('\\', '/')
                arguments.append(f"{map_host}:{map_container}")
            # Also map host file for url resolution.
            arguments.append("-v")
            arguments.append(f"{self.hosts_modified_file}:/etc/hosts:ro")
            arguments.append("webratio/nodejs-http-server:0.9.0")
            arguments.append("http-server")
            arguments.append(self.get_docker_map_dir(self.get_service_path(service), True))
            arguments.append("-S")
            arguments.append("-C")
            arguments.append(list(self.certs.values())[0].split(":")[0])
            arguments.append("-K")
            arguments.append(list(self.certs_key.values())[0].split(":")[0])
            arguments.append("-p")
            arguments.append(f"{self.get_service_port(service)}")

        command_with_args = subprocess.list2cmdline(command + arguments)
        if return_list:
            command_with_args = command + arguments

        return command_with_args, env, container_name


    def update_hosts_file(self) -> str:
        """
        Create modified hosts file
        """
        hosts_org = os.path.join(self.testdata_dir, 'hosts').replace('\\', '/')
        hosts_modified_path = os.path.join(self.output_dir, 'hosts').replace('\\', '/')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        with open(hosts_org, "rt") as fin:
            with open(hosts_modified_path, "wt") as fout:
                for line in fin:
                    fout.write(line.replace('{host_ip}', self.server_host_ip(True)))
        if not self.is_windows:
            os.chmod(hosts_modified_path, 0o777)
        return hosts_modified_path

    def get_service_start_string(self, service: str, port: int=0) -> str:
        """
        Return service start string which will be compared in log file.

        Examples:
        | Get Service Start String | SERVICE |
        """
        if service not in self.config.fms_start_sequence:
            raise Exception(f"Service not found to return start string: {service}")

        # Return default start string is service has not provided specific string.
        start_string = self.config.imperium_services[service].get('start_string', None)
        if start_string == None:
            if not port:
                port = self.get_service_port(service)
                if isinstance(port, list):
                    port = port[-1]
            if self.run_env != 'local' or self.https:
                return f"https://0.0.0.0:{port}"
            else:
                return f"http://0.0.0.0:{port}"
        else:
            return start_string


    def get_service_path(self, service: str, is_docker: bool=False, web_dot_net_path=False) -> str:
        if service not in self.config.fms_start_sequence or is_docker:
            return IMPERIUM_DIR
        elif self.release != 'local' and (service.startswith('Centurion_') or service.startswith('Overwatch') or web_dot_net_path):
            return os.path.dirname(os.path.dirname(os.path.normpath(os.path.join(IMPERIUM_DIR, self.config.imperium_services[service].get('path'))))).replace('\\', '/')
        else:
            return os.path.join(IMPERIUM_DIR, self.config.imperium_services[service].get('path')).replace('\\', '/')


    def get_service_port(self, service: str):
        """
        Return port at which service should start

        Examples:
        | Get Service Port | Service |
        """
        if service not in self.config.fms_start_sequence and service not in self.config.docker_start_sequence:
            raise Exception(f"Service not found to return port: {service}")

        if service in self.config.fms_start_sequence:
            return self.config.imperium_services[service]['port']
        else:
            return self.config.docker_services[service]['port']


    def get_launch_profile(self, service: str) -> str:
        """
        Return launch profile of service if available

        Examples:
        | Get Launch Profile | Service |
        """
        if service not in self.config.fms_start_sequence:
            raise Exception(f"Service not found to return launch profile: {service}")

        if 'launch_profile' in self.config.imperium_services[service]:
            return self.config.imperium_services[service]['launch_profile']
        else:
            return ""

    def _update_centurion_config(self, build_path: str, asset_id: str):
        """
        Update centurion config to point to defined url's.
        """
        config_file_path = os.path.join(build_path, 'config.js').replace('\\', '/')
        # Update url in config file to point to system url.
        if not os.path.exists(config_file_path) or os.stat(config_file_path).st_size == 0:
            raise Exception(f"Unable to locate config.js for centurion at {config_file_path}")

        replaced_content = ""
        with open(config_file_path, 'r') as fp:
            for line in fp:
                stripped_line = line.strip()
                if stripped_line.startswith('ImperiumHubUrl:'):
                    imperium_hub_url = self.get_service_url(f'FieldSignal_{asset_id}')
                    line = f'  ImperiumHubUrl: "{imperium_hub_url}/ImperiumHub",\n'
                elif stripped_line.startswith('FieldAuthUrl:'):
                    identity_base_url = self.get_service_url('IdentityService')
                    line = f'  FieldAuthUrl: "{identity_base_url}/Field",\n'
                elif stripped_line.startswith('DailyPlanManualUploadUrl:'):
                    daily_planner_url = self.get_service_url('DailyPlanner')
                    line = f'  DailyPlanManualUploadUrl: "{daily_planner_url}/DailyPlan/import?autoapproved=true",\n'
                elif stripped_line.startswith('MineModelDraftServiceUrl:'):
                    mine_model_draft_service_url = self.get_service_url('MineModelDraftService')
                    line = f'  MineModelDraftServiceUrl: "{mine_model_draft_service_url}/draft",\n'
                elif stripped_line.startswith('TerrainBridgeBaseUrl:'):
                    terrain_bridge_url = self.get_service_url('LoadAndDumpEvaluator')
                    line = f'  TerrainBridgeBaseUrl: "{terrain_bridge_url}",\n'
                elif stripped_line.startswith('MaterialBalancesBaseUrl:'):
                    material_balances_url = self.get_service_url('MaterialLedgerService')
                    line = f'  MaterialBalancesBaseUrl: "{material_balances_url}",\n'
                elif stripped_line.startswith('LocalOffsetX:'):
                    x = MAPS[self.map]['x']
                    line = f'  LocalOffsetX: "{x}",\n'
                elif stripped_line.startswith('LocalOffsetY:'):
                    y = MAPS[self.map]['y']
                    line = f'  LocalOffsetY: "{y}",\n'
                elif stripped_line.startswith('EnableAuthenticationSkip:'):
                    line = f'  EnableAuthenticationSkip: "true"'
                    if stripped_line.endswith(','):
                        line += ','
                    line += '\n'
                for key, value in self.config.imperium_services.Centurion.environment.items():
                    if key.startswith('FeatureToggles__') and stripped_line.startswith(key.replace('FeatureToggles__', '')):
                        line = f'  {key.replace("FeatureToggles__", "")}: "{value}"'
                        if stripped_line.endswith(','):
                            line += ','
                        line += '\n'
                        break

                replaced_content += line

        with open(config_file_path, 'w') as fp:
            fp.write(replaced_content)


    def _update_overwatch_config(self, build_path: str):
        """
        Update overwatch config to point to defined url's.
        """
        config_file_path = os.path.join(build_path, 'config.js').replace('\\', '/')
        # Update url in config file to point to system url.
        if not os.path.exists(config_file_path) or os.stat(config_file_path).st_size == 0:
            raise Exception(f"Unable to locate config.js for overwatch at {config_file_path}")

        replaced_content = ""
        with open(config_file_path, 'r') as fp:
            for line in fp:
                stripped_line = line.strip()
                if stripped_line.startswith('ImperiumHubUrl:'):
                    imperium_hub_url = self.get_service_url('FieldSignalOffice')
                    line = f'  ImperiumHubUrl: "{imperium_hub_url}/ImperiumHub",\n'
                elif stripped_line.startswith('AssetStateReportingServiceUrl:'):
                    asset_state_reporting_url = self.get_service_url('AssetStateReportingService')
                    line = f'  AssetStateReportingServiceUrl: "{asset_state_reporting_url}",\n'
                elif stripped_line.startswith('DailyPlanManualUploadUrl:'):
                    daily_planner_url = self.get_service_url('DailyPlanner')
                    line = f'  DailyPlanManualUploadUrl: "{daily_planner_url}/DailyPlan/import?autoapproved=true",\n'
                elif stripped_line.startswith('MaterialDestinationBaseUrl:'):
                    material_destination_manager_url = self.get_service_url('MaterialDestinationManager')
                    line = f'  MaterialDestinationBaseUrl: "{material_destination_manager_url}",\n'
                elif stripped_line.startswith('MiningBlockUploadUrl:'):
                    mining_block_upload_url = self.get_service_url('MineModelService')
                    line = f'  MiningBlockUploadUrl: "{mining_block_upload_url}/miningblock/import",\n'
                elif stripped_line.startswith('SurveyBaseUrl:'):
                    survey_base_url = self.get_service_url('Survey')
                    line = f'  SurveyBaseUrl: "{survey_base_url}",\n'
                elif stripped_line.startswith('MineModelDraftServiceUrl:'):
                    mine_model_draft_service_url = self.get_service_url('MineModelDraftService')
                    line = f'  MineModelDraftServiceUrl: "{mine_model_draft_service_url}/draft",\n'
                elif stripped_line.startswith('MineModelDraftServiceBaseUrl:'):
                    mine_model_draft_service_base_url = self.get_service_url('MineModelDraftService')
                    line = f'  MineModelDraftServiceBaseUrl: "{mine_model_draft_service_base_url}",\n'
                elif stripped_line.startswith('MineModelServiceUrl:'):
                    mine_model_service_url = self.get_service_url('MineModelService')
                    line = f'  MineModelServiceUrl: "{mine_model_service_url}",\n'
                elif stripped_line.startswith('MineModelControlServiceBaseUrl:'):
                    mine_model_control_service_url = self.get_service_url('MineModelControlService')
                    line = f'  MineModelControlServiceBaseUrl: "{mine_model_control_service_url}",\n'
                elif stripped_line.startswith('AssignmentAggregatorServiceBaseUrl:'):
                    assignment_agg_service_url = self.get_service_url('Aggregator')
                    line = f'  AssignmentAggregatorServiceBaseUrl: "{assignment_agg_service_url}",\n'
                # elif stripped_line.startswith('MaterialBalancesBaseUrl:'):
                #     material_balances_url = self.get_service_url('MaterialBalances')
                #     line = f'  MaterialBalancesBaseUrl: "{material_balances_url}",\n'
                elif stripped_line.startswith('IdentityBaseUrl:'):
                    identity_base_url = self.get_service_url('IdentityService')
                    line = f'  IdentityBaseUrl: "{identity_base_url}",\n'
                elif stripped_line.startswith('AssetManagerBaseUrl:'):
                    asset_manager_base_url = self.get_service_url('AssetManager')
                    line = f'  AssetManagerBaseUrl: "{asset_manager_base_url}",\n'
                elif stripped_line.startswith('LocalOffsetX:'):
                    x = MAPS[self.map]['x']
                    line = f'  LocalOffsetX: "{x}",\n'
                elif stripped_line.startswith('LocalOffsetY:'):
                    y = MAPS[self.map]['y']
                    line = f'  LocalOffsetY: "{y}",\n'
                elif stripped_line.startswith('EnableAuthenticationSkip:'):
                    line = f'  EnableAuthenticationSkip: "true"'
                    if stripped_line.endswith(','):
                        line += ','
                    line += '\n'
                for key, value in self.config.imperium_services.Overwatch.environment.items():
                    if key.startswith('FeatureToggles__') and stripped_line.startswith(key.replace('FeatureToggles__', '')):
                        line = f'  {key.replace("FeatureToggles__", "")}: "{value}"'
                        if stripped_line.endswith(','):
                            line += ','
                        line += '\n'
                        break
                replaced_content += line

        with open(config_file_path, 'w') as fp:
            fp.write(replaced_content)
