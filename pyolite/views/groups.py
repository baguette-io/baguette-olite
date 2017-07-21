from unipath import Path
import re

from pyolite.repo import Repo
from pyolite.models.group import Group


ACCEPTED_PERMISSIONS = set('RW+CD')


class ListGroups(object):
    def __init__(self, repository):
        self.repository_model = repository
        self.repo = Repo(Path(repository.path, "conf/repos/%s.conf" % repository.name))

    def with_group(func):
        """
        Decorator to retrieve the group object given a group name.
        """
        def decorated(self, group, *args, **kwargs):
            """
            :param group: The group name
            :type group: str
            """
            try:
                group = Group.get(group, self.repository_model.path, self.repository_model.git)
            except ValueError:
                group = Group(group, self.repository_model.path, self.repository_model.git)
            return func(self, group, *args, **kwargs)
        return decorated

    @with_user
    def add(self, user, permission):
        if user.name in self.repo.users:
            return user

        if set(map(lambda permission: permission.upper(), permission)) - \
             ACCEPTED_PERMISSIONS != set([]):
            raise ValueError('Invalid permissions. They must be from %s' %
                                             ACCEPTED_PERMISSIONS)

        self.repo.write("        %s         =        %s\n" % (permission, user.name))

        commit_message = 'User %s added to repo %s with permissions: %s' %\
                                         (user, self.repository_model.name, permission)
        self.repository_model.git.commit(['conf'], commit_message)

        user.repos.append(self.repo)
        return user

    @with_user
    def remove(self, user):
        pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s\s+' % user.name
        self.repo.replace(pattern, "")

        self.repository_model.git.commit(['conf'],
                                                 "Deleted user %s from repository %s" %
                                                 (user.name, self.repository_model.name))

    def list(self):
        users = []
        for user in self.repo.users:
            if user=="None":
                continue
            pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s\s+' % user
            with open(str(self.repo.path)) as f:
                config = f.read()
                for match in re.compile(pattern).finditer(config):
                    perm = match.group(2)
            users.append({"name":user,"permission":perm})
        return users

    def __iter__(self):
        for user in self._user:
            yield user

    def __getitem__(self, item):
        return self._groups[item]

    def __setitem__(self, item, value):
        self._groups[item] = value

    def __add__(self, items):
        for item in items:
            self.append(item)

    def __str__(self):
        return "['%s']" % ', '.join(self.repo.users)
