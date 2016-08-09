# Copyright 2012-2013 Aaron O'Mullan <aaron.omullan@friendco.de>
#
# This program is free software; you can redistribute it and/or
# modify it only under the terms of the GNU GPLv2 and/or the Apache
# License, Version 2.0.  See the COPYING file for further details.

from gittle import Gittle

from config import repo_path

g = Gittle(repo_path)


def print_files(group_name, paths):
    if not paths:
        return
    sorted_paths = sorted(paths)
    print(("\n%s :" % group_name))
    print(('\n'.join(sorted_paths)))

#print_files('Changes not staged for commit', g.modified_unstaged_files)
#print_files('Changes staged for commit', g.modified_staged_files)
#print_files('Ignored files', g.ignored_files)
print_files('Modified files', g.modified_files)
print_files('Untracked Files', g.untracked_files)
print_files('Tracked Files', g.tracked_files)
print_files('Trackable Files', g.trackable_files)
