from unipath import Path

class Group(object):
    def __init__(self, path, git, name):
        self.path = path
        self.git = git
        self.name = name
        self.users = []

    @classmethod
    def get_by_name(cls, name, path, git):
        path = Path(path, 'groups/{}.conf'.format(name))
        if path.exists():
            return Group(path, git, name)
        else:
            return None

    @classmethod
    def get(cls, group, path, git):
        if isinstance(group, basestring):
            group = Group.get_by_name(group, path, git)

        if not isinstance(group, Group) or not group:
            message = 'Missing user or invalid type'
            raise ValueError(message)
        return group

    def __str__(self):
        return "<Group: %s >" % self.name

    def __repr__(self):
        return "<Group: %s >" % self.name
