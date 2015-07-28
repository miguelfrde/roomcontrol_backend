import pytest

from roomcontrol.utils.localstorage import LocalStorage


TEST_FILE = """
[kind1]
a=1
b=2

[kind2]
c=3
"""


@pytest.fixture
def ls(tmpdir):
    p = tmpdir.join('test_localstorage.in')
    p.write(TEST_FILE)
    obj = LocalStorage(str(p))
    return obj


def test_set_corresponds_to_get(ls):
    ls.set('kind2', 'd', '4')
    assert ls.get('kind2', 'd') == '4'


def test_set_all_corresponds_to_get_all(ls):
    data = {'e': '5', 'f': '6'}
    ls.set_all('kind3', data)
    assert ls.get_all('kind3') == data
