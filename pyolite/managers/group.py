import os
from unipath import Path
from pyolite import Group
from pyolite.abstracts import Manager

class GroupManager(Manager):

    def get(self, name):
        """
        Given a name, retrieve the group.
        :param name: the group name to retrieve.
        :type name: str
        :returns: The group retrieved.
        :rtype: pyolite.models.Group
        """
        return Group.get(name, self.path, self.git)

    def create(self, name):
        """
        Given a name, create the group. Idempotent.
        :param name: the group name to create.
        :type name: str
        :returns: The group created.
        :rtype: pyolite.models.Group
        """
        path = Path(os.path.join(self.path, 'conf', 'groups', '{}.conf'.format(name)))
        if path.exists():#Already exist
            return self.get(name)
        # If there are missing parent paths in the group path, create them so we don't get IOErrors
        # In the case of a repo having names with slashes (e.g. "username/reponame")
        elif path.parent != Path(""):
            path.parent.mkdir(parents=True)
        #
        path.write_file("")
        self.git.commit([str(path)], 'Created group %s' % name)
        return Group(entity, self.path, self.git)

    def delete(self, name):
        """
        Given a name, delete the group. Idempotent.
        :param name: the group name to delete.
        :type name: str
        :returns: The deletion status.
        :rtype: bool
        """
        group = self.get(name)
        if not group:
            return False
        path = Path(os.path.join(self.path, 'conf', 'groups', '{}.conf'.format(name)))
        if not path.exists():#Already exist
            return False
        path.remove()
        self.git.commit([str(path)], 'Deleted group {}.'.format(name))

    def all(self):
        """
        Retrieve all the groups.
        :rtype: list
        """
        groups = []
        path = Path(self.path, os.path.join('conf', 'groups'))
        for obj in path.walk():
            if obj.isdir():
                continue
            files = re.compile('(\w+.conf$)').findall(str(obj))
            if files:
                groups += files
        return [Group.get(group[:-5], self.path, self.git) for group in set(groups)]
