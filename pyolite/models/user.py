import re
from six import string_types
from  unipath import Path

from pyolite.views import ListKeys


class User(object):
    def __init__(self, name, path, git, **kwargs):
        self.name = name
        self.path = path
        self.git = git
        self.regex = re.compile(r'=( *)(\w+)')
        #
        self.repos = kwargs.get('repos') or []
        self.keys = ListKeys(self, kwargs.get('keys') or [])

    @classmethod
    def get_by_name(cls, name, path, git):
        # get user's keys
        key_path = Path(str(path), 'keydir')
        keys = [key for key in key_path.walk() if key.endswith('%s.pub' % name)]

        # get user's repos
        repos = []
        repos_path = Path(path, 'conf/')
        for repo in repos_path.walk():
            if repo.isdir():
                continue

            with open(str(repo)) as f:
                if name in f.read():
                    repos.append(repo)

        if repos or keys:
            return cls(name, path, git, repos=repos, keys=keys)
        return None

    @classmethod
    def get(cls, user, path, git):
        if isinstance(user, string_types):
            user = User.get_by_name(user, str(path), git)
        if not isinstance(user, User) or not user:
            message = 'Missing user or invalid type'
            raise ValueError(message)
        return user

    @property
    def is_admin(self):
        for repo in self.repos:
            if 'gitolite.conf' in repo:
                return True
        return False

    def __str__(self):
        return "< %s >" % self.name

    def __repr__(self):
        return "< %s >" % self.name
