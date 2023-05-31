__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

"""
IMPORTANT:

This file is being used by scripts and outside robot framework. Please do not add
any robot framework dependency.
"""

import os

from typing import Dict, List

ASSET_PORTS_START = 3020

# SDK used.
NODE_DOCKER='node:12.22.0'

AUTOMATED_TEST_DIR = os.path.dirname(os.path.abspath(os.path.dirname(os.path.realpath(__file__)))).replace('\\', '/')
IMPERIUM_DIR = os.path.dirname(AUTOMATED_TEST_DIR)

ARTIFACTORY_URL = 'artifactory.fmgl.com.au'
ARTIFACTORY_DOCKER_URL = 'https://artifactory.fmgl.com.au/artifactory/api/storage/docker-ams-fms/{}/?list&listFolders=1'
ARTIFACTORY_DOCKER_IMAGE_PREFIX = 'artifactory.fmgl.com.au/docker-ams-fms'

CERTS_DIR = os.path.join(IMPERIUM_DIR, 'infrastructure', 'certificates')

# Supported screen resolution
SUPPORTED_SCREEN_RESOLUTIONS: Dict = {
    'Centurion': ['1024', '768'],
    'Overwatch': ['2560', '1080'],
    'DataSimulator': ['1280', '1024'],
}

REDACT_REGION: Dict = {
    'Centurion': ['0', '1264', '0', '150'],
    'Overwatch': ['0', '2560', '0', '80'],
    'AssetHistoryTimeStamp': ['470', '85', '40', '20']
}
# here we have to update tho code autoupgrade browser drivers
BROWSER_DRIVER = {
    'firefox': {
        'driver': 'v0.30.0',
        'docker_image': 'selenium/standalone-firefox:98.0',
    },
    'chrome': {

        'driver': '113.0.5672.63',
        'docker_image': 'selenium/standalone-chrome:108.0',
    }
}

RABBITMQ_POLL_THRESHOLD_SECS = 5

MAPS = {
    'Hazelmere': {
        'x': '-40652026',
        'y': '-646788798',
        'fms_domain': 49,
        'default_asset': 'DT5401',
        'default_participant_id': 3,
        'allowed_assets': {
            'DT5430-T': {'x': 40646710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5431-T': {'x': 40646910, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5410-D': {'x': 40647710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5411-D': {'x': 40647910, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5420-B': {'x': 40648710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5421-B': {'x': 40648910, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5422-B': {'x': 40649710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5401': {'x': 40646710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5402': {'x': 40652946, 'y': 646777409, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5403': {'x': 40653146, 'y': 646777409, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5404': {'x': 40654146, 'y': 646777109, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'DT5403-VB': {'x': 40653146, 'y': 646777409, 'z': 1700, 'yaw': 0, "class": "DumpTruck"},
            'LV001': {'x': 40646710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "LightVehicle"},
            'EX7109': {'x': 40655146, 'y': 646786109, 'z': 1700, 'yaw': 0, "class": "Excavator"},
            'EX7110': {'x': 40652246, 'y': 646787809, 'z': 1700, 'yaw': 0, "class": "Excavator"},
            'AHT001': {'x': 40646710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck", 'ParticipantId': 3, 'mode': 'auto'},
            'AHT002': {'x': 40646710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck", 'ParticipantId': 4, 'mode': 'auto'},
            'AHT003-ER': {'x': 40646710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "DumpTruck", 'ParticipantId': 4, 'mode': 'auto'},
            'DZ001': {'x': 40646710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "WheelDozer"},
            'WL4434': {'x': 40646710, 'y': 646780169, 'z': 1700, 'yaw': 0, "class": "WheelLoader"},
        }
    },
    'FlindersDrive': {
        'x': '-77949000',
        'y': '-752574000',
        'fms_domain': 49,
        'default_asset': 'AHT001',
        'default_participant_id': 3,
        'allowed_assets': {
            'ALV020': {'x': 77975035, 'y': 752491329, 'z': -601, 'yaw': 0.0, "class": "LightVehicle"},
            'EX001': {'x': 77952584, 'y': 752588545, 'z': -601, 'yaw': 0.0, "class": "Excavator"},
            'AHT001': {'x': 77934584, 'y': 752588545, 'z': -601, 'yaw': 1.797, "class": "DumpTruck", 'ParticipantId': 3, 'mode': 'auto', 'ip': '10.47.104.124'},
            'AHT002': {'x': 77977035, 'y': 752491729, 'z': -601, 'yaw': 0, "class": "DumpTruck", 'ParticipantId': 4, 'mode': 'auto'},
            'AHT003': {'x': 77977035, 'y': 752491729, 'z': -601, 'yaw': 0.0, "class": "DumpTruck", 'ParticipantId': 5, 'mode': 'auto'},
        }
    },
    'FlyingFish': {
        'x': '-70315117',
        'y': '-750019969',
        'fms_domain': 49,
        'default_asset': 'AHT001',
        'default_participant_id': 3,
        'allowed_assets': {
            'ALV020': {'x': 70315117, 'y': 750019969, 'z': -601, 'yaw': 0.0, "class": "LightVehicle"},
            'EX001': {'x': 70308952, 'y': 750019975, 'z': -601, 'yaw': 0.0, "class": "Excavator"},
            'AHT001': {'x': 70031296, 'y': 750029530, 'z': -601, 'yaw': 1.797, "class": "DumpTruck", 'ParticipantId': 3, 'mode': 'auto', 'ip': '10.47.104.124'},
            'AHT002': {'x': 70234704, 'y': 750023936, 'z': -601, 'yaw': 0, "class": "DumpTruck", 'ParticipantId': 4, 'mode': 'auto'},
            'AHT003': {'x': 70638232, 'y': 750022563, 'z': -601, 'yaw': 0.0, "class": "DumpTruck", 'ParticipantId': 5, 'mode': 'auto'},
        }
    },
    'IronBridgeDemo': {
        'x': '-71255607',
        'y': '-764868091',
        'fms_domain': 49,
        'default_asset': 'RD4578',
        'default_participant_id': 3,
        'allowed_assets': {
            'RD4578': {'x': 71255607, 'y': 764868091, 'z': -601, 'yaw': 0.0, "class": "DumpTruck"},
            'RD4579': {'x': 71271207, 'y': 764884091, 'z': -601, 'yaw': 0.0, "class": "DumpTruck"},
            'RD4580': {'x': 71262807, 'y': 764856591, 'z': -601, 'yaw': 5.1836, "class": "DumpTruck"},
            'RD2031': {'x': 71271307, 'y': 764835891, 'z': -601, 'yaw': 5.1836, "class": "DumpTruck"},
            'RD2028': {'x': 71280165, 'y': 764822979, 'z': -601, 'yaw': 5.340, "class": "DumpTruck"},
            'RD2025': {'x': 71320220, 'y': 764859996, 'z': -601, 'yaw': 1.623, "class": "DumpTruck"},
            'EX8277': {'x': 71253694, 'y': 764836886, 'z': -601, 'yaw': 5.235, "class": "Excavator"},
            'EX2366': {'x': 71247555, 'y': 764848583, 'z': -601, 'yaw': 0.157, "class": "Excavator"},
            'EX8109': {'x': 71377297, 'y': 764823714, 'z': -601, 'yaw': 0.366, "class": "Excavator"},
            'IB0051': {'x': 71383111, 'y': 764833945, 'z': -601, 'yaw': 1.038, "class": "LightVehicle"},
            'IB0031': {'x': 71362245, 'y': 764831024, 'z': -601, 'yaw': 0.0, "class": "LightVehicle"},
            'DZ0001': {'x': 71374418, 'y': 764804541, 'z': -601, 'yaw': 5.602, "class": "WheelDozer"},
            'DZ0002': {'x': 71371000, 'y': 764786663, 'z': -601, 'yaw': 4.502, "class": "WheelDozer"},
            'DZ0003': {'x': 71353015, 'y': 764809419, 'z': -601, 'yaw': 1.727, "class": "WheelDozer"},
            'DZ0004': {'x': 71344876, 'y': 764844979, 'z': -601, 'yaw': 1.832, "class": "WheelDozer"},
            'LV010': {'x': 71325460, 'y': 764853682, 'z': -601, 'yaw': 2.932, "class": "LightVehicle"},
            'LV011': {'x': 71327501, 'y': 764866348, 'z': -601, 'yaw': 0.052, "class": "LightVehicle"},
        }
    }
}

DEPLOYED_ENVS = {
    'dev': {
        'certs': {
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'dev', 'apps.dev.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.dev.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt:ro",
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.dev.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt:ro",
        },
        'certs_key': {
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'dev', 'apps.dev.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-ca-cert.key')}".replace('\\', '/'):
                "/keys/apps.dev.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-ca-cert.key:ro",
        },
        'url': "https://{}.apps.dev.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud",
        "http2": True,
    },
    'test': {
        'certs': {
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'test', 'apps.test.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.test.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt:ro",
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.test.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt:ro",
        },
        'certs_key': {
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'test', 'apps.test.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-ca-cert.key')}".replace('\\', '/'):
                "/keys/apps.test.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-ca-cert.key:ro",
        },
        'url': "https://{}.apps.test.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud",
        "http2": True,
    },
    'int': {
        'certs': {
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'int', 'apps.int.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.int.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt:ro",
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.int.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt:ro",
        },
        'certs_key': {
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'int', 'apps.int.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-ca-cert.key')}".replace('\\', '/'):
                "/keys/apps.int.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-ca-cert.key:ro",
        },
        'url': "https://{}.apps.int.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud",
        "http2": True,
    },
    'stg': {
        'certs': {
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'stg', 'apps.stg.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.stg.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt:ro",
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.stg.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt:ro",
        },
        'certs_key': {
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'stg', 'apps.stg.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-ca-cert.key')}".replace('\\', '/'):
                "/keys/apps.stg.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-ca-cert.key:ro",
        },
        'url': "https://{}.apps.stg.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud",
        "http2": True,
    },
    'hzltest': {
        'certs': {
            f"{os.path.join(CERTS_DIR, 'hazelmere', 'apps.hzltest.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.hzltest.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.crt:ro",
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.int.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt:ro",
        },
        'certs_key': {
            f"{os.path.join(CERTS_DIR, 'hazelmere', 'apps.hzltest.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-wildcard-ca-cert.key')}".replace('\\', '/'):
                "/keys/apps.hzltest.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud:ro",
        },
        'url': "https://{}.apps.hzltest.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud",
        "http2": True,
    },
    'local': {
        'certs': {
            f"{os.path.join(CERTS_DIR, 'local', 'fms.localdev.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/fms.localdev.crt:ro",
            f"{os.path.join(CERTS_DIR, 'docker_swarm', 'fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt')}".replace('\\', '/'):
                "/usr/local/share/ca-certificates/apps.dev.fms-swarm-nonprod.npe.apse2.fmgawsdev.cloud-root-ca-cert.crt:ro",
        },
        'certs_key': {
            f"{os.path.join(CERTS_DIR, 'local', 'fms.localdev.key')}".replace('\\', '/'):
                "/keys/fms.localdev.key:ro",
        },
        'url': "https://{}.apps.fms-dev.local",
        "http2": True,
    },
}

TELEMETRY_DATA = {
    'payload': {
        'identifier': 1,
        'description': 'Payload',
        'default_value': 0
    },
    'vasGpsSpeed': {
        'identifier': 2,
        'description': 'Gps Speed',
        'default_value': 0
    },
    'smuHours': {
        'identifier': 3,
        'description': 'Smu Hours',
        'default_value': 1000
    },
    'manualFuelLevel': {
        'identifier': 4,
        'description': 'Manual Fuel Level',
        'default_value': 10
    },
    'altitude': {
        'identifier': 5,
        'description': 'Altitude',
        'default_value': 0
    },
    'latitude': {
        'identifier': 6,
        'description': 'Latitude',
        'default_value': 0
    },
    'longitude': {
        'identifier': 7,
        'description': 'Longitude',
        'default_value': 0
    },
    'groundSpeed': {
        'identifier': 8,
        'description': 'Ground Speed',
        'default_value': 0
    },
    'inputVoltage': {
        'identifier': 9,
        'description': 'Input Voltage',
        'default_value': 27.308
    },
    'trayTilt': {
        'identifier': 10,
        'description': 'Tray Tilt',
        'default_value': 0
    },
    'trayAngle': {
        'identifier': 11,
        'description': 'Tray Angle',
        'default_value': 0
    },
    'transmissionGear': {
        'identifier': 12,
        'description': 'Transmission Gear',
        'default_value': 64
    },
    'fuelRate': {
        'identifier': 13,
        'description': 'Fuel Rate',
        'default_value': 21.3999996
    },
    'engineSpeed': {
        'identifier': 14,
        'description': 'Engine Speed',
        'default_value': 700.5
    },
    'coolantTemp': {
        'identifier': 15,
        'description': 'Coolant Temp',
        'default_value': 70
    },
    'throttlePosition': {
        'identifier': 16,
        'description': 'Throttle Position',
        'default_value': 27.60000381
    },
    'sensorFuelLevel': {
        'identifier': 17,
        'description': 'Sensor Fuel Level',
        'default_value': 472.27
    },
    'sensorPayload': {
        'identifier': 18,
        'description': 'Sensor Pay load',
        'default_value': 0
    },
    'leftFrontStrutPressure': {
        'identifier': 19,
        'description': 'Left Front Strut Pressure',
        'default_value': 1952
    },
    'rightFrontStrutPressure': {
        'identifier': 20,
        'description': 'Right Front Strut Pressure',
        'default_value': 1962
    },
    'leftRearStrutPressure': {
        'identifier': 21,
        'description': 'Left Rear Strut Pressure',
        'default_value': 2653
    },
    'rightRearStrutPressure': {
        'identifier': 22,
        'description': 'Right Rear Strut Pressure',
        'default_value': 2674
    },
    'p7Y': {
        'identifier': 23,
        'description': 'P7Y',
        'default_value': 32784
    },
    'transmissionShifts': {
        'identifier': 24,
        'description': 'Transmission Shifts',
        'default_value': 0
    },
    'parkBrakeState': {
        'identifier': 25,
        'description': 'Park Brake State',
        'default_value': 32767
    },
    'travelLoaded': {
        'identifier': 26,
        'description': 'Travel Loaded',
        'default_value': 0
    },
    'travelEmpty': {
        'identifier': 27,
        'description': 'Travel Empty',
        'default_value': 0
    },
    'travelLoadedDistance': {
        'identifier': 28,
        'description': 'Travel Loaded Distance',
        'default_value': 0
    },
    'travelEmptyDistance': {
        'identifier': 29,
        'description': 'Travel Empty Distance',
        'default_value': 0
    },
    'stoppedLoaded': {
        'identifier': 30,
        'description': 'Stopped Loaded',
        'default_value': 0
    },
    'stoppedEmpty': {
        'identifier': 31,
        'description': 'Stopped Empty',
        'default_value': 0
    },
    'loadingPasses': {
        'identifier': 32,
        'description': 'Loading Passes',
        'default_value': 0
    },
    'loadingTime': {
        'identifier': 33,
        'description': 'Loading Time',
        'default_value': 0
    },
    'payloadState': {
        'identifier': 34,
        'description': 'Payload State',
        'default_value': 5
    }
}