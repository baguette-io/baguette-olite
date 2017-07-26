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
            group = Group.get(group, self.path, self.git)
        except ValueError:
            group = Group(group, self.path, self.git)
        return func(self, group, *args, **kwargs)
    return decorated

class ListGroups(object):
    def __init__(self, parent):
        self.parent = parent

    @with_group
    def add(self, group, permission):
        if group.name in self.parent.objects:
            return group
        #
        if set(map(lambda permission: permission.upper(), permission)) - ACCEPTED_PERMISSIONS != set([]):
            raise ValueError('Invalid permissions. They must be from %s' % ACCEPTED_PERMISSIONS)
        #
        self.parent.write("        %s         =        @%s\n" % (permission, group.name))
        commit_message = 'Group %s added to %s with permissions: %s' % (group, self.parent, permission)
        self.parent.git.commit(['conf'], commit_message)
        group.repos.append(self.parent)
        return group

    @with_group
    def edit(self, group, permission):
        pattern = r'(\s*)([RW+DC]*)(\s*)=@(\s*)%s\s+' % group.name
        string = r"\n        %s        =        @%s" % (permission, user.name)
        self.parent.replace(pattern, string)
        self.parent.git.commit(['conf'], "Group %s has %s permission for %s" % (group.name, permission, self.parent))
        return group

    @with_group
    def remove(self, group):
        pattern = r'(\s*)([RW+DC]*)(\s*)=@(\s*)%s\s+' % group.name
        self.parent.replace(pattern, "")
        self.parent.git.commit(['conf'], "Deleted group %s from %s" % (group.name, self.parent))

    def list(self):
        groups = []
        for group in self.parent.objects:
            if group == "None":
                continue
            pattern = r'(\s*)([RW+DC]*)(\s*)=@(\s*)%s\s+' % group
            with open(str(self.parent.path)) as f:
                config = f.read()
                for match in re.compile(pattern).finditer(config):
                    perm = match.group(2)
            groups.append({"name":group, "permission":perm})
        return groups

    def __str__(self):
        return "['%s']" % ', '.join(self.parent.objects)
