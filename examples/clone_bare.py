from gittle import Gittle

repo_path = '/tmp/gittle_bare'
repo_url = 'git://github.com/AaronO/dulwich.git'

repo = Gittle.clone_bare(repo_url, repo_path)

print((repo.tracked_files))
