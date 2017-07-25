import os
import pytest
from mock import MagicMock, patch, call
from pyolite import User
from pyolite.views import ListUsers
from pyolite.models.repository import Repository
from unipath import Path


@pytest.fixture
def tmpolite(tmpdir):
    root = str(tmpdir)
    config = os.path.join(str(root), 'config')
    git = MagicMock()
    os.mkdir(os.path.join(root, 'conf'))
    os.mkdir(os.path.join(root, 'keydir'))
    open(config, 'w').write('')
    return Path(root), git


def test_if_we_add_invalid_permissions_it_should_raise_ValueError(tmpolite):
    path, git = tmpolite
    repo = Repository('name', path, git)
    with pytest.raises(ValueError):
        repo.users.add('test', 'hiRW+')


def test_it_should_add_a_new_user_to_repo_if_is_valid(tmpolite):
        path, git = tmpolite
        repo = Repository('name', path, git)
        repo.users.add('test', 'RW+')

        content = '    RW+     =    another_user\n'
        assert content in open(path).read()

        message = 'User another_user added to repo test_repo ' \
                  'with permissions: RW+'
        git.commit.has_calls([call(['conf'], message)])

def test_user_removing():
    mocked_repo = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mock_single_user = MagicMock()
    mock_single_user.name = 'another_user'
    mock_single_user.__str__ = lambda x: 'another_user'

    mocked_repository.name = 'test_repo'
    mocked_repository.path = 'path'

    mocked_user.get.return_value = mock_single_user
    mocked_repo.users = ['user']

    with patch.multiple('pyolite.views.users',
                        Repo=MagicMock(return_value=mocked_repo),
                        User=mocked_user):
        repo_users = ListUsers(mocked_repository)
        repo_users.remove('test')

        pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % 'another_user'
        mocked_repo.replace.assert_called_once_with(pattern, "")

        message = "Deleted user another_user from repository test_repo"
        mocked_repository.git.commit.has_calls([call(['conf'], message)])

def test_user_edit_permissions():
    mocked_repo = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mock_single_user = MagicMock()
    mock_single_user.name = 'another_user'
    mock_single_user.__str__ = lambda x: 'another_user'

    mocked_repository.name = 'test_repo'
    mocked_repository.path = 'path'

    mocked_user.get.return_value = mock_single_user
    mocked_repo.users = ['user']

    with patch.multiple('pyolite.views.users',
                        Repo=MagicMock(return_value=mocked_repo),
                        User=mocked_user):
        repo_users = ListUsers(mocked_repository)
        repo_users.edit('test', 'R')

        pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % 'another_user'
        string = r"\n    %s    =    %s" % ('R', 'another_user')
        mocked_repo.replace.assert_called_once_with(pattern, string)

        message = "User another_user has R permission for repository test_repo"
        mocked_repository.git.commit.has_calls([call(['conf'], message)])

def test_user_get_or_create():
    mocked_repo = MagicMock()
    mocked_repository = MagicMock()

    mocked_repository.name = 'test_repo'
    mocked_repository.path = 'path'

    with patch.multiple('pyolite.views.users',
                        Repo=MagicMock(return_value=mocked_repo)):
        found_user = object()
        mocked_user_get = MagicMock(return_value=found_user)

        with patch.multiple('pyolite.models.user.User', get=mocked_user_get):
            repo_users = ListUsers(mocked_repository)

            # user found
            user = repo_users.get_or_create('test_user')
            assert user is found_user

            # user created
            mocked_user_get.side_effect = ValueError
            user = repo_users.get_or_create('test_user')
            assert user.name is 'test_user'
