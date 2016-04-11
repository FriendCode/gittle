"""
# Copyright 2013 Aaron O'Mullan <aaron.omullan@friendco.de>
#
# This program is free software; you can redistribute it and/or
# modify it only under the terms of the GNU GPLv2 and/or the Apache
# License, Version 2.0.  See the COPYING file for further details.

from gittle import Gittle


def random_char():
    while True:
        yield random.choice(string.ascii_letters)

TMP_FILES = {
    'local': {
        'a'
        'b': random_content(),
    },
    'remote': {

    }

}


GIT_PATHS = {
    'remote': '/tmp/gittle_test_remote',
    'local': '/tmp/gittle_test_local',
}



def random_content(length=512):
    return ''.join([
        random.choice(string.ascii_letters)
        for x in xrange(length)
    ])


def create_remote():
    remote = Gittle.init(TMP_REMOTE_GIT)


def create_local():
    local = Gittle.init(TMP_LOCAL_GIT)
"""
