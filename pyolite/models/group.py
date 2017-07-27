import os
import re
from six import string_types
from unipath import Path
from pyolite.abstracts import Config

class Group(Config):
    def __init__(self, name, path, git):
        self.name = name
        self.path = path
        self.git = git
        self.config = os.path.join(path, 'conf', 'groups', '{}.conf'.format(name))
        self.regex = re.compile(r'(@{}) = (\w+)'.format(self.name))

    @classmethod
    def get(cls, name, path, git):
        """
        Try to retrieve a group, given a name.
        :rtype: pyolite.models.Group
        :raises ValueError: if the group does not exist.
        """
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
