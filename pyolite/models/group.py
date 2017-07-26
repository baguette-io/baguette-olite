import re
from six import string_types
from unipath import Path
from pyolite.views import ListUsers

class Group(object):
    def __init__(self, name, path, git):
        self.name = name
        self.path = path
        self.git = git
        self.config = os.path.join(path, 'conf', 'groups', '{}.conf'.format(name))
        self.regex = re.compile(r'=( *)@(\w+)')
        self.users = ListUsers(self)

    @classmethod
    def get(cls, name, path, git):
        group = None
        if isinstance(name, string_types):
            _path = Path(os.path.join(path, 'conf', 'groups', '{}.conf'.format(name)))
            if _path.exists():
                group = Group(name, path, git)
        if not isinstance(name, Group) or not group:
            message = 'Missing group or invalid type'
            raise ValueError(message)
        return group

    def __str__(self):
        return "<Group: %s >" % self.name

    def __repr__(self):
        return "<Group: %s >" % self.name
