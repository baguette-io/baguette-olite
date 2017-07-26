import os
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
                return Group(name, path, git)
        elif isinstance(name, Group):
            return name
        raise ValueError('Missing group : <%s>, or invalid type : %s' % (name, type(name)))

    def __str__(self):
        return "<Group: %s >" % self.name

    def __repr__(self):
        return "<Group: %s >" % self.name
