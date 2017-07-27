import os
from unipath import Path
from pyolite import Group, User
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

    def get_or_create(self, name):
        """
        Given a name, retrieve the group.
        Otherwise create it.
        :param name: the group name to retrieve/create.
        :type name: str
        :returns: The group retrieved.
        :rtype: pyolite.models.Group
        """
        return self.create(name)

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
        return Group(name, self.path, self.git)

    def delete(self, name):
        """
        Given a name, delete the group. Idempotent.
        :param name: the group name to delete.
        :type name: str
        :returns: The deletion status.
        :rtype: bool
        """
        path = Path(os.path.join(self.path, 'conf', 'groups', '{}.conf'.format(name)))
        if not path.exists():#Already exist
            return False
        path.remove()
        self.git.commit([str(path)], 'Deleted group {}.'.format(name))
        return True

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
            files = re.compile(r'(\w+.conf$)').findall(str(obj))
            if files:
                groups += files
        return [Group.get(group[:-5], self.path, self.git) for group in set(groups)]

    def user_add(self, group, user):
        """
        Add an user into a group.
        :param group: The group on which the operation occurs.
        :type group: str, pyolite.models.Group
        :param user: the user to add.
        :type user: str, pyolite.models.User
        :returns: The add status.
        :rtype: bool
        """
        #1. Check for non existing objects
        try:
            group = self.get(group)
        except ValueError:
            return False
        try:
            user = User.get(user, self.path, self.git)
        except ValueError:
            return False
        #2. Idempotency
        if user.name in group.objects:
            return True
        #3. Create
        group.write("@{} = {}\n".format(group.name, user.name))
        return True

    def user_delete(self, group, user):
        """
        Delete an user from a group.
        :param group: The group on which the operation occurs.
        :type group: str, pyolite.models.Group
        :param user: the user to delete.
        :type user: str, pyolite.models.User
        :returns: The deletion status.
        :rtype: bool
        """
        #1. Check for non existing objects
        try:
            group = self.get(group)
        except ValueError:
            return False
        try:
            user = User.get(user, self.path, self.git)
        except ValueError:
            return False
        #2. Idempotency
        if user.name not in group.objects:
            return True
        #3. Delete
        group.replace("@{} = {}\n".format(group.name, user.name), "")
        return True
