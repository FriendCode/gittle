from gittle import Gittle


g = Gittle('.')


def print_files(group_name, paths):
    if not paths:
        return
    sorted_paths = sorted(paths)
    print("\n%s :" % group_name)
    print('\n'.join(sorted_paths))

print_files('Changes not staged for commit', g.modified_unstaged_files)
print_files('Changes staged for commit', g.modified_staged_files)
print_files('Untracked Files', g.untracked_files)
print_files('Tracked Files', g.tracked_files)
