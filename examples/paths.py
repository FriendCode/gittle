# Copyright 2013 Aaron O'Mullan <aaron.omullan@friendco.de>
#
# This program is free software; you can redistribute it and/or
# modify it only under the terms of the GNU GPLv2 and/or the Apache
# License, Version 2.0.  See the COPYING file for further details.

import os
from functools import partial

from gittle import Gittle

BASE_DIR = '/Users/aaron/git/'
absbase = partial(os.path.join, BASE_DIR)

TRIES = 1
PATHS = map(absbase, [
    'gittle/',
    'loadfire/',
])


def paths_exists(repo):
    tracked_files = repo.tracked_files

    return all([
        os.path.exists(path)
        for path in [
            repo.abspath(repopath)
            for repopath in tracked_files
        ]
    ])


def changed_entires(repo):
    return repo._changed_entries()

TESTS = (
    paths_exists,
    changed_entires,
)


def test_repo(repo_path):
    repo = Gittle(repo_path)
    return all([
        test(repo)
        for test in TESTS
    ])


def main():
    paths = PATHS * TRIES
    for path in paths:
        print('Testing : %s' % path)
        test_repo(path)


if __name__ == '__main__':
    main()
