__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import os
import psutil

class ExceptionWithScreenImage(Exception):
    """Capturea a Page Screenshot before throwing the exception"""
    def __init__(self, message=None):
        old_log_level = BuiltIn().run_keyword('Set Log Level', 'INFO')
        BuiltIn().run_keyword('Capture Page Screenshot')
        BuiltIn().run_keyword('Set Log Level', old_log_level)
        if os.name != 'nt':
            logger.info('CPU count: {} Load averages: 1, 5, and 15 min: {}'.format(os.cpu_count(), os.getloadavg()))
        logger.info('System memory usage: {}'.format(psutil.virtual_memory()))        
        self.msg = f"{message}" if message else ""
    def __str__(self):
        return self.msg
