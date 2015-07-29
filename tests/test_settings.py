from flask import url_for

import pytest

import roomcontrol.utils.localstorage as ls


TEST_FILE = """
[settings]
serverip=0.0.0.0
notify=False
sendpic=True
"""


@pytest.fixture
def storage_file(tmpdir):
    p = tmpdir.join('test_storage.in')
    p.write(TEST_FILE)
    ls.set_storage_file(str(p))


def test_response_get_settings(storage_file, client):
    assert client.get(url_for('main.settings')).status_code == 200


def test_get_returns_right_vals(storage_file, client):
    res = client.get(url_for('main.settings'))
    assert res.json == {
        'serverip': '0.0.0.0',
        'notify': 'False',
        'sendpic': 'True'
    }


def test_post_response_ok(storage_file, client):
    res = client.post(
        url_for('main.settings'),
        data='{}',
        headers={'Content-Type': 'application/json'})
    assert res.status_code == 200


def test_post_response_sends_ok_message(storage_file, client):
    res = client.post(
        url_for('main.settings'),
        data='{}',
        headers={'Content-Type': 'application/json'})
    assert res.data == b'settings updated'


def test_post_updates_all_fields(storage_file, client):
    client.post(
        url_for('main.settings'),
        data='{"serverip": "127.0.0.1", "notify": true, "sendpic": false}',
        headers={'Content-Type': 'application/json'})
    settings = ls.get_all('settings')
    assert settings['serverip'] == '127.0.0.1'
    assert settings['notify'] == 'True'
    assert settings['sendpic'] == 'False'


def test_post_updates_some_fields(storage_file, client):
    client.post(
        url_for('main.settings'),
        data='{"notify": true, "sendpic": false}',
        headers={'Content-Type': 'application/json'})
    settings = ls.get_all('settings')
    assert settings['serverip'] == '0.0.0.0'
    assert settings['notify'] == 'True'
    assert settings['sendpic'] == 'False'


def test_post_ignores_unexistant_fields(storage_file, client):
    client.post(
        url_for('main.settings'),
        data='{"fantasy": "fiction"}',
        headers={'Content-Type': 'application/json'})
    settings = ls.get_all('settings')
    with pytest.raises(KeyError):
        assert settings['fantasy'] == 'fiction'
