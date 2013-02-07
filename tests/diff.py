from gittle import Gittle

repo = Gittle('.')

lastest = [
    info['sha']
    for info in repo.commit_info()[:2]
]

print(repo.diff_between(*lastest))
