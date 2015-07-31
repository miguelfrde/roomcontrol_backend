import unittest.mock as mock

from nameko.testing.services import worker_factory

import pytest

from roomcontrol.services.http_entrypoint import HttpEntrypointService


@pytest.fixture
def http_ep():
    sample_settings = {
        'serverip': '0.0.0.0',
        'notify': 'False',
        'sendpic': 'True'
    }
    service = worker_factory(HttpEntrypointService)
    service.storage_rpc.get_all = mock.Mock(return_value=sample_settings)
    return service


def test_get_settings_calls_storage_get_all(http_ep):
    http_ep.get_settings(None)
    http_ep.storage_rpc.get_all.assert_called_once_with('settings')


def test_update_settings_calls_storage_set_all(http_ep):
    request = mock.Mock()
    data = b'{"serverip": "1.1.1.1", "notify": true, "sendpic": false}'
    out = {'serverip': '1.1.1.1', 'notify': 'True', 'sendpic': 'False'}
    request.get_data = mock.Mock(return_value=data)
    http_ep.update_settings(request)
    http_ep.storage_rpc.set_all.assert_called_once_with('settings', out)


def test_update_settings_ignores_unknown_attrs(http_ep):
    request = mock.Mock()
    data = b'{"serverip": "1.1.1.1", "random": 2, "sendpic": false}'
    out = {'serverip': '1.1.1.1', 'notify': 'False', 'sendpic': 'False'}
    request.get_data = mock.Mock(return_value=data)
    http_ep.update_settings(request)
    http_ep.storage_rpc.set_all.assert_called_once_with('settings', out)
