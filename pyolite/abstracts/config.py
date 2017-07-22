import abc
import re
import fcntl

class Config(object):
    """
    Config file management.
    """
    __metaclass__ = abc.ABCMeta

    @property
    def path(self):
        raise NotImplementedError

    @property
    def regex(self):
        raise NotImplementedError

    def replace(self, pattern, string):
        with open(str(self.path), 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            #
            content = f.read()
            content = re.sub(pattern, string, content)
            #
            f.seek(0)
            f.write(content)
            f.truncate()
            fcntl.flock(f, fcntl.LOCK_UN)

    @property
    def objects(self):
        if not self.path.exists():
            return []

        objects = []
        with open(str(self.path)) as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            config = f.read()
            fcntl.flock(f, fcntl.LOCK_UN)
            for match in self.regex.finditer(config):
                objects.append(match.group(2))
        return objects

    def write(self, string):
        with open(self.path, 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(string)
            fcntl.flock(f, fcntl.LOCK_UN)

    def overwrite(self, string):
        with open(self.path, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(string)
            fcntl.flock(f, fcntl.LOCK_UN)
