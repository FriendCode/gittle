from gittle import Gittle

repo = Gittle('.')

lastest = reversed([
    info['sha']
    for info in repo.commit_info()[1:3]
])

print(repo.diff_between(*lastest))

print("""

Last Diff

""")


print(repo.diff('HEAD'))
