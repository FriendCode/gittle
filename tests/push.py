from gittle import Gittle

# Constants
repo_path = '/Users/aaron/git/gittle'
repo_url = 'git@friendco.de:friendcode/gittle.git'

# RSA private key
key_file = open('/Users/aaron/git/friendcode-conf/rsa/friendcode_rsa')

# Gittle repo
g = Gittle('.')

# Authentication
g.auth(pkey=key_file)

# Do push
g.push_to(repo_url)
