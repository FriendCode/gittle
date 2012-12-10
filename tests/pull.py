from gittle import Gittle

from .config import repo_path, repo_url, key_file

# Gittle repo
g = Gittle(repo_path, origin_url=repo_url)

# Authentication
g.auth(pkey=key_file)

# Do pull
g.pull()
