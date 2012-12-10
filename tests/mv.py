from gittle import Gittle

from config import repo_path

g = Gittle(repo_path)

g.mv([
    ('setup.py', 'new.py'),
])
