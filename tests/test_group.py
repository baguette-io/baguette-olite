import mock
import os
import pytest
from pyolite import Pyolite
from pyolite import Group

@pytest.fixture
def olite(tmpdir):
    with mock.patch('pyolite.git.Git.commit', mock.MagicMock()):
        pyolite = Pyolite(str(tmpdir))
        yield pyolite

@pytest.fixture
def group1(olite):
    return olite.groups.create('group1')

def test_create(olite):
    group = olite.groups.create('test_create')
    assert os.path.exists(group.config)
    assert open(group.config).read() == ""

def test_create_idempotent(olite):
    group = olite.groups.create('test_create')
    assert olite.groups.create('test_create')
    assert os.path.exists(group.config)
    assert open(group.config).read() == ""

def test_get(olite, group1):
    group2 = olite.groups.get('group1')
    assert group1.name == group2.name
    assert group1.path == group2.path
    assert group1.config == group2.config
    assert open(group1.config).read() == open(group2.config).read() == ""
    #
    group3 = Group('group1', olite.groups.path, olite.groups.git)
    assert group1.config == group2.config == group3.config

def test_get_not_exist(olite):
    with pytest.raises(ValueError):
        olite.groups.get('inexistant')
    #
    with pytest.raises(ValueError):
        Group.get('inexistant', olite.groups.path, olite.groups.git)

def test_get_or_create(olite):
    group1 = olite.groups.get_or_create('test_create')
    group2 = olite.groups.get_or_create('test_create')
    assert group1.name == group2.name
    assert group1.path == group2.path
    assert group1.config == group2.config
    assert open(group1.config).read() == ""
    assert open(group2.config).read() == ""

def test_all(olite):
    olite.groups.create('group1')
    olite.groups.create('group2')
    olite.groups.create('group3')
    listdir = os.listdir(os.path.join(olite.admin_repository, 'conf', 'groups'))
    assert len(listdir) == 3
    assert sorted(listdir) == ['group1.conf', 'group2.conf', 'group3.conf']

def test_delete(olite, group1):
    assert os.path.exists(group1.config) is True
    assert olite.groups.delete('group1') is True
    assert os.path.exists(group1.config) is False

def test_delete_not_exist(olite):
    assert olite.groups.delete('group2') is False
