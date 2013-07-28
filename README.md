# Gittle

Gittle is a high-level pure-python git library.
It builds upon dulwich which provides most of the low-level machinery

# You can use it for :

- Local
  - [X] Common git operations (add, rm, mv, commit, log)
  - [X] Branch operations (creating, switching, deleting)

- Remote
  - [X] Fetching
  - [X] Pushing
  - [X] Pulling (needs merging)

- Merging
  - [] Fast forward
  - [] Recursive
  - [] Merge branches

- Diff
  - [X] Filter binary files

# Examples : 

### Clone a repository

  from gittle import Gittle
  
  repo_path = '/tmp/gittle_bare'
  repo_url = 'git://github.com/FriendCode/gittle.git'
  
  repo = Gittle.clone(repo_url, repo_path)
  
Or clone bare repository :

  repo = Gittle.clone_bare(repo_url, repo_path)

### Init repository from a path

  repo = Gittle.init(path)

### Commit

  repo.stage("test.txt")
  repo.commit(name="Samy Pesse", email="samy@friendco.de", message="This is a commit")
  
### Move file

  repo.mv([
      ('setup.py', 'new.py'),
  ])

### Pull

  repo = Gittle(repo_path, origin_uri=repo_url)
  
  # Authentication with RSA private key
  key_file = open('/Users/Me/keys/rsa/private_rsa')
  repo.auth(pkey=key_file)
  
  # Do push
  repo.pull()

### Push

  repo = Gittle(repo_path, origin_uri=repo_url)
  
  # Authentication with RSA private key
  key_file = open('/Users/Me/keys/rsa/private_rsa')
  repo.auth(pkey=key_file)
  
  # Do push
  g.push()


### Create a GIT server

  from gittle import GitServer
  server = GitServer('/', 'localhost')
  server.serve_forever()
  
### Get file version

  versions = repo.get_file_versions('gittle/gittle.py')
  print("Found %d versions out of a total of %d commits" % (len(versions), repo.commit_count()))
  
