import logging

from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient

log = logging.getLogger(__name__)


class CallfireClient:
    def __init__(self, login, password, config=None):
        self.config = {
            'validate_responses': False,
            'proxies': {}
        }
        self.config.update({} if config is None else config)

        log.debug('CallfireClient.config %s', self.config)
        self.http_client = RequestsClient()
        self.http_client.session.proxies.update(self.config['proxies'])
        self.http_client.set_basic_auth('api.callfire.com', login, password)
        self.swagger_client = SwaggerClient.from_url(
            spec_url=self.swagger_url(),
            http_client=self.http_client,
            config=self.config)

    def __getattr__(self, item):
        return getattr(self.swagger_client, item)

    @staticmethod
    def swagger_url():
        return 'https://www.callfire.com/v2/api-docs/swagger.json'
