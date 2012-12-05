# Dulwich imports
from dulwich.repo import Repo as DRepo
from dulwich.client import get_transport_and_path

# Local imports
from . import utils


class Gittle(object):
    DEFAULT_MESSAGE = '**No Message**'
    DEFAULT_USER_INFO = {
        'name': None,
        'email': None,
    }

    def __init__(self, repo_or_path):
        if isinstance(repo_or_path, DRepo):
            self.repo = repo_or_path
            self.path = self.repo.path
        elif isinstance(repo_or_path, basestring):
            self.path = repo_or_path
            self.repo = DRepo(repo_or_path)
        else:
            raise Exception('Gittle must be initialized with either a dulwich repository or a string to the path')

    @classmethod
    def init(cls, path):
        """Initialize a repository"""
        repo = DRepo.init(path)
        return cls(repo)

    @classmethod
    def init_bare(cls, path):
        repo = DRepo.init_bare(path)
        return cls(repo)

    @classmethod
    def clone_remote(cls, remote_path, local_path, **kwargs):
        """Clone a remote repository"""
        # Initialize the local repository
        local_repo = DRepo.init(local_path)

        # Get client
        client, host_path = get_transport_and_path(remote_path, **kwargs)

        # Fetch data from remote repository
        remote_refs = client.fetch(host_path, local_repo,
            determine_wants=local_repo.object_store.determine_wants_all)

        # Update head
        local_repo["HEAD"] = remote_refs["HEAD"]

        # Add origin
        return cls(local_repo)

    def clone(cls):
        """Clone a local repository"""
        pass

    def _commit(self, commiter=None, author=None, message=None, *args, **kwargs):
        message = message or self.DEFAULT_MESSAGE
        return self.repo.do_commit(message=message)

    # Like: git commmit -a
    def commit(self, name=None, email=None, message=None):
        user_info = {
            'name': name,
            'email': email,
        }
        return self._commit(
            commiter=user_info,
            author=user_info,
            message=message)

    # Commit only a set of files
    def commit_files(self):
        pass

    # Like: git add
    @utils.arglist_method
    def add(self, files):
        return self.repo.stage(files)

    # Like: git rm
    @utils.arglist_method
    def rm(self, files, force=False):
        pass

    # Like: git mv
    @utils.arglist_method
    def mv(self, files):
        pass

    @utils.arglist_method
    def checkout(self, files):
        pass
