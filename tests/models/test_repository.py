from mock import MagicMock, patch

from pyolite.models.repository import Repository


def test_it_should_be_possible_to_retrieve_by_name_a_repo():
    mocked_users = MagicMock()
    mocked_file = MagicMock()
    mocked_dir = MagicMock()
    mocked_path = MagicMock()

    mocked_dir.isdir.return_value = True
    mocked_file.isdir.return_value = False
    mocked_file.__str__ = lambda x: 'tests/fixtures/get_repo_by_name.conf'

    mocked_path.walk.return_value = [mocked_file, mocked_dir]

    with patch.multiple('pyolite.models.repository',
                        Path=MagicMock(return_value=mocked_path),
                        ListUsers=MagicMock(return_value=mocked_users)):
        repo = Repository.get_by_name('new_one', 'simple_path', 'git')

        assert repo.name == 'new_one'
        assert repo.path == 'simple_path'
        assert repo.git == 'git'
        assert repo.users == mocked_users


def test_if_we_find_only_directories_should_return_none():
    mocked_users = MagicMock()
    mocked_dir = MagicMock()
    mocked_path = MagicMock()

    mocked_dir.isdir.return_value = True

    mocked_path.walk.return_value = [mocked_dir]

    with patch.multiple('pyolite.models.repository',
                        Path=MagicMock(return_value=mocked_path),
                        ListUsers=MagicMock(return_value=mocked_users)):
        repo = Repository.get_by_name('new_one', 'simple_path', 'git')
        assert repo == None
