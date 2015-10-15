import os

import pytest

from roomcontrol.services.localstorage import LocalStorageService

TEST_FILE = """
[kind1]
a = 1
b = 2

[kind2]
c = 3
"""


TEST_FILE_EDIT_SET = """
[kind1]
a = 1
b = 2

[kind2]
c = 3
d = 4
""".strip()

TEST_FILE_EDIT_SET_ALL_OPT1 = """
[kind1]
a = 1
b = 2

[kind2]
c = 3

[kind3]
e = 5
f = 6
""".strip()

TEST_FILE_EDIT_SET_ALL_OPT2 = """
[kind1]
a = 1
b = 2

[kind2]
c = 3

[kind3]
f = 6
e = 5
""".strip()


@pytest.fixture
def localstorage(tmpdir):
    p = tmpdir.join('test_localstorage.in')
    p.write(TEST_FILE)
    os.environ['ROOMCONTROL_STORAGE'] = str(p)
    ls = LocalStorageService()
    return ls


def test_sets_env_variable_on_change_file(localstorage):
    localstorage.set_storage_file('test.cfg')
    assert os.environ.get('ROOMCONTROL_STORAGE') == 'test.cfg'


def test_sets_variable_on_change_file(localstorage):
    localstorage.set_storage_file('test.cfg')
    assert localstorage.storage_file == 'test.cfg'


def test_set_corresponds_to_get(localstorage):
    localstorage.set('kind2', 'd', '4')
    assert localstorage.get('kind2', 'd') == '4'


def test_set_all_corresponds_to_get_all_parsed(localstorage):
    data = {'e': '5', 'f': 6, 'g': 'ab', 'h': True}
    expected = {'e': 5, 'f': 6, 'g': 'ab', 'h': True}
    localstorage.set_all('kind3', data)
    assert localstorage.get_all('kind3') == expected


def test_set_edits_file(localstorage):
    localstorage.set('kind2', 'd', '4')
    with open(os.environ['ROOMCONTROL_STORAGE'], 'r') as f:
        assert f.read().strip() == TEST_FILE_EDIT_SET


def test_set_all_edits_file(localstorage):
    localstorage.set_all('kind3', {'e': '5', 'f': '6'})
    with open(os.environ['ROOMCONTROL_STORAGE'], 'r') as f:
        fcontent = f.read().strip()
        assert fcontent == TEST_FILE_EDIT_SET_ALL_OPT1 or \
            fcontent == TEST_FILE_EDIT_SET_ALL_OPT2
