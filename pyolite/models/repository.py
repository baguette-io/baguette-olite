import os
import re
from unipath import Path
from pyolite.views import ListUsers
from pyolite.abstracts import Config


class Repository(Config):
    def __init__(self, name, path, git):
        self.name = name
        self.path = path
        self.config = os.path.join(path, 'conf', 'repos', '{}.conf'.format(name))
        self.git = git
        self.regex = re.compile('=( *)[@|](\w+)')
        #
        self.users = ListUsers(self)

    @classmethod
    def get(cls, lookup_repo, path, git):
        """
        Try to retrieve a repository, given a name.
        :rtype: pyolite.models.Repo
        :raises ValueError: if the repo does not exist.
        """
        repo = cls.get_by_name(lookup_repo, path, git)
        if not repo:
            raise ValueError("Missing repo : %s" % lookup_repo)
        return repo

    @classmethod
    def get_by_name(cls, lookup_repo, path, git):
        for obj in Path(path, 'conf').walk():
            if obj.isdir():
                continue

            with open(str(obj)) as f:
                if "repo %s" % lookup_repo in f.read():
                    return cls(lookup_repo, path, git)
        return None

    def __str__(self):
        return "<Repository: %s >" % self.name

    def __repr__(self):
        return "<Repository: %s >" % self.name
