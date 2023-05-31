__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

import requests
import httpx
import asyncio
from test_code.Environment import Environment
from test_code.ImperiumServices import ImperiumServices

class BaseClient:
    __base_url = None
    _imperium_services = None
    _environment = None

    @property
    def imperium_services(self):
        if not self._imperium_services:
            self._imperium_services = ImperiumServices()
        return self._imperium_services

    @property
    def environment(self):
        if not self._environment:
            self._environment = Environment()
        return self._environment

    def __init__(self, url=None):
        self.__base_url = url

    async def http_request(self, url: str, data=None, headers=None):
        cert = None
        if self.imperium_services.certs:
            cert = (list(self.imperium_services.certs.keys())[0], list(self.imperium_services.certs_key.keys())[0]) 
        async with httpx.AsyncClient(http2=True, cert=cert, verify=False) as client:
            if data:
                response = await client.post(url=url, data=data, headers=headers)
            else:
                response = await client.get(url=url, headers=headers)
            response.raise_for_status()
            return response

    def get(self, url, headers={'Accept' : 'application/json', 'Content-Type' : 'application/json'}, service: str=None):
        if service is not None:
            self.__base_url = self.imperium_services.get_service_url(service)
        self.environment.env_log('Get: ' + self.__base_url + url, 'debug')
        response = asyncio.run(self.http_request(self.__base_url + url, headers=headers))
        if response.status_code != 200:
            raise Exception('Response Status: ' + str(response.status_code))

        self.environment.env_log('Response: ' + response.text, 'trace')
        return response

    def post(self, url, headers, body):

        self.environment.env_log('Post: {} with body: {}'.format(self.__base_url + url, body), 'debug')

        response = asyncio.run(self.http_request(self.__base_url + url, headers=headers, data=body))
        if response.status_code != 200:
            raise Exception('Response Status: ' + str(response.status_code))

        self.environment.env_log('Response: ' + response.text, 'trace')

        return response

    def patch(self, url, headers, body = None):
        self.environment.env_log('patch: ' + url + ' with body: {}'.format(body), 'debug')

        response = requests.patch(url = self.__base_url + url, headers = headers, data=body)
        self.environment.env_log('Response Status: ' + str(response.status_code), 'trace')
        self.environment.env_log('Response: ' + response.text, 'trace')

        return response

    def put(self, url, headers, body):
        self.environment.env_log('Put: ' + url + ' with body: ' + body, 'debug')

        response = requests.put(url = self.__base_url + url, headers = headers, data=body)
        self.environment.env_log('Response Status: ' + str(response.status_code), 'trace')
        self.environment.env_log('Response: ' + response.text, 'trace')

        return response

    def delete(self, url, headers):
        self.environment.env_log('Delete: ' + url, 'debug')

        response = requests.delete(url = self.__base_url + url, headers = headers)
        self.environment.env_log('Response Status: ' + str(response.status_code), 'trace')
        self.environment.env_log('Response: ' + response.text, 'trace')

        return response