from unipath import Path

from pyolite import Repository
from pyolite.abstracts import Manager


class RepositoryManager(Manager):

    def get(self, entity):
        return Repository.get_by_name(entity, self.path, self.git)

    def create(self, entity):
        repo_file = Path(self.path, 'conf/repos/%s.conf' % entity)
        if repo_file.exists():
            raise ValueError('Repository %s already exists' % entity)
        # If there are missing parent paths in the repo path, create them so we don't get IOErrors
        # In the case of a repo having names with slashes (e.g. "username/reponame")
        elif repo_file.parent != Path(""):
            repo_file.parent.mkdir(parents=True)

        repo_file.write_file("repo %s\n" % entity)

        self.git.commit([str(repo_file)], 'Created repo %s' % entity)

        return Repository(entity, self.path, self.git)

    def delete(self, lookup_repo_name):
        repo = Repository(lookup_repo_name, self.path, self.git)
        if not repo:
            return
        dest = Path(self.path, 'conf/repos/%s.conf' % lookup_repo_name)
        if dest.exists():
            dest.remove()
            self.git.commit([str(dest)], 'Deleted repo %s.' % lookup_repo_name)

    def all(self):
        repos = []
        repo_dir = Path(self.path, 'conf/repos')

        for obj in repo_dir.walk():
            if obj.isdir():
                continue

            files = re.compile('(\w+.conf$)').findall(str(obj))
            if files:
                repos += files

        return [Repository.get_by_name(repo[:-5], self.path, self.git)
                        for repo in set(repos)]
