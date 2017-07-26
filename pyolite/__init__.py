from pyolite.models import Group, User, Repository
from pyolite.managers import GroupManager, RepositoryManager, UserManager

class Pyolite(object):

    def __init__(self, admin_repository):
        self.admin_repository = admin_repository
        #
        self.users = UserManager(admin_repository)
        self.repos = RepositoryManager(admin_repository)
        self.groups = GroupManager(admin_repository)
