import re
from pyolite.models import Group


ACCEPTED_PERMISSIONS = set('RW+CD')


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

class ListGroups(object):
    def __init__(self, parent):
        self.parent = parent

    @with_group
    def add(self, user, permission):
        if user.name in self.parent.objects:
            return user
        #
        if set(map(lambda permission: permission.upper(), permission)) - ACCEPTED_PERMISSIONS != set([]):
            raise ValueError('Invalid permissions. They must be from %s' % ACCEPTED_PERMISSIONS)
        #
        self.parent.write("        %s         =        %s\n" % (permission, user.name))
        commit_message = 'User %s added to %s with permissions: %s' % (user, self.parent, permission)
        self.parent.git.commit(['conf'], commit_message)
        #
        if isinstance(self.parent, Repo):
            user.repos.append(self.parent)
        elif isinstance(self.parent, Group):
            user.groups.append(self.parent)
        else:
            raise TypeError
        return user

    @with_group
    def edit(self, user, permission):
        pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s\s+' % user.name
        string = r"\n        %s        =        %s" % (permission, user.name)
        self.parent.replace(pattern, string)
        self.parent.git.commit(['conf'], "User %s has %s permission for %s" % (user.name, permission, self.parent))
        return user

    @with_group
    def remove(self, user):
        pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s\s+' % user.name
        self.parent.replace(pattern, "")
        self.parent.git.commit(['conf'], "Deleted user %s from %s" % (user.name, self.parent))

    def list(self):
        users = []
        for user in self.parent.objects:
            if user == "None":
                continue
            pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s\s+' % user
            with open(str(self.parent.path)) as f:
                config = f.read()
                for match in re.compile(pattern).finditer(config):
                    perm = match.group(2)
            users.append({"name":user, "permission":perm})
        return users

    def __iter__(self):
        for user in self._users:
            yield user

    def __getitem__(self, item):
        return self._users[item]

    def __setitem__(self, item, value):
        self._users[item] = value

    def __add__(self, items):
        for item in items:
            self.append(item)

    def __str__(self):
        return "['%s']" % ', '.join(self.parent.objects)
