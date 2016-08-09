from gittle import Gittle

repo = Gittle('.')

lastest = [
    info['sha']
    for info in repo.commit_info()[1:3]
]

print((repo.diff(*lastest, diff_type='classic')))

print("""

Last Diff

""")


print((list(repo.diff('HEAD'))))
