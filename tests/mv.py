from gittle import Gittle

g = Gittle('.')

g.mv([
    ('setup.py', 'new.py'),
])
