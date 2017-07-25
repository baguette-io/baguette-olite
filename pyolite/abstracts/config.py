import abc
import fcntl
import six
import re
from unipath import Path

@six.add_metaclass(abc.ABCMeta)
class Config(object):
    """
    Config file management.
    """

    def path(self):
        raise NotImplementedError

    def regex(self):
        raise NotImplementedError

    def replace(self, pattern, string):
        with open(str(self.config), 'r+') as f:
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
        if not self.config.exists():
            return []

        objects = []
        with open(str(self.config)) as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            config = f.read()
            fcntl.flock(f, fcntl.LOCK_UN)
            for match in self.regex.finditer(config):
                objects.append(match.group(2))
        return objects

    def write(self, string):
        with open(self.config, 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(string)
            fcntl.flock(f, fcntl.LOCK_UN)

    def overwrite(self, string):
        with open(self.config, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(string)
            fcntl.flock(f, fcntl.LOCK_UN)
