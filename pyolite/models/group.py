import re
from six import string_types
from unipath import Path
from pyolite.views import ListUsers

class Group(object):
    def __init__(self, name, path, git):
        self.name = name
        self.path = path
        self.config = os.path.join(path, 'conf', 'groups', '{}.conf'.format(name))
        self.git = git
        self.regex = re.compile(r'=( *)(@\w+)')
        self.users = ListUsers(self)

    @classmethod
    def get_by_name(cls, name, path, git):
        path = Path(path, 'groups/{}.conf'.format(name))
        if path.exists():
            return Group(name, path, git)
        else:
            return None

    @classmethod
    def get(cls, group, path, git):
        if isinstance(group, string_types):
            group = Group.get_by_name(group, path, git)

        if not isinstance(group, Group) or not group:
            message = 'Missing group or invalid type'
            raise ValueError(message)
        return group

    def __str__(self):
        return "<Group: %s >" % self.name

    def __repr__(self):
        return "<Group: %s >" % self.name
