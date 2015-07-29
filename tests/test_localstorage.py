import os

import pytest

import roomcontrol.utils.localstorage as ls


TEST_FILE = """
[kind1]
a=1
b=2

[kind2]
c=3
"""


@pytest.fixture
def init_test_file(tmpdir):
    p = tmpdir.join('test_localstorage.in')
    os.environ['ROOMCONTROL_STORAGE'] = str(p)
    p.write(TEST_FILE)


def test_set_corresponds_to_get(init_test_file):
    ls.set('kind2', 'd', '4')
    assert ls.get('kind2', 'd') == '4'


def test_set_all_corresponds_to_get_all(init_test_file):
    data = {'e': '5', 'f': '6'}
    ls.set_all('kind3', data)
    assert ls.get_all('kind3') == data
