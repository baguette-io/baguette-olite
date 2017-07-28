import re
from unipath import Path

from pyolite.abstracts import Manager
from pyolite import Group, Repository, User
from pyolite.managers import GroupManager


class UserManager(Manager):
    def create(self, name, key=None, key_path=None):
        if key is None and key_path is None:
            raise ValueError('You need to specify a key or key_path')

        user = User(name, self.path, self.git)
        user.keys.append(key or key_path)
        return user

    def get(self, name):
        return User.get_by_name(name, self.path, self.git)

    def delete(self, name):
        user = User.get_by_name(name, self.path, self.git)
        if not user:
            return
        dest = Path(self.path, 'keydir/%s' % name)
        for repo in user.repos:
            Repository.get(repo, self.path, self.git).users.remove(user.name)
        for group in user.groups:
            GroupManager(self.path).user_delete(group, user.name)
        if dest.exists():
            dest.rmtree()
            self.git.commit([str(dest)], 'Deleted user %s.' % name)

    def all(self):
        users = []
        key_dir = Path(self.path, 'keydir')

        for obj in key_dir.walk():
            if obj.isdir():
                continue

            files = re.compile(r'(\w+.pub)').findall(str(obj))
            if files:
                users += files

        return [User.get_by_name(user[:-4], self.path, self.git)
                        for user in set(users)]
