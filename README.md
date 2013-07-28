# Gittle - Pythonic Git for Humans

Gittle is a high-level pure-python git library.
It builds upon dulwich which provides most of the low-level machinery

## Why implement Git in Python ?

### NEED FOR AWESOMENESS :
- Git is Awesome
- Python is Awesome
- Automating Git isn't so Awesome

### TO SOLVE MY OWN PROBLEMS AT FRIENDCODE :
- Automate git repo management (push/pull, commit, etc ...)
- Scriptable and usable from Python 
- Easy to use & good interoperability in a SOA environment

### USE IT FOR :
- Local
  - [X] Common git operations (add, rm, mv, commit, log)
  - [X] Branch operations (creating, switching, deleting)
- Remote
  - [X] Fetching
  - [X] Pushing
  - [X] Pulling (needs merging)
- Merging
  - [-] Fast forward
  - [-] Recursive
  - [-] Merge branches
- Diff
  - [X] Filter binary files

## Examples : 

### Clone a repository

```python
from gittle import Gittle

repo_path = '/tmp/gittle_bare'
repo_url = 'git://github.com/FriendCode/gittle.git'

repo = Gittle.clone(repo_url, repo_path)
```

With authentication (see Authentication section for more information) :

```python
auth = GittleAuth(pkey=key)
Gittle.clone(repo_url, repo_path, auth=auth)
```

Or clone bare repository :

```python
repo = Gittle.clone_bare(repo_url, repo_path)
```

### Init repository from a path

```python
repo = Gittle.init(path)
```

### Commit

```python
repo.stage("test.txt")
repo.commit(name="Samy Pesse", email="samy@friendco.de", message="This is a commit")
```

### Move file

```python
repo.mv([
  ('setup.py', 'new.py'),
])
```

### Pull

```python
repo = Gittle(repo_path, origin_uri=repo_url)

# Authentication with RSA private key
key_file = open('/Users/Me/keys/rsa/private_rsa')
repo.auth(pkey=key_file)

# Do push
repo.pull()
```

### Push

```python
repo = Gittle(repo_path, origin_uri=repo_url)

# Authentication with RSA private key
key_file = open('/Users/Me/keys/rsa/private_rsa')
repo.auth(pkey=key_file)

# Do push
repo.push()
```

### Authentication for remote operations

```python
# With a key
key_file = open('/Users/Me/keys/rsa/private_rsa')
repo.auth(pkey=key_file)

# With username and password
repo.auth(username="your_name", password="your_password")
```

### Create a new branch

```python
new_branch = "dev"
base_branch = "master"
repo.create_branch(base_branch, new_branch)
```

### Get file version

```python
versions = repo.get_file_versions('gittle/gittle.py')
print("Found %d versions out of a total of %d commits" % (len(versions), repo.commit_count()))
```

### Get pending files (files to commit)

```python
repo.pending_files
```

Or get diff working :

```python
repo.diff_working(None)
```

### Count number of commit

```python
repo.commit_count
```

### Get information for commits

List commits :

```python
# Get 20 first commits
repo.commit_info(start=0, end=20)
```

With a given commit :

```python
commit = "a2105a0d528bf770021de874baf72ce36f6c3ccc"
```

Diff with another commit :

```python
old_commit = repo.get_previous_commit(commit, n=1)
print repo.diff(commit, old_commit)
```

Explore commit files using :

```python
commit = "a2105a0d528bf770021de874baf72ce36f6c3ccc"

# Files tree
print repo.commit_tree(commit)

# List files in a subpath
print repo.commit_ls(commit, "testdir")

# Read a file
print repo.commit_file(commit, "testdir/test.txt")
```

### Create a GIT server

```python
from gittle import GitServer
server = GitServer('/', 'localhost')
server.serve_forever()
```
