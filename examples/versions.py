from gittle import Gittle

repo = Gittle('.')
versions = repo.get_file_versions('gittle/gittle.py')

print(("Found %d versions out of a total of %d commits" % (len(versions), repo.commit_count())))
