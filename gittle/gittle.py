# From the future
from __future__ import absolute_import

# Python imports
import os
import copy
from hashlib import sha1
from shutil import rmtree
from functools import partial
import logging

# Dulwich imports
from dulwich.repo import Repo as DulwichRepo
from dulwich.client import get_transport_and_path
from dulwich.index import build_index_from_tree, changes_from_tree

# Local imports
from gittle import utils
from gittle.auth import GittleAuth
from gittle.exceptions import InvalidRemoteUrl


# Exports
__all__ = ('Gittle',)


class Gittle(object):
    DEFAULT_BRANCH = 'master'
    DEFAULT_MESSAGE = '**No Message**'
    DEFAULT_USER_INFO = {
        'name': None,
        'email': None,
    }

    HIDDEN_REGEXES = [
        # Hide git directory
        r'.*\/\.git\/.*',
    ]

    # Name pattern truths
    # Used for detecting if files are :
    # - deleted
    # - added
    # - changed
    PATTERN_ADDED = (False, True)
    PATTERN_REMOVED = (True, False)
    PATTERN_MODIFIED = (True, True)

    def __init__(self, repo_or_path, origin_uri=None, auth=None, *args, **kwargs):
        if isinstance(repo_or_path, DulwichRepo):
            self.repo = repo_or_path
        elif isinstance(repo_or_path, basestring):
            path = os.path.abspath(repo_or_path)
            self.repo = DulwichRepo(path)
        else:
            raise Exception('Gittle must be initialized with either a dulwich repository or a string to the path')

        # Set path
        self.path = self.repo.path

        # The remote url
        self.origin_uri = origin_uri

        # Build ignore filter
        self.hidden_regexes = copy.copy(self.HIDDEN_REGEXES)
        self.hidden_regexes.extend(self._get_ignore_regexes())
        self.ignore_filter = utils.path_filter_regex(self.hidden_regexes)
        self.filters = [
            self.ignore_filter,
        ]

        # Get authenticator
        if auth:
            self.authenticator = auth
        else:
            self.auth(*args, **kwargs)

    def _format_author(self, name, email):
        return "%s <%s>" % (name, email)

    def _format_userinfo(self, userinfo):
        name = userinfo.get('name')
        email = userinfo.get('email')
        if name and email:
            return self._format_author(name, email)
        return None

    @property
    def walker(self):
        """
        Very simple, basic walker
        """
        return self.repo.revision_history(self.repo.head())

    def commit_info(self):
        return map(utils.commit_info, self.walker)

    @property
    def git_dir(self):
        return self.repo.controldir()

    def auth(self, *args, **kwargs):
        self.authenticator = GittleAuth(*args, **kwargs)
        return self.authenticator

    # Generate a branch selector (used for pushing)
    def _wants_branch(self, branch_name=None):
        branch_name = branch_name or self.DEFAULT_BRANCH

        def wants_func(old):
            refs_key = "refs/heads/%s" % branch_name
            return {
                refs_key: self.repo.refs["HEAD"]
            }
        return wants_func

    def _get_ignore_regexes(self):
        gitignore_filename = os.path.join(self.path, '.gitignore')
        if not os.path.exists(gitignore_filename):
            return []
        lines = open(gitignore_filename).readlines()
        globers = map(lambda line: line.rstrip(), lines)
        return utils.globers_to_regex(globers)

    # Get the absolute path for a file in the git repo
    def abspath(self, repo_file):
        return os.path.abspath(
            os.path.join(self.path, repo_file)
        )

    # Get the relative path from the absolute path
    def relpath(self, abspath):
        return os.path.relpath(abspath, self.path)

    @property
    def last_commit(self):
        return self.repo[self.repo.head()]

    @property
    def index(self):
        return self.repo.open_index()

    @classmethod
    def init(cls, path):
        """Initialize a repository"""
        repo = DulwichRepo.init(path)
        return cls(repo)

    @classmethod
    def init_bare(cls, path):
        repo = DulwichRepo.init_bare(path)
        return cls(repo)

    def get_client(self, origin_uri=None, **kwargs):
        # Get the remote URL
        origin_uri = origin_uri or self.origin_uri

        # Fail if inexistant
        if not origin_uri:
            raise InvalidRemoteUrl()

        client_kwargs = {}
        auth_kwargs = self.authenticator.kwargs()

        client_kwargs.update(auth_kwargs)
        client_kwargs.update(kwargs)

        client, remote_path = get_transport_and_path(origin_uri, **client_kwargs)
        return client, remote_path

    def push_to(self, origin_uri, branch_name=None):
        selector = self._wants_branch(branch_name=branch_name)
        client, remote_path = self.get_client(origin_uri)
        return client.send_pack(remote_path, selector, self.repo.object_store.generate_pack_contents)

    # Like: git push
    def push(self, origin_uri=None, branch_name=None):
        return self.push_to(origin_uri, branch_name)

    # Not recommended at ALL ... !!!
    def dirty_pull_from(self, origin_uri, branch_name=None):
        # Remove all previously existing data
        rmtree(self.path)
        os.makedirs(self.path)
        self.repo = DulwichRepo.init(self.path)

        # Fetch brand new copy from remote
        return self.pull_from(origin_uri, branch_name)

    def pull_from(self, origin_uri, branch_name=None):
        return self.fetch(origin_uri)

    # Like: git pull
    def pull(self, origin_uri=None, branch_name=None):
        return self.pull_from(origin_uri, branch_name)

    def fetch_remote(self, origin_uri=None):
        # Get client
        client, remote_path = self.get_client(origin_uri=origin_uri)

        # Fetch data from remote repository
        remote_refs = client.fetch(remote_path, self.repo)

        return remote_refs

    def fetch(self, origin_uri=None):
        # Remote refs
        remote_refs = self.fetch_remote(origin_uri)

        # Update head
        self.repo["HEAD"] = remote_refs["HEAD"]

        # Checkout modifications to working directory
        return self.checkout_all()

    @classmethod
    def clone(cls, origin_uri, local_path, auth=None, mkdir=True, **kwargs):
        """Clone a remote repository"""
        if mkdir and not(os.path.exists(local_path)):
            os.makedirs(local_path)

        # Initialize the local repository
        local_repo = DulwichRepo.init(local_path)

        repo = cls(local_repo, origin_uri=origin_uri, auth=auth)

        repo.fetch()

        # Add origin
        # TODO

        return repo

    def _commit(self, committer=None, author=None, message=None, *args, **kwargs):
        modified_files = self.modified_files
        logging.warning("STAGING : %s" % modified_files)
        self.add(modified_files)
        message = message or self.DEFAULT_MESSAGE
        author_msg = self._format_userinfo(author)
        committer_msg = self._format_userinfo(committer)
        return self.repo.do_commit(
            message=message,
            author=author_msg,
            committer=committer_msg)

    # Like: git commmit -a
    def commit(self, name=None, email=None, message=None):
        user_info = {
            'name': name,
            'email': email,
        }
        return self._commit(
            committer=user_info,
            author=user_info,
            message=message)

    # Commit only a set of files
    def commit_files(self, files, *args, **kwargs):
        pass

    # Push all local commits
    # and pull all remote commits
    def sync(self, origin_uri=None):
        self.push(origin_uri)
        return self.pull(origin_uri)

    def lookup_entry(self, relpath, trackable_files=set()):
        if not relpath in trackable_files:
            raise KeyError

        abspath = self.abspath(relpath)

        with open(abspath, 'rb') as git_file:
            data = git_file.read()
            s = sha1()
            s.update("blob %u\0" % len(data))
            s.update(data)
        return (s.hexdigest(), os.stat(abspath).st_mode)

    @property
    @utils.transform(set)
    def tracked_files(self):
        return list(self.index)

    @property
    @utils.transform(set)
    def raw_files(self):
        return utils.subpaths(self.path)

    @property
    @utils.transform(set)
    def ignored_files(self):
        return utils.subpaths(self.path, filters=self.filters)

    @property
    #@utils.memoize
    @utils.transform(set)
    def trackable_files(self):
        return self.raw_files - self.ignored_files

    @property
    @utils.transform(set)
    def untracked_files(self):
        return self.trackable_files - self.tracked_files

    """
    @property
    @utils.transform(set)
    def modified_staged_files(self):
        "Checks if the file has changed since last commit"
        timestamp = self.last_commit.commit_time
        index = self.index
        return [
            f
            for f in self.tracked_files
            if index[f][1][0] > timestamp
        ]
    """

    # Return a list of tuples
    # representing the changed elements in the git tree
    def _changed_entries(self):
        obj_sto = self.repo.object_store
        tree_id = self.repo['HEAD'].tree
        names = self.trackable_files

        lookup_func = partial(self.lookup_entry, trackable_files=names)

        # Format = [((old_name, new_name), (old_mode, new_mode), (old_sha, new_sha)), ...]
        tree_diff = changes_from_tree(names, lookup_func, obj_sto, tree_id, want_unchanged=False)
        return list(tree_diff)

    @utils.transform(set)
    def _changed_entries_by_pattern(self, pattern):
        changed_entries = self._changed_entries()
        filtered_paths = [
            utils.first_true(names)
            for names, modes, sha in changed_entries
            if tuple(map(bool, names)) == pattern and utils.first_true(names)
        ]

        return filtered_paths

    @property
    @utils.transform(set)
    def removed_files(self):
        return self._changed_entries_by_pattern(self.PATTERN_REMOVED) - self.ignored_files

    @property
    @utils.transform(set)
    def added_files(self):
        return self._changed_entries_by_pattern(self.PATTERN_ADDED) - self.ignored_files

    @property
    @utils.transform(set)
    def modified_files(self):
        modified_files = self._changed_entries_by_pattern(self.PATTERN_MODIFIED) - self.ignored_files
        return modified_files

    @property
    @utils.transform(set)
    def modified_unstaged_files(self):
        timestamp = self.last_commit.commit_time
        return [
            f
            for f in self.tracked_files
            if os.stat(self.abspath(f)).st_mtime > timestamp
        ]

    """
    @property
    @utils.transform(set)
    def modified_files(self):
        return self.modified_staged_files | self.modified_unstaged_files
    """

    # Like: git add
    @utils.arglist_method
    def stage(self, files):
        return self.repo.stage(files)

    def add(self, *args, **kwargs):
        return self.stage(*args, **kwargs)

    # Like: git rm
    @utils.arglist_method
    def rm(self, files, force=False):
        index = self.index
        index_files = filter(lambda f: f in index, files)
        for f in index_files:
            del self.index[f]
        return index.write()

    def mv_fs(self, file_pair):
        old_name, new_name = file_pair
        os.rename(old_name, new_name)

    # Like: git mv
    @utils.arglist_method
    def mv(self, files_pair):
        index = self.index
        files_in_index = filter(lambda f: f[0] in index, files_pair)
        map(self.mv_fs, files_in_index)
        old_files = map(utils.first, files_in_index)
        new_files = map(utils.last, files_in_index)
        self.add(new_files)
        self.rm(old_files)
        self.add(old_files)
        return

    def checkout_all(self):
        # Rebuild index
        return build_index_from_tree(self.repo.path, self.repo.index_path(),
                        self.repo.object_store, self.repo['HEAD'].tree)

    @utils.arglist_method
    def checkout(self, files):
        pass

    @utils.arglist_method
    def reset(self, files, commit='HEAD'):
        pass

    def rm_all(self):
        self.index.clear()
        return self.index.write()

    # Get the nth parent back for a given commit
    def _get_commits_nth_parent(self, commit, n):
        parents = commit.parents
        if n == 0 or not parents:
            return commit
        parent_sha = parents[0]
        parent = self.repo[parent_sha]
        return self._get_commits_nth_parent(parent, n - 1)

    def _parse_reference(self, ref_string):
        # COMMIT_REF~x
        if '~' in ref_string:
            ref, count = ref_string.split('~')
            commit = self.repo[ref]
            return self._get_commits_nth_parent(commit, count)
        return self.repo[ref_string]

    def __hash__(self):
        """
        This is required otherwise the memoize function
        will just mess it up
        """
        return hash(self.path)
