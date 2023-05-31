__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from test_code.services.BaseClient import BaseClient

class RoutingService(BaseClient):

    def __init__(self):
        super().__init__(self.imperium_services.get_service_url('RoutingService'))

    def get_url(self):
        return self.imperium_services.get_service_url('RoutingService')

    def get_headers(self):
        return {'Accept' : 'application/json', 'Content-Type' : 'application/json'}