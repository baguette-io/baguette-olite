from .managers import RepositoryManager, UserManager
from .models import User, Repository

class Pyolite(object):

    def __init__(self, admin_repository):
        self.admin_repository = admin_repository
        #
        self.users = UserManager(admin_repository)
        self.repos = RepositoryManager(admin_repository)
        #self.groups = GroupManager(admin_repository)
