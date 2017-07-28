import os
from unipath import Path
from pyolite import Group, Repository, User
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
        #1. Remove the conf file
        path = Path(os.path.join(self.path, 'conf', 'groups', '{}.conf'.format(name)))
        if not path.exists():#Already exist
            return False
        path.remove()
        #2. Remove it from the repos file.
        for repo in Path(self.path, 'conf', 'repos').walk():
            if repo.isdir():
                continue
            with open(str(repo)) as f:
                if name in f.read():
                    Repository.get(os.path.splitext(os.path.basename(repo))[0], self.path, self.git).replace(r'.*= *@%s\n' % name, '')
        #3. Commit
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
        commit_message = 'User %s added to group %s' % (user.name, group.name)
        self.git.commit(['conf'], commit_message)
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
        commit_message = 'User %s deleted from group %s' % (user.name, group.name)
        self.git.commit(['conf'], commit_message)
        return True

    def repo_add(self, group, repo, permission):
        """
        Add a group to a repo.
        :param group: The group on which the operation occurs.
        :type group: str, pyolite.models.Group
        :param repo: the repo to add the group.
        :type repo: str, pyolite.models.Repository
        :param permission: The group permission
        :type permission: str
        :returns: The add status.
        :rtype: bool
        """
        #1. Check for non existing objects
        try:
            group = self.get(group)
        except ValueError:
            return False
        try:
            repo = Repository.get(repo, self.path, self.git)
        except ValueError:
            return False
        #2. Check for permissions
        permission = permission.upper()
        accepted = set('RW+CD')
        if set(i for i in permission) - accepted != set([]):
            return False
        #3. Idempotency (we don't give a ** about the permission for idempotency)
        if group.name in repo.objects:
            return True
        #4. Create
        repo.write("       %s         =        @%s\n" % (permission, group.name))
        commit_message = 'Group %s added to repo %s' % (group.name, repo.name)
        self.git.commit(['conf'], commit_message)
        return True

    def repo_delete(self, group, repo):
        """
        Remove a group from a repo.
        :param group: The group on which the operation occurs.
        :type group: str, pyolite.models.Group
        :param repo: the repo to delete the group from.
        :type repo: str, pyolite.models.Repository
        :returns: The deletion status.
        :rtype: bool
        """
        #1. Check for non existing objects
        try:
            group = self.get(group)
        except ValueError:
            return False
        try:
            repo = Repository.get(repo, self.path, self.git)
        except ValueError:
            return False
        #2. Idempotency
        if group.name not in repo.objects:
            return True
        #3. Delete
        repo.replace(r'.*= *@%s\n' % group.name, '')
        commit_message = 'Group %s deleted from repo %s' % (group.name, repo.name)
        self.git.commit(['conf'], commit_message)
        return True
