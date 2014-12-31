# Gittle - Pythonic Git for Humans

Gittle is a high-level pure-python git library.
It builds upon dulwich which provides most of the low-level machinery

## Install it

    pip install gittle

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

Or clone bare repository (no working directory) :

```python
repo = Gittle.clone(repo_url, repo_path, bare=True)
```

### Init repository from a path

```python
repo = Gittle.init(path)
```

### Get repository information

```python
# Get list of objects
repo.commits

# Get list of branches
repo.branches

# Get list of modified files (in current working directory)
repo.modified_files

# Get diff between latest commits
repo.diff('HEAD', 'HEAD~1')
```

### Commit

```python
# Stage single file
repo.stage('file.txt')

# Stage multiple files
repo.stage(['other1.txt', 'other2.txt'])

# Do the commit
repo.commit(name="Samy Pesse", email="samy@friendco.de", message="This is a commit")
```

### Pull

```python
repo = Gittle(repo_path, origin_uri=repo_url)

# Authentication with RSA private key
key_file = open('/Users/Me/keys/rsa/private_rsa')
repo.auth(pkey=key_file)

# Do pull
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

### Branch

```python
# Create branch off master
repo.create_branch('dev', 'master')

# Checkout the branch
repo.switch_branch('dev')

# Create an empty branch (like 'git checkout --orphan')
repo.create_orphan_branch('NewBranchName')

# Print a list of branches
print(repo.branches)

# Remove a branch
repo.remove_branch('dev')

# Print a list of branches
print(repo.branches)
```

### Get file version

```python
versions = repo.get_file_versions('gittle/gittle.py')
print("Found %d versions out of a total of %d commits" % (len(versions), repo.commit_count()))
```

### Get list of modified files (in current working directory)

```python
repo.modified_files
```

### Count number of commits

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

# Read only
GitServer('/', 'localhost').serve_forever()

# Read/Write
GitServer('/', 'localhost', perm='rw').serve_forever()
```

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

# Building and uploading to PyPi

```
python setup.py sdist bdist_egg upload
```
