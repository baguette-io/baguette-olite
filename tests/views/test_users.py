import os
import pytest
import random
import string
from mock import MagicMock, patch, call
from pyolite import User
from pyolite.views import ListUsers
from pyolite.models.repository import Repository
from unipath import Path


def random_name(length=10):
       return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

@pytest.fixture
def tmpolite(tmpdir):
    name = random_name()
    root = str(tmpdir)
    git = MagicMock()
    os.mkdir(os.path.join(root, 'conf'))
    os.mkdir(os.path.join(root, 'conf', 'groups'))
    os.mkdir(os.path.join(root, 'conf', 'repos'))
    os.mkdir(os.path.join(root, 'keydir'))
    open(os.path.join(root, 'conf', 'groups','%s.conf' % name), 'w').write('')
    open(os.path.join(root, 'conf', 'repos','%s.conf' % name), 'w').write('')
    return name, Path(root), git


def test_if_we_add_invalid_permissions_it_should_raise_ValueError(tmpolite):
    name, path, git = tmpolite
    repo = Repository(name, path, git)
    with pytest.raises(ValueError):
        repo.users.add('test', 'hiRW+')


def test_it_should_add_a_new_user_to_repo_if_is_valid(tmpolite):
        name, path, git = tmpolite
        repo = Repository(name, path, git)
        repo.users.add('test', 'RW+')

        content = '        RW+         =        test\n'
        assert content in open(repo.config).read()

        message = 'User test added to repo test_repo ' \
                  'with permissions: RW+'
        git.commit.has_calls([call(['conf'], message)])

def test_user_removing(tmpolite):
        name, path, git = tmpolite
        repo = Repository(name, path, git)
        #
        repo.users.add('test', 'RW+')
        content = '        RW+         =        test\n'
        assert content in open(repo.config).read()
        #
        repo.users.remove('test')
        assert '' in open(repo.config).read()

        message = "Deleted user test from repository test_repo"
        git.commit.has_calls([call(['conf'], message)])

def test_user_edit_permissions(tmpolite):
    name, path, git = tmpolite
    repo = Repository(name, path, git)
    #
    repo.users.add('test', 'RW+')
    repo.users.add('toto', 'RW+')
    content = '        RW+         =        test\n'
    assert content in open(repo.config).read()
    content = '        RW+         =        toto\n'
    assert content in open(repo.config).read()
    #
    repo.users.edit('test', 'R')
    content = '        R        =        test\n'
    assert content in open(repo.config).read()
    content = '        RW+         =        toto\n'
    assert content in open(repo.config).read()
    #
    message = "User another_user has R permission for repository test_repo"
    git.commit.has_calls([call(['conf'], message)])
